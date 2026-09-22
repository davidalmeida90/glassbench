import type { Meta } from "../api";
import { fmtDuration } from "../format";
import type { RunView } from "../runState";

export function StageStrip({ run, meta, now }: { run: RunView; meta: Meta; now: number }) {
  const ended = run.status === "failed" || run.status === "cancelled";
  return (
    <section className="panel stages" aria-label="Pipeline stages">
      {meta.stages.map((stage) => {
        const agents = run.order.map((id) => run.agents[id]).filter((a) => a && a.stage === stage.id);
        const done = agents.filter((a) => a.state === "done").length;
        const running = agents.find((a) => a.state === "running");
        const failed = agents.find((a) => a.state === "failed");
        const starts = agents.flatMap((a) => a.visits.map((v) => v.start));
        const ends = agents.flatMap((a) => a.visits.map((v) => v.end ?? now));
        const span = starts.length ? Math.max(...ends) - Math.min(...starts) : 0;
        let status;
        if (!agents.length) status = <span className="muted">Not selected</span>;
        else if (running)
          status = (
            <>
              <span style={{ color: "var(--accent)", fontWeight: 600 }}>{running.label} working</span>
              <span className="mono muted" style={{ fontSize: 11 }}>{fmtDuration(span)}</span>
            </>
          );
        else if (failed) status = <span style={{ color: "var(--bad)", fontWeight: 600 }}>{failed.label} failed</span>;
        else if (done === agents.length)
          status = (
            <>
              <span>Done</span>
              <span className="mono muted" style={{ fontSize: 11 }}>{fmtDuration(span)}</span>
            </>
          );
        else if (ended) status = <span className="muted">{done > 0 ? "Stopped" : "Not run"}</span>;
        else if (done > 0) status = <span className="muted">Waiting for next turn</span>;
        else status = <span className="muted">Queued</span>;
        return (
          <div className="stage" key={stage.id}>
            <div className="panel-head">
              <span className="cap">{stage.label}</span>
              <span className="mono muted" style={{ fontSize: 10.5 }}>
                {done}/{agents.length}
              </span>
            </div>
            <div className="stage-segs">
              {agents.map((a) => (
                <span key={a.id} className={`s-${a.state}${a.state === "running" ? " live" : ""}`} title={`${a.name}: ${a.state}`} />
              ))}
            </div>
            <div className="stage-status">{status}</div>
          </div>
        );
      })}
    </section>
  );
}
