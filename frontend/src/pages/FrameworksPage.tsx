import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, type Framework } from "../api";
import { FrameworkDiagram } from "../components/FrameworkDiagram";
import { Markdown } from "../components/Markdown";

const TABS = ["Overview", "Flow", "Agents", "Data", "Evidence"] as const;
type Tab = (typeof TABS)[number];
const STAGE_LABEL: Record<string, string> = {
  analysts: "Analysts", research: "Research debate", trading: "Trading", risk: "Risk debate", portfolio: "Decision",
  strategy: "Strategy", risk_limits: "Risk",
};
const ROLE_LABEL: Record<string, string> = { quick: "Quick LLM", deep: "Deep LLM", rule: "Rule, no LLM" };

export default function FrameworksPage() {
  const { frameworkId } = useParams();
  const navigate = useNavigate();
  const [list, setList] = useState<Framework[]>();
  const [error, setError] = useState<string>();
  const [tab, setTab] = useState<Tab>("Overview");
  const [agent, setAgent] = useState<string | null>(null);

  useEffect(() => {
    api.frameworks().then(setList).catch((e) => setError(String(e.message ?? e)));
  }, []);

  const fw = useMemo(() => list?.find((f) => f.id === frameworkId) ?? list?.[0], [list, frameworkId]);
  useEffect(() => {
    if (list && !frameworkId && list[0]) navigate(`/frameworks/${list[0].id}`, { replace: true });
  }, [list, frameworkId, navigate]);
  useEffect(() => setAgent(null), [fw?.id]);

  if (error) return <div className="error">{error}</div>;
  if (!list || !fw) return <div className="empty">Loading frameworks…</div>;

  const selectedAgent = fw.agents.find((a) => a.id === agent) ?? null;

  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <h1>Frameworks</h1>
          <span className="subtitle">The open-source harnesses Glassbench can run or plans to run: how each one decides, what it reads, and what the evidence says.</span>
        </div>
      </header>

      <div className="fw-layout">
        <aside className="fw-list">
          {list.map((f) => (
            <Link key={f.id} to={`/frameworks/${f.id}`} className={`fw-item${f.id === fw.id ? " on" : ""}`}>
              <div className="fw-item-head">
                <b>{f.name}</b>
                <span className={`pill ${f.status === "connected" ? "pill-done" : "pill-quiet"}`}>{f.status === "connected" ? "Connected" : "Planned"}</span>
              </div>
              <span className="muted" style={{ fontSize: 12 }}>{f.org}{f.version ? ` · ${f.version.replace(/\+.*/, "")}` : ""}</span>
              <span className="muted" style={{ fontSize: 11.5 }}>{f.runs} run{f.runs === 1 ? "" : "s"} recorded</span>
            </Link>
          ))}
        </aside>

        <section className="panel fw-detail">
          <div className="fw-head">
            <div>
              <h2>{fw.name}<span className="muted" style={{ fontWeight: 400, marginLeft: 8, fontSize: 14 }}>{fw.org}</span></h2>
              <p className="fw-tagline">{fw.tagline}</p>
            </div>
            <div className="fw-links">
              {fw.links.map((l) => (
                <a key={l.url} className="btn" href={l.url} target="_blank" rel="noreferrer">{l.label} ↗</a>
              ))}
            </div>
          </div>
          <div className="tabs" role="tablist" style={{ padding: "0 16px" }}>
            {TABS.map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} className={`tab${tab === t ? " on" : ""}`} onClick={() => setTab(t)}>{t}</button>
            ))}
          </div>

          <div className="panel-pad fw-body">
            {tab === "Overview" && (
              <>
                <p className="fw-summary">{fw.summary}</p>
                <div className="facts">
                  {fw.facts.map((f) => (
                    <div key={f.label} className="fact">
                      <span className="cap">{f.label}</span>
                      <b>{f.value}</b>
                      {f.note && <span className="muted" style={{ fontSize: 11.5 }}>{f.note}</span>}
                    </div>
                  ))}
                </div>
                <h3 className="cap" style={{ marginTop: 8 }}>Mechanism</h3>
                <FrameworkDiagram flow={fw.flow} selected={agent} onSelect={(id) => { setAgent(id); if (id && fw.agents.some((a) => a.id === id)) setTab("Agents"); }} />
              </>
            )}

            {tab === "Flow" && (
              <>
                <FrameworkDiagram flow={fw.flow} selected={agent} onSelect={setAgent} />
                <ol className="fw-steps">
                  {fw.flow.stages.map((s, i) => (
                    <li key={s.id}>
                      <b>{s.label}</b> <span className="muted">· {s.nodes.map((n) => n.label).join(", ")}</span>
                      {i === 0 && <span className="muted"> · the run starts here</span>}
                    </li>
                  ))}
                </ol>
                <ul className="assumptions">
                  {fw.flow.notes.map((n) => <li key={n}>{n}</li>)}
                </ul>
              </>
            )}

            {tab === "Agents" && (
              <div className="fw-agents">
                <div className="table-wrap">
                  <table className="table compact">
                    <thead>
                      <tr>
                        <th>Agent</th>
                        <th>Stage</th>
                        <th>Model</th>
                        <th>Reads</th>
                      </tr>
                    </thead>
                    <tbody>
                      {fw.agents.map((a) => (
                        <tr key={a.id} className={a.id === agent ? "hl-row" : ""} onClick={() => setAgent(a.id === agent ? null : a.id)}>
                          <td style={{ fontWeight: 600 }}>{a.name}</td>
                          <td>{STAGE_LABEL[a.stage] ?? a.stage}</td>
                          <td className="mono" style={{ fontSize: 11.5 }}>{ROLE_LABEL[a.role] ?? a.role}</td>
                          <td className="clip" style={{ maxWidth: 260, color: "var(--ink-2)" }} title={a.reads.join(", ")}>{a.reads.join(", ")}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="fw-agent-card">
                  {selectedAgent ? (
                    <>
                      <span className="cap">{STAGE_LABEL[selectedAgent.stage] ?? selectedAgent.stage} · {ROLE_LABEL[selectedAgent.role] ?? selectedAgent.role}</span>
                      <h3>{selectedAgent.name}</h3>
                      <p>{selectedAgent.what}</p>
                      {selectedAgent.tools && (
                        <p className="muted" style={{ fontSize: 12 }}>
                          Tools: <span className="mono">{selectedAgent.tools}</span>
                        </p>
                      )}
                      <p className="muted" style={{ fontSize: 12 }}>Reads: {selectedAgent.reads.join(", ")}</p>
                    </>
                  ) : (
                    <span className="muted">Pick an agent in the table or the diagram to read what it does.</span>
                  )}
                </div>
              </div>
            )}

            {tab === "Data" && (
              <div className="table-wrap">
                <table className="table compact static">
                  <thead>
                    <tr>
                      <th>Source</th>
                      <th>Used for</th>
                      <th>Point in time on past dates</th>
                    </tr>
                  </thead>
                  <tbody>
                    {fw.data.map((d) => (
                      <tr key={d.source}>
                        <td style={{ fontWeight: 600 }}>{d.source}</td>
                        <td style={{ whiteSpace: "normal" }}>{d.used_for}</td>
                        <td style={{ whiteSpace: "normal", color: "var(--ink-2)" }}>{d.point_in_time}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {tab === "Evidence" && (
              <div className="evidence">
                {fw.evidence.map((e) => (
                  <div key={e.claim} className="evidence-item">
                    <Markdown text={`**${e.claim}**`} />
                    <span className="muted" style={{ fontSize: 12 }}>{e.source}{e.note ? ` · ${e.note}` : ""}</span>
                  </div>
                ))}
                <p className="caption">Performance claims are listed as reported; none is an endorsement. See the Backtests page for Glassbench's own replays.</p>
              </div>
            )}
          </div>
        </section>
      </div>
    </>
  );
}
