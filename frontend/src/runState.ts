import type { AgentMeta, Decision, DeskEvent, Meta, Stage } from "./api";

export type AgentState = "waiting" | "running" | "done" | "failed";

export type LlmCall = {
  id: string;
  model: string;
  start: number;
  end?: number;
  tokensIn?: number;
  tokensOut?: number;
  cached?: number;
  reasoning?: number;
  cost?: number | null;
  promptChars?: number;
  failed?: string;
};

export type ToolCall = {
  id: string;
  tool: string;
  args: Record<string, unknown>;
  start: number;
  end?: number;
  chars?: number;
  preview?: string;
  file?: string;
  flag?: string | null;
  failed?: string;
};

export type Visit = { start: number; end?: number };
export type Batch = { start: number; end?: number; calls: string[] };
export type Flag = { agent: string | null; label: string; source: string; detail: string; ts: number };

export type AgentView = AgentMeta & {
  state: AgentState;
  visits: Visit[];
  llm: LlmCall[];
  tools: ToolCall[];
  batches: Batch[];
  report: string;
  live: string;
  reasoning: string;
  structured?: Record<string, any>;
  error?: string;
};

export type RunView = {
  status: "queued" | "running" | "finished" | "failed" | "cancelled";
  engine: string;
  variant?: string;
  /** Agents and stages the run declared for itself (AI Hedge Fund); TradingAgents runs use the app's meta. */
  agentMeta?: AgentMeta[];
  stages?: Stage[];
  ticker: string;
  tradeDate: string;
  depth: number;
  deepModel: string;
  quickModel: string;
  queuedAt?: number;
  startedAt?: number;
  finishedAt?: number;
  instrument?: string;
  agents: Record<string, AgentView>;
  order: string[];
  flags: Flag[];
  memory?: { chars: number; preview: string };
  totals: { llm: number; tools: number; tokensIn: number; tokensOut: number; cost: number };
  rating?: string;
  decision?: Decision;
  error?: string;
  lastSeq: number;
};

export function emptyRun(meta: Meta): RunView {
  return {
    status: "queued",
    engine: "tradingagents",
    ticker: "",
    tradeDate: "",
    depth: 1,
    deepModel: "",
    quickModel: "",
    agents: {},
    order: meta.agents.map((a) => a.id),
    flags: [],
    totals: { llm: 0, tools: 0, tokensIn: 0, tokensOut: 0, cost: 0 },
    lastSeq: 0,
  };
}

function agentFor(run: RunView, meta: Meta, id: string | null): AgentView | undefined {
  if (!id) return undefined;
  if (!run.agents[id]) {
    const m = run.agentMeta?.find((a) => a.id === id) ?? meta.agents.find((a) => a.id === id);
    if (!m) return undefined;
    run.agents[id] = { ...m, state: "waiting", visits: [], llm: [], tools: [], batches: [], report: "", live: "", reasoning: "" };
    if (!run.order.includes(id)) run.order.push(id);
  }
  return run.agents[id];
}

