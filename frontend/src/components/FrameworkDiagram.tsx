import { useMemo, useState } from "react";
import type { FlowSpec } from "../api";

const COL_W = 166;
const NODE_W = 142;
const NODE_H = 46;
const ROW_GAP = 16;
const HEAD_H = 46;
const PAD_X = 16;
const PAD_Y = 12;

const MODE_LABEL: Record<string, string> = { parallel: "in parallel", rounds: "debate, N rounds", sequential: "one step", tools: "tool calls" };

export function FrameworkDiagram({ flow, selected, onSelect }: { flow: FlowSpec; selected?: string | null; onSelect?: (id: string | null) => void }) {
  const [hover, setHover] = useState<string | null>(null);
  const layout = useMemo(() => {
    const rows = Math.max(...flow.stages.map((s) => s.nodes.length));
    const height = PAD_Y + HEAD_H + rows * NODE_H + (rows - 1) * ROW_GAP + PAD_Y + 8;
    const pos = new Map<string, { x: number; y: number; stage: number }>();
    flow.stages.forEach((stage, si) => {
      const n = stage.nodes.length;
      const block = n * NODE_H + (n - 1) * ROW_GAP;
      const top = PAD_Y + HEAD_H + (rows * NODE_H + (rows - 1) * ROW_GAP - block) / 2;
      stage.nodes.forEach((node, ni) => pos.set(node.id, { x: PAD_X + si * COL_W + (COL_W - NODE_W) / 2, y: top + ni * (NODE_H + ROW_GAP), stage: si }));
    });
    return { pos, width: PAD_X * 2 + flow.stages.length * COL_W, height };
  }, [flow]);

  const focus = hover ?? selected ?? null;
  const touching = (a: string, b: string) => focus != null && (a === focus || b === focus);

  return (
    <div className="diagram-wrap">
      <svg viewBox={`0 0 ${layout.width} ${layout.height}`} width="100%" style={{ minWidth: layout.width * 0.72, maxWidth: layout.width * 1.1, display: "block" }} role="img" aria-label="Framework flow diagram">
        <defs>
          <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0 0.5 L8 4 L0 7.5 Z" className="dg-arrow" />
          </marker>
          <marker id="arrow-hl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0 0.5 L8 4 L0 7.5 Z" className="dg-arrow hl" />
          </marker>
        </defs>
        {flow.stages.map((stage, si) => {
          const x0 = PAD_X + si * COL_W;
          return (
            <g key={stage.id}>
              {si % 2 === 1 && <rect x={x0} y={PAD_Y - 4} width={COL_W} height={layout.height - PAD_Y * 2 + 8} className="dg-col" />}
              <text x={x0 + COL_W / 2} y={PAD_Y + 14} textAnchor="middle" className="dg-stage">{stage.label}</text>
              <text x={x0 + COL_W / 2} y={PAD_Y + 30} textAnchor="middle" className="dg-mode">{MODE_LABEL[stage.mode] ?? stage.mode}</text>
            </g>
          );
        })}
        {flow.edges.map(([from, to, kind], k) => {
          const a = layout.pos.get(from);
          const b = layout.pos.get(to);
          if (!a || !b) return null;
          const hl = touching(from, to);
          if (kind === "both") {
            // Debate partners in the same column: a two-headed arc on the right edge.
            const x = a.x + NODE_W + 6;
            const y1 = a.y + NODE_H / 2;
            const y2 = b.y + NODE_H / 2;
            const bulge = 22;
            return (
              <path key={k} d={`M${x} ${y1} C${x + bulge} ${y1}, ${x + bulge} ${y2}, ${x} ${y2}`} className={`dg-edge debate${hl ? " hl" : ""}`}
                markerStart={`url(#${hl ? "arrow-hl" : "arrow"})`} markerEnd={`url(#${hl ? "arrow-hl" : "arrow"})`} />
            );
          }
          const x1 = a.x + NODE_W;
          const y1 = a.y + NODE_H / 2;
          const x2 = b.x;
          const y2 = b.y + NODE_H / 2;
          const dx = Math.max((x2 - x1) / 2, 24);
          return <path key={k} d={`M${x1} ${y1} C${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`} className={`dg-edge${hl ? " hl" : ""}`} markerEnd={`url(#${hl ? "arrow-hl" : "arrow"})`} />;
        })}
        {flow.stages.flatMap((stage) =>
          stage.nodes.map((node) => {
            const p = layout.pos.get(node.id)!;
            const on = focus === node.id;
            return (
              <g
                key={node.id}
                className={`dg-node ${node.kind}${on ? " on" : ""}${onSelect ? " clickable" : ""}`}
                transform={`translate(${p.x} ${p.y})`}
                onMouseEnter={() => setHover(node.id)}
                onMouseLeave={() => setHover(null)}
                onClick={() => onSelect?.(selected === node.id ? null : node.id)}
              >
                <rect width={NODE_W} height={NODE_H} rx="6" />
                <circle cx="13" cy={NODE_H / 2} r="4" className="dg-dot" />
                <text x="25" y={node.sub ? 19 : NODE_H / 2 + 1} dominantBaseline={node.sub ? "auto" : "middle"} className="dg-label">{node.label}</text>
                {node.sub && <text x="25" y="34" className="dg-sub">{node.sub}</text>}
              </g>
            );
          }),
        )}
      </svg>
      <div className="legend" style={{ marginTop: 8 }}>
        <span className="legend-item"><i className="dg-key quick" /> Quick LLM</span>
        <span className="legend-item"><i className="dg-key deep" /> Deep LLM</span>
        <span className="legend-item"><i className="dg-key data" /> Data or quant</span>
        <span className="legend-item"><i className="dg-key rule" /> Rule, no LLM</span>
        <span className="legend-item"><svg width="24" height="10"><path d="M2 5 C8 0, 16 10, 22 5" className="dg-edge debate" /></svg> Debate</span>
      </div>
    </div>
  );
}
