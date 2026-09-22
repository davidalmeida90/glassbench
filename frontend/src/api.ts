export type Stage = { id: string; label: string };
export type AgentMeta = {
  id: string;
  label: string;
  name: string;
  stage: string;
  role: "quick" | "deep";
  reads: string[];
  analyst_key: string | null;
};
export type EngineBuild = { version: string; commit: string; adjusted: boolean; changes: string[] };

export type Meta = {
  version: string;
  stages: Stage[];
  agents: AgentMeta[];
  analysts: string[];
  models: { quick: string[]; deep: string[] };
  pricing: Record<string, { input: number; output: number }>;
  default_trade_date: string;
  engine_version?: string;
  engine_builds?: Record<string, EngineBuild>;
  keys: { name: string; present: boolean; length: number }[];
  variants?: Record<string, { label: string; detail: string }>;
};

export type Decision = {
  research?: { recommendation?: string | null; rationale?: string | null; strategic_actions?: string | null };
  trader?: { action?: string | null; reasoning?: string | null; entry_price?: number | null; stop_loss?: number | null; position_sizing?: string | null };
  portfolio?: { rating?: string | null; executive_summary?: string | null; investment_thesis?: string | null; price_target?: number | null; time_horizon?: string | null } | null;
};

export type Run = {
  id: string;
  ticker: string;
  trade_date: string;
  analysts: string[];
  depth: number;
  deep_model: string;
  quick_model: string;
  status: "queued" | "running" | "finished" | "failed" | "cancelled";
  engine: string;
  engine_version: string;
  provider: string;
  purpose?: "live" | "backtest";
  backtest_id?: string | null;
  memory?: "shared" | "off";
  variant?: string;
  models_served?: string[] | null;
  created_at: number;
  started_at: number | null;
  finished_at: number | null;
  rating: string | null;
  decision: Decision | null;
  tokens_in: number;
  tokens_out: number;
  cost_usd: number;
  llm_calls: number;
  tool_calls: number;
  flags: number;
  error: string | null;
  progress?: { order: string[]; state: Record<string, string> };
};

export type DeskEvent = {
  run_id: string;
  seq: number;
  ts: number;
  type: string;
  agent: string | null;
  payload: Record<string, any>;
};

export type IbkrConfig = { host: string; port: number; client_id: number };
export type BrokerId = "none" | "alpaca" | "ibkr";
export type DeskSettings = { broker: BrokerId; ibkr: IbkrConfig; brokers: Record<BrokerId, { label: string; detail: string }> };
export type BrokerCheck = { ok: boolean; summary: string; details: string[] };

export type SearchSnippet = { agent: string | null; type: string; seq: number; snippet: string };
export type SearchResult = { query: string; total_hits: number; runs: { run_id: string; hits: number; snippets: SearchSnippet[] }[] };

export type RunFile = { path: string; label: string | null; bytes: number; group: "artifacts" | "tool_outputs" };

export type BacktestItem = {
  ticker: string;
  date: string;
  status: Run["status"] | "pending";
  reused: boolean;
  attempts: number;
  run_id: string | null;
  rating: string | null;
  cost_usd: number;
  duration_s: number | null;
};
export type Backtest = {
  id: string;
  name: string;
  created_at: number;
  status: "ready" | "running" | "paused" | "finished" | "cancelled";
  budget_usd: number;
  note: string | null;
  config: {
    tickers: string[];
    dates: string[];
    analysts: string[];
    depth: number;
    deep_model: string;
    quick_model: string;
    memory: string;
    engine_version: string;
    variant?: string;
    grid: { frequency?: string; start?: string; end?: string; grid_size?: number; sample?: number | null };
  };
  items: BacktestItem[];
  counts: Record<string, number>;
  spent_usd: number;
  estimate_per_run_usd: number;
  estimate_remaining_usd: number;
  estimate_total_usd: number;
};

