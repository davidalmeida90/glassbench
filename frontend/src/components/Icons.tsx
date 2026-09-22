import type { AgentState } from "../runState";

export function StateMarker({ state }: { state: AgentState | "skipped" }) {
  if (state === "done")
    return (
      <svg width="12" height="12" viewBox="0 0 12 12" aria-label="done">
        <rect x="0.5" y="0.5" width="11" height="11" rx="2.5" fill="var(--ink)" />
        <path d="M3.2 6.2l1.8 1.8 3.8-4" stroke="#fff" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  if (state === "running")
    return (
      <svg className="live" width="12" height="12" viewBox="0 0 12 12" aria-label="running">
        <rect x="1" y="1" width="10" height="10" rx="2.5" fill="none" stroke="var(--accent)" strokeWidth="2" />
        <rect x="4" y="4" width="4" height="4" rx="1" fill="var(--accent)" />
      </svg>
    );
  if (state === "failed")
    return (
      <svg width="12" height="12" viewBox="0 0 12 12" aria-label="failed">
        <rect x="0.5" y="0.5" width="11" height="11" rx="2.5" fill="var(--bad)" />
        <path d="M4 4l4 4M8 4l-4 4" stroke="#fff" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    );
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" aria-label="waiting">
      <rect x="1" y="1" width="10" height="10" rx="2.5" fill="none" stroke="var(--line)" strokeWidth="1.5" />
    </svg>
  );
}

export function DownloadIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
      <path d="M7 2.5v6.5M4.2 6.6L7 9.4l2.8-2.8M3 11.5h8" stroke="currentColor" strokeWidth="1.4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function ChevronIcon({ open }: { open: boolean }) {
  return (
    <svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true" style={{ transform: open ? "rotate(90deg)" : "none", transition: "transform 120ms" }}>
      <path d="M3.5 2l3 3-3 3" stroke="currentColor" strokeWidth="1.4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function PlusIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true">
      <path d="M6 2v8M2 6h8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}
