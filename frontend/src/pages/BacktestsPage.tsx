import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, type Backtest, type BacktestItem } from "../api";
import { VARIANT_LABELS, modelLabel, versionLabel } from "../components/RunFilters";
import { fmtDuration, fmtUsd, ratingColor } from "../format";
import { StatusCell } from "./RunsPage";

const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };
const BT_STATUS: Record<Backtest["status"], [string, string]> = {
  ready: ["pill-quiet", "Ready"],
  running: ["pill-live", "Running"],
  paused: ["pill-quiet", "Paused"],
  finished: ["pill-done", "Finished"],
  cancelled: ["pill-bad", "Cancelled"],
};

export default function BacktestsPage() {
  const [list, setList] = useState<Backtest[]>();
  const [error, setError] = useState<string>();

  const load = useCallback(() => {
    api.backtests().then(setList).catch((e) => setError(String(e.message ?? e)));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const live = list?.some((b) => b.status === "running" || b.counts.running > 0 || b.counts.queued > 0);
  useEffect(() => {
    if (!live) return;
    const t = window.setInterval(load, 3000);
    return () => window.clearInterval(t);
  }, [live, load]);

  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <h1>Backtests</h1>
          <span className="subtitle">Agent decisions on past dates, generated under a hard budget cap. Every run is also kept in Runs with its full log.</span>
        </div>
      </header>
      {error && <div className="error">{error}</div>}
      {list && list.length === 0 && (
        <section className="panel panel-pad">
          <div className="empty">No backtests yet.</div>
        </section>
      )}
      {list?.map((bt) => <BacktestCard key={bt.id} bt={bt} onChange={load} />)}
    </>
  );
}

function BacktestCard({ bt, onChange }: { bt: Backtest; onChange: () => void }) {
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const c = bt.config;
  const done = bt.counts.finished + bt.counts.failed + bt.counts.cancelled;
  const inFlight = bt.counts.running + bt.counts.queued;
  const committed = Math.min(bt.spent_usd + inFlight * bt.estimate_per_run_usd, bt.budget_usd);
  const [pillClass, pillLabel] = BT_STATUS[bt.status];
  const dated = c.grid.sample ? `${c.dates.length} of ${c.grid.grid_size} weekly dates` : `${c.dates.length} weekly dates`;

  const act = async (action: "start" | "pause" | "cancel") => {
    setBusy(true);
    setError(undefined);
    try {
      await api.backtestAction(bt.id, action);
      onChange();
    } catch (e: any) {
      setError(String(e.message ?? e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="panel panel-pad bt">
      <div className="bt-head">
        <div>
          <h2>
            {bt.name} <span className={`pill ${pillClass}`}>{pillLabel}</span>
          </h2>
          <div className="bt-config">
            TradingAgents {versionLabel(c.engine_version)} · {c.variant ? `${VARIANT_LABELS[c.variant] ?? c.variant} · ` : ""}{c.tickers.join(" + ")} · {dated} from {c.grid.start} to {c.grid.end} · {c.analysts.map((a) => ANALYST_NAMES[a] ?? a).join(" + ")} · memory {c.memory} ·{" "}
            <span className="mono" style={{ fontSize: 11.5 }}>{modelLabel(c.quick_model)} · {modelLabel(c.deep_model)}</span> · debate rounds {c.depth}
          </div>
        </div>
        <div className="bt-actions">
          {(bt.status === "ready" || bt.status === "paused") && (
            <button className="btn btn-primary" disabled={busy} onClick={() => act("start")}>{bt.status === "ready" ? "Start" : "Resume"}</button>
          )}
          {bt.status === "running" && <button className="btn" disabled={busy} onClick={() => act("pause")}>Pause</button>}
          {(bt.status === "running" || bt.status === "paused" || bt.status === "ready") && (
            <button className="btn btn-ghost" disabled={busy} onClick={() => act("cancel")}>Cancel</button>
          )}
        </div>
      </div>

      <div className="metrics">
        <div className="metric"><span className="cap">Runs done</span><b>{done} / {bt.items.length}</b></div>
        <div className="metric"><span className="cap">In flight</span><b>{inFlight}</b></div>
        <div className="metric"><span className="cap">Failed</span><b style={{ color: bt.counts.failed ? "var(--bad)" : undefined }}>{bt.counts.failed}</b></div>
        <div className="metric"><span className="cap">Est. per run</span><b>{fmtUsd(bt.estimate_per_run_usd)}</b></div>
        <div className="budget">
          <span className="cap">Spent {fmtUsd(bt.spent_usd)} of {fmtUsd(bt.budget_usd)} cap</span>
          <div className="budget-bar" role="img" aria-label={`Spent ${fmtUsd(bt.spent_usd)} of ${fmtUsd(bt.budget_usd)}`}>
            <em style={{ left: 0, width: `${(committed / bt.budget_usd) * 100}%` }} />
            <i style={{ width: `${Math.min(bt.spent_usd / bt.budget_usd, 1) * 100}%` }} />
          </div>
          <span className="muted" style={{ fontSize: 11.5 }}>About {fmtUsd(bt.estimate_remaining_usd)} still to spend</span>
        </div>
      </div>

      {bt.counts.finished > 0 && (
        <div className="cta-center">
          <button className="btn btn-primary btn-lg" onClick={() => navigate(`/backtests/${bt.id}`)}>
            View results →
          </button>
          <span className="muted">Equity curves, trades with reasons, benchmarks and the placebo, from {bt.counts.finished} finished decision{bt.counts.finished === 1 ? "" : "s"}. No extra LLM cost.</span>
        </div>
      )}

      {bt.note && <div className="bt-note">{bt.note}</div>}
      {error && <div className="error">{error}</div>}

      <div className="table-wrap">
        <table className="table">
          <thead>
            <tr>
              <th>Decision date</th>
              <th>Ticker</th>
              <th>Status</th>
              <th>Rating</th>
              <th className="r">Cost est.</th>
              <th className="r">Duration</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {bt.items.map((it) => (
              <ItemRow key={`${it.date}-${it.ticker}`} it={it} onOpen={() => it.run_id && navigate(`/runs/${it.run_id}`)} />
            ))}
          </tbody>
        </table>
      </div>

      <p className="bt-honesty">
        This page generates the decisions; View results replays them into trades, returns and benchmarks at no extra LLM cost. Prices are
        cut at each decision date and today's company profile is withheld. Financial statements may include figures filed after the date, and the model may
        already know how these dates played out. Failed runs are retried once and never counted as Holds.
      </p>
    </section>
  );
}

function ItemRow({ it, onOpen }: { it: BacktestItem; onOpen: () => void }) {
  const dash = <span className="muted">—</span>;
  const notes = [it.reused && "reused earlier run", it.attempts > 1 && `${it.attempts} attempts`].filter(Boolean).join(" · ");
  return (
    <tr onClick={onOpen} style={{ cursor: it.run_id ? "pointer" : "default" }}>
      <td className="num">{it.date}</td>
      <td style={{ fontWeight: 700 }}>{it.ticker}</td>
      <td>{it.status === "pending" ? <span className="muted">Waiting</span> : <StatusCell status={it.status} />}</td>
      <td className="rating" style={{ color: ratingColor(it.rating) }}>{it.rating ?? dash}</td>
      <td className="r">{it.cost_usd ? fmtUsd(it.cost_usd) : dash}</td>
      <td className="r">{it.duration_s != null ? fmtDuration(it.duration_s) : dash}</td>
      <td className="muted">{notes || ""}</td>
    </tr>
  );
}
