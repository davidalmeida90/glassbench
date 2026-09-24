"""Run one AI Hedge Fund cycle for Glassbench and stream it as JSON lines.

This script runs inside AI Hedge Fund's own virtual environment, never inside
Glassbench's: the two projects pin different LangChain versions. Glassbench
starts it as a subprocess, passes API keys through the environment, and turns
every line printed on stdout into a run event. Nothing here imports Glassbench.

    python aihf_driver.py --ticker AAPL --date 2026-09-18 --strategy deep-value \
        --model deepseek-flash --run-dir <folder>

stdout: one JSON object per line, {"type": ..., "agent": ..., **payload}
stderr: AI Hedge Fund's own log lines, kept by Glassbench in the run folder.

Each run gets its own prompt cache folder. AI Hedge Fund's cache keeps the
exact prompt and response behind every signal, which is the audit trail
Glassbench wants, but a shared cache would answer a rerun from the previous run
and hide exactly the run to run variance Glassbench measures.

Vendor data stays private. Financial Datasets allows derived outputs (signals,
reasoning, weights) to be shared, not the underlying data, so raw responses and
the prompts that quote them go to --private-dir, which is never published. The
event stream carries only derived facts: for a data call, the row count, the
date span and the number of fields, never the values.

--fixture swaps the data client and the LLM for canned test doubles. Tests use
it to check the event stream offline; Glassbench never passes it for a run.
"""

from __future__ import annotations

import argparse
import contextvars
import json
import os
import sys
import time
import traceback
import uuid
from pathlib import Path

CURRENT_AGENT: contextvars.ContextVar[str | None] = contextvars.ContextVar("aihf_agent", default=None)
STRATEGY_DIR_NAME = "strategies"


def emit(type_: str, agent: str | None = None, **payload) -> None:
    line = {"type": type_, "agent": agent, **payload}
    sys.stdout.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# LLM calls: one LangChain callback per chat model, tagged with the agent that owns it
def _usage(response) -> tuple[int, int, int, str | None]:
    tokens_in = tokens_out = reasoning = 0
    served = None
    try:
        message = response.generations[0][0].message
        usage = getattr(message, "usage_metadata", None) or {}
        tokens_in = int(usage.get("input_tokens") or 0)
        tokens_out = int(usage.get("output_tokens") or 0)
        reasoning = int((usage.get("output_token_details") or {}).get("reasoning") or 0)
        served = (getattr(message, "response_metadata", None) or {}).get("model_name")
    except (AttributeError, IndexError, TypeError, ValueError):
        pass
    if not tokens_in and isinstance(getattr(response, "llm_output", None), dict):
        usage = response.llm_output.get("token_usage") or {}
        tokens_in = int(usage.get("prompt_tokens") or 0)
        tokens_out = int(usage.get("completion_tokens") or 0)
    return tokens_in, tokens_out, reasoning, served


def make_llm_tap():
    from langchain_core.callbacks import BaseCallbackHandler

    class LlmTap(BaseCallbackHandler):
        """Reports each chat call with its tokens and the model the provider actually served."""

        def __init__(self, model: str):
            self.model = model
            self._start: dict[str, float] = {}

        def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
            self._start[str(run_id)] = time.time()
            chars = sum(len(str(getattr(m, "content", ""))) for batch in messages for m in batch)
            emit("llm.started", CURRENT_AGENT.get(), call=str(run_id), model=self.model, prompt_chars=chars)

        def on_llm_end(self, response, *, run_id, **kwargs):
            tokens_in, tokens_out, reasoning, served = _usage(response)
            start = self._start.pop(str(run_id), time.time())
            emit("llm.finished", CURRENT_AGENT.get(), call=str(run_id), model=self.model, served_model=served,
                 tokens_in=tokens_in, tokens_out=tokens_out, reasoning=reasoning, cached=0,
                 duration=round(time.time() - start, 3))

        def on_llm_error(self, error, *, run_id, **kwargs):
            self._start.pop(str(run_id), None)
            emit("llm.failed", CURRENT_AGENT.get(), call=str(run_id), error=str(error)[:500])

    return LlmTap


class TimedLLM:
    """For clients without LangChain underneath (Jev, the fixture): time each call, no token counts."""

    def __init__(self, inner):
        self._inner = inner
        self.model = inner.model

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def complete(self, system: str, user: str) -> str:
        call = uuid.uuid4().hex
        start = time.time()
        emit("llm.started", CURRENT_AGENT.get(), call=call, model=self.model, prompt_chars=len(system) + len(user))
        try:
            out = self._inner.complete(system, user)
        except Exception as exc:
            emit("llm.failed", CURRENT_AGENT.get(), call=call, error=str(exc)[:500])
            raise
        emit("llm.finished", CURRENT_AGENT.get(), call=call, model=self.model, served_model=None, tokens_in=0,
             tokens_out=0, reasoning=0, cached=0, duration=round(time.time() - start, 3))
        return out


