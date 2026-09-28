import { useState } from 'react';
import { api, type Scenario } from '@/lib/api';
import { useOps } from '@/store/useOps';

const SCENARIOS: { id: Scenario; label: string; hotkey: string }[] = [
  { id: 'uplink-congestion', label: 'Inject Uplink Congestion', hotkey: '⇧1' },
  { id: 'dns-failure', label: 'Inject DNS Failure', hotkey: '⇧2' },
  { id: 'server-spike', label: 'Inject Server Spike', hotkey: '⇧3' },
];

export function DemoControls() {
  const demo = useOps((s) => s.demo);
  const [error, setError] = useState<string | null>(null);
  const busy = demo.state !== 'idle';

  const run = async (fn: () => Promise<unknown>) => {
    setError(null);
    try {
      await fn();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  };

  return (
    <div className="absolute bottom-3 left-3 z-20 w-72 rounded-xl border border-noc-line bg-noc-panel/95 p-3 shadow-xl">
      <div className="mb-2 flex items-center justify-between text-xs">
        <span className="font-semibold text-slate-200">Demo Controls</span>
        <span className="font-mono uppercase text-slate-500">{demo.state}</span>
      </div>
      <div className="space-y-1.5">
        {SCENARIOS.map((s) => (
          <button
            key={s.id}
            type="button"
            disabled={busy}
            onClick={() => void run(() => api.inject(s.id))}
            className="flex w-full items-center justify-between rounded-lg border border-noc-line bg-noc-bg/60 px-2.5 py-2 text-left text-xs text-slate-200 hover:border-info/50 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span>{s.label}</span>
            <span className="font-mono text-slate-500">{s.hotkey}</span>
          </button>
        ))}
        <button
          type="button"
          onClick={() => void run(() => api.reset())}
          className="mt-1 w-full rounded-lg border border-warn/40 bg-warn/10 px-2.5 py-2 text-xs text-warn hover:bg-warn/20"
        >
          Reset Demo <span className="float-right font-mono opacity-70">⇧R</span>
        </button>
      </div>
      {error && <p className="mt-2 text-[11px] text-crit">{error}</p>}
    </div>
  );
}
