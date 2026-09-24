import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, type Meta, type Run, type SearchResult } from "../api";
import { RunDots } from "../components/CommitteeBoard";
import { DownloadIcon, PlusIcon } from "../components/Icons";
import { EMPTY_FILTERS, RATINGS, RunFilters, applyFilters, engineName, modelLabel, versionLabel, versionTitle, type Filters } from "../components/RunFilters";
import { fmtClock, fmtDate, fmtDuration, fmtPrice, fmtUsd, ratingColor } from "../format";

const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };
const AGENT_NAMES: Record<string, string> = {
  market: "Market", sentiment: "Sentiment", news: "News", fundamentals: "Fundamentals", bull: "Bull", bear: "Bear",
  research_manager: "Research Mgr", trader: "Trader", aggressive: "Aggressive", conservative: "Conservative", neutral: "Neutral", portfolio_manager: "Portfolio Mgr",
  buffett: "Buffett", munger: "Munger", graham: "Graham", lynch: "Lynch", druckenmiller: "Druckenmiller", pead: "Earnings drift",
  blend: "Blend", risk: "Risk limits", execution: "Execution",
};

const KIND: Record<string, string> = { "report.updated": "report", "llm.reasoning": "reasoning", "tool.result": "tool result", "tool.called": "tool call", "data.flag": "flag", "decision.structured": "decision", "run.failed": "error" };

type SortKey = "created" | "ticker" | "trade_date" | "rating" | "duration" | "cost" | "flags";
type FrameworkView = "all" | "tradingagents" | "ai_hedge_fund";
const FRAMEWORK_VIEWS: { id: FrameworkView; label: string }[] = [
  { id: "all", label: "All" },
  { id: "tradingagents", label: "TradingAgents" },
  { id: "ai_hedge_fund", label: "AI Hedge Fund" },
];
const duration = (r: Run) => (r.started_at ? (r.finished_at ?? Date.now() / 1000) - r.started_at : -1);
const SORTERS: Record<SortKey, (r: Run) => number | string> = {
  created: (r) => r.created_at,
  ticker: (r) => r.ticker,
  trade_date: (r) => r.trade_date,
  rating: (r) => (r.rating ? RATINGS.indexOf(r.rating) : 99),
  duration,
  cost: (r) => r.cost_usd,
  flags: (r) => r.flags,
};

function Snippet({ text }: { text: string }) {
  // Matches come marked as [[ ]] from the search index; render them as highlights.
  const parts = text.split(/\[\[|\]\]/);
  return (
    <span>
      {parts.map((part, i) => (i % 2 === 1 ? <mark key={i}>{part}</mark> : <span key={i}>{part}</span>))}
    </span>
  );
}

