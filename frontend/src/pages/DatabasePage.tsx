import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, type Run, type SearchResult } from "../api";
import { DownloadIcon } from "../components/Icons";
import { RATINGS, VARIANT_LABELS, engineLabel, modelLabel, versionLabel, versionTitle } from "../components/RunFilters";
import { fmtDate, fmtPrice, fmtUsd, ratingColor } from "../format";
import { StatusCell } from "./RunsPage";

const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };
const HORIZONS = ["≤ 1 month", "1–3 months", "3–6 months", "6–12 months", "> 1 year", "Other", "None"];

/** Bucket the portfolio manager's free-text horizon ("3-6 months", "Event-driven; reassess…") so it can be filtered. */
export function horizonBucket(text: string | null | undefined): string {
  if (!text) return "None";
  const t = text.toLowerCase();
  const m = t.match(/(\d+(?:\.\d+)?)\s*(?:-|–|to)?\s*(\d+(?:\.\d+)?)?\s*(day|week|month|quarter|year)/);
  if (!m) return "Other";
  const upper = Number(m[2] ?? m[1]);
  const months = { day: upper / 30, week: upper / 4.33, month: upper, quarter: upper * 3, year: upper * 12 }[m[3] as "day"] ?? upper;
  if (months <= 1) return "≤ 1 month";
  if (months <= 3) return "1–3 months";
  if (months <= 6) return "3–6 months";
  if (months <= 12) return "6–12 months";
  return "> 1 year";
}

type Facet = { key: string; label: string; values: (r: Run) => string[]; format?: (v: string) => string; order?: string[] };

const FACETS: Facet[] = [
  { key: "framework", label: "Framework", values: (r) => [engineLabel(r)] },
  { key: "variant", label: "Variant", values: (r) => [r.variant ? VARIANT_LABELS[r.variant] ?? r.variant : "Stock"] },
  { key: "quick", label: "Quick LLM", values: (r) => [r.quick_model], format: modelLabel },
  { key: "deep", label: "Deep LLM", values: (r) => [r.deep_model], format: modelLabel },
  { key: "served", label: "Model actually served", values: (r) => (r.models_served ?? []).map((s) => s.split("->").pop()!.trim()), format: modelLabel },
  { key: "provider", label: "Provider", values: (r) => [r.provider || "unknown"] },
  { key: "ticker", label: "Ticker", values: (r) => [r.ticker] },
  { key: "rating", label: "Rating", values: (r) => [r.rating ?? "None"], order: [...RATINGS, "None"] },
  { key: "horizon", label: "Horizon", values: (r) => [horizonBucket(r.decision?.portfolio?.time_horizon)], order: HORIZONS },
  { key: "analysts", label: "Analysts", values: (r) => r.analysts, format: (a) => ANALYST_NAMES[a] ?? a, order: ["market", "social", "news", "fundamentals"] },
  { key: "depth", label: "Debate rounds", values: (r) => [String(r.depth)] },
  { key: "purpose", label: "Purpose", values: (r) => [r.purpose ?? "live"], format: (p) => (p === "live" ? "Live" : "Backtest") },
  { key: "memory", label: "Memory", values: (r) => [r.memory ?? "shared"] },
  { key: "status", label: "Status", values: (r) => [r.status], format: (s) => s[0].toUpperCase() + s.slice(1) },
];

const GROUPS = FACETS.filter((f) => ["framework", "variant", "quick", "deep", "served", "ticker", "horizon", "purpose", "rating"].includes(f.key));

type Selection = Record<string, Set<string>>;

function matches(run: Run, sel: Selection, skip?: string): boolean {
  for (const f of FACETS) {
    if (f.key === skip) continue;
    const chosen = sel[f.key];
    if (!chosen || chosen.size === 0) continue;
    if (!f.values(run).some((v) => chosen.has(v))) return false;
  }
  return true;
}

