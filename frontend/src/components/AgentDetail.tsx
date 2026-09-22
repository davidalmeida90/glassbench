import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api";
import { argsSummary, fmtClock, fmtDuration, fmtTokens, fmtUsd, firstLine } from "../format";
import { agentDuration, type AgentView, type RunView, type ToolCall } from "../runState";
import { ChevronIcon } from "./Icons";
import { Markdown } from "./Markdown";

type Tab = "activity" | "report" | "inputs";

export function AgentDetail({ runId, run, agent, now }: { runId: string; run: RunView; agent: AgentView; now: number }) {
  const isAnalyst = agent.stage === "analysts";
  const [tab, setTab] = useState<Tab>(isAnalyst ? "activity" : "report");
  useEffect(() => setTab(agent.stage === "analysts" ? "activity" : "report"), [agent.id, agent.stage]);

  const tokensIn = agent.llm.reduce((s, c) => s + (c.tokensIn || 0), 0);
  const tokensOut = agent.llm.reduce((s, c) => s + (c.tokensOut || 0), 0);
  const cost = agent.llm.reduce((s, c) => s + (c.cost || 0), 0);
  const models = [...new Set(agent.llm.map((c) => c.model.replace("deepseek-", "")))].join(", ");
  const dur = agentDuration(agent, now);

  return (
    <div className="panel panel-pad detail">
      <div className="panel-head">
        <div className="detail-title">
          <b>{agent.name}</b>
          <span className="muted" style={{ fontSize: 12 }}>
            {agent.state === "waiting"
              ? "waiting for its turn"
              : [models || agent.role, `${agent.llm.length} LLM call${agent.llm.length === 1 ? "" : "s"}`, agent.tools.length ? `${agent.tools.length} tools` : null, dur != null ? fmtDuration(dur) : null]
                  .filter(Boolean)
                  .join(" · ")}
          </span>
        </div>
        <div className="tabs" role="tablist">
          {(["activity", "report", "inputs"] as Tab[]).map((t) => (
            <button key={t} className={`tab${tab === t ? " on" : ""}`} role="tab" aria-selected={tab === t} onClick={() => setTab(t)}>
              {t === "activity" ? "Activity" : t === "report" ? "Output" : "Inputs"}
            </button>
          ))}
        </div>
      </div>

      {tab === "activity" && <Activity runId={runId} agent={agent} now={now} />}
      {tab === "report" && <Output agent={agent} />}
      {tab === "inputs" && <Inputs agent={agent} run={run} />}

      {agent.llm.length > 0 && (
        <div className="kv-foot">
          <span>Tokens in <b>{fmtTokens(tokensIn)}</b></span>
          <span>out <b>{fmtTokens(tokensOut)}</b></span>
          <span>Cost <b>{fmtUsd(cost)}</b> <span className="muted">est.</span></span>
        </div>
      )}
    </div>
  );
}

function Activity({ runId, agent, now }: { runId: string; agent: AgentView; now: number }) {
  const items = useMemo(() => {
    const list: ({ kind: "llm"; start: number; i: number } | { kind: "batch"; start: number; i: number })[] = [
      ...agent.llm.map((c, i) => ({ kind: "llm" as const, start: c.start, i })),
      ...agent.batches.map((b, i) => ({ kind: "batch" as const, start: b.start, i })),
    ];
    return list.sort((a, b) => a.start - b.start);
  }, [agent.llm, agent.batches]);

  if (!items.length) return <div className="empty">Nothing yet. Steps appear here as this agent works.</div>;

  let round = 0;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {items.map((item) => {
        if (item.kind === "llm") {
          const c = agent.llm[item.i];
          const running = c.end == null;
          return (
            <div className="llm-row" key={c.id}>
              <span className={`dot${running ? " live" : ""}`} style={{ background: running ? "var(--accent)" : c.model.includes("pro") ? "var(--bar-pro)" : "var(--bar-flash)" }} />
              <span>
                <b style={{ fontWeight: 600 }}>LLM call</b> <span className="muted">· {c.model}{c.reasoning ? ` · ${fmtTokens(c.reasoning)} reasoning` : ""}</span>
                {c.failed && <span style={{ color: "var(--bad)" }}> · failed</span>}
              </span>
              <span className="mono muted" style={{ fontSize: 10.5 }}>
                {running ? `${fmtClock(c.start)} · writing ${fmtDuration(now - c.start)}` : `${fmtTokens(c.tokensIn)} in · ${fmtTokens(c.tokensOut)} out · ${fmtDuration((c.end || now) - c.start)}`}
              </span>
            </div>
          );
        }
        const batch = agent.batches[item.i];
        round += 1;
        const calls = agent.tools.filter((t) => batch.calls.includes(t.id));
        return (
          <div key={`batch-${item.i}`}>
            <div className="round-head">
              <span>
                Tool round {round} · {calls.length} {calls.length === 1 ? "call" : "calls in parallel"}
              </span>
              <span className="mono">
                {fmtClock(batch.start)}
                {batch.end ? ` → ${fmtClock(batch.end)}` : ""}
              </span>
            </div>
            {calls.map((t) => (
              <ToolRow key={t.id} runId={runId} call={t} />
            ))}
          </div>
        );
      })}
    </div>
  );
}

