export function fmtDuration(seconds: number | null | undefined): string {
  if (seconds == null || !isFinite(seconds)) return "—";
  const s = Math.max(0, Math.round(seconds));
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, "0")}s`;
  return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, "0")}m`;
}

export function fmtClockDuration(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

export function fmtClock(ts: number, withSeconds = true): string {
  return new Date(ts * 1000).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: withSeconds ? "2-digit" : undefined });
}

export function fmtDate(ts: number): string {
  return new Date(ts * 1000).toLocaleDateString("en-GB", { day: "numeric", month: "short" });
}

export function fmtTokens(n: number | null | undefined): string {
  if (!n) return "0";
  if (n < 1000) return String(n);
  if (n < 1_000_000) return `${(n / 1000).toFixed(n < 10_000 ? 1 : 0)}k`;
  return `${(n / 1_000_000).toFixed(2)}M`;
}

export function fmtUsd(n: number | null | undefined): string {
  if (n == null) return "—";
  if (n === 0) return "$0";
  if (n < 0.01) return `$${n.toFixed(4)}`;
  return `$${n.toFixed(n < 1 ? 3 : 2)}`;
}

export function fmtBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

export function fmtPrice(n: number | null | undefined): string {
  return n == null ? "—" : n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function argsSummary(args: Record<string, unknown> | undefined): string {
  if (!args) return "";
  const values = Object.entries(args)
    .filter(([k]) => !["curr_date", "symbol", "ticker"].includes(k))
    .map(([, v]) => (typeof v === "string" ? v : JSON.stringify(v)));
  // Words first (topic, indicator), then dates and numbers.
  const isWordy = (v: string) => /[a-z]{3,}/i.test(v) && !/^\d{4}-\d{2}-\d{2}$/.test(v);
  return [...values.filter(isWordy), ...values.filter((v) => !isWordy(v))].join(" · ");
}

export function firstLine(text: string | undefined, max = 90): string {
  if (!text) return "";
  const line = text
    .split("\n")
    .map((l) => l.replace(/^[#>*\-\s|]+/, "").trim())
    .find((l) => l.length > 0) || "";
  return line.length > max ? `${line.slice(0, max - 1)}…` : line;
}

export function ratingColor(rating: string | null | undefined): string {
  switch ((rating || "").toLowerCase()) {
    case "buy":
      return "var(--rating-buy)";
    case "overweight":
      return "var(--rating-overweight)";
    case "hold":
      return "var(--rating-hold)";
    case "underweight":
      return "var(--rating-underweight)";
    case "sell":
      return "var(--rating-sell)";
    default:
      return "var(--muted)";
  }
}
