import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api, type BacktestResults, type SimMetrics, type SimPeriod, type SimTicker, type VariantCompare } from "../api";
import { Legend, LineChart, type LegendItem, type Level, type Marker, type Span } from "../components/Charts";
import { VARIANT_LABELS, modelLabel, versionLabel } from "../components/RunFilters";
import { fmtPrice, fmtUsd, ratingColor } from "../format";

const COLORS: Record<string, string> = {
  agents_levels: "var(--series-1)",
  agents_rating: "var(--series-2)",
  buy_hold: "var(--series-3)",
  ma_cross: "var(--series-4)",
};
const DASH: Record<string, string | undefined> = { ma_cross: "5 4" };
const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };
const COSTS = [0, 10, 25];

function pct(v: number | null | undefined, digits = 1, sign = true): string {
  if (v == null || !isFinite(v)) return "—";
  const s = (v * 100).toFixed(digits);
  return `${sign && v > 0 ? "+" : ""}${s}%`;
}
const num = (v: number | null | undefined, digits = 2) => (v == null || !isFinite(v) ? "—" : v.toFixed(digits));

export default function BacktestResultsPage() {
  const { backtestId = "" } = useParams();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const cost = COSTS.includes(Number(params.get("cost"))) ? Number(params.get("cost")) : 10;
  const [data, setData] = useState<BacktestResults>();
  const [compare, setCompare] = useState<VariantCompare>();
  const [error, setError] = useState<string>();
  const tab = params.get("tab") ?? undefined;
  const setParam = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    next.set(key, value);
    setParams(next, { replace: true });
  };
  const setCost = (v: number) => setParam("cost", String(v));
  const setTab = (v: string) => setParam("tab", v);

  useEffect(() => {
    setError(undefined);
    api.backtestResults(backtestId, cost).then(setData).catch((e) => setError(String(e.message ?? e)));
    api.backtestCompare(backtestId, cost).then(setCompare).catch(() => setCompare(undefined));
  }, [backtestId, cost]);

  const views = useMemo(() => (data ? [...data.tickers, ...(data.combined ? [data.combined] : [])] : []), [data]);
  const view = views.find((v) => v.ticker === tab) ?? views[0];

  if (error) return <div className="error">{error}</div>;
  if (!data || !view) return <div className="empty">Replaying saved decisions against prices…</div>;

  const c = data.config;
  const perTicker = c.dates.length;
  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4, minWidth: 0 }}>
          <Link to="/backtests" className="back-link">← Backtests</Link>
          <h1>{data.name}</h1>
          <span className="subtitle">
            TradingAgents {versionLabel(c.engine_version)}{c.variant ? ` · ${VARIANT_LABELS[c.variant] ?? c.variant}` : ""} · {c.tickers.join(" + ")} · {perTicker} decisions per stock ({c.grid.sample ? `${perTicker} of ${c.grid.grid_size} weekly dates` : "weekly"}) ·{" "}
            {c.analysts.map((a) => ANALYST_NAMES[a] ?? a).join(" + ")} · memory {c.memory} · {modelLabel(c.quick_model)} · {modelLabel(c.deep_model)} · LLM cost {fmtUsd(data.spent_usd)}
          </span>
        </div>
        <label className="filter-field" style={{ flexShrink: 0 }}>
          <span className="cap">Trading costs</span>
          <select id="bt-cost" className="select" value={cost} onChange={(e) => setCost(Number(e.target.value))}>
            {COSTS.map((x) => (
              <option key={x} value={x}>{x} bps per trade</option>
            ))}
          </select>
        </label>
      </header>

      {perTicker < 26 && (
        <div className="bt-note">
          Demo: {perTicker} decisions per stock is far too few to judge skill. Use this page to check the method and read how the agents behaved.
        </div>
      )}

      {data.siblings && data.siblings.length > 1 && (
        <div className="variant-bar">
          <span className="cap">Framework variant</span>
          <div className="seg" role="radiogroup" aria-label="Framework variant">
            {data.siblings.map((s) => (
              <button
                key={s.id}
                role="radio"
                aria-checked={s.id === backtestId}
                className={s.id === backtestId ? "on" : ""}
                onClick={() => navigate(`/backtests/${s.id}?${new URLSearchParams({ tab: view.ticker, cost: String(cost) })}`)}
                title={s.name}
              >
                {s.variant ? VARIANT_LABELS[s.variant] ?? s.variant : "Stock"}
                {s.finished < s.total && <small>{s.finished}/{s.total}</small>}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="tabs" role="tablist" aria-label="Stock">
        {views.map((v) => (
          <button key={v.ticker} role="tab" aria-selected={v.ticker === view.ticker} className={`tab${v.ticker === view.ticker ? " on" : ""}`} onClick={() => setTab(v.ticker)}>
            {v.ticker === "Combined" ? "Both, equal weight" : v.ticker}
          </button>
        ))}
      </div>

      {compare && compare.variants.length > 1 && <VariantTable compare={compare} ticker={view.ticker} current={backtestId} cost={cost} />}

      <TickerView key={`${backtestId}-${view.ticker}`} view={view} data={data} />
    </>
  );
}

const RATING_SHORT: Record<string, string> = { Buy: "B", Overweight: "O", Hold: "H", Underweight: "U", Sell: "S" };

function VariantTable({ compare, ticker, current, cost }: { compare: VariantCompare; ticker: string; current: string; cost: number }) {
  const navigate = useNavigate();
  return (
    <section className="panel panel-pad res-section">
      <div className="res-head">
        <h2>Variants on these dates</h2>
        <p className="caption">Same stocks, dates, analysts and models; only the framework variant differs. Click a row to open it.</p>
      </div>
      <div className="table-wrap">
        <table className="table compact">
          <thead>
            <tr>
              <th>Variant</th>
              <th>Ratings</th>
              <th className="r">Rating only</th>
              <th className="r">Trader levels</th>
              <th className="r">Trades</th>
              <th className="r">Buy and hold</th>
              <th className="r">LLM cost</th>
            </tr>
          </thead>
          <tbody>
            {compare.variants.map((v) => {
              const row = v.views[ticker];
              return (
                <tr key={v.id} className={v.id === current ? "hl-row" : ""} onClick={() => navigate(`/backtests/${v.id}?${new URLSearchParams({ tab: ticker, cost: String(cost) })}`)}>
                  <td style={{ fontWeight: 600 }}>
                    {v.variant ? VARIANT_LABELS[v.variant] ?? v.variant : "Stock"}
                    {v.finished < v.total && <span className="muted" style={{ fontWeight: 400 }}> · {v.finished}/{v.total} runs</span>}
                  </td>
                  <td>
                    {row ? (
                      <span className="rating-chips">
                        {Object.entries(row.ratings).map(([r, n]) => (
                          <span key={r} className="rating-chip" style={{ color: ratingColor(r) }} title={`${n} × ${r}`}>{n} {r}</span>
                        ))}
                      </span>
                    ) : (
                      <span className="muted">waiting</span>
                    )}
                  </td>
                  <td className="r">{pct(row?.rating_only?.total_return)}</td>
                  <td className="r">{pct(row?.levels?.total_return)}</td>
                  <td className="r">{row?.levels ? `${row.levels.trades} / ${row.rating_only?.trades ?? 0}` : "—"}</td>
                  <td className="r">{pct(row?.buy_hold)}</td>
                  <td className="r">{fmtUsd(v.spent_usd)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="caption">Trades column: trader levels / rating only. Partly finished variants replay only their finished decisions.</p>
    </section>
  );
}

function shortReason(reason: string): string {
  let m = reason.match(/^rating (\w+)/);
  if (m) return `rated ${m[1]}`;
  m = reason.match(/close [\d.]+ above ([\d.]+)/);
  if (m) return `close above ${m[1]}`;
  m = reason.match(/^confirmation entry ([\d.]+)/);
  if (m) return `broke above ${m[1]}`;
  m = reason.match(/^pullback entry ([\d.]+)/);
  if (m) return `dip to ${m[1]}`;
  m = reason.match(/at or below ([\d.]+)/);
  if (m) return `stop ${m[1]} broken`;
  m = reason.match(/^stop ([\d.]+)/);
  if (m) return `stop ${m[1]} hit`;
  return reason;
}

function TransactionLog({ periods, hl, onHover }: { periods: SimPeriod[]; hl: number | null; onHover: (n: number | null) => void }) {
  const navigate = useNavigate();
  return (
    <div className="table-wrap">
      <table className="table compact log-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Period</th>
            <th className="r">Position</th>
            <th>Why it changed</th>
            <th className="r">Stock</th>
            <th className="r">Book, approx.</th>
            <th>Verdict</th>
          </tr>
        </thead>
        <tbody>
          {periods.map((p, k) => {
            const n = p.opened_by?.n ?? null;
            const verdictClass = p.verdict === "held" ? "held" : p.verdict === "missed gain" ? "missed" : p.verdict === "avoided loss" ? "avoided" : "flat";
            return (
              <tr
                key={k}
                className={n != null && n === hl ? "hl" : ""}
                onMouseEnter={() => onHover(n)}
                onMouseLeave={() => onHover(null)}
                onClick={() => p.opened_by?.run_id && navigate(`/runs/${p.opened_by.run_id}`)}
                title={p.opened_by?.run_id ? "Open the run behind this change" : undefined}
                style={{ cursor: p.opened_by?.run_id ? "pointer" : "default" }}
              >
                <td>{n != null ? <span className="log-num">{n}</span> : <span className="muted">start</span>}</td>
                <td className="num" style={{ whiteSpace: "nowrap" }}>
                  {p.start} → {p.ongoing ? <span className="muted">now</span> : p.end}
                </td>
                <td className="r">{pct(p.weight, 0, false)}</td>
                <td>
                  {p.opened_by ? (
                    <>
                      <b style={{ color: p.opened_by.side === "buy" ? "var(--good)" : "var(--bad)" }}>{p.opened_by.side === "buy" ? "Buy" : "Sell"}</b> at {fmtPrice(p.opened_by.price)} ·{" "}
                      {p.opened_by.reasons.map(shortReason).join(", ")}
                    </>
                  ) : (
                    <span className="muted">Starting position</span>
                  )}
                </td>
                <td className="r">{pct(p.stock_return)}</td>
                <td className="r">{pct(p.book_return)}</td>
                <td>
                  <span className={`verdict ${verdictClass}`}>{p.verdict === "held" ? "In the stock" : p.verdict === "flat" ? "In cash" : p.verdict}</span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function Headline({ view }: { view: SimTicker }) {
  const get = (k: string) => view.strategies.find((s) => s.key === k)?.metrics;
  const lv = get("agents_levels");
  const rt = get("agents_rating");
  const bh = get("buy_hold");
  const holds = view.decisions?.filter((d) => d.rating === "Hold").length ?? 0;
  const total = view.decisions?.length ?? 0;
  return (
    <p className="headline">
      Trading the agents' own entry and stop levels returned <b>{pct(lv?.total_return)}</b> over {lv?.days ?? 0} trading days, against{" "}
      <b>{pct(bh?.total_return)}</b> for buy and hold.
      {rt && rt.trades === 0
        ? ` Ratings alone never traded${total ? `: ${holds} of ${total} decisions were Hold` : ""}.`
        : ` Ratings alone returned ${pct(rt?.total_return)}.`}
    </p>
  );
}

function TickerView({ view, data }: { view: SimTicker; data: BacktestResults }) {
  const navigate = useNavigate();
  const isTicker = view.ticker !== "Combined";
  const idx = useMemo(() => new Map(view.dates.map((d, i) => [d, i])), [view.dates]);
  const nearest = (day: string) => {
    if (idx.has(day)) return idx.get(day)!;
    let best = 0;
    view.dates.forEach((d, i) => d <= day && (best = i));
    return best;
  };

  const equitySeries = view.strategies.map((s) => ({ key: s.key, label: s.label, color: COLORS[s.key], values: s.equity, dash: DASH[s.key] }));
  const bandFlat = view.placebo.p95.every((v, i) => Math.abs(v - view.placebo.p5[i]) < 1e-6);
  const legend: LegendItem[] = [
    ...view.strategies.map((s) => ({ label: s.label, color: COLORS[s.key], kind: DASH[s.key] ? ("dash" as const) : ("line" as const) })),
    { label: `Random placebo, 5th to 95th percentile (${view.placebo.sims} ${view.placebo.exhaustive ? (view.placebo.sims === 1 ? "ordering" : "orderings") : "draws"})`, color: "var(--band)", kind: "band" },
  ];

  const [annotate, setAnnotate] = useState<"agents_levels" | "agents_rating">("agents_levels");
  const [hl, setHl] = useState<number | null>(null);
  const annotated = view.strategies.find((s) => s.key === annotate);
  const trades = annotated?.trades ?? [];
  const groups = useMemo(() => {
    const out: { n: number; date: string; side: "buy" | "sell"; price: number; weight: number; reasons: string[] }[] = [];
    for (const t of trades) {
      const n = t.n ?? out.length + 1;
      const last = out[out.length - 1];
      if (last && last.n === n) {
        last.reasons.push(t.reason);
        last.side = t.side;
        last.weight = t.weight_after;
      } else out.push({ n, date: t.date, side: t.side, price: t.price, weight: t.weight_after, reasons: [t.reason] });
    }
    return out;
  }, [trades]);
  const withLabels = groups.length <= 8;
  const equityMarkers: Marker[] = annotated
    ? groups.map((g) => {
        const i = nearest(g.date);
        const why = g.reasons.map(shortReason).join(", ");
        return {
          i,
          y: annotated.equity[i],
          shape: g.side === "buy" ? "up" : "down",
          color: g.side === "buy" ? "var(--good)" : "var(--bad)",
          badge: String(g.n),
          label: withLabels ? `${g.side === "buy" ? "Buy" : "Sell"} to ${pct(g.weight, 0, false)} · ${why}` : undefined,
          highlight: hl === g.n,
          onHover: (on: boolean) => setHl(on ? g.n : null),
          title: `${g.n}. ${g.date} ${g.side} at ${fmtPrice(g.price)}, position now ${pct(g.weight, 0, false)} · ${g.reasons.join("; ")}`,
        };
      })
    : [];
  const holdingSpans: Span[] = (annotated?.periods ?? [])
    .filter((p) => p.weight > 1e-6)
    .map((p) => ({
      i0: nearest(p.start),
      i1: nearest(p.end),
      color: "var(--series-1)",
      opacity: 0.05 + 0.07 * Math.min(p.weight, 1),
      title: `Holding ${pct(p.weight, 0, false)} from ${p.start} to ${p.ongoing ? "now" : p.end}`,
    }));

  const levelsStrategy = annotated;
  const priceMarkers: Marker[] = [];
  const priceLevels: Level[] = [];
  if (isTicker && view.decisions && view.close) {
    view.decisions.forEach((d, k) => {
      const i = nearest(d.date);
      const next = k + 1 < view.decisions!.length ? nearest(view.decisions![k + 1].date) : view.dates.length - 1;
      const i1 = Math.max(next, Math.min(i + 1, view.dates.length - 1));
      if (d.close != null) {
        const kind = d.entry != null && d.close != null ? (d.entry < d.close ? "pullback" : "confirmation") : "";
        if (d.entry != null) priceLevels.push({ i0: i, i1, y: d.entry, color: "var(--series-1)", dash: "5 4", title: `Entry ${fmtPrice(d.entry)} (${kind})` });
        if (d.stop != null) priceLevels.push({ i0: i, i1, y: d.stop, color: "var(--bad)", dash: "2 3", title: `Stop ${fmtPrice(d.stop)}` });
      }
    });
    groups.forEach((g) =>
      priceMarkers.push({
        i: nearest(g.date),
        y: g.price,
        shape: g.side === "buy" ? "up" : "down",
        color: g.side === "buy" ? "var(--good)" : "var(--bad)",
        badge: String(g.n),
        highlight: hl === g.n,
        onHover: (on: boolean) => setHl(on ? g.n : null),
        title: `${g.n}. ${g.date} ${g.side} at ${fmtPrice(g.price)} · ${g.reasons.join("; ")}`,
      }),
    );
    view.decisions.forEach((d) => {
      const i = nearest(d.date);
      priceMarkers.push({
        i,
        y: view.close![i],
        shape: "dot",
        badge: d.rating ? RATING_SHORT[d.rating] ?? "?" : "×",
        color: ratingColor(d.rating),
        title: `${d.date} · ${d.rating ?? d.status} at ${fmtPrice(d.close)}${d.entry != null ? ` · entry ${fmtPrice(d.entry)}` : ""}${d.stop != null ? ` · stop ${fmtPrice(d.stop)}` : ""} · click to open the run`,
        onClick: d.run_id ? () => navigate(`/runs/${d.run_id}`) : undefined,
      });
    });
  }
  const ratingsPresent = [...new Set(view.decisions?.map((d) => d.rating ?? "No rating") ?? [])];

  return (
    <>
      <section className="panel panel-pad res-section">
        <div className="res-head">
          <h2>Growth of 100</h2>
          <Headline view={view} />
        </div>
        <div className="chart-controls">
          <Legend items={legend} />
          {isTicker && (
            <div className="seg" role="radiogroup" aria-label="Transactions to label">
              {(["agents_levels", "agents_rating"] as const).map((k) => {
                const s = view.strategies.find((x) => x.key === k);
                return (
                  <button key={k} role="radio" aria-checked={annotate === k} className={annotate === k ? "on" : ""} onClick={() => setAnnotate(k)}>
                    Label {k === "agents_levels" ? "trader levels" : "rating only"}
                    <small>{s?.metrics.trades ?? 0} trades</small>
                  </button>
                );
              })}
            </div>
          )}
        </div>
        <LineChart
          label={`Equity curves for ${view.ticker}`}
          dates={view.dates}
          series={equitySeries}
          band={{ lo: view.placebo.p5, hi: view.placebo.p95, label: "Placebo 5th to 95th" }}
          markers={isTicker ? equityMarkers : []}
          spans={isTicker ? holdingSpans : []}
          height={isTicker && groups.length ? 320 : 260}
          format={(v) => v.toFixed(0)}
          zero={100}
        />
        {bandFlat && <p className="caption">Placebo band is a single line: every decision has the same rating, so shuffling them changes nothing.</p>}
        {isTicker && annotated?.periods && (
          <>
            <h3 className="cap" style={{ marginTop: 6 }}>What happened · {annotated.label}</h3>
            {groups.length === 0 && <p className="caption">No transactions: this strategy stayed in its starting position all period.</p>}
            <TransactionLog periods={annotated.periods} hl={hl} onHover={setHl} />
            <p className="caption">
              Numbers match the badges on the charts; shading marks days in the stock. For a single stock a trade earns exactly what the stock did
              while held, so the verdict for time in cash says whether sitting out missed a gain or avoided a loss. Book return is position × stock
              return, before costs. Click a row to open the run that caused the change.
            </p>
          </>
        )}
      </section>

      {isTicker && view.close && (
        <section className="panel panel-pad res-section">
          <div className="res-head">
            <h2>Price and decisions</h2>
            <p className="caption">Each dot is one agent run, lettered by rating: click it to replay the analysis. Dashed lines show the entry and stop levels the trader set, live until the next decision. Shading and numbered fills follow the strategy chosen above.</p>
          </div>
          <Legend
            items={[
              { label: "Close", color: "var(--ink-2)", kind: "line" },
              ...ratingsPresent.map((r) => ({ label: `${r} decision`, color: ratingColor(r === "No rating" ? null : r), kind: "dot" as const })),
              { label: "Entry level", color: "var(--series-1)", kind: "dash" },
              { label: "Stop level", color: "var(--bad)", kind: "dash" },
              { label: "Buy fill", color: "var(--good)", kind: "up" },
              { label: "Sell fill", color: "var(--bad)", kind: "down" },
            ]}
          />
          <LineChart
            label={`${view.ticker} price with agent decisions`}
            dates={view.dates}
            series={[{ key: "close", label: view.ticker, color: "var(--ink-2)", values: view.close }]}
            markers={priceMarkers}
            levels={priceLevels}
            spans={holdingSpans}
            height={300}
            format={(v) => v.toFixed(0)}
          />
        </section>
      )}

      <section className="panel panel-pad res-section">
        <div className="res-head">
          <h2>Drawdown</h2>
          <p className="caption">Distance below the previous peak.</p>
        </div>
        <LineChart
          label={`Drawdown for ${view.ticker}`}
          dates={view.dates}
          series={view.strategies.map((s) => ({ key: s.key, label: s.label, color: COLORS[s.key], values: s.drawdown, dash: DASH[s.key] }))}
          height={180}
          format={(v) => `${(v * 100).toFixed(0)}%`}
          zero={0}
        />
      </section>

      <section className="panel panel-pad res-section">
        <h2>Performance</h2>
        <div className="table-wrap">
          <table className="table compact static">
            <thead>
              <tr>
                <th>Strategy</th>
                <th className="r">Return</th>
                <th className="r">Annualised</th>
                <th className="r">Volatility</th>
                <th className="r">Sharpe</th>
                <th className="r">Max drawdown</th>
                <th className="r">Time in market</th>
                <th className="r">Trades</th>
                <th className="r">Costs</th>
              </tr>
            </thead>
            <tbody>
              {view.strategies.map((s) => (
                <MetricsRow key={s.key} label={s.label} color={COLORS[s.key]} m={s.metrics} />
              ))}
              <tr>
                <td>
                  <span className="swatch" style={{ background: "var(--band)" }} />
                  Random placebo, median
                </td>
                <td className="r">{pct(view.placebo.p50[view.placebo.p50.length - 1] / 100 - 1)}</td>
                <td className="r muted" colSpan={7} style={{ textAlign: "left" }}>
                  5th to 95th percentile {pct(view.placebo.p5[view.placebo.p5.length - 1] / 100 - 1)} to {pct(view.placebo.p95[view.placebo.p95.length - 1] / 100 - 1)} ·
                  rating-only agents beat or match {pct(view.placebo.agent_percentile, 0, false)} of placebo outcomes
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="caption">Sharpe uses a zero risk-free rate. Annualised figures from under a year of data overstate precision.</p>
      </section>

      {isTicker && (
        <div className="res-grid">
          <section className="panel panel-pad res-section">
            <h2>Decisions</h2>
            <div className="table-wrap">
              <table className="table compact">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Rating</th>
                    <th className="r">Close</th>
                    <th className="r">Entry</th>
                    <th className="r">Stop</th>
                    <th className="r">Return to next decision</th>
                  </tr>
                </thead>
                <tbody>
                  {view.decisions?.map((d) => (
                    <tr key={d.date} onClick={() => d.run_id && navigate(`/runs/${d.run_id}`)} title="Open the run">
                      <td className="num">{d.date}</td>
                      <td className="rating" style={{ color: ratingColor(d.rating) }}>{d.rating ?? d.status}</td>
                      <td className="r">{fmtPrice(d.close)}</td>
                      <td className="r">{fmtPrice(d.entry)}</td>
                      <td className="r">{fmtPrice(d.stop)}</td>
                      <td className="r">{pct(d.forward_return)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel panel-pad res-section">
            <h2>Hold rule sensitivity</h2>
            <p className="caption">Same saved ratings replayed under other readings of Hold. No extra LLM cost.</p>
            <div className="table-wrap">
            <table className="table compact static">
              <thead>
                <tr>
                  <th>Rule</th>
                  <th className="r">Return</th>
                  <th className="r">Max drawdown</th>
                  <th className="r">In market</th>
                </tr>
              </thead>
              <tbody>
                {view.sensitivity?.map((s) => (
                  <tr key={s.key}>
                    <td>{s.label}</td>
                    <td className="r">{pct(s.metrics.total_return)}</td>
                    <td className="r">{pct(s.metrics.max_drawdown)}</td>
                    <td className="r">{pct(s.metrics.time_in_market, 0, false)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
            {view.by_rating && view.by_rating.length > 0 && (
              <>
                <h3 className="cap" style={{ marginTop: 18 }}>Return after each rating</h3>
                <div className="table-wrap">
                <table className="table compact static">
                  <thead>
                    <tr>
                      <th>Rating</th>
                      <th className="r">Decisions</th>
                      <th className="r">Average return</th>
                      <th className="r">Share up</th>
                      <th className="r">Hit rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {view.by_rating.map((r) => (
                      <tr key={r.rating}>
                        <td className="rating" style={{ color: ratingColor(r.rating) }}>{r.rating}</td>
                        <td className="r">{r.n}</td>
                        <td className="r">{pct(r.mean_forward_return)}</td>
                        <td className="r">{pct(r.share_up, 0, false)}</td>
                        <td className="r">{r.hit_rate == null ? <span className="muted" title="Hold makes no directional call">n/a</span> : pct(r.hit_rate, 0, false)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                </div>
              </>
            )}
          </section>
        </div>
      )}

      {isTicker && levelsStrategy?.trades && (
        <section className="panel panel-pad res-section">
          <h2>All fills · {levelsStrategy.label}</h2>
          {levelsStrategy.trades.length === 0 ? (
            <div className="empty">No trades: no entry level was reached and no rating asked for a position.</div>
          ) : (
            <div className="table-wrap">
              <table className="table compact">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Date</th>
                    <th>Side</th>
                    <th className="r">Fill</th>
                    <th className="r">Position</th>
                    <th>Why</th>
                    <th className="r">Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {levelsStrategy.trades.map((t, k) => (
                    <tr key={k} className={t.n != null && t.n === hl ? "hl-row" : ""} onMouseEnter={() => setHl(t.n ?? null)} onMouseLeave={() => setHl(null)}
                      onClick={() => t.run_id && navigate(`/runs/${t.run_id}`)} title="Open the run behind this trade">
                      <td>{t.n != null && <span className="log-num">{t.n}</span>}</td>
                      <td className="num">{t.date}</td>
                      <td style={{ color: t.side === "buy" ? "var(--good)" : "var(--bad)", fontWeight: 600 }}>{t.side === "buy" ? "Buy" : "Sell"}</td>
                      <td className="r">{fmtPrice(t.price)}</td>
                      <td className="r">{pct(t.weight_before, 0, false)} → {pct(t.weight_after, 0, false)}</td>
                      <td>{t.reason}</td>
                      <td className="r">{t.cost.toFixed(3)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <p className="caption">Cost is in the same units as the starting 100.</p>
        </section>
      )}

      <section className="panel panel-pad res-section">
        <h2>How to read this</h2>
        {view.notes?.map((n) => (
          <p key={n} className="bt-note">{n}</p>
        ))}
        <ul className="assumptions">
          <li>Each decision is made after the close of its date and trades at the next session's open, with {data.assumptions.cost_bps} bps on every traded dollar. Cash earns nothing; long only.</li>
          <li><b>Rating only:</b> Buy 100%, Overweight 50%, Hold keeps the position, Underweight and Sell flat. A failed run keeps the position and never counts as a Hold.</li>
          <li><b>Trader levels:</b> also acts on the entry and stop inside each decision. An entry below the close is a pullback buy, above it a confirmation buy, each adding 50%. The stop sells everything. Never stopped out on the entry bar.</li>
          <li><b>Benchmarks:</b> buy and hold from the first decision; a 50/200-day moving-average rule checked on the same decision dates; a placebo that shuffles the agents' own ratings across the dates.</li>
          <li><b>Data:</b> {data.assumptions.prices}. Prices are cut at each decision date and today's company profile is withheld from past runs, but financial statements may include figures filed after the date.</li>
          <li><b>Memorisation:</b> the model may already know how these dates turned out. No result here can separate skill from recall.</li>
        </ul>
      </section>
    </>
  );
}

function MetricsRow({ label, color, m }: { label: string; color: string; m: SimMetrics }) {
  return (
    <tr>
      <td>
        <span className="swatch" style={{ background: color }} />
        {label}
      </td>
      <td className="r" style={{ fontWeight: 600 }}>{pct(m.total_return)}</td>
      <td className="r">{pct(m.annual_return)}</td>
      <td className="r">{pct(m.volatility, 1, false)}</td>
      <td className="r">{num(m.sharpe)}</td>
      <td className="r">{pct(m.max_drawdown)}</td>
      <td className="r">{pct(m.time_in_market, 0, false)}</td>
      <td className="r">{m.trades}</td>
      <td className="r">{m.costs.toFixed(3)}</td>
    </tr>
  );
}
