/**
 * Glassbench mark: a pane of glass standing on a bench, with the trace of what happened visible
 * through it. Ink for the structure, cobalt for what is live (direction A "Instrument").
 * Drawn on a 32 unit grid so it stays crisp at 16 px (favicon) and at 40 px (sidebar).
 */
export function Logo({ size = 30 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" role="img" aria-label="Glassbench">
      {/* the pane */}
      <rect x="6.5" y="3.5" width="19" height="17.5" rx="3.2" fill="var(--accent-soft)" stroke="var(--ink)" strokeWidth="2.2" />
      {/* the trace seen through it */}
      <path d="M10.5 16 L14 12.2 L17.2 14.6 L21.5 8.8" stroke="var(--accent)" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="21.5" cy="8.8" r="1.7" fill="var(--accent)" />
      {/* the bench */}
      <path d="M2.8 25 H29.2" stroke="var(--ink)" strokeWidth="2.6" strokeLinecap="round" />
      <path d="M7.5 25 V29.2 M24.5 25 V29.2" stroke="var(--ink)" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}
