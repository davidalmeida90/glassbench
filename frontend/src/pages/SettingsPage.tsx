import { useEffect, useState } from "react";
import { api, type BrokerCheck, type BrokerId, type DeskSettings, type IbkrConfig, type Meta } from "../api";

const ORDER: BrokerId[] = ["none", "alpaca", "ibkr"];
const KEY_NAMES: Record<string, string> = {
  DEEPSEEK_API_KEY: "DeepSeek",
  FRED_API_KEY: "FRED",
  ALPACA_API_KEY: "Alpaca key ID",
  ALPACA_SECRET_KEY: "Alpaca secret",
};

export default function SettingsPage({ meta, onBrokerChange }: { meta: Meta; onBrokerChange: (s: DeskSettings) => void }) {
  const [settings, setSettings] = useState<DeskSettings>();
  const [broker, setBroker] = useState<BrokerId>("none");
  const [ibkr, setIbkr] = useState<IbkrConfig>({ host: "127.0.0.1", port: 4002, client_id: 17 });
  const [check, setCheck] = useState<BrokerCheck>();
  const [checking, setChecking] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => {
    api.settings().then((s) => {
      setSettings(s);
      setBroker(s.broker);
      setIbkr(s.ibkr);
    }).catch((e) => setError(String(e.message || e)));
  }, []);

  const dirty = !!settings && (broker !== settings.broker || (broker === "ibkr" && JSON.stringify(ibkr) !== JSON.stringify(settings.ibkr)));

  const runCheck = async () => {
    setChecking(true);
    setCheck(undefined);
    try {
      setCheck(await api.checkBroker({ broker, ibkr }));
    } catch (e: any) {
      setCheck({ ok: false, summary: String(e.message || e), details: [] });
    } finally {
      setChecking(false);
    }
  };

  const save = async () => {
    setError(undefined);
    try {
      const s = await api.saveSettings({ broker, ibkr });
      setSettings(s);
      onBrokerChange(s);
      setSaved(true);
      window.setTimeout(() => setSaved(false), 2000);
    } catch (e: any) {
      setError(String(e.message || e));
    }
  };

  return (
    <>
      <header className="page-head">
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          <h1>Settings</h1>
          <span className="subtitle">Where orders will go, which keys are loaded, and the prices used for cost estimates.</span>
        </div>
      </header>

      <section className="panel panel-pad settings-section">
        <div className="settings-head">
          <div>
            <h2>Broker</h2>
            <p className="muted">Paper accounts only. Glassbench does not place orders yet; strategy rules and order routing come in phase 4. This sets where they will go and checks the connection now.</p>
          </div>
        </div>

        <div className="broker-options" role="radiogroup" aria-label="Broker">
          {settings &&
            ORDER.map((id) => {
              const b = settings.brokers[id];
              const on = broker === id;
              return (
                <button
                  key={id}
                  role="radio"
                  aria-checked={on}
                  className={`broker-option${on ? " on" : ""}`}
                  onClick={() => {
                    setBroker(id);
                    setCheck(undefined);
                  }}
                >
                  <span className="radio" aria-hidden="true">{on && <span />}</span>
                  <span style={{ display: "flex", flexDirection: "column", gap: 3, textAlign: "left" }}>
                    <b>{b.label}</b>
                    <span className="muted">{b.detail}</span>
                  </span>
                </button>
              );
            })}
        </div>

        {broker === "ibkr" && (
          <div className="ibkr-fields">
            <div className="field">
              <label htmlFor="ib-host">Host</label>
              <input id="ib-host" className="input" value={ibkr.host} onChange={(e) => setIbkr({ ...ibkr, host: e.target.value })} />
            </div>
            <div className="field">
              <label htmlFor="ib-port">Port</label>
              <input id="ib-port" className="input" type="number" value={ibkr.port} onChange={(e) => setIbkr({ ...ibkr, port: Number(e.target.value) })} />
              <span className="hint">4002 Gateway · 7497 TWS</span>
            </div>
            <div className="field">
              <label htmlFor="ib-client">Client ID</label>
              <input id="ib-client" className="input" type="number" value={ibkr.client_id} onChange={(e) => setIbkr({ ...ibkr, client_id: Number(e.target.value) })} />
            </div>
          </div>
        )}

        <div className="settings-actions">
          <button className="btn" onClick={runCheck} disabled={checking || broker === "none"}>
            {checking ? "Checking…" : "Test connection"}
          </button>
          <button className="btn btn-primary" onClick={save} disabled={!dirty}>
            {saved ? "Saved" : "Save"}
          </button>
          {check && (
            <div className="check-result">
              <span className="dot" style={{ background: check.ok ? "var(--good)" : "var(--bad)" }} />
              <div>
                <div style={{ fontWeight: 600 }}>{check.summary}</div>
                {check.details.map((d) => (
                  <div key={d} className="muted" style={{ fontSize: 12.5 }}>{d}</div>
                ))}
              </div>
            </div>
          )}
          {error && <span className="error">{error}</span>}
        </div>
      </section>

      <section className="settings-grid">
        <div className="panel panel-pad settings-section">
          <h2>Keys</h2>
          <p className="muted">Read from .env at the repository root when Glassbench starts. Values never reach the browser. Edit the file, then restart Glassbench.</p>
          <table className="table compact">
            <tbody>
              {meta.keys.map((k) => (
                <tr key={k.name} style={{ cursor: "default" }}>
                  <td><span className="dot" style={{ display: "inline-block", marginRight: 8, background: k.present ? "var(--good)" : "var(--line)" }} />{KEY_NAMES[k.name] ?? k.name}</td>
                  <td className="mono muted">{k.name}</td>
                  <td className="r muted">{k.present ? `loaded · ${k.length} chars` : "not set"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="panel panel-pad settings-section">
          <h2>Model prices</h2>
          <p className="muted">USD per million tokens, used for the cost estimates. Edit PRICING in backend/deskapp/settings.py when DeepSeek changes prices.</p>
          <table className="table compact">
            <thead>
              <tr><th>Model</th><th className="r">Input</th><th className="r">Output</th></tr>
            </thead>
            <tbody>
              {Object.entries(meta.pricing).map(([m, p]) => (
                <tr key={m} style={{ cursor: "default" }}>
                  <td className="mono">{m}</td>
                  <td className="r">${p.input.toFixed(3)}</td>
                  <td className="r">${p.output.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}