function ToolRow({ runId, call }: { runId: string; call: ToolCall }) {
  const [open, setOpen] = useState(false);
  return (
    <details className="tool-row" open={open} onToggle={(e) => setOpen((e.target as HTMLDetailsElement).open)}>
      <summary>
        <span className="tool-name" style={{ display: "flex", gap: 6, alignItems: "center" }}>
          <ChevronIcon open={open} />
          {call.tool}
        </span>
        <span className="tool-args" title={argsSummary(call.args)}>{argsSummary(call.args)}</span>
        <span className="tool-res">
          {call.end == null ? <span className="muted live">fetching…</span> : call.failed ? <span style={{ color: "var(--bad)" }}>{call.failed}</span> : firstLine(call.preview, 120)}
          {call.flag && <span className="tool-flag">{call.flag}</span>}
        </span>
        <span className="tool-dur">{call.end ? fmtDuration(call.end - call.start) : ""}</span>
      </summary>
      {open && (
        <div className="tool-body">
          <pre>{call.preview || "No output"}</pre>
          <div className="links">
            <span className="mono muted" style={{ fontSize: 11 }}>{JSON.stringify(call.args)}</span>
            {call.file && (
              <>
                <a href={api.fileUrl(runId, call.file)} target="_blank" rel="noreferrer">Full output ({(call.chars || 0).toLocaleString()} chars)</a>
                <a href={api.fileUrl(runId, call.file, true)}>Download</a>
              </>
            )}
          </div>
        </div>
      )}
    </details>
  );
}

function Output({ agent }: { agent: AgentView }) {
  const streaming = agent.state === "running" && !!agent.live;
  const text = agent.report && !(agent.state === "running" && agent.live) ? agent.report : agent.live || agent.report;
  const thinking = agent.state === "running" && !agent.live && !!agent.reasoning;
  const reasoningTokens = agent.llm.reduce((s, c) => s + (c.reasoning || 0), 0);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {agent.reasoning && <Reasoning text={agent.reasoning} live={thinking} tokens={reasoningTokens} />}
      {text ? (
        <div style={{ maxHeight: 620, overflowY: "auto", paddingRight: 6 }}>
          <Markdown text={text} streaming={streaming} />
        </div>
      ) : agent.state === "running" ? (
        <div className="empty">{thinking ? "The answer starts once reasoning is done." : <span className="live">Waiting for the model…</span>}</div>
      ) : (
        <div className="empty">No output yet.</div>
      )}
    </div>
  );
}

function Reasoning({ text, live, tokens }: { text: string; live: boolean; tokens: number }) {
  const [open, setOpen] = useState(live);
  const body = useRef<HTMLDivElement>(null);
  useEffect(() => setOpen(live), [live]);
  useEffect(() => {
    if (live && body.current) body.current.scrollTop = body.current.scrollHeight;
  }, [text, live]);
  return (
    <div className={`reasoning${live ? " is-live" : ""}`}>
      <button className="reasoning-head" onClick={() => setOpen((v) => !v)} aria-expanded={open}>
        <ChevronIcon open={open} />
        <span style={{ fontWeight: 600 }}>Reasoning</span>
        {live ? <span className="live" style={{ color: "var(--accent)" }}>thinking</span> : <span className="muted">{tokens ? `${fmtTokens(tokens)} tokens` : ""}</span>}
      </button>
      {open && (
        <div className="reasoning-body" ref={body}>
          {text}
          {live && <span className="caret live" />}
        </div>
      )}
    </div>
  );
}

function Inputs({ agent, run }: { agent: AgentView; run: RunView }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 13 }}>
      <div>
        <div className="cap" style={{ paddingBottom: 6 }}>What this agent reads</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {agent.reads.map((r) => (
            <div key={r} className="file-row" style={{ minHeight: 22 }}>
              <span className={r.includes("_") ? "mono" : ""} style={{ fontSize: r.includes("_") ? 11.5 : 13, color: "var(--ink-2)" }}>{r}</span>
            </div>
          ))}
        </div>
      </div>
      {agent.id === "portfolio_manager" && (
        <div>
          <div className="cap" style={{ paddingBottom: 6 }}>Lessons from past decisions</div>
          {run.memory ? <Markdown text={run.memory.preview} /> : <div className="muted">No resolved past decisions for {run.ticker} yet.</div>}
        </div>
      )}
      {run.instrument && (
        <div>
          <div className="cap" style={{ paddingBottom: 6 }}>Instrument context given to every agent</div>
          <div className="prose" style={{ fontSize: 12.5 }}>{run.instrument}</div>
        </div>
      )}
    </div>
  );
}