/** Mutates a draft copy; call through applyEvents so React sees a new object. */
function apply(run: RunView, meta: Meta, e: DeskEvent) {
  if (e.seq <= run.lastSeq) return;
  run.lastSeq = e.seq;
  const p = e.payload;
  const a = agentFor(run, meta, e.agent);
  switch (e.type) {
    case "run.queued":
      run.ticker = p.ticker;
      run.tradeDate = p.trade_date;
      run.depth = p.depth;
      run.deepModel = p.deep_model;
      run.quickModel = p.quick_model;
      run.queuedAt = e.ts;
      run.engine = p.engine ?? "tradingagents";
      run.variant = p.variant || undefined;
      if (p.agent_meta) {
        run.agentMeta = p.agent_meta;
        run.stages = p.stages;
      }
      run.order = p.agents;
      for (const id of p.agents as string[]) agentFor(run, meta, id);
      break;
    case "run.started":
      run.status = "running";
      run.startedAt = e.ts;
      break;
    case "instrument.resolved":
      run.instrument = p.context;
      break;
    case "memory.context":
      run.memory = { chars: p.chars, preview: p.preview };
      break;
    case "agent.started":
      if (a) {
        a.state = "running";
        a.visits.push({ start: e.ts });
        a.live = "";
      }
      break;
    case "agent.finished":
      if (a) {
        const v = a.visits[a.visits.length - 1];
        if (v) v.end = e.ts;
        a.state = "done";
      }
      break;
    case "agent.failed":
      if (a) {
        a.state = "failed";
        a.error = p.error;
      }
      break;
    case "tools.started":
      a?.batches.push({ start: e.ts, calls: [] });
      if (a) a.state = "running";
      break;
    case "tools.finished":
      if (a) {
        const b = a.batches[a.batches.length - 1];
        if (b) b.end = e.ts;
      }
      break;
    case "llm.started":
      run.totals.llm += 1;
      if (a) {
        a.llm.push({ id: p.call, model: p.model, start: e.ts, promptChars: p.prompt_chars });
        if (a.reasoning) a.reasoning += "\n\n";
      }
      break;
    case "llm.reasoning":
      if (a) a.reasoning += p.text;
      break;
    case "llm.finished": {
      const call = a?.llm.find((c) => c.id === p.call);
      if (call) Object.assign(call, { end: e.ts, tokensIn: p.tokens_in, tokensOut: p.tokens_out, cached: p.cached, reasoning: p.reasoning, cost: p.cost_usd });
      run.totals.tokensIn += p.tokens_in || 0;
      run.totals.tokensOut += p.tokens_out || 0;
      run.totals.cost += p.cost_usd || 0;
      break;
    }
    case "llm.failed": {
      const call = a?.llm.find((c) => c.id === p.call);
      if (call) Object.assign(call, { end: e.ts, failed: p.error });
      break;
    }
    case "llm.delta":
      if (a) a.live += p.text;
      break;
    case "tool.called":
      run.totals.tools += 1;
      if (a) {
        a.tools.push({ id: p.call, tool: p.tool, args: p.args, start: e.ts });
        const b = a.batches[a.batches.length - 1];
        if (b && !b.end) b.calls.push(p.call);
      }
      break;
    case "tool.result": {
      const call = a?.tools.find((c) => c.id === p.call);
      if (call) Object.assign(call, { end: e.ts, chars: p.chars, preview: p.preview, file: p.file, flag: p.flag });
      break;
    }
    case "tool.failed": {
      const call = a?.tools.find((c) => c.id === p.call);
      if (call) Object.assign(call, { end: e.ts, failed: p.error });
      break;
    }
    case "report.updated":
      if (a) a.report = p.text;
      break;
    case "decision.structured":
      if (a) a.structured = p;
      break;
    case "data.flag":
      run.flags.push({ agent: e.agent, label: p.label, source: p.source, detail: p.detail, ts: e.ts });
      break;
    case "run.finished":
      run.status = "finished";
      run.finishedAt = e.ts;
      run.rating = p.rating;
      run.decision = p.decision;
      break;
    case "run.failed":
      run.status = "failed";
      run.finishedAt = e.ts;
      run.error = p.error;
      for (const ag of Object.values(run.agents)) if (ag.state === "running") ag.state = "failed";
      break;
    case "run.cancelled":
      run.status = "cancelled";
      run.finishedAt = e.ts;
      for (const ag of Object.values(run.agents)) if (ag.state === "running") ag.state = "failed";
      break;
  }
}

export function applyEvents(run: RunView, meta: Meta, events: DeskEvent[]): RunView {
  const draft: RunView = structuredClone(run);
  for (const e of events) apply(draft, meta, e);
  return draft;
}

export function currentAgent(run: RunView): string | undefined {
  const running = run.order.filter((id) => run.agents[id]?.state === "running");
  return running[running.length - 1];
}

export function agentSpan(a: AgentView): { start?: number; end?: number } {
  if (!a.visits.length) return {};
  return { start: a.visits[0].start, end: a.visits[a.visits.length - 1].end };
}

export function agentDuration(a: AgentView, now: number): number | undefined {
  if (!a.visits.length) return undefined;
  return a.visits.reduce((sum, v) => sum + ((v.end ?? now) - v.start), 0);
}

/** The meta a run is drawn with: its own agents and stages when it declared them. */
export function viewMeta(meta: Meta, run?: RunView): Meta {
  return run?.agentMeta ? { ...meta, agents: run.agentMeta, stages: run.stages ?? meta.stages } : meta;
}

export const TERMINAL = new Set(["finished", "failed", "cancelled"]);