def instrument_llm(model_obj) -> None:
    llm = getattr(model_obj, "_llm", None)
    if llm is None:
        return  # quant model: no LLM
    chat = getattr(llm, "_chat", None)
    if chat is not None:
        tap_cls = make_llm_tap()
        chat.callbacks = [*(chat.callbacks or []), tap_cls(llm.model)]
    else:
        model_obj._llm = TimedLLM(llm)


# ---------------------------------------------------------------------------
# Data calls: every fetch an analyst makes shows up as a tool call on its lane
class DataTap:
    """Wraps the data client: every fetch becomes a tool call on the analyst's lane, and every response,
    inside a lane or not, is kept whole in the run folder (tool_outputs/), so the run can be audited and
    replayed without asking the data API again."""

    def __init__(self, inner, out_dir: Path | None = None, link_prefix: str = ""):
        self._inner = inner
        self._out = out_dir
        self._prefix = link_prefix  # how the run page reaches the file ("private/" when kept outside the run)

    def __getattr__(self, name):
        attr = getattr(self._inner, name)
        if not callable(attr) or not name.startswith("get_"):
            return attr

        def call(*args, **kwargs):
            agent = CURRENT_AGENT.get()
            shown = {"ticker": args[0] if args else kwargs.get("ticker"),
                     **{f"arg{i}": v for i, v in enumerate(args[1:], 1) if isinstance(v, (str, int, float))},
                     **{k: v for k, v in kwargs.items() if isinstance(v, (str, int, float))}}
            call_id = uuid.uuid4().hex
            if agent is not None:
                emit("tool.called", agent, call=call_id, tool=name, args=shown)
            try:
                result = attr(*args, **kwargs)
            except Exception as exc:
                if agent is not None:
                    emit("tool.failed", agent, call=call_id, tool=name, error=str(exc)[:500])
                raise
            saved = self._save(name, shown, result)
            if agent is not None:
                emit("tool.result", agent, call=call_id, tool=name, file=saved, **_describe(result))
            return result

        return call

    def _save(self, name: str, shown: dict, result) -> str | None:
        if self._out is None:
            return None
        import hashlib

        self._out.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha1(json.dumps(shown, sort_keys=True, default=str).encode()).hexdigest()[:10]
        rel = f"tool_outputs/{name.removeprefix('get_')}_{shown.get('ticker') or 'all'}_{digest}.json"
        rows = result if isinstance(result, list) else [result] if result is not None else []
        body = [r.model_dump(mode="json") if hasattr(r, "model_dump") else r for r in rows]
        (self._out.parent / rel).write_text(json.dumps({"call": name, "args": shown, "rows": body}, indent=1, default=str),
                                            encoding="utf-8")
        return self._prefix + rel


DATE_FIELDS = ("report_period", "time", "date", "filing_date", "report_date")


def _describe(result) -> dict:
    """What came back, without the values: row count, date span and field count only."""
    if result is None:
        return {"chars": 0, "rows": 0, "preview": "no data returned", "flag": "No data returned"}
    rows = result if isinstance(result, list) else [result]
    if not rows:
        return {"chars": 0, "rows": 0, "preview": "no rows returned", "flag": "No data returned"}
    dumped = [r.model_dump(exclude_none=True) if hasattr(r, "model_dump") else r for r in rows]
    first = dumped[0] if isinstance(dumped[0], dict) else {}
    key = next((k for k in DATE_FIELDS if k in first), None)
    dates = sorted(str(d.get(key))[:10] for d in dumped if key and isinstance(d, dict) and d.get(key))
    span = f" · {dates[0]} to {dates[-1]}" if dates else ""
    return {"chars": len(json.dumps(dumped, default=str)), "rows": len(rows),
            "preview": f"{len(rows)} row{'s' if len(rows) != 1 else ''}{span} · {len(first)} fields per row", "flag": None}


# ---------------------------------------------------------------------------
# Analysts: one lane per analyst, its signal as the structured decision
model_obj_for_text: dict = {}  # analyst name -> model object, for model-specific wording


