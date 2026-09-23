import { useEffect, useState } from "react";
import { api, type RunFile } from "../api";
import { fmtBytes, fmtPrice, firstLine, ratingColor } from "../format";
import { TERMINAL, type RunView } from "../runState";
import { DownloadIcon } from "./Icons";

export function DecisionCard({ run }: { run: RunView }) {
  const rm = run.agents.research_manager?.structured ?? run.decision?.research;
  const tr = run.agents.trader?.structured ?? run.decision?.trader;
  const pm = run.agents.portfolio_manager?.structured ?? run.decision?.portfolio ?? undefined;
  const entry = tr?.entry_price as number | undefined;
  const stop = tr?.stop_loss as number | undefined;
  const target = pm?.price_target as number | undefined;
  const risk = entry != null && stop != null ? entry - stop : undefined;
  const rr = risk && risk > 0 && target != null ? (target - entry!) / risk : undefined;
  const finalRating = run.rating || pm?.rating;
  const ended = run.status === "failed" || run.status === "cancelled";
  const idle = ended ? "not reached" : "waiting";

  return (
    <div className="panel panel-pad" style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      <div className="panel-head">
        <span className="panel-title">Decision</span>
        {finalRating ? (
          <span className="rating" style={{ color: ratingColor(finalRating), fontSize: 15 }}>{finalRating}</span>
        ) : (
          <span className="muted" style={{ fontSize: 11.5 }}>{run.status === "failed" || run.status === "cancelled" ? "no final rating" : "final rating pending"}</span>
        )}
      </div>
      <div className="kv">
        <span className="k">Research Mgr</span>
        <span className="v" title={rm?.rationale || ""}>{rm?.rationale ? firstLine(rm.rationale, 60) : <span className="muted">{run.agents.research_manager?.state === "running" ? "weighing the debate…" : idle}</span>}</span>
        <span className="rating" style={{ color: ratingColor(rm?.recommendation) }}>{rm?.recommendation || "—"}</span>

        <span className="k">Trader</span>
        <span className="v num">
          {tr?.action ? (
            [entry != null ? `entry ${fmtPrice(entry)}` : null, stop != null ? `stop ${fmtPrice(stop)}` : null].filter(Boolean).join(" · ") || "no levels given"
          ) : (
            <span className="muted">{run.agents.trader?.state === "running" ? "drafting the proposal…" : idle}</span>
          )}
        </span>
        <span className="rating" style={{ color: ratingColor(tr?.action) }}>{tr?.action || "—"}</span>

        <span className="k">Portfolio Mgr</span>
        <span className="v">{pm?.time_horizon ? `horizon ${pm.time_horizon}` : <span className="muted">{run.agents.portfolio_manager?.state === "running" ? "deciding…" : idle}</span>}</span>
        <span className="rating" style={{ color: ratingColor(pm?.rating) }}>{pm?.rating || "—"}</span>
      </div>
      {(risk != null || target != null) && (
        <div className="kv-foot">
          {risk != null && <span>Risk per share <b>{fmtPrice(risk)}</b></span>}
          {target != null && <span>Target <b>{fmtPrice(target)}</b></span>}
          {rr != null && <span>Reward/risk <b>{rr.toFixed(2)}</b></span>}
        </div>
      )}
      {pm?.executive_summary && <p style={{ margin: 0, fontSize: 12.5, lineHeight: 1.55, color: "var(--ink-2)" }}>{pm.executive_summary}</p>}
      {run.error && <p className="error" style={{ margin: 0 }}>{run.error}</p>}
      {finalRating && <p className="advice-note">Model output from a research tool, not a recommendation to buy, sell or hold. Not investment advice.</p>}
    </div>
  );
}

export function FlagsCard({ run }: { run: RunView }) {
  const grouped = new Map<string, { label: string; agent: string | null; detail: string; count: number }>();
  for (const f of run.flags) {
    const key = `${f.agent}|${f.label}`;
    const g = grouped.get(key);
    if (g) g.count += 1;
    else grouped.set(key, { label: f.label, agent: f.agent, detail: f.detail, count: 1 });
  }
  const items = [...grouped.values()];
  return (
    <div className="panel panel-pad" style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      <div className="panel-head">
        <span className="panel-title">Data flags</span>
        <span className="muted" style={{ fontSize: 11.5 }}>{items.length ? `${run.flags.length} raised` : "none so far"}</span>
      </div>
      {items.map((f, i) => (
        <div className="flag-row" key={i} title={f.detail}>
          <i />
          <span className="muted">{f.agent ? run.agents[f.agent]?.label ?? f.agent : "Engine"}</span>
          <span>
            {f.label}
            {f.count > 1 && <span className="muted"> × {f.count}</span>}
            <span className="muted" style={{ display: "block", fontSize: 11.5, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{firstLine(f.detail, 70)}</span>
          </span>
        </div>
      ))}
    </div>
  );
}

export function FilesCard({ runId, run }: { runId: string; run: RunView }) {
  const [files, setFiles] = useState<RunFile[]>([]);
  const [showTools, setShowTools] = useState(false);
  const done = TERMINAL.has(run.status);

  useEffect(() => {
    let alive = true;
    const load = () => api.files(runId).then((f) => alive && setFiles(f)).catch(() => undefined);
    load();
    if (done) return () => void (alive = false);
    const t = window.setInterval(load, 5000);
    return () => {
      alive = false;
      window.clearInterval(t);
    };
  }, [runId, done]);

  const artifacts = files.filter((f) => f.group === "artifacts" && f.label);
  const toolOutputs = files.filter((f) => f.group === "tool_outputs");

  return (
    <div className="panel panel-pad" style={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div className="panel-head" style={{ paddingBottom: 4 }}>
        <span className="panel-title">Files</span>
        {done ? (
          <a className="btn" href={api.bundleUrl(runId)} style={{ height: 28, fontSize: 12 }}>
            <DownloadIcon /> Download all (.zip)
          </a>
        ) : (
          <span className="muted" style={{ fontSize: 11.5 }}>reports are written when the run ends</span>
        )}
      </div>
      {artifacts.map((f) => (
        <div className="file-row" key={f.path}>
          <a href={api.fileUrl(runId, f.path)} target="_blank" rel="noreferrer">{f.label}</a>
          <span style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <span className="mono muted" style={{ fontSize: 10.5 }}>{fmtBytes(f.bytes)}</span>
            <a href={api.fileUrl(runId, f.path, true)} aria-label={`Download ${f.label}`}><DownloadIcon /></a>
          </span>
        </div>
      ))}
      {toolOutputs.length > 0 && (
        <>
          <button className="file-row btn-ghost" style={{ border: 0, background: "none", cursor: "pointer", padding: 0, color: "var(--ink-2)" }} onClick={() => setShowTools((v) => !v)}>
            <span>Raw tool outputs <span className="muted">({toolOutputs.length})</span></span>
            <span className="muted" style={{ fontSize: 11.5 }}>{showTools ? "hide" : "show"}</span>
          </button>
          {showTools &&
            toolOutputs.map((f) => (
              <div className="file-row" key={f.path} style={{ minHeight: 22 }}>
                <a className="mono" style={{ fontSize: 11 }} href={api.fileUrl(runId, f.path)} target="_blank" rel="noreferrer">{f.path.replace("tool_outputs/", "")}</a>
                <span className="mono muted" style={{ fontSize: 10.5 }}>{fmtBytes(f.bytes)}</span>
              </div>
            ))}
        </>
      )}
    </div>
  );
}
