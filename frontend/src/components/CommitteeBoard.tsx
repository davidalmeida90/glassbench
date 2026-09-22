import { useState } from "react";
import type { Meta } from "../api";
import { conclusionFor, liveLineFor, phaseFor, readsLabel, type Phase } from "../conclusions";
import { fmtDuration, fmtTokens } from "../format";
import { agentDuration, type AgentView, type RunView } from "../runState";

const PHASE_LABEL: Record<Phase, string> = { waiting: "Waiting", tools: "Reading data", thinking: "Thinking", typing: "Writing", done: "Done", failed: "Failed" };

export function CommitteeBoard({ run, meta, now, selected, onSelect }: { run: RunView; meta: Meta; now: number; selected?: string; onSelect: (id: string) => void }) {
  const [reasoning, setReasoning] = useState(false);
  const ended = run.status === "failed" || run.status === "cancelled";
  return (
    <section className="panel board" aria-label="Committee board">
      <div className="board-head">
        <span className="cap">Committee</span>
        <span className="muted" style={{ fontSize: 12 }}>What each agent is doing now, and what it concluded. Click a card to open its full output.</span>
        <label className="board-toggle">
          <input type="checkbox" checked={reasoning} onChange={(e) => setReasoning(e.target.checked)} /> show reasoning while thinking
        </label>
      </div>
      <div className="board-grid">
        {meta.stages.map((stage) => {
          const agents = run.order.map((id) => run.agents[id]).filter((a): a is AgentView => !!a && a.stage === stage.id);
          if (!agents.length) return null;
          return (
            <div key={stage.id} className="board-stage">
              <span className="cap board-stage-label">{stage.label}</span>
              {agents.map((a) => {
                const phase = phaseFor(a);
                const line = phase === "done" ? conclusionFor(a) : phase === "waiting" ? (ended ? "not reached" : `will read ${a.reads.slice(0, 2).map(readsLabel).join(", ").toLowerCase()}`) : liveLineFor(a);
                const shown = phase === "thinking" && !reasoning ? "thinking…" : line;
                const secs = agentDuration(a, now);
                const tokens = a.llm.reduce((s, c) => s + (c.tokensOut ?? 0), 0);
                return (
                  <button key={a.id} className={`board-card ${phase}${selected === a.id ? " sel" : ""}`} onClick={() => onSelect(a.id)} title={phase === "done" ? a.report.slice(0, 400) : undefined}>
                    <div className="board-card-head">
                      <span className={`dot${phase === "tools" || phase === "thinking" || phase === "typing" ? " live" : ""}`} />
                      <b>{a.label}</b>
                      <span className="board-phase">{PHASE_LABEL[phase]}</span>
                    </div>
                    <div className={`board-line${phase === "typing" || phase === "thinking" || phase === "tools" ? " live" : ""}`}>{shown || (phase === "done" ? "finished, no summary yet" : "")}</div>
                    {(phase === "done" || secs) && (
                      <div className="board-meta">
                        {secs != null && <span>{fmtDuration(secs)}</span>}
                        {tokens > 0 && <span>{fmtTokens(tokens)} tok</span>}
                        {a.tools.length > 0 && <span>{a.tools.length} tool{a.tools.length === 1 ? "" : "s"}</span>}
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          );
        })}
      </div>
    </section>
  );
}

const DOT_CLASS: Record<string, string> = { done: "done", running: "live", failed: "failed", waiting: "" };

/** Twelve small dots for a run in the list: one per agent, coloured by state. */
export function RunDots({ progress, order }: { progress: Record<string, string>; order: string[] }) {
  const running = order.find((id) => progress[id] === "running");
  return (
    <span className="run-dots" title={running ? `${running.replace("_", " ")} working` : undefined}>
      {order.map((id) => (
        <i key={id} className={DOT_CLASS[progress[id] ?? "waiting"]} title={`${id.replace("_", " ")}: ${progress[id] ?? "waiting"}`} />
      ))}
    </span>
  );
}