def signal_text(sig) -> str:
    md = sig.metadata or {}
    if md.get("abstained"):
        return f"**Abstained**: {md.get('abstain_reason') or sig.reasoning}"
    lines = []
    if sig.value == 0 and not sig.reasoning and "signal" not in md:
        window = getattr(model_obj_for_text.get(sig.model_name), "_signal_window_days", None)
        when = f"within {window} days of" if window else "right after"
        return (f"**No view**: this model only takes a position {when} an earnings surprise, and none was filed "
                f"in that window before {sig.date}. Conviction 0.")
    if "signal" in md:
        lines.append(f"**Signal**: {str(md['signal']).capitalize()}, confidence {md.get('confidence', 0):.0f}%")
    lines.append(f"**Conviction**: {sig.value:+.2f} (from -1 bearish to +1 bullish)")
    if sig.components:
        parts = ", ".join(f"{k} {v:+.3f}" for k, v in sig.components.items())
        lines.append(f"**Components**: {parts}")
    if sig.reasoning:
        lines.append(f"**Reasoning**: {sig.reasoning}")
    return "\n\n".join(lines)


def instrument_predict(model_obj, agent_id: str) -> None:
    inner = model_obj.predict

    def predict(ticker, date, data_client):
        token = CURRENT_AGENT.set(agent_id)
        start = time.time()
        emit("agent.started", agent_id, visit=1, as_of=date)
        try:
            sig = inner(ticker, date, data_client)
        except Exception as exc:
            emit("agent.failed", agent_id, error=f"{type(exc).__name__}: {exc}"[:500])
            raise
        finally:
            CURRENT_AGENT.reset(token)
        md = sig.metadata or {}
        emit("report.updated", agent_id, text=f"**Assessment as of**: {date}\n\n" + signal_text(sig))
        emit("decision.structured", agent_id, as_of=date, signal=md.get("signal"), confidence=md.get("confidence"),
             conviction=round(sig.value, 4), reasoning=sig.reasoning, abstained=bool(md.get("abstained")),
             abstain_reason=md.get("abstain_reason"), components=sig.components or None, model=md.get("model"),
             prompt_key=md.get("prompt_key"))
        emit("agent.finished", agent_id, duration=round(time.time() - start, 3))
        return sig

    model_obj.predict = predict


# ---------------------------------------------------------------------------
# Fixture: canned data and answers, for offline tests of the event stream only
class FixtureData:
    def get_prices(self, ticker, start_date, end_date, **kwargs):
        from datetime import date, timedelta

        from hedge_fund.data.models import Price

        close = 100.0 if ticker == "SPY" else 200.0
        day, last, bars = date.fromisoformat(start_date), date.fromisoformat(end_date), []
        while day <= last:
            if day.weekday() < 5:  # a bar per weekday, so sessions follow each other as they do in real data
                bars.append(Price(open=close, close=close, high=close, low=close, volume=1000, time=f"{day.isoformat()}T00:00:00Z"))
            day += timedelta(days=1)
        return bars

    def get_financial_metrics(self, ticker, end_date, period="ttm", limit=10):
        from hedge_fund.data.models import FinancialMetrics

        quarters = ["2026-06-30", "2026-03-31", "2025-12-31", "2025-09-30", "2025-06-30", "2025-03-31", "2024-12-31", "2024-09-30"]
        return [FinancialMetrics(ticker=ticker, report_period=q, period="ttm", filing_date=q, return_on_equity=0.25,
                                 gross_margin=0.45, book_value_per_share=20.0, market_cap=2e12) for q in quarters[:limit]]

    def get_company_facts(self, ticker):
        return None

    def get_earnings_history(self, ticker, *args, **kwargs):
        return []

    def get_earnings(self, ticker):
        return None

    def get_news(self, *args, **kwargs):
        return []

    def get_insider_trades(self, *args, **kwargs):
        return []

    def get_market_cap(self, ticker, end_date):
        return 2e12


class FixtureLLM:
    model = "fixture"
    ANSWERS = {"buffett": ("bullish", 70), "munger": ("neutral", 50), "graham": ("bearish", 60),
               "lynch": ("bullish", 55), "druckenmiller": ("bearish", 40)}

    def __init__(self, persona: str):
        self.persona = persona

    def complete(self, system: str, user: str) -> str:
        signal, confidence = self.ANSWERS.get(self.persona, ("neutral", 50))
        return json.dumps({"signal": signal, "confidence": confidence, "reasoning": f"Fixture answer for {self.persona}."})