export default function DatabasePage() {
  const navigate = useNavigate();
  const [runs, setRuns] = useState<Run[]>();
  const [error, setError] = useState<string>();
  const [sel, setSel] = useState<Selection>({});
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [query, setQuery] = useState("");
  const [search, setSearch] = useState<SearchResult>();
  const [searching, setSearching] = useState(false);
  const [groupBy, setGroupBy] = useState("quick");
  const [open, setOpen] = useState<Record<string, boolean>>({ framework: true, quick: true, deep: true, ticker: true, rating: true, horizon: true, purpose: true });

  const load = useCallback(() => api.allRuns().then(setRuns).catch((e) => setError(String(e.message ?? e))), []);
  useEffect(() => {
    load();
  }, [load]);

  const searchIds = useMemo(() => (search ? new Set(search.runs.map((r) => r.run_id)) : undefined), [search]);
  const base = useMemo(
    () => (runs ?? []).filter((r) => (!from || r.trade_date >= from) && (!to || r.trade_date <= to) && (!searchIds || searchIds.has(r.id))),
    [runs, from, to, searchIds],
  );
  const shown = useMemo(() => base.filter((r) => matches(r, sel)).sort((a, b) => b.created_at - a.created_at), [base, sel]);

  const counts = useMemo(() => {
    const out: Record<string, Map<string, number>> = {};
    for (const f of FACETS) {
      const m = new Map<string, number>();
      for (const r of base) {
        if (!matches(r, sel, f.key)) continue;
        for (const v of new Set(f.values(r))) m.set(v, (m.get(v) ?? 0) + 1);
      }
      out[f.key] = m;
    }
    return out;
  }, [base, sel]);

  const toggle = (key: string, value: string) =>
    setSel((s) => {
      const next = new Set(s[key] ?? []);
      next.has(value) ? next.delete(value) : next.add(value);
      return { ...s, [key]: next };
    });
  const active = Object.values(sel).reduce((n, s) => n + s.size, 0) + (from ? 1 : 0) + (to ? 1 : 0) + (search ? 1 : 0);

  const runSearch = async () => {
    const q = query.trim();
    if (!q) return setSearch(undefined);
    setSearching(true);
    try {
      setSearch(await api.search(q));
    } finally {
      setSearching(false);
    }
  };

  const summary = useMemo(() => {
    const ratings = new Map<string, number>();
    for (const r of shown) if (r.rating) ratings.set(r.rating, (ratings.get(r.rating) ?? 0) + 1);
    return {
      tickers: new Set(shown.map((r) => r.ticker)).size,
      cost: shown.reduce((s, r) => s + (r.cost_usd || 0), 0),
      ratings: RATINGS.filter((x) => ratings.has(x)).map((x) => [x, ratings.get(x)!] as const),
    };
  }, [shown]);

  const groupFacet = GROUPS.find((g) => g.key === groupBy)!;
  const grouped = useMemo(() => {
    const rows = new Map<string, { n: number; holds: number; rated: number; cost: number; failed: number }>();
    for (const r of shown) {
      for (const v of new Set(groupFacet.values(r))) {
        const g = rows.get(v) ?? { n: 0, holds: 0, rated: 0, cost: 0, failed: 0 };
        g.n += 1;
        g.cost += r.cost_usd || 0;
        if (r.rating) {
          g.rated += 1;
          if (r.rating === "Hold") g.holds += 1;
        }
        if (r.status === "failed") g.failed += 1;
        rows.set(v, g);
      }
    }
    return [...rows.entries()].sort((a, b) => b[1].n - a[1].n);
  }, [shown, groupFacet]);

  if (error) return <div className="error">{error}</div>;
  if (!runs) return <div className="empty">Loading the run database…</div>;

  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <h1>Database</h1>
          <span className="subtitle">Every run ever recorded, live or backtest, with its framework, models, decision and full log. Filter on the left, search inside the logs, open any row.</span>
        </div>
        <a className="btn" href="/api/runs.csv"><DownloadIcon /> Export CSV</a>
      </header>

      <div className="db-layout">
        <aside className="db-facets">
          <div className="db-facet">
            <span className="cap">Trade date</span>
            <div style={{ display: "flex", gap: 6 }}>
              <input className="input" type="date" value={from} onChange={(e) => setFrom(e.target.value)} aria-label="From" style={{ width: "50%" }} />
              <input className="input" type="date" value={to} onChange={(e) => setTo(e.target.value)} aria-label="To" style={{ width: "50%" }} />
            </div>
          </div>
          {FACETS.map((f) => {
            const m = counts[f.key];
            const values = [...m.keys()].sort((a, b) => (f.order ? (f.order.indexOf(a) + 1 || 99) - (f.order.indexOf(b) + 1 || 99) : (m.get(b)! - m.get(a)!) || a.localeCompare(b)));
            const chosen = sel[f.key] ?? new Set<string>();
            const isOpen = open[f.key] ?? false;
            if (values.length === 0 && chosen.size === 0) return null;
            return (
              <div key={f.key} className="db-facet">
                <button className="db-facet-head" onClick={() => setOpen((o) => ({ ...o, [f.key]: !isOpen }))} aria-expanded={isOpen}>
                  <span className="cap">{f.label}</span>
                  <span className="muted" style={{ fontSize: 11 }}>{chosen.size ? `${chosen.size} chosen` : `${values.length}`} {isOpen ? "▾" : "▸"}</span>
                </button>
                {isOpen && (
                  <div className="db-values">
                    {values.map((v) => {
                      const on = chosen.has(v);
                      return (
                        <button key={v} className={`db-value${on ? " on" : ""}`} aria-pressed={on} onClick={() => toggle(f.key, v)}>
                          <span className="clip" style={{ color: f.key === "rating" ? ratingColor(v) : undefined }}>{f.format ? f.format(v) : v}</span>
                          <span className="db-count">{m.get(v) ?? 0}</span>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
          {active > 0 && (
            <button className="btn btn-ghost" style={{ color: "var(--accent)", alignSelf: "flex-start" }} onClick={() => { setSel({}); setFrom(""); setTo(""); setSearch(undefined); setQuery(""); }}>
              Clear all filters
            </button>
          )}
        </aside>

        <div className="db-main">
          <form className="log-search" onSubmit={(e) => { e.preventDefault(); runSearch(); }}>
            <input className="input" style={{ flex: 1, minWidth: 220 }} placeholder='Search inside reports and reasoning, e.g. "golden cross" or "valuation not provided"' value={query} onChange={(e) => setQuery(e.target.value)} aria-label="Search inside logs" />
            <button className="btn" type="submit" disabled={searching}>{searching ? "Searching…" : "Search logs"}</button>
            {search && <button className="btn btn-ghost" type="button" onClick={() => { setSearch(undefined); setQuery(""); }}>Clear</button>}
          </form>

          <div className="filters-summary">
            <b>{shown.length}</b> of {runs.length} runs · {summary.tickers} tickers
            {summary.ratings.map(([x, n]) => (
              <span key={x}>{" · "}<span style={{ color: ratingColor(x), fontWeight: 600 }}>{x}</span> {n}</span>
            ))}
            {" · "}{fmtUsd(summary.cost)} est.
            {search && <span>{" · "}{search.total_hits} text matches for “{search.query}”</span>}
          </div>

          <section className="panel panel-pad res-section">
            <div className="chart-controls">
              <h2 style={{ margin: 0, fontSize: 14 }}>Breakdown</h2>
              <div className="seg" role="radiogroup" aria-label="Group by">
                {GROUPS.map((g) => (
                  <button key={g.key} role="radio" aria-checked={groupBy === g.key} className={groupBy === g.key ? "on" : ""} onClick={() => setGroupBy(g.key)}>{g.label}</button>
                ))}
              </div>
            </div>
            <div className="table-wrap">
              <table className="table compact static">
                <thead>
                  <tr>
                    <th>{groupFacet.label}</th>
                    <th className="r">Runs</th>
                    <th className="r">Rated</th>
                    <th className="r">Hold share</th>
                    <th className="r">Failed</th>
                    <th className="r">Avg cost</th>
                    <th className="r">Total cost</th>
                  </tr>
                </thead>
                <tbody>
                  {grouped.map(([v, g]) => (
                    <tr key={v}>
                      <td style={{ fontWeight: 600, color: groupBy === "rating" ? ratingColor(v) : undefined }}>{groupFacet.format ? groupFacet.format(v) : v}</td>
                      <td className="r">{g.n}</td>
                      <td className="r">{g.rated}</td>
                      <td className="r">{g.rated ? `${Math.round((g.holds / g.rated) * 100)}%` : "—"}</td>
                      <td className="r" style={{ color: g.failed ? "var(--bad)" : undefined }}>{g.failed}</td>
                      <td className="r">{fmtUsd(g.n ? g.cost / g.n : 0)}</td>
                      <td className="r">{fmtUsd(g.cost)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel">
            {shown.length === 0 ? (
              <div className="panel-pad"><div className="empty">No runs match these filters.</div></div>
            ) : (
              <div className="table-wrap">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Status</th>
                      <th>Ticker</th>
                      <th>Trade date</th>
                      <th>Framework</th>
                      <th>Variant</th>
                      <th>Quick · Deep</th>
                      <th>Rating</th>
                      <th>Horizon</th>
                      <th className="r">Target</th>
                      <th className="r">Entry</th>
                      <th className="r">Stop</th>
                      <th>Analysts</th>
                      <th>Purpose</th>
                      <th className="r">Cost</th>
                      <th>Run</th>
                    </tr>
                  </thead>
                  <tbody>
                    {shown.map((r) => {
                      const d = r.decision;
                      const dash = <span className="muted">—</span>;
                      return (
                        <tr key={r.id} onClick={() => navigate(`/runs/${r.id}`)}>
                          <td><StatusCell status={r.status} /></td>
                          <td style={{ fontWeight: 700 }}>{r.ticker}</td>
                          <td className="num">{r.trade_date}</td>
                          <td title={versionTitle(r.engine_version)}>TradingAgents <span className="muted mono" style={{ fontSize: 10.5 }}>{versionLabel(r.engine_version)}</span></td>
                          <td style={{ color: "var(--ink-2)" }}>{r.variant ? VARIANT_LABELS[r.variant] ?? r.variant : "Stock"}</td>
                          <td className="mono" style={{ fontSize: 11.5, color: "var(--ink-2)" }}>{modelLabel(r.quick_model)} · {modelLabel(r.deep_model)}</td>
                          <td className="rating" style={{ color: ratingColor(r.rating) }}>{r.rating ?? dash}</td>
                          <td className="clip" title={d?.portfolio?.time_horizon ?? undefined}>{horizonBucket(d?.portfolio?.time_horizon)}</td>
                          <td className="r">{d?.portfolio?.price_target != null ? fmtPrice(d.portfolio.price_target) : dash}</td>
                          <td className="r">{d?.trader?.entry_price != null ? fmtPrice(d.trader.entry_price) : dash}</td>
                          <td className="r">{d?.trader?.stop_loss != null ? fmtPrice(d.trader.stop_loss) : dash}</td>
                          <td className="mono" style={{ fontSize: 11 }}>{r.analysts.map((a) => (ANALYST_NAMES[a] ?? a)[0]).join("")}</td>
                          <td className="muted">{r.purpose === "backtest" ? "Backtest" : "Live"}</td>
                          <td className="r">{fmtUsd(r.cost_usd)}</td>
                          <td className="muted" title={r.id}>{fmtDate(r.created_at)}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>
      </div>
    </>
  );
}
