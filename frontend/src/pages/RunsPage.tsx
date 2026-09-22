import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, type Meta, type Run, type SearchResult } from "../api";
import { RunDots } from "../components/CommitteeBoard";
import { DownloadIcon, PlusIcon } from "../components/Icons";
import { EMPTY_FILTERS, RATINGS, RunFilters, applyFilters, engineLabel, modelLabel, versionLabel, versionTitle, type Filters } from "../components/RunFilters";
import { fmtClock, fmtDate, fmtDuration, fmtPrice, fmtUsd, ratingColor } from "../format";

const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };
const AGENT_NAMES: Record<string, string> = {
  market: "Market", sentiment: "Sentiment", news: "News", fundamentals: "Fundamentals", bull: "Bull", bear: "Bear",
  research_manager: "Research Mgr", trader: "Trader", aggressive: "Aggressive", conservative: "Conservative", neutral: "Neutral", portfolio_manager: "Portfolio Mgr",
};

const KIND: Record<string, string> = { "report.updated": "report", "llm.reasoning": "reasoning", "tool.result": "tool result", "tool.called": "tool call", "data.flag": "flag", "decision.structured": "decision", "run.failed": "error" };

type SortKey = "created" | "ticker" | "trade_date" | "rating" | "duration" | "cost" | "flags";
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

  const shown = useMemo(() => {
    if (!runs) return [];
    const get = SORTERS[sort.key];
    return applyFilters(runs, filters, searchIds).sort((a, b) => {
      const va = get(a);
      const vb = get(b);
      return (va < vb ? -1 : va > vb ? 1 : 0) * sort.dir;
    });
  }, [runs, filters, searchIds, sort]);

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

      {runs && runs.length > 0 && <RunFilters runs={runs} filters={filters} onChange={setFilters} search={search} onSearch={setSearch} shown={shown} />}

      <div className="cta-bar">
        <div>
          <b>Run the agents on a ticker</b>
          <span className="muted">Pick stocks, a date and the analysts; watch the twelve agents work and keep the full log.</span>
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
                      <td title={versionTitle(r.engine_version)}>
                        {engineLabel(r).replace(/ .*/, "")}
                        <span className="muted mono" style={{ fontSize: 10.5, marginLeft: 6 }}>{versionLabel(r.engine_version)}</span>
                      </td>
                      <td className="mono" style={{ fontSize: 11.5, color: "var(--ink-2)" }}>{modelLabel(r.quick_model)} · {modelLabel(r.deep_model)}</td>
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

function NewRunDialog({ meta, onClose, onStarted }: { meta: Meta; onClose: () => void; onStarted: (ids: string[]) => void }) {
  const [tickers, setTickers] = useState("NVDA");
  const [date, setDate] = useState(meta.default_trade_date);
  const [analysts, setAnalysts] = useState<string[]>(meta.analysts);
  const [depth, setDepth] = useState(1);
  const [quick, setQuick] = useState(meta.models.quick[0]);
  const [deep, setDeep] = useState(meta.models.deep[0]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

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
      const res = await api.start({ tickers: list, trade_date: date, analysts, depth, quick_model: quick, deep_model: deep });
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
        <div className="row2">
          <div className="field">
            <label htmlFor="tickers">Tickers</label>
            <input id="tickers" className="input" value={tickers} onChange={(e) => setTickers(e.target.value)} autoFocus placeholder="NVDA, AAPL" />
            <span className="hint">{list.length > 1 ? `${list.length} runs, two at a time` : "Separate several with commas"}</span>
          </div>
          <div className="field">
            <label htmlFor="trade-date">Analysis date</label>
            <input id="trade-date" className="input" type="date" value={date} max={meta.default_trade_date} onChange={(e) => setDate(e.target.value)} />
            <span className="hint" style={{ color: pastDate ? "var(--warn)" : undefined }}>
              {pastDate ? "Past dates get an empty news feed" : "Today gives the fullest news and profile data"}
            </span>
          </div>
        </div>
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
            <label htmlFor="quick-model">Models · quick / deep</label>
            <div style={{ display: "flex", gap: 8 }}>
              <select id="quick-model" className="select" value={quick} onChange={(e) => setQuick(e.target.value)} style={{ flex: 1, minWidth: 0 }}>
                {meta.models.quick.map((m) => <option key={m} value={m}>{m.replace("deepseek-", "")}</option>)}
              </select>
              <select id="deep-model" className="select" aria-label="Deep model" value={deep} onChange={(e) => setDeep(e.target.value)} style={{ flex: 1, minWidth: 0 }}>
                {meta.models.deep.map((m) => <option key={m} value={m}>{m.replace("deepseek-", "")}</option>)}
              </select>
            </div>
          </div>
        </div>
        {error && <div className="error">{error}</div>}
        <div className="dialog-foot">
          <span className="muted" style={{ fontSize: 12 }}>DeepSeek · paper only · no orders are placed</span>
          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn btn-ghost" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" disabled={busy || !list.length || !analysts.length} onClick={submit}>
              {busy ? "Starting…" : list.length > 1 ? `Start ${list.length} runs` : "Start run"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
