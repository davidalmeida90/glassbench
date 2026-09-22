import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";

export type Series = { key: string; label: string; color: string; values: number[]; dash?: string };
export type Band = { lo: number[]; hi: number[]; label: string };
export type Marker = { i: number; y: number; shape: "dot" | "up" | "down"; color: string; title: string; onClick?: () => void; badge?: string; label?: string; highlight?: boolean; onHover?: (on: boolean) => void };
export type Span = { i0: number; i1: number; opacity: number; color: string; title: string };
export type Level = { i0: number; i1: number; y: number; color: string; dash: string; title: string };
export type LegendItem = { label: string; color: string; kind: "line" | "dash" | "band" | "dot" | "up" | "down" };

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function useWidth() {
  const ref = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(0);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    setWidth(el.clientWidth);
    const ro = new ResizeObserver(() => setWidth(el.clientWidth));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, width] as const;
}

function niceTicks(min: number, max: number, count = 4): number[] {
  if (!isFinite(min) || !isFinite(max)) return [];
  if (min === max) {
    const pad = Math.abs(min) * 0.05 || 1;
    min -= pad;
    max += pad;
  }
  const raw = (max - min) / count;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) ?? raw;
  const ticks = [];
  for (let v = Math.ceil(min / step) * step; v <= max + step * 1e-6; v += step) ticks.push(Math.round(v / step) * step);
  return ticks;
}

function monthTicks(dates: string[], maxTicks: number): { i: number; label: string }[] {
  const all: { i: number; label: string }[] = [];
  for (let i = 1; i < dates.length; i++) {
    if (dates[i].slice(0, 7) !== dates[i - 1].slice(0, 7)) {
      const m = Number(dates[i].slice(5, 7)) - 1;
      all.push({ i, label: m === 0 ? `${MONTHS[m]} ${dates[i].slice(0, 4)}` : MONTHS[m] });
    }
  }
  const every = Math.max(1, Math.ceil(all.length / maxTicks));
  return all.filter((_, k) => k % every === 0 || all[k].label.includes(" "));
}

export function Legend({ items }: { items: LegendItem[] }) {
  return (
    <div className="legend">
      {items.map((it) => (
        <span key={it.label} className="legend-item">
          <svg width="18" height="10" aria-hidden="true">
            {it.kind === "line" && <line x1="1" x2="17" y1="5" y2="5" stroke={it.color} strokeWidth="2" strokeLinecap="round" />}
            {it.kind === "dash" && <line x1="1" x2="17" y1="5" y2="5" stroke={it.color} strokeWidth="2" strokeDasharray="4 3" />}
            {it.kind === "band" && <rect x="1" y="1" width="16" height="8" rx="2" fill={it.color} />}
            {it.kind === "dot" && <circle cx="9" cy="5" r="4" fill={it.color} />}
            {it.kind === "up" && <path d="M9 1 L14 9 L4 9 Z" fill={it.color} />}
            {it.kind === "down" && <path d="M9 9 L14 1 L4 1 Z" fill={it.color} />}
          </svg>
          {it.label}
        </span>
      ))}
    </div>
  );
}

