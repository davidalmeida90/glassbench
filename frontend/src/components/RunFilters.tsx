import { useEffect, useMemo, useState } from "react";
import { api, type Run, type SearchResult } from "../api";
import type { EngineBuild } from "../api";
import { fmtTokens, fmtUsd, ratingColor } from "../format";

export const RATINGS = ["Buy", "Overweight", "Hold", "Underweight", "Sell", "REVIEW"];
const STATUSES: Run["status"][] = ["finished", "running", "queued", "failed", "cancelled"];
const ANALYST_NAMES: Record<string, string> = { market: "Market", social: "Sentiment", news: "News", fundamentals: "Fundamentals" };

export type Filters = {
  query: string;
  rating: string;
  status: string;
  engine: string;
  purpose: string;
  quick: string;
  deep: string;
  analysts: string[];
  dateFrom: string;
  dateTo: string;
};

export const EMPTY_FILTERS: Filters = { query: "", rating: "all", status: "all", engine: "all", purpose: "all", quick: "all", deep: "all", analysts: [], dateFrom: "", dateTo: "" };

export const VARIANT_LABELS: Record<string, string> = { prompt_pre1196: "Decisive wording", pit_valuation: "+ EDGAR as filed", edgar_statements: "EDGAR statements", edgar_valuation: "EDGAR statements + valuation" };

// Which engine commits are the framework as released and which carry Glassbench's own changes. Filled from /api/meta.
let ENGINE_BUILDS: Record<string, EngineBuild> = {};

export function setEngineBuilds(builds: Record<string, EngineBuild> | undefined) {
  ENGINE_BUILDS = builds ?? {};
}

/** "0.5.0" for a release commit, "0.5.0 adjusted" for the fork. */
export function versionLabel(engineVersion: string | undefined): string {
  if (!engineVersion) return "";
  const base = engineVersion.replace(/^v/, "").replace(/\+.*/, "");
  return ENGINE_BUILDS[engineVersion]?.adjusted ? `${base} adjusted` : base;
}

/** Tooltip: the commit, and for the fork what sets it apart from the release. */
export function versionTitle(engineVersion: string | undefined, engine?: string): string {
  const build = engineVersion ? ENGINE_BUILDS[engineVersion] : undefined;
  const commit = (engineVersion || "").replace(/.*\+/, "") || "unknown";
  if (engine && engine !== "tradingagents") return `commit ${commit} · ${engineName({ engine })} as cloned`;
  if (!build?.adjusted) return `commit ${commit} · TradingAgents as released`;
  return `commit ${commit} · release ${build.version} plus Glassbench's changes: ${build.changes.join("; ") || "see the fork"}`;
}

export function engineName(r: Pick<Run, "engine">): string {
  return r.engine === "tradingagents" ? "TradingAgents" : r.engine === "ai_hedge_fund" ? "AI Hedge Fund" : r.engine || "unknown";
}

export function engineLabel(r: Pick<Run, "engine" | "engine_version">): string {
  const name = engineName(r);
  return r.engine_version ? `${name} ${versionLabel(r.engine_version)}` : name;
}

export function modelLabel(m: string): string {
  return m.replace("deepseek-", "");
}

export function applyFilters(runs: Run[], f: Filters, searchIds?: Set<string>): Run[] {
  const q = f.query.trim().toUpperCase();
  return runs.filter(
    (r) =>
      (!q || r.ticker.includes(q) || r.trade_date.includes(q)) &&
      (f.rating === "all" || r.rating === f.rating) &&
      (f.status === "all" || r.status === f.status) &&
      (f.engine === "all" || engineLabel(r) === f.engine) &&
      (f.purpose === "all" || (r.purpose ?? "live") === f.purpose) &&
      (f.quick === "all" || r.quick_model === f.quick) &&
      (f.deep === "all" || r.deep_model === f.deep) &&
      f.analysts.every((a) => r.analysts.includes(a)) &&
      (!f.dateFrom || r.trade_date >= f.dateFrom) &&
      (!f.dateTo || r.trade_date <= f.dateTo) &&
      (!searchIds || searchIds.has(r.id)),
  );
}

function Select({ id, label, value, options, onChange, format }: { id: string; label: string; value: string; options: string[]; onChange: (v: string) => void; format?: (v: string) => string }) {
  return (
    <label className="filter-field">
      <span className="cap">{label}</span>
      <select id={id} className="select" value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="all">Any</option>
        {options.map((o) => (
          <option key={o} value={o}>{format ? format(o) : o}</option>
        ))}
      </select>
    </label>
  );
}