export default function RunsPage({ meta }: { meta: Meta }) {
  const [runs, setRuns] = useState<Run[]>();
  const [error, setError] = useState<string>();
  const [dialog, setDialog] = useState(false);
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS);
  const [search, setSearch] = useState<SearchResult>();
  const [sort, setSort] = useState<{ key: SortKey; dir: 1 | -1 }>({ key: "created", dir: -1 });
  // Opens on All every time; the switch only narrows the list while you are on the page.
  const [framework, setFramework] = useState<FrameworkView>("all");
  const navigate = useNavigate();

  const load = useCallback(() => api.runs().then(setRuns).catch((e) => setError(String(e.message || e))), []);
  useEffect(() => {
    load();
  }, [load]);
  const anyLive = runs?.some((r) => r.status === "running" || r.status === "queued");
  useEffect(() => {
    if (!anyLive) return;
    const t = window.setInterval(load, 3000);
    return () => window.clearInterval(t);
  }, [anyLive, load]);

  const searchIds = useMemo(() => (search ? new Set(search.runs.map((r) => r.run_id)) : undefined), [search]);
  const snippets = useMemo(() => new Map(search?.runs.map((r) => [r.run_id, r]) ?? []), [search]);

  const counts = useMemo(() => {
    const c = { all: runs?.length ?? 0, tradingagents: 0, ai_hedge_fund: 0 };
    for (const r of runs ?? []) c[(r.engine || "tradingagents") === "ai_hedge_fund" ? "ai_hedge_fund" : "tradingagents"] += 1;
    return c;
  }, [runs]);
  const inFramework = useMemo(
    () => (runs ?? []).filter((r) => framework === "all" || ((r.engine || "tradingagents") === "ai_hedge_fund" ? "ai_hedge_fund" : "tradingagents") === framework),
    [runs, framework],
  );

  const shown = useMemo(() => {
    if (!runs) return [];
    const get = SORTERS[sort.key];
    return applyFilters(inFramework, filters, searchIds).sort((a, b) => {
      const va = get(a);
      const vb = get(b);
      return (va < vb ? -1 : va > vb ? 1 : 0) * sort.dir;
    });
  }, [runs, inFramework, filters, searchIds, sort]);

  const sortable = (label: string, key: SortKey, right = false) => (
    <th className={right ? "r" : undefined} aria-sort={sort.key === key ? (sort.dir === 1 ? "ascending" : "descending") : "none"}>
      <button
        className="th-sort"
        onClick={() => setSort((s) => ({ key, dir: s.key === key ? ((-s.dir) as 1 | -1) : key === "ticker" ? 1 : -1 }))}
      >
        {label}
        <span className="sort-mark">{sort.key === key ? (sort.dir === 1 ? "↑" : "↓") : ""}</span>
      </button>
    </th>
  );

  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <h1>Runs</h1>
          <span className="subtitle">The record of every analysis: framework, models, decision, cost and the full log. Open one to replay it step by step.</span>
        </div>
        <a className="btn" href="/api/runs.csv">
          <DownloadIcon /> Export CSV
        </a>
      </header>

      {runs && runs.length > 0 && (
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <span className="label" style={{ margin: 0 }}>Framework</span>
          <div className="seg" role="group" aria-label="Show runs from">
            {FRAMEWORK_VIEWS.map((f) => (
              <button key={f.id} className={framework === f.id ? "on" : ""} aria-pressed={framework === f.id} onClick={() => setFramework(f.id)}>
                {f.label} <span className="muted" style={{ marginLeft: 4 }}>{counts[f.id]}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {runs && runs.length > 0 && <RunFilters runs={inFramework} filters={filters} onChange={setFilters} search={search} onSearch={setSearch} shown={shown} />}

      <div className="cta-bar">
        <div>
          <b>{framework === "ai_hedge_fund" ? "Run the fund on a ticker" : "Run the agents on a ticker"}</b>
          <span className="muted">
            {framework === "ai_hedge_fund"
              ? "Pick a strategy and a date; each analyst scores the stock, the strategy blends, a simulated broker fills. Every call is logged."
              : "Pick stocks, a date and the analysts; watch the twelve agents work and keep the full log."}
          </span>
        </div>
        <button className="btn btn-primary btn-lg" onClick={() => setDialog(true)}>
          <PlusIcon /> New run
        </button>
      </div>

      <section className="panel">
        {error && <div className="panel-pad error">{error}</div>}
        {runs && runs.length === 0 && (
          <div className="panel-pad">
            <div className="empty">No runs yet. Start one to watch the twelve agents work through a ticker.</div>
          </div>
        )}
        {runs && runs.length > 0 && shown.length === 0 && (
          <div className="panel-pad">
            <div className="empty">{search ? "No run's log contains that text." : "No runs match these filters."}</div>
          </div>
        )}
        {shown.length > 0 && (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Status</th>
                  {sortable("Ticker", "ticker")}
                  {sortable("Trade date", "trade_date")}
                  <th>Framework</th>
                  <th>Models</th>
                  {sortable("Rating", "rating")}
                  <th className="r">Entry</th>
                  <th className="r">Stop</th>
                  <th className="r">Target</th>
                  <th>Horizon</th>
                  {sortable("Cost est.", "cost", true)}
                  {sortable("Flags", "flags", true)}
                  {sortable("Started", "created")}
                </tr>
              </thead>
              <tbody>
                {shown.map((r) => {
                  const d = r.decision;
                  const dash = <span className="muted">—</span>;
                  const hit = snippets.get(r.id);
                  const open = () => navigate(`/runs/${r.id}`);
                  return [
                    <tr key={r.id} onClick={open}>
                      <td>
                        <StatusCell status={r.status} />
                        {r.progress && r.progress.order.length > 0 && <RunDots progress={r.progress.state} order={r.progress.order} />}
                      </td>
                      <td style={{ fontWeight: 700 }}>
                        {r.ticker}
                        {r.purpose === "backtest" && <span className="tag-bt" title={`Backtest run · memory ${r.memory ?? "off"}`}>BT</span>}
                      </td>
                      <td className="num">{r.trade_date}</td>
                      <td title={versionTitle(r.engine_version, r.engine)}>
                        {engineName(r)}
                        <span className="muted mono" style={{ fontSize: 10.5, marginLeft: 6 }}>{versionLabel(r.engine_version)}</span>
                      </td>
                      <td className="mono" style={{ fontSize: 11.5, color: "var(--ink-2)" }}>{r.quick_model === r.deep_model ? modelLabel(r.quick_model) : `${modelLabel(r.quick_model)} · ${modelLabel(r.deep_model)}`}</td>
                      <td className="rating" style={{ color: ratingColor(r.rating) }}>{r.rating ?? dash}</td>
                      <td className="r">{d?.trader?.entry_price != null ? fmtPrice(d.trader.entry_price) : dash}</td>
                      <td className="r">{d?.trader?.stop_loss != null ? fmtPrice(d.trader.stop_loss) : dash}</td>
                      <td className="r">{d?.portfolio?.price_target != null ? fmtPrice(d.portfolio.price_target) : dash}</td>
                      <td className="clip" title={d?.portfolio?.time_horizon ?? undefined} style={{ color: "var(--ink-2)" }}>{d?.portfolio?.time_horizon ?? dash}</td>
                      <td className="r">{fmtUsd(r.cost_usd)}</td>
                      <td className="r" style={{ color: r.flags ? "var(--warn)" : "var(--muted)" }}>{r.flags}</td>
                      <td className="muted" title={`${fmtDate(r.created_at)} ${fmtClock(r.created_at, false)} · ${r.started_at ? fmtDuration(duration(r)) : "not started"}`}>{fmtDate(r.created_at)}</td>
                    </tr>,
                    hit && (
                      <tr key={`${r.id}-hits`} className="snippet-row" onClick={open}>
                        <td colSpan={13}>
                          {hit.snippets.map((s) => (
                            <div className="snippet" key={s.seq}>
                              <span className="who">{s.agent ? AGENT_NAMES[s.agent] ?? s.agent : "Engine"} · {KIND[s.type] ?? s.type}</span>
                              <Snippet text={s.snippet} />
                            </div>
                          ))}
                          {hit.hits > hit.snippets.length && <div className="muted" style={{ fontSize: 11.5, paddingLeft: 170 }}>and {hit.hits - hit.snippets.length} more in this run</div>}
                        </td>
                      </tr>
                    ),
                  ];
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {dialog && (
        <NewRunDialog
          meta={meta}
          initialEngine={framework === "ai_hedge_fund" && meta.engines?.ai_hedge_fund?.installed ? "ai_hedge_fund" : "tradingagents"}
          onClose={() => setDialog(false)}
          onStarted={(ids) => {
            setDialog(false);
            if (ids.length === 1) navigate(`/runs/${ids[0]}`);
            else load();
          }}
        />
      )}
    </>
  );
}

export function StatusCell({ status }: { status: Run["status"] }) {
  const map = {
    running: ["var(--accent)", "Running", true],
    queued: ["var(--muted)", "Queued", false],
    finished: ["var(--good)", "Finished", false],
    failed: ["var(--bad)", "Failed", false],
    cancelled: ["var(--muted)", "Cancelled", false],
  } as const;
  const [color, label, pulse] = map[status];
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 8 }}>
      <span className={`dot${pulse ? " live" : ""}`} style={{ background: color }} />
      {label}
    </span>
  );
}

function NewRunDialog({ meta, onClose, onStarted, initialEngine = "tradingagents" }: { meta: Meta; onClose: () => void; onStarted: (ids: string[]) => void; initialEngine?: "tradingagents" | "ai_hedge_fund" }) {
  const [tickers, setTickers] = useState("NVDA");
  const [date, setDate] = useState(meta.default_trade_date);
  const [analysts, setAnalysts] = useState<string[]>(meta.analysts);
  const [depth, setDepth] = useState(1);
  const providers = meta.providers ?? [{ id: "deepseek", label: "DeepSeek", key: "DEEPSEEK_API_KEY", present: true, quick: meta.models.quick, deep: meta.models.deep }];
  const [provider, setProvider] = useState(providers[0].id);
  const prov = providers.find((p) => p.id === provider) ?? providers[0];
  const [quick, setQuick] = useState(prov.quick[0] ?? "");
  const [deep, setDeep] = useState(prov.deep[0] ?? "");
  const pickProvider = (id: string) => {
    const p = providers.find((x) => x.id === id) ?? providers[0];
    setProvider(p.id);
    setQuick(p.quick[0] ?? "");
    setDeep(p.deep[0] ?? "");
  };
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  const aihf = meta.engines?.ai_hedge_fund;
  const [engine, setEngine] = useState<"tradingagents" | "ai_hedge_fund">(initialEngine);
  const [strategy, setStrategy] = useState<string>(aihf?.strategies?.[0]?.name ?? "custom");
  const [aihfAnalysts, setAihfAnalysts] = useState<string[]>(aihf?.analysts?.filter((a) => a.kind === "llm").map((a) => a.name) ?? []);
  const [aihfModel, setAihfModel] = useState<string>(aihf?.default_model ?? "deepseek-flash");
  const aihfModelMeta = aihf?.models?.find((m) => m.model_name === aihfModel);
  const aihfLabel = (name: string) => aihf?.analysts?.find((a) => a.name === name)?.label ?? name;
  const aihfBlocked = !aihf?.installed
    ? aihf?.error ?? "AI Hedge Fund is not installed"
    : !aihf.data_key?.present
    ? "FINANCIAL_DATASETS_API_KEY is not loaded. AI Hedge Fund reads prices and fundamentals from financialdatasets.ai (the key is free, the data needs prepaid credits): put it in .env at the repository root, then restart Glassbench."
    : aihfModelMeta && !aihfModelMeta.present
    ? `${aihfModelMeta.key} is not loaded for ${aihfModelMeta.display_name}.`
    : strategy === "custom" && !aihfAnalysts.length
    ? "Pick at least one analyst."
    : undefined;
  const isAihf = engine === "ai_hedge_fund";

  const list = tickers.split(/[\s,;]+/).map((t) => t.trim().toUpperCase()).filter(Boolean);
  const pastDate = date < meta.default_trade_date;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const submit = async () => {
    setBusy(true);
    setError(undefined);
    try {
      const res = isAihf
        ? await api.start({
            tickers: list, trade_date: date, analysts: meta.analysts, depth: 1, quick_model: "deepseek-v4-flash", deep_model: "deepseek-v4-pro", provider: "deepseek",
            engine, strategy: strategy === "custom" ? null : strategy, aihf_analysts: strategy === "custom" ? aihfAnalysts : null, aihf_model: aihfModel,
          })
        : await api.start({ tickers: list, trade_date: date, analysts, depth, quick_model: quick.trim(), deep_model: deep.trim(), provider });
      onStarted(res.run_ids);
    } catch (e: any) {
      setError(String(e.message || e));
      setBusy(false);
    }
  };

  return (
    <div className="scrim" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="dialog" role="dialog" aria-modal="true" aria-labelledby="new-run-title">
        <h2 id="new-run-title">New run</h2>
        <div className="field">
          <span className="label">Framework</span>
          <div className="seg">
            <button className={engine === "tradingagents" ? "on" : ""} onClick={() => setEngine("tradingagents")}>TradingAgents</button>
            <button className={isAihf ? "on" : ""} disabled={!aihf?.installed} title={aihf?.installed ? `AI Hedge Fund ${aihf.version ?? ""}` : aihf?.error} onClick={() => setEngine("ai_hedge_fund")}>AI Hedge Fund</button>
          </div>
        </div>
        <div className="row2">
          <div className="field">
            <label htmlFor="tickers">Tickers</label>
            <input id="tickers" className="input" value={tickers} onChange={(e) => setTickers(e.target.value)} autoFocus placeholder="NVDA, AAPL" />
            <span className="hint">{list.length > 1 ? `${list.length} runs, two at a time` : "Separate several with commas"}</span>
          </div>
          <div className="field">
            <label htmlFor="trade-date">Analysis date</label>
            <input id="trade-date" className="input" type="date" value={date} max={meta.default_trade_date} onChange={(e) => setDate(e.target.value)} />
            <span className="hint" style={{ color: pastDate && !isAihf ? "var(--warn)" : undefined }}>
              {isAihf ? "Filled at the next completed close; a recent date may come back pending" : pastDate ? "Past dates get an empty news feed" : "Today gives the fullest news and profile data"}
            </span>
          </div>
        </div>
        {isAihf ? (
          <>
            <div className="row2">
              <div className="field" style={{ minWidth: 0 }}>
                <label htmlFor="aihf-strategy">Strategy</label>
                <select id="aihf-strategy" className="select" style={{ width: "100%", minWidth: 0 }} value={strategy} onChange={(e) => setStrategy(e.target.value)}>
                  {aihf?.strategies?.map((s) => (
                    <option key={s.name} value={s.name}>
                      {s.display_name} · {s.models.map((m) => `${aihfLabel(m.name)}${m.weight !== 1 ? ` x${m.weight}` : ""}`).join(", ")}
                    </option>
                  ))}
                  <option value="custom">Custom · pick the analysts</option>
                </select>
                <span className="hint">{strategy === "custom" ? "Equal blend weights; long and short when any analyst may short" : `Blend mode ${aihf?.strategies?.find((s) => s.name === strategy)?.mode.replace("_", " ") ?? ""}`}</span>
              </div>
              <div className="field" style={{ minWidth: 0 }}>
                <label htmlFor="aihf-model">Model</label>
                <select id="aihf-model" className="select" style={{ width: "100%", minWidth: 0 }} value={aihfModel} onChange={(e) => setAihfModel(e.target.value)}>
                  {aihf?.models?.map((m) => <option key={m.model_name} value={m.model_name}>{m.display_name}{m.present ? "" : " (no key)"}</option>)}
                </select>
                <span className="hint">Every LLM analyst runs on it; the earnings drift model uses no LLM</span>
              </div>
            </div>
            {strategy === "custom" && (
              <div className="field">
                <span className="label">Analysts</span>
                <div className="checks">
                  {aihf?.analysts?.map((a) => {
                    const on = aihfAnalysts.includes(a.name);
                    return (
                      <button key={a.name} className={`check${on ? " on" : ""}`} aria-pressed={on} title={a.what}
                        onClick={() => setAihfAnalysts((cur) => (on ? cur.filter((x) => x !== a.name) : (aihf?.analysts ?? []).map((x) => x.name).filter((x) => x === a.name || cur.includes(x))))}>
                        {a.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
            <p className="muted" style={{ fontSize: 11.5, margin: 0 }}>
              One cycle per stock: each analyst scores it, the strategy blends the convictions, risk limits apply and a simulated broker fills at the next close. Glassbench maps the blended conviction to a rating so both frameworks share one table.
            </p>
            {aihfBlocked && <div className="error">{aihfBlocked}</div>}
          </>
        ) : (
          <>
        <div className="field">
          <span className="label">Analysts</span>
          <div className="checks">
            {meta.analysts.map((a) => {
              const on = analysts.includes(a);
              return (
                <button
                  key={a}
                  className={`check${on ? " on" : ""}`}
                  aria-pressed={on}
                  onClick={() => setAnalysts((cur) => (on ? cur.filter((x) => x !== a) : meta.analysts.filter((x) => x === a || cur.includes(x))))}
                >
                  {ANALYST_NAMES[a] ?? a}
                </button>
              );
            })}
          </div>
          <span className="hint">Bull, Bear, Research manager, Trader, the risk team and Portfolio manager always run.</span>
        </div>
        <div className="row2">
          <div className="field">
            <span className="label">Debate rounds</span>
            <div className="seg">
              {[1, 2, 3].map((d) => (
                <button key={d} className={depth === d ? "on" : ""} onClick={() => setDepth(d)}>{d}</button>
              ))}
            </div>
          </div>
          <div className="field">
            <label htmlFor="provider">Provider</label>
            <select id="provider" className="select" value={provider} onChange={(e) => pickProvider(e.target.value)}>
              {providers.map((p) => <option key={p.id} value={p.id}>{p.label}{p.key && !p.present ? " (no key)" : ""}</option>)}
            </select>
          </div>
          <div className="field">
            <label htmlFor="quick-model">Models · quick / deep</label>
            <div style={{ display: "flex", gap: 8 }}>
              <input id="quick-model" className="input" list="quick-model-ids" value={quick} onChange={(e) => setQuick(e.target.value)} placeholder="quick model id" style={{ flex: 1, minWidth: 0 }} />
              <datalist id="quick-model-ids">{prov.quick.map((m) => <option key={m} value={m} />)}</datalist>
              <input id="deep-model" className="input" list="deep-model-ids" aria-label="Deep model" value={deep} onChange={(e) => setDeep(e.target.value)} placeholder="deep model id" style={{ flex: 1, minWidth: 0 }} />
              <datalist id="deep-model-ids">{prov.deep.map((m) => <option key={m} value={m} />)}</datalist>
            </div>
            <p className="muted" style={{ fontSize: 11.5, marginTop: 4 }}>Any model id your provider serves. The quick model reads and debates, the deep model is called by the two managers.</p>
          </div>
        </div>
          </>
        )}
        {error && <div className="error">{error}</div>}
        <div className="dialog-foot">
          <span className="muted" style={{ fontSize: 12 }}>
            {isAihf ? `AI Hedge Fund ${aihf?.version ?? ""} · simulated broker · no orders are placed` : `${prov.label}${prov.key && !prov.present ? ` · ${prov.key} not loaded` : ""} · paper only · no orders are placed`}
          </span>
          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn btn-ghost" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" disabled={busy || !list.length || (isAihf ? !!aihfBlocked : !analysts.length || !quick.trim() || !deep.trim() || (!!prov.key && !prov.present))} onClick={submit}>
              {busy ? "Starting…" : list.length > 1 ? `Start ${list.length} runs` : "Start run"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
