import { useEffect, useRef, useState } from "react";
import { api, type DeskEvent, type Meta } from "./api";
import { setEngineBuilds } from "./components/RunFilters";
import { applyEvents, emptyRun, TERMINAL, type RunView } from "./runState";

let metaPromise: Promise<Meta> | null = null;

export function useMeta(): { meta?: Meta; error?: string } {
  const [meta, setMeta] = useState<Meta>();
  const [error, setError] = useState<string>();
  useEffect(() => {
    metaPromise ??= api.meta().then((m) => {
      setEngineBuilds(m.engine_builds); // before any page reads a version label
      return m;
    });
    metaPromise.then(setMeta).catch((e) => {
      metaPromise = null;
      setError(String(e.message || e));
    });
  }, []);
  return { meta, error };
}

/** Replays a run's stored events, then follows live ones. Batches renders to ~8 fps. */
export function useRunStream(runId: string, meta?: Meta): { run?: RunView; connected: boolean } {
  const [run, setRun] = useState<RunView>();
  const [connected, setConnected] = useState(false);
  const pending = useRef<DeskEvent[]>([]);
  const state = useRef<RunView | undefined>(undefined);

  useEffect(() => {
    if (!meta) return;
    state.current = emptyRun(meta);
    pending.current = [];
    setRun(undefined);
    const source = new EventSource(api.eventsUrl(runId));
    source.onopen = () => setConnected(true);
    source.onmessage = (msg) => pending.current.push(JSON.parse(msg.data));
    source.addEventListener("end", () => {
      source.close();
      setConnected(false);
    });
    source.onerror = () => {
      setConnected(false);
      if (state.current && TERMINAL.has(state.current.status)) source.close();
    };
    const timer = window.setInterval(() => {
      if (!pending.current.length || !state.current) return;
      const batch = pending.current;
      pending.current = [];
      state.current = applyEvents(state.current, meta, batch);
      setRun(state.current);
    }, 120);
    return () => {
      source.close();
      window.clearInterval(timer);
    };
  }, [runId, meta]);

  return { run, connected };
}

export function useNow(active: boolean, intervalMs = 1000): number {
  const [now, setNow] = useState(() => Date.now() / 1000);
  useEffect(() => {
    if (!active) return;
    const t = window.setInterval(() => setNow(Date.now() / 1000), intervalMs);
    return () => window.clearInterval(t);
  }, [active, intervalMs]);
  return now;
}
