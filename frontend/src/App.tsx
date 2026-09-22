import { useEffect, useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { api, type DeskSettings } from "./api";
import { Logo } from "./components/Logo";
import { versionLabel, versionTitle } from "./components/RunFilters";
import { useMeta } from "./hooks";
import RunPage from "./pages/RunPage";
import BacktestResultsPage from "./pages/BacktestResultsPage";
import BacktestsPage from "./pages/BacktestsPage";
import DatabasePage from "./pages/DatabasePage";
import FrameworksPage from "./pages/FrameworksPage";
import RunsPage from "./pages/RunsPage";
import SettingsPage from "./pages/SettingsPage";

const KEY_LABEL: Record<string, string> = { DEEPSEEK_API_KEY: "DeepSeek", FRED_API_KEY: "FRED" };

export default function App() {
  const { meta, error } = useMeta();
  const [settings, setSettings] = useState<DeskSettings>();
  useEffect(() => {
    api.settings().then(setSettings).catch(() => undefined);
  }, []);
  const brokerLabel = settings ? settings.brokers[settings.broker].label : "";
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <Logo size={32} />
          <div className="brand-text">
            <b>Glassbench</b>
            <span title={versionTitle(meta?.engine_version)}>TradingAgents<br />{versionLabel(meta?.engine_version)}</span>
          </div>
        </div>
        <nav className="nav">
          <NavLink to="/runs">Runs</NavLink>
          <NavLink to="/frameworks">Frameworks</NavLink>
          <NavLink to="/database">Database</NavLink>
          <NavLink to="/backtests">Backtests</NavLink>
          <NavLink to="/settings">Settings</NavLink>
        </nav>
        <div className="sidebar-foot">
          <div className="cap">Keys</div>
          {meta?.keys.filter((k) => KEY_LABEL[k.name]).map((k) => (
            <div className="keyrow" key={k.name}>
              <span className="dot" style={{ background: k.present ? "var(--good)" : "var(--bad)" }} />
              {KEY_LABEL[k.name]}
              <span className="muted" style={{ marginLeft: "auto", fontSize: 11.5 }}>{k.present ? "loaded" : "missing"}</span>
            </div>
          ))}
          {error && <div className="error">Backend offline: {error}</div>}
          <NavLink to="/settings" className="keyrow broker-link">
            <span className="dot" style={{ background: settings?.broker && settings.broker !== "none" ? "var(--accent)" : "var(--line)" }} />
            Broker
            <span className="muted" style={{ marginLeft: "auto", fontSize: 11.5 }}>{brokerLabel || "…"}</span>
          </NavLink>
        </div>
      </aside>
      <main className="main">
        {!meta ? (
          <div className="empty">{error ? "Glassbench's backend is not reachable. Start it with desk.ps1." : "Loading…"}</div>
        ) : (
          <Routes>
            <Route path="/" element={<Navigate to="/runs" replace />} />
            <Route path="/runs" element={<RunsPage meta={meta} />} />
            <Route path="/runs/:runId" element={<RunPage meta={meta} />} />
            <Route path="/frameworks" element={<FrameworksPage />} />
            <Route path="/frameworks/:frameworkId" element={<FrameworksPage />} />
            <Route path="/database" element={<DatabasePage />} />
            <Route path="/backtests" element={<BacktestsPage />} />
            <Route path="/backtests/:backtestId" element={<BacktestResultsPage />} />
            <Route path="/settings" element={<SettingsPage meta={meta} onBrokerChange={setSettings} />} />
            <Route path="*" element={<Navigate to="/runs" replace />} />
          </Routes>
        )}
      </main>
    </div>
  );
}
