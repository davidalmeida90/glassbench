import { useEffect, useRef, useState } from "react";
import type { Meta } from "../api";
import { fmtClock, fmtDuration, fmtTokens } from "../format";
import type { AgentView, RunView } from "../runState";
import { StateMarker } from "./Icons";

const LANE = 22;
const STAGE_GAP = 7;
const AXIS = 24;
const TICK_STEPS = [5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600];

type Tip = { x: number; y: number; title: string; lines: string[] };

export function Timeline({
  run,
  meta,
  now,
  selected,
  onSelect,
}: {
  run: RunView;
  meta: Meta;
  now: number;
  selected?: string;
  onSelect: (id: string) => void;
}) {
  const plotRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(900);
  const [tip, setTip] = useState<Tip | null>(null);

  useEffect(() => {
    const el = plotRef.current;
    if (!el) return;
    const ro = new ResizeObserver(([entry]) => setWidth(Math.max(320, entry.contentRect.width)));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const live = run.status === "running" || run.status === "queued";
  const t0 = run.startedAt ?? run.queuedAt ?? now;
  const tEnd = run.finishedAt ?? now;
  const span = Math.max(60, (tEnd - t0) * 1.04);
  const x = (t: number) => ((t - t0) / span) * width;
  const step = TICK_STEPS.find((s) => span / s <= 9) ?? 3600;
  const firstTick = Math.ceil(t0 / step) * step;
  const ticks: number[] = [];
  for (let t = firstTick; t <= t0 + span; t += step) ticks.push(t);

  // lane layout grouped by stage
  const rows: { agent: AgentView; top: number }[] = [];
  let y = 0;
  meta.stages.forEach((stage) => {
    const agents = run.order.map((id) => run.agents[id]).filter((a) => a && a.stage === stage.id);
    if (!agents.length) return;
    if (rows.length) y += STAGE_GAP;
    agents.forEach((agent) => {
      rows.push({ agent, top: y });
      y += LANE;
    });
  });
  const lanesHeight = y;

  const show = (evt: React.MouseEvent, title: string, lines: string[]) => {
    const box = plotRef.current!.getBoundingClientRect();
    setTip({ x: evt.clientX - box.left, y: evt.clientY - box.top, title, lines });
  };

  return (
    <section className="panel timeline" aria-label="Run timeline">
      <div className="panel-head">
        <span className="panel-title">Timeline</span>
        <div className="legend">
          <span><i style={{ background: "var(--bar-flash)" }} />LLM call · flash</span>
          <span><i style={{ background: "var(--bar-pro)" }} />LLM call · pro</span>
          <span><i className="hatch" />Data fetch · waiting</span>
          <span><i style={{ width: 1.5, height: 12, background: "var(--accent)", verticalAlign: -2 }} />Tool batch</span>
        </div>
      </div>
      <div className="tl-grid">
        <div className="tl-labels">
          {rows.map(({ agent }, i) => {
            const gapBefore = i > 0 && rows[i - 1].agent.stage !== agent.stage;
            const meta = agent.tools.length ? `${agent.tools.length} tools` : agent.llm.length ? `${agent.llm.length} call${agent.llm.length > 1 ? "s" : ""}` : "";
            return (
              <div key={agent.id}>
                {gapBefore && <div className="tl-gap" />}
                <button
                  className={`tl-label${selected === agent.id ? " sel" : ""}`}
                  style={{ color: agent.state === "waiting" ? "var(--muted)" : "var(--ink)" }}
                  onClick={() => onSelect(agent.id)}
                >
                  <StateMarker state={agent.state} />
                  <span className="name" title={agent.name}>{agent.label.replace(" Manager", " Mgr")}</span>
                  <span className="meta">{meta}</span>
                </button>
              </div>
            );
          })}
        </div>

        <div className="tl-plot" ref={plotRef} style={{ height: lanesHeight + AXIS }} onMouseLeave={() => setTip(null)}>
          <svg width={width} height={lanesHeight + AXIS} style={{ display: "block", overflow: "visible" }}>
            <defs>
              <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <rect width="6" height="6" fill="var(--hatch-b)" />
                <rect width="3" height="6" fill="var(--hatch-a)" />
              </pattern>
            </defs>
            {ticks.map((t) => (
              <g key={t}>
                <line x1={x(t)} x2={x(t)} y1={0} y2={lanesHeight} stroke="var(--line-2)" />
                <text x={x(t)} y={lanesHeight + 16} textAnchor="middle" fontSize="10" fill="var(--muted)" fontFamily="var(--font-mono)">
                  {fmtClock(t, step < 60)}
                </text>
              </g>
            ))}
            {rows.map(({ agent, top }) => (
              <g key={agent.id} onClick={() => onSelect(agent.id)} style={{ cursor: "pointer" }}>
                <line x1={0} x2={width} y1={top + LANE - 0.5} y2={top + LANE - 0.5} stroke="var(--line-2)" />
                <rect x={0} y={top} width={width} height={LANE} fill={selected === agent.id ? "var(--accent-soft)" : "transparent"} opacity={0.45} />
                {agent.visits.map((visit, vi) => {
                  const firstLlm = agent.llm.find((c) => c.start >= visit.start - 0.05 && (visit.end == null || c.start <= visit.end));
                  const prepEnd = firstLlm ? firstLlm.start : visit.end ?? now;
                  if (prepEnd - visit.start < 1.2) return null;
                  return (
                    <rect
                      key={`prep-${vi}`}
                      x={x(visit.start)}
                      y={top + 6}
                      width={Math.max(2, x(prepEnd) - x(visit.start))}
                      height={10}
                      rx={2}
                      fill="url(#hatch)"
                      onMouseMove={(e) => show(e, `${agent.name} · preparing data`, [`${fmtDuration(prepEnd - visit.start)} before the first LLM call`])}
                    />
                  );
                })}
                {agent.llm.map((call) => {
                  const end = call.end ?? now;
                  const running = call.end == null && live;
                  const pro = call.model.includes("pro");
                  return (
                    <rect
                      key={call.id}
                      x={x(call.start)}
                      y={top + 6}
                      width={Math.max(2.5, x(end) - x(call.start))}
                      height={10}
                      rx={2}
                      fill={running ? "var(--accent)" : call.failed ? "var(--bad)" : pro ? "var(--bar-pro)" : "var(--bar-flash)"}
                      className={running ? "live" : undefined}
                      onMouseMove={(e) =>
                        show(e, `${agent.name} · ${call.model}`, [
                          `${fmtClock(call.start)} · ${fmtDuration(end - call.start)}`,
                          call.end ? `${fmtTokens(call.tokensIn)} in · ${fmtTokens(call.tokensOut)} out${call.reasoning ? ` · ${fmtTokens(call.reasoning)} reasoning` : ""}` : "writing…",
                        ])
                      }
                    />
                  );
                })}
                {agent.batches.map((batch, bi) => {
                  const bx = x(batch.start);
                  const bw = Math.max(1.5, x(batch.end ?? now) - bx);
                  const names = agent.tools.filter((t) => batch.calls.includes(t.id)).map((t) => t.tool).filter((v, i, arr) => arr.indexOf(v) === i).join(", ");
                  const tipFor = (e: React.MouseEvent) =>
                    show(e, `${agent.name} · ${batch.calls.length} tool${batch.calls.length === 1 ? "" : "s"} in parallel`, [names, `${fmtClock(batch.start)} · ${fmtDuration((batch.end ?? now) - batch.start)}`]);
                  return (
                    <g key={`b-${bi}`} onMouseMove={tipFor}>
                      <rect x={bx - 0.75} y={top + 3} width={1.5} height={16} fill="var(--accent)" />
                      <rect x={bx} y={top + 18} width={bw} height={2} fill="var(--accent)" opacity={0.55} />
                      <rect x={bx - 4} y={top} width={bw + 8} height={LANE} fill="transparent" />
                    </g>
                  );
                })}
              </g>
            ))}
            {live && run.startedAt && (
              <g>
                <line x1={x(now)} x2={x(now)} y1={-4} y2={lanesHeight} stroke="var(--accent)" strokeWidth={1.5} />
              </g>
            )}
          </svg>
          {tip && (
            <div className="tl-tip" style={{ left: tip.x, top: tip.y }}>
              <div style={{ fontWeight: 600 }}>{tip.title}</div>
              {tip.lines.filter(Boolean).map((l, i) => (
                <div key={i} className="mono" style={{ fontSize: 10.5 }}>{l}</div>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