export function RunFilters({
  runs,
  filters,
  onChange,
  search,
  onSearch,
  shown,
}: {
  runs: Run[];
  filters: Filters;
  onChange: (f: Filters) => void;
  search?: SearchResult;
  onSearch: (result?: SearchResult) => void;
  shown: Run[];
}) {
  const [logQuery, setLogQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [open, setOpen] = useState(false);

  const options = useMemo(
    () => ({
      engines: [...new Set(runs.map(engineLabel))].sort(),
      quick: [...new Set(runs.map((r) => r.quick_model))].sort(),
      deep: [...new Set(runs.map((r) => r.deep_model))].sort(),
      analysts: [...new Set(runs.flatMap((r) => r.analysts))].sort(),
    }),
    [runs],
  );
  const set = (patch: Partial<Filters>) => onChange({ ...filters, ...patch });
  const active =
    [filters.rating, filters.status, filters.engine, filters.purpose, filters.quick, filters.deep].filter((v) => v !== "all").length +
    filters.analysts.length +
    (filters.dateFrom ? 1 : 0) +
    (filters.dateTo ? 1 : 0);

  useEffect(() => {
    if (active > 0) setOpen(true);
  }, [active]);

  const runSearch = async () => {
    const q = logQuery.trim();
    if (!q) {
      onSearch(undefined);
      return;
    }
    setSearching(true);
    try {
      onSearch(await api.search(q));
    } finally {
      setSearching(false);
    }
  };

  const summary = useMemo(() => {
    const counts = new Map<string, number>();
    for (const r of shown) if (r.rating) counts.set(r.rating, (counts.get(r.rating) ?? 0) + 1);
    return {
      tickers: new Set(shown.map((r) => r.ticker)).size,
      cost: shown.reduce((s, r) => s + (r.cost_usd || 0), 0),
      tokens: shown.reduce((s, r) => s + r.tokens_in + r.tokens_out, 0),
      ratings: RATINGS.filter((x) => counts.has(x)).map((x) => [x, counts.get(x)!] as const),
    };
  }, [shown]);

  return (
    <section className="filters-block">
      <div className="filters">
        <input className="input" style={{ width: 200 }} placeholder="Ticker or date" value={filters.query} onChange={(e) => set({ query: e.target.value })} aria-label="Filter by ticker or date" />
        <form
          className="log-search"
          onSubmit={(e) => {
            e.preventDefault();
            runSearch();
          }}
        >
          <input
            className="input"
            style={{ width: 300 }}
            placeholder='Search inside the logs, e.g. "golden cross" or rate limited'
            value={logQuery}
            onChange={(e) => setLogQuery(e.target.value)}
            aria-label="Search inside logs"
          />
          <button className="btn" type="submit" disabled={searching}>{searching ? "Searching…" : "Search logs"}</button>
          {search && (
            <button
              className="btn btn-ghost"
              type="button"
              onClick={() => {
                setLogQuery("");
                onSearch(undefined);
              }}
            >
              Clear
            </button>
          )}
        </form>
        <button className={`btn${open ? " on" : ""}`} type="button" aria-expanded={open} onClick={() => setOpen((v) => !v)}>
          Filters{active ? ` · ${active}` : ""}
        </button>
        <span className="filters-summary">
          <b>{shown.length}</b> of {runs.length} runs · {summary.tickers} tickers
          {summary.ratings.map(([x, n]) => (
            <span key={x}>
              {" · "}
              <span style={{ color: ratingColor(x), fontWeight: 600 }}>{x}</span> {n}
            </span>
          ))}
          {" · "}
          {fmtTokens(summary.tokens)} tokens · {fmtUsd(summary.cost)} est.
        </span>
      </div>

      {open && (
        <div className="filters-panel">
          <Select id="f-engine" label="Framework" value={filters.engine} options={options.engines} onChange={(v) => set({ engine: v })} />
          <Select id="f-purpose" label="Purpose" value={filters.purpose} options={["live", "backtest"]} onChange={(v) => set({ purpose: v })} format={(s) => (s === "live" ? "Live" : "Backtest")} />
          <Select id="f-quick" label="Quick LLM" value={filters.quick} options={options.quick} onChange={(v) => set({ quick: v })} format={modelLabel} />
          <Select id="f-deep" label="Deep LLM" value={filters.deep} options={options.deep} onChange={(v) => set({ deep: v })} format={modelLabel} />
          <Select id="f-rating" label="Rating" value={filters.rating} options={RATINGS} onChange={(v) => set({ rating: v })} />
          <Select id="f-status" label="Status" value={filters.status} options={STATUSES} onChange={(v) => set({ status: v })} format={(s) => s[0].toUpperCase() + s.slice(1)} />
          <label className="filter-field">
            <span className="cap">Trade date from</span>
            <input className="input" type="date" value={filters.dateFrom} onChange={(e) => set({ dateFrom: e.target.value })} />
          </label>
          <label className="filter-field">
            <span className="cap">To</span>
            <input className="input" type="date" value={filters.dateTo} onChange={(e) => set({ dateTo: e.target.value })} />
          </label>
          <div className="filter-field">
            <span className="cap">Analysts included</span>
            <div className="checks">
              {options.analysts.map((a) => {
                const on = filters.analysts.includes(a);
                return (
                  <button key={a} type="button" className={`check${on ? " on" : ""}`} aria-pressed={on} style={{ height: 30 }} onClick={() => set({ analysts: on ? filters.analysts.filter((x) => x !== a) : [...filters.analysts, a] })}>
                    {ANALYST_NAMES[a] ?? a}
                  </button>
                );
              })}
            </div>
          </div>
          {active > 0 && (
            <button className="btn btn-ghost" type="button" style={{ alignSelf: "flex-end", color: "var(--accent)" }} onClick={() => onChange({ ...EMPTY_FILTERS, query: filters.query })}>
              Reset filters
            </button>
          )}
        </div>
      )}

      {search && (
        <div className="search-note">
          <b>{search.total_hits}</b> matches for “{search.query}” in {search.runs.length} run{search.runs.length === 1 ? "" : "s"}. Matching text is shown under each run.
        </div>
      )}
    </section>
  );
}