# ---------------------------------------------------------------------------
def build_spec(args):
    from hedge_fund.fund.spec import FundSpec, custom_strategy, load_strategy
    import hedge_fund

    if args.strategy:
        path = Path(hedge_fund.__file__).parent / STRATEGY_DIR_NAME / f"{args.strategy}.yaml"
        strategy = load_strategy(path)
    else:
        strategy = custom_strategy([a.strip() for a in args.analysts.split(",") if a.strip()])
    return FundSpec(
        schema_version=2, name="glassbench", strategies=[strategy.model_dump()],
        risk={"max_position_pct": args.max_position, "max_gross_exposure": 1.0},
        capital=args.capital, rebalance="weekly", benchmark="SPY",
    )


def agent_ids(fund) -> dict[int, str]:
    counts: dict[str, int] = {}
    for _, staff in fund.strategies:
        for m in staff:
            counts[m.name] = counts.get(m.name, 0) + 1
    ids = {}
    for strategy, staff in fund.strategies:
        for m in staff:
            ids[id(m)] = m.name if counts[m.name] == 1 else f"{strategy.name}.{m.name}"
    return ids


def stage_events(record: dict, executed: bool) -> None:
    decision = record if executed else record.get("proposal", {})
    for s in decision.get("strategies", []):
        agent = "blend"
        emit("agent.started", agent, visit=1)
        emit("decision.structured", agent, strategy=s.get("name"), slice=s.get("slice"), convictions=s.get("convictions"),
             weights=s.get("weights"), flat_reason=s.get("flat_reason"), eligible_scores=s.get("eligible_scores"))
        conv = ", ".join(f"{t} {v:+.3f}" for t, v in (s.get("convictions") or {}).items()) or "none"
        weights = ", ".join(f"{t} {v:+.1%}" for t, v in (s.get("weights") or {}).items()) or "flat"
        text = f"**Strategy**: {s.get('name')}\n\n**Blended conviction**: {conv}\n\n**Sleeve weights**: {weights}"
        if s.get("flat_reason"):
            text += f"\n\n**Flat because**: {s['flat_reason']}"
        emit("report.updated", agent, text=text)
        emit("agent.finished", agent, duration=0)
    emit("agent.started", "risk", visit=1)
    clamps = decision.get("clamps") or []
    emit("decision.structured", "risk", target_weights=decision.get("target_weights"), clamps=clamps,
         final_weights=decision.get("final_weights"), risk_scale_factor=decision.get("risk_scale_factor"))
    lines = [f"**Target weights**: " + (", ".join(f"{t} {w:+.1%}" for t, w in (decision.get("target_weights") or {}).items()) or "flat"),
             f"**Final weights**: " + (", ".join(f"{t} {w:+.1%}" for t, w in (decision.get("final_weights") or {}).items()) or "flat")]
    if clamps:
        lines.append("**Clamps**: " + "; ".join(
            f"{c.get('limit')} on {c.get('ticker') or 'the whole book'}: {c.get('before', 0):+.1%} to {c.get('after', 0):+.1%}"
            for c in clamps))
    emit("report.updated", "risk", text="\n\n".join(lines))
    emit("agent.finished", "risk", duration=0)
    emit("agent.started", "execution", visit=1)
    if executed:
        emit("decision.structured", "execution", status="executed", execution_as_of=record.get("execution_as_of"),
             orders=record.get("orders"), fills=record.get("fills"), positions=record.get("positions"),
             cash=record.get("cash"), nav=record.get("nav"))
        fills = "; ".join(f"{f.get('side', '')} {f.get('shares', f.get('quantity', ''))} {f.get('ticker', '')} at {f.get('price', '')}"
                          for f in record.get("fills") or []) or "no fills"
        emit("report.updated", "execution", text=f"**Simulated execution** at the close of {record.get('execution_as_of')}\n\n"
                                                    f"**Fills**: {fills}\n\n**NAV**: {record.get('nav'):,.2f}")
    else:
        emit("decision.structured", "execution", status="pending", reason=record.get("reason"),
             scheduled_execution_date=record.get("scheduled_execution_date"))
        emit("report.updated", "execution", text=f"**Pending**: {record.get('reason')}")
    emit("agent.finished", "execution", duration=0)


