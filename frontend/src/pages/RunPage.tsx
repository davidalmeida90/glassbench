import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type Meta } from "../api";
import { AgentDetail } from "../components/AgentDetail";
import { CommitteeBoard } from "../components/CommitteeBoard";
import { DecisionCard, FilesCard, FlagsCard } from "../components/SideCards";
import { StageStrip } from "../components/StageStrip";
import { Timeline } from "../components/Timeline";
import { fmtClockDuration, fmtTokens, fmtUsd } from "../format";
import { useNow, useRunStream } from "../hooks";
import { currentAgent, TERMINAL, viewMeta } from "../runState";

export default function RunPage({ meta }: { meta: Meta }) {
  const { runId = "" } = useParams();
  const { run } = useRunStream(runId, meta);
  const live = !!run && !TERMINAL.has(run.status);
  const now = useNow(live, 500);
  const [selected, setSelected] = useState<string>();
  const [board, setBoard] = useState<boolean>(() => {
    try {
      return localStorage.getItem("desk.board") !== "off";
    } catch {
      return true;
    }
  });
  const toggleBoard = () => {
    setBoard((v) => {
      try {
        localStorage.setItem("desk.board", v ? "off" : "on");
      } catch {
        /* per-viewer convenience only */
      }
      return !v;
    });
  };
  const [pinned, setPinned] = useState(false);
  const [cancelling, setCancelling] = useState(false);

  // Follow the agent that is working unless the user picked one.
  const active = run ? currentAgent(run) : undefined;
  useEffect(() => {
    if (!pinned && active) setSelected(active);
  }, [active, pinned]);
  useEffect(() => {
    if (run && !selected) setSelected(run.order.find((id) => run.agents[id]?.state !== "waiting") ?? run.order[0]);
  }, [run, selected]);

  if (!run || !run.ticker) return <div className="empty">Loading run…</div>;

  const end = run.finishedAt ?? now;
  const elapsed = run.startedAt ? end - run.startedAt : 0;
  const done = run.order.filter((id) => run.agents[id]?.state === "done").length;
  const agent = selected ? run.agents[selected] : undefined;
  const analysts = run.order.filter((id) => run.agents[id]?.stage === "analysts").length;
  const vm = viewMeta(meta, run);
  const aihfRun = run.engine === "ai_hedge_fund";
  const statusPill =
    run.status === "running" ? (
      <span className="pill pill-live"><span className="dot live" style={{ background: "var(--accent)" }} />Running{active ? ` · ${run.agents[active]?.label}` : ""}</span>
    ) : run.status === "queued" ? (
      <span className="pill pill-quiet">Queued</span>
    ) : run.status === "finished" ? (
      <span className="pill pill-done">Finished</span>
    ) : (
      <span className="pill pill-bad">{run.status === "failed" ? "Failed" : "Cancelled"}</span>
    );

  return (
    <>
      <header className="run-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <div className="crumb"><Link to="/runs">Runs</Link> / {run.tradeDate}</div>
          <div className="titlerow">
            <h1>{run.ticker}</h1>
            <span className="subtitle">
              {aihfRun
                ? `AI Hedge Fund · ${run.variant === "custom" || !run.variant ? "custom strategy" : run.variant} · ${analysts} analyst${analysts === 1 ? "" : "s"} · ${run.quickModel.replace("deepseek-", "")}`
                : `${analysts} analyst${analysts === 1 ? "" : "s"} · ${run.depth} debate round${run.depth === 1 ? "" : "s"} · ${run.quickModel.replace("deepseek-", "")} / ${run.deepModel.replace("deepseek-", "")}`}
            </span>
            {statusPill}
          </div>
        </div>
        <div className="metrics">
          <div className="metric"><span className="cap">Elapsed</span><b>{fmtClockDuration(elapsed)}</b></div>
          <div className="metric"><span className="cap">Agents</span><b>{done} / {run.order.length}</b></div>
          <div className="metric"><span className="cap">LLM calls</span><b>{run.totals.llm}</b></div>
          <div className="metric"><span className="cap">Tool calls</span><b>{run.totals.tools}</b></div>
          <div className="metric"><span className="cap">Tokens</span><b>{fmtTokens(run.totals.tokensIn + run.totals.tokensOut)}</b></div>
          <div className="metric"><span className="cap">Cost est.</span><b>{fmtUsd(run.totals.cost)}</b></div>
          <button className={`btn${board ? " on" : ""}`} aria-pressed={board} onClick={toggleBoard}>
            {board ? "Hide committee" : "Committee board"}
          </button>
          {live && (
            <button
              className="btn"
              disabled={cancelling}
              onClick={() => {
                setCancelling(true);
                api.cancel(runId).catch(() => setCancelling(false));
              }}
            >
              {cancelling ? "Stopping after this step…" : "Cancel run"}
            </button>
          )}
        </div>
      </header>

      {board && (
        <CommitteeBoard
          run={run}
          meta={vm}
          now={now}
          selected={selected}
          onSelect={(id) => {
            setSelected(id);
            setPinned(id !== active);
          }}
        />
      )}
      <StageStrip run={run} meta={vm} now={now} />
      <Timeline
        run={run}
        meta={vm}
        now={now}
        selected={selected}
        onSelect={(id) => {
          setSelected(id);
          setPinned(id !== active);
        }}
      />

      <section className="split">
        <div className="stack">
          {agent && <AgentDetail runId={runId} run={run} agent={agent} now={now} />}
          {pinned && active && (
            <button className="btn btn-ghost" style={{ alignSelf: "flex-start", color: "var(--accent)" }} onClick={() => setPinned(false)}>
              Follow the working agent ({run.agents[active]?.label})
            </button>
          )}
        </div>
        <div className="stack">
          <DecisionCard run={run} />
          <FlagsCard run={run} />
          <FilesCard runId={runId} run={run} />
        </div>
      </section>
    </>
  );
}