export function LineChart({
  label,
  dates,
  series,
  band,
  markers = [],
  levels = [],
  spans = [],
  height = 260,
  format,
  zero,
}: {
  label: string;
  dates: string[];
  series: Series[];
  band?: Band;
  markers?: Marker[];
  levels?: Level[];
  spans?: Span[];
  height?: number;
  format: (v: number) => string;
  zero?: number;
}) {
  const [ref, width] = useWidth();
  const [hover, setHover] = useState<number | null>(null);
  const n = dates.length;
  const endLabels = width >= 620;
  const pad = { l: 54, r: endLabels ? 150 : 14, t: 12, b: 26 };
  const plotW = Math.max(width - pad.l - pad.r, 10);
  const plotH = height - pad.t - pad.b;

  const { y0, y1, ticks } = useMemo(() => {
    const vals: number[] = [];
    series.forEach((s) => vals.push(...s.values));
    if (band) vals.push(...band.lo, ...band.hi);
    markers.forEach((m) => vals.push(m.y));
    levels.forEach((l) => vals.push(l.y));
    if (zero != null) vals.push(zero);
    const finite = vals.filter((v) => isFinite(v));
    const t = niceTicks(Math.min(...finite), Math.max(...finite), Math.max(3, Math.round(plotH / 55)));
    return { y0: Math.min(t[0], ...finite), y1: Math.max(t[t.length - 1], ...finite), ticks: t };
  }, [series, band, markers, levels, zero, plotH]);

  const x = (i: number) => pad.l + (n <= 1 ? 0 : (i / (n - 1)) * plotW);
  const y = (v: number) => pad.t + (y1 === y0 ? plotH / 2 : (1 - (v - y0) / (y1 - y0)) * plotH);
  const path = (values: number[]) => values.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join("");

  const labels = useMemo(() => {
    const items = series.map((s) => ({ s, y: y(s.values[s.values.length - 1]) }));
    items.sort((a, b) => a.y - b.y);
    for (let k = 1; k < items.length; k++) if (items[k].y - items[k - 1].y < 15) items[k].y = items[k - 1].y + 15;
    const overflow = items.length ? items[items.length - 1].y - (pad.t + plotH) : 0;
    if (overflow > 0) items.forEach((it) => (it.y -= overflow));
    return items;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [series, y0, y1, width, height]);

  useEffect(() => setHover(null), [dates]);

  const onMove = (e: React.MouseEvent<SVGSVGElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const i = Math.round(((e.clientX - rect.left - pad.l) / plotW) * (n - 1));
    setHover(i >= 0 && i < n ? i : null);
  };

  const hx = hover != null ? x(hover) : 0;
  return (
    <div ref={ref} className="chart">
      {width > 0 && (
        <svg width={width} height={height} role="img" aria-label={label} onMouseMove={onMove} onMouseLeave={() => setHover(null)}>
          {ticks.map((t) => (
            <g key={t}>
              <line x1={pad.l} x2={pad.l + plotW} y1={y(t)} y2={y(t)} className={zero === t ? "grid zero" : "grid"} />
              <text x={pad.l - 8} y={y(t)} className="axis" textAnchor="end" dominantBaseline="middle">{format(t)}</text>
            </g>
          ))}
          {monthTicks(dates, Math.max(3, Math.floor(plotW / 70))).map((t) => (
            <text key={t.i} x={x(t.i)} y={height - 8} className="axis" textAnchor="middle">{t.label}</text>
          ))}
          {spans.map((sp, k) => (
            <rect key={`span-${k}`} x={x(sp.i0)} y={pad.t} width={Math.max(x(sp.i1) - x(sp.i0), 1)} height={plotH} fill={sp.color} opacity={sp.opacity}>
              <title>{sp.title}</title>
            </rect>
          ))}
          {band && (
            <path
              d={`${band.hi.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join("")}${band.lo
                .map((v, i) => [i, v] as const)
                .reverse()
                .map(([i, v]) => `L${x(i).toFixed(1)} ${y(v).toFixed(1)}`)
                .join("")}Z`}
              className="band"
            />
          )}
          {levels.map((l, k) => (
            <line key={k} x1={x(l.i0)} x2={x(l.i1)} y1={y(l.y)} y2={y(l.y)} stroke={l.color} strokeWidth="1.5" strokeDasharray={l.dash}>
              <title>{l.title}</title>
            </line>
          ))}
          {series.map((s) => (
            <path key={s.key} d={path(s.values)} fill="none" stroke={s.color} strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" strokeDasharray={s.dash} />
          ))}
          {markers.map((m, k) => {
            const cx = x(m.i);
            const cy = y(m.y);
            const size = m.highlight ? 1.35 : 1;
            const shape =
              m.shape === "dot" ? (
                <circle cx={cx} cy={cy} r={5.5 * size} fill={m.color} stroke="var(--surface)" strokeWidth="2" />
              ) : m.shape === "up" ? (
                <path d={`M${cx} ${cy + 3} l${6 * size} ${10 * size} h${-12 * size} Z`} fill={m.color} stroke="var(--surface)" strokeWidth="1.5" />
              ) : (
                <path d={`M${cx} ${cy - 3} l${6 * size} ${-10 * size} h${-12 * size} Z`} fill={m.color} stroke="var(--surface)" strokeWidth="1.5" />
              );
            // Badges sit beyond the triangle; alternate the distance so neighbouring labels do not collide.
            const dir = m.shape === "down" ? -1 : 1;
            const stagger = m.shape === "dot" ? 0 : k % 2 === 0 ? 0 : 14;
            const by = m.shape === "dot" ? cy - 14 : cy + dir * (24 + stagger);
            const nearRight = cx > pad.l + plotW - 170;
            return (
              <g key={k} className={`marker${m.onClick ? " clickable" : ""}${m.highlight ? " hl" : ""}`} onClick={m.onClick}
                onMouseEnter={() => m.onHover?.(true)} onMouseLeave={() => m.onHover?.(false)}>
                <circle cx={cx} cy={m.shape === "dot" ? cy : m.shape === "up" ? cy + 8 : cy - 8} r="11" fill="transparent" />
                {shape}
                {m.badge && m.shape !== "dot" && (
                  <>
                    <line x1={cx} x2={cx} y1={cy + dir * 13} y2={by - dir * 7} className="badge-stem" />
                    <circle cx={cx} cy={by} r="7.5" className="badge-bg" stroke={m.color} />
                    <text x={cx} y={by} className="badge-text" textAnchor="middle" dominantBaseline="central">{m.badge}</text>
                  </>
                )}
                {m.badge && m.shape === "dot" && (
                  <text x={cx} y={by} className="dot-tag" textAnchor="middle">{m.badge}</text>
                )}
                {m.label && (
                  <text x={nearRight ? cx - 12 : cx + 12} y={by} className="marker-label" textAnchor={nearRight ? "end" : "start"} dominantBaseline="central">{m.label}</text>
                )}
                <title>{m.title}</title>
              </g>
            );
          })}
          {endLabels &&
            labels.map(({ s, y: ly }) => (
              <g key={s.key}>
                <line x1={pad.l + plotW + 8} x2={pad.l + plotW + 20} y1={ly} y2={ly} stroke={s.color} strokeWidth="2" strokeDasharray={s.dash} />
                <text x={pad.l + plotW + 26} y={ly} dominantBaseline="middle" className="end-label">
                  {format(s.values[s.values.length - 1])} <tspan className="end-name">{s.label}</tspan>
                </text>
              </g>
            ))}
          {hover != null && <line x1={hx} x2={hx} y1={pad.t} y2={pad.t + plotH} className="crosshair" />}
          {hover != null &&
            series.map((s) => <circle key={s.key} cx={hx} cy={y(s.values[hover])} r="3.5" fill={s.color} stroke="var(--surface)" strokeWidth="1.5" />)}
        </svg>
      )}
      {hover != null && (
        <div className="chart-tip" style={{ left: hx, transform: hx > width * 0.6 ? "translateX(calc(-100% - 12px))" : "translateX(12px)" }}>
          <div className="mono">{dates[hover]}</div>
          {series.map((s) => (
            <div key={s.key} className="tip-row">
              <i style={{ background: s.color }} />
              <span>{s.label}</span>
              <b>{format(s.values[hover])}</b>
            </div>
          ))}
          {band && (
            <div className="tip-row">
              <i style={{ background: "var(--band)" }} />
              <span>{band.label}</span>
              <b>{format(band.lo[hover])} to {format(band.hi[hover])}</b>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
