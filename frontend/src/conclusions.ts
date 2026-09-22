import type { AgentView } from "./runState";

export type Phase = "waiting" | "tools" | "thinking" | "typing" | "done" | "failed";

const TOOL_WORDS: Record<string, string> = {
  get_stock_data: "price history", get_indicators: "indicators", get_verified_market_snapshot: "market snapshot",
  get_fundamentals: "company profile", get_balance_sheet: "balance sheet", get_income_statement: "income statement",
  get_cashflow: "cash flow", get_news: "news", get_global_news: "global news", get_fred_series: "FRED data",
  get_polymarket: "Polymarket odds", get_stocktwits: "StockTwits", get_reddit: "Reddit",
};

export function phaseFor(a: AgentView): Phase {
  if (a.state === "failed") return "failed";
  if (a.state === "done") return "done";
  if (a.state === "waiting") return "waiting";
  const batch = a.batches[a.batches.length - 1];
  if (batch && !batch.end) return "tools";
  if (a.live.trim()) return "typing";
  return "thinking";
}

/** What the agent is doing right now, as one short line. */
export function liveLineFor(a: AgentView): string {
  const phase = phaseFor(a);
  if (phase === "tools") {
    const open = a.tools.filter((t) => !t.end);
    const names = [...new Set(open.map((t) => TOOL_WORDS[t.tool] ?? t.tool.replace(/^get_/, "").replace(/_/g, " ")))];
    return names.length ? `reading ${names.join(", ")}…` : "calling tools…";
  }
  if (phase === "typing") return lastFragment(a.live, 140);
  if (phase === "thinking") return a.reasoning.trim() ? `thinking: ${lastFragment(a.reasoning, 120)}` : "thinking…";
  return "";
}

function lastFragment(text: string, max: number): string {
  const clean = text.replace(/[#*_`>|]+/g, " ").replace(/\s+/g, " ").trim();
  if (clean.length <= max) return clean;
  const tail = clean.slice(-max);
  const cut = tail.search(/[.!?]\s|\s/);
  return `…${cut > 0 && cut < max / 2 ? tail.slice(cut + 1).trim() : tail}`;
}

const SPEAKER = /^\s*(bull|bear|aggressive|conservative|neutral|risky|safe)\s+(analyst|researcher)\s*:\s*/i;
const FILLER = /^(i now have|let me|i will|i'll|alright|okay|ok,|first,|here is|here's|now that)/i;
const SUMMARY_HEAD = /^(#+\s*)?(\**)?\s*(summary|bottom line|conclusion|key takeaways?|verdict|overall|net assessment|recommendation)\b/i;

function sentences(text: string): string[] {
  const clean = text
    .replace(SPEAKER, "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/^\s*\|.*$/gm, " ")          // tables
    .replace(/^\s*[-*]\s+/gm, "")          // bullets
    .replace(/-{3,}/g, " ")                // horizontal rules
    .replace(/[#*_`>]+/g, "")
    .replace(/\s+/g, " ")
    .trim();
  return clean
    .split(/(?<=[.!?])\s+(?=[A-Z0-9$"“(])/)
    .map((s) => s.trim().replace(/\s+\d+\.$/, ""))  // a numbered heading glued to the sentence end
    .filter((s) => s.length > 20);
}

const TABLE_ISH = /→|\bnote:|withheld|^\s*(support|resistance) levels?:|analysis date:|exchange:/i;
const STANCE = /\b(bullish|bearish|neutral|overbought|oversold|uptrend|downtrend|trend is|suggests?|indicates?|favou?rs?|risk\/reward|risk-reward|asymmetr|overvalued|undervalued|expensive|cheap|conviction|verdict|bottom line|in short|therefore|the (right|correct) (call|action)|i (recommend|would|conclude)|my (position|view|stance|call))\b/i;

function trim(s: string, max: number): string {
  return s.length > max ? `${s.slice(0, max - 1).replace(/[,;:]?\s+\S*$/, "")}…` : s;
}

function firstGood(lines: string[], max = 170): string {
  const ok = lines.filter((l) => !FILLER.test(l) && !TABLE_ISH.test(l));
  return trim(ok[0] ?? lines[0] ?? "", max);
}

/** A sentence that states a view, preferring later ones (closings) over openings. */
function stanceSentence(lines: string[], max = 170): string {
  const ok = lines.filter((l) => !FILLER.test(l) && !TABLE_ISH.test(l) && STANCE.test(l));
  return ok.length ? trim(ok[ok.length - 1], max) : "";
}

export function readsLabel(key: string): string {
  return key
    .replace(/_history$/, "'s arguments")
    .replace(/^trader_investment_plan$/, "trader's proposal")
    .replace(/_report$/, " report")
    .replace(/_/g, " ");
}

/** One line that states what the agent concluded, from its structured output when it has one, else from its text. */
export function conclusionFor(a: AgentView): string {
  const s = a.structured ?? {};
  if (a.id === "portfolio_manager" && (s.rating || a.report)) {
    const head = s.rating ? `${s.rating}` : "";
    const body = firstGood(sentences(s.executive_summary || s.investment_thesis || a.report), 150);
    return [head, body].filter(Boolean).join(" · ");
  }
  if (a.id === "trader" && (s.action || a.report)) {
    const bits = [s.action, s.entry_price != null ? `entry ${s.entry_price}` : null, s.stop_loss != null ? `stop ${s.stop_loss}` : null].filter(Boolean);
    return bits.length ? bits.join(" · ") : firstGood(sentences(a.report));
  }
  if (a.id === "research_manager" && (s.recommendation || a.report)) {
    const head = s.recommendation ? `${s.recommendation}` : "";
    const body = firstGood(sentences(s.strategic_actions || s.rationale || a.report), 150);
    return [head, body].filter(Boolean).join(" · ");
  }
  if (!a.report.trim()) return "";
  const text = a.report;
  const all = sentences(text);
  if (a.stage === "analysts") {
    // Prefer the summary section; inside it, a sentence that states a view beats a table row.
    const lines = text.split("\n");
    const at = lines.findIndex((l) => SUMMARY_HEAD.test(l));
    if (at >= 0) {
      const section = sentences(lines.slice(at + 1, at + 40).join("\n"));
      const got = stanceSentence(section) || firstGood(section);
      if (got) return got;
    }
    return stanceSentence(all) || firstGood(all);
  }
  // Debaters: the closing view beats the opening flourish.
  const paragraphs = text.split(/\n\s*\n/).map((p) => sentences(p)).filter((p) => p.length);
  const last = paragraphs[paragraphs.length - 1] ?? [];
  return stanceSentence(all) || firstGood(last) || firstGood(all);
}