export type SimMetrics = {
  total_return: number;
  annual_return: number | null;
  volatility: number | null;
  sharpe: number | null;
  max_drawdown: number;
  time_in_market: number;
  trades: number;
  costs: number;
  days: number;
};
export type SimTrade = { date: string; side: "buy" | "sell"; price: number; weight_before: number; weight_after: number; cost: number; reason: string; run_id: string | null; n?: number };
export type SimPeriod = {
  start: string;
  end: string;
  start_price: number;
  end_price: number;
  weight: number;
  stock_return: number;
  book_return: number;
  verdict: "held" | "missed gain" | "avoided loss" | "flat";
  ongoing: boolean;
  opened_by: { n: number; side: "buy" | "sell"; reasons: string[]; run_id: string | null; price: number; weight_before: number; weight_after: number } | null;
};
export type SimStrategy = { key: string; label: string; equity: number[]; weights: number[]; drawdown: number[]; trades?: SimTrade[]; periods?: SimPeriod[]; metrics: SimMetrics };
export type BacktestSibling = { id: string; name: string; variant: string; status: Backtest["status"]; finished: number; total: number; spent_usd: number };
export type VariantCompare = {
  variants: (BacktestSibling & {
    views: Record<string, { ratings: Record<string, number>; levels: SimMetrics | null; rating_only: SimMetrics | null; buy_hold: number | null }>;
  })[];
};
export type SimPlacebo = { p5: number[]; p50: number[]; p95: number[]; sims: number; exhaustive: boolean; agent_percentile: number | null };
export type SimDecision = { date: string; rating: string | null; status: string; run_id: string | null; entry: number | null; stop: number | null; close: number | null; forward_return: number | null };
export type SimTicker = {
  ticker: string;
  dates: string[];
  close?: number[];
  decisions?: SimDecision[];
  strategies: SimStrategy[];
  placebo: SimPlacebo;
  sensitivity?: { key: string; label: string; metrics: SimMetrics }[];
  by_rating?: { rating: string; n: number; mean_forward_return: number; share_up: number; hit_rate: number | null }[];
  notes?: string[];
};
export type BacktestResults = {
  backtest_id: string;
  name: string;
  config: Backtest["config"];
  spent_usd: number;
  tickers: SimTicker[];
  combined: SimTicker | null;
  siblings?: BacktestSibling[];
  assumptions: { cost_bps: number; fill: string; cash_return: number; hold_add: number; prices: string; placebo_sims: number; ma: number[]; risk_free: number };
};

export type FlowNode = { id: string; label: string; kind: "quick" | "deep" | "data" | "rule"; sub?: string };
export type FlowStage = { id: string; label: string; mode: string; nodes: FlowNode[] };
export type FlowSpec = { stages: FlowStage[]; edges: [string, string, string?][]; notes: string[] };
export type FrameworkAgent = { id: string; name: string; stage: string; role: string; reads: string[]; what: string; tools: string | null };
export type Framework = {
  id: string;
  name: string;
  org: string;
  version: string | null;
  status: "connected" | "planned";
  tagline: string;
  summary: string;
  links: { label: string; url: string }[];
  facts: { label: string; value: string; note?: string }[];
  flow: FlowSpec;
  agents: FrameworkAgent[];
  data: { source: string; used_for: string; point_in_time: string }[];
  evidence: { claim: string; source: string; note: string }[];
  runs: number;
};

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      message = typeof body.detail === "string" ? body.detail : Array.isArray(body.detail) ? body.detail.map((d: any) => d.msg).join("; ") : message;
    } catch {
      /* keep status text */
    }
    throw new Error(message);
  }
  return res.json() as Promise<T>;
}

export const api = {
  meta: () => fetch("/api/meta").then((r) => json<Meta>(r)),
  runs: () => fetch("/api/runs").then((r) => json<{ runs: Run[] }>(r)).then((d) => d.runs),
  allRuns: () => fetch("/api/runs?limit=100000").then((r) => json<{ runs: Run[] }>(r)).then((d) => d.runs),
  frameworks: () => fetch("/api/frameworks").then((r) => json<{ frameworks: Framework[] }>(r)).then((d) => d.frameworks),
  run: (id: string) => fetch(`/api/runs/${id}`).then((r) => json<Run>(r)),
  files: (id: string) => fetch(`/api/runs/${id}/files`).then((r) => json<{ files: RunFile[] }>(r)).then((d) => d.files),
  cancel: (id: string) => fetch(`/api/runs/${id}/cancel`, { method: "POST" }).then((r) => json<unknown>(r)),
  start: (body: { tickers: string[]; trade_date: string; analysts: string[]; depth: number; deep_model: string; quick_model: string }) =>
    fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then((r) =>
      json<{ run_ids: string[] }>(r),
    ),
  search: (q: string) => fetch(`/api/search?q=${encodeURIComponent(q)}`).then((r) => json<SearchResult>(r)),
  settings: () => fetch("/api/settings").then((r) => json<DeskSettings>(r)),
  saveSettings: (body: { broker: BrokerId; ibkr?: IbkrConfig }) =>
    fetch("/api/settings", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then((r) => json<DeskSettings>(r)),
  checkBroker: (body: { broker: BrokerId; ibkr?: IbkrConfig }) =>
    fetch("/api/broker/check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then((r) => json<BrokerCheck>(r)),
  fileUrl: (id: string, path: string, download = false) => `/api/runs/${id}/files/${path}${download ? "?download=true" : ""}`,
  bundleUrl: (id: string) => `/api/runs/${id}/bundle.zip`,
  eventsUrl: (id: string) => `/api/runs/${id}/events`,
  backtests: () => fetch("/api/backtests").then((r) => json<{ backtests: Backtest[] }>(r)).then((d) => d.backtests),
  backtestResults: (id: string, costBps: number) => fetch(`/api/backtests/${id}/results?cost_bps=${costBps}`).then((r) => json<BacktestResults>(r)),
  backtestCompare: (id: string, costBps: number) => fetch(`/api/backtests/${id}/compare?cost_bps=${costBps}`).then((r) => json<VariantCompare>(r)),
  backtestAction: (id: string, action: "start" | "pause" | "cancel") => fetch(`/api/backtests/${id}/${action}`, { method: "POST" }).then((r) => json<Backtest>(r)),
};