def describe() -> int:
    """What this install offers, straight from its registries: analysts, library strategies, models."""
    import importlib.metadata as md

    import hedge_fund
    from hedge_fund.fund.spec import load_strategy
    from hedge_fund.llm import env_var_for
    from hedge_fund.signals import ALPHA_MODEL_REGISTRY, get_investment_approach
    from hedge_fund.signals.llm_agent import LLMAgent

    root = Path(hedge_fund.__file__).parent
    analysts = []
    for name, cls in ALPHA_MODEL_REGISTRY.items():
        doc = (cls.__doc__ or "").strip().splitlines()
        analysts.append({"name": name, "kind": "llm" if issubclass(cls, LLMAgent) else "quant",
                         "approach": get_investment_approach(name), "what": doc[0].strip() if doc else ""})
    strategies = []
    for path in sorted((root / STRATEGY_DIR_NAME).glob("*.yaml")):
        s = load_strategy(path)
        strategies.append({"name": s.name, "display_name": s.display_name or s.name.replace("-", " ").title(), "mode": s.blend.mode,
                           "models": [{"name": m.name, "weight": m.weight} for m in s.models]})
    models = []
    for m in json.loads((root / "llm" / "api_models.json").read_text(encoding="utf-8")):
        models.append({"model_name": m["model_name"], "display_name": m.get("display_name") or m["model_name"],
                       "provider": m.get("provider"), "key": env_var_for(m.get("provider") or "")})
    print(json.dumps({"version": md.version("aihf"), "analysts": analysts, "strategies": strategies, "models": models}))
    return 0


def main() -> int:
    if "--describe" in sys.argv:
        return describe()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--date", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--strategy", help="a library strategy, e.g. deep-value")
    group.add_argument("--analysts", help="comma separated analysts for a custom strategy, e.g. buffett,graham")
    parser.add_argument("--model", default="deepseek-flash")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--capital", type=float, default=100_000.0)
    parser.add_argument("--max-position", type=float, default=0.25)
    parser.add_argument("--data-cache", help="folder for AI Hedge Fund's data cache, so a fetch is never paid twice")
    parser.add_argument("--private-dir", help="where raw vendor data and prompts go, never published (default: the run folder)")
    parser.add_argument("--fixture", action="store_true", help="canned data and answers, for tests only")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    os.environ["HEDGE_FUND_LLM_MODEL"] = args.model
    try:
        if not args.fixture and not os.environ.get("FINANCIAL_DATASETS_API_KEY"):
            raise RuntimeError("FINANCIAL_DATASETS_API_KEY is not set. AI Hedge Fund reads all prices and fundamentals from "
                               "financialdatasets.ai; put the key in .env at the Glassbench repository root.")

        import importlib.metadata as md
        from hedge_fund.brokers import SimBroker
        from hedge_fund.fund import Fund
        from hedge_fund.llm import PromptCache
        from hedge_fund.pipeline import run_cycle
        from hedge_fund.pipeline.models import PendingRunResult
        import hedge_fund.signals.llm_agent as llm_agent

        real_cache = PromptCache
        private = Path(args.private_dir) if args.private_dir else run_dir
        prefix = "private/" if args.private_dir else ""
        llm_agent.PromptCache = lambda *a, **k: real_cache(private / "prompts")  # this run's own cache and audit trail
        if args.fixture:
            llm_agent.make_llm = lambda *a, **k: FixtureLLM("unknown")

        spec = build_spec(args)
        fund = Fund(spec)
        ids = agent_ids(fund)
        lanes = []
        for strategy, staff in fund.strategies:
            for m in staff:
                if args.fixture and hasattr(m, "_llm"):
                    m._llm = FixtureLLM(m.name)
                instrument_llm(m)
                instrument_predict(m, ids[id(m)])
                model_obj_for_text[m.name] = m
                weight = next((ms.weight for ms in strategy.models if ms.name == m.name), 1.0)
                lanes.append({"id": ids[id(m)], "model": m.name, "strategy": strategy.name, "blend_weight": weight,
                              "kind": "llm" if hasattr(m, "_llm") else "quant"})

        emit("driver.started", None, aihf_version=md.version("aihf"), spec=json.loads(spec.model_dump_json()),
             lanes=lanes, model=args.model, fixture=args.fixture)

        outputs = private / "tool_outputs"
        if args.fixture:
            data = DataTap(FixtureData(), outputs, prefix)
        else:
            from hedge_fund.data import CachedDataClient, FDClient

            # Every successful response is kept on disk and reused: a stock and date is paid for once.
            cached = CachedDataClient(FDClient(), cache_dir=args.data_cache) if args.data_cache else CachedDataClient(FDClient())
            data = DataTap(cached, outputs, prefix)
        result = run_cycle(fund, args.date, SimBroker(cash=spec.capital), data, [args.ticker.upper()])
        executed = not isinstance(result, PendingRunResult)
        record = json.loads(result.model_dump_json())
        (run_dir / "record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        stage_events(record, executed)
        emit("driver.finished", None, status="executed" if executed else "pending", record=record)
        return 0
    except Exception as exc:
        emit("driver.failed", None, error=f"{type(exc).__name__}: {exc}"[:1000], traceback=traceback.format_exc(limit=8)[-3000:])
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
