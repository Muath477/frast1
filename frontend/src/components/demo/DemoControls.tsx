import { useState } from 'react';
import { api, type Scenario } from '@/lib/api';
import { useOps } from '@/store/useOps';

const SCENARIOS: { id: Scenario; label: string; hotkey: string }[] = [
  { id: 'uplink-congestion', label: 'Uplink congestion', hotkey: '⇧1' },
  { id: 'dns-failure', label: 'DNS failure', hotkey: '⇧2' },
  { id: 'server-spike', label: 'Server spike', hotkey: '⇧3' },
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
    <div className="rq-panel rq-panel--quiet absolute bottom-3 start-3 z-20 w-[300px]">
      <div className="rq-slab-title">
        <span>Inject</span>
        <span className="rq-mono !normal-case !tracking-normal text-[var(--text-2)]">{demo.state}</span>
      </div>
      <div className="flex flex-col">
        {SCENARIOS.map((s) => (
          <button
            key={s.id}
            type="button"
            disabled={busy}
            onClick={() => void run(() => api.inject(s.id))}
            className="flex w-full items-center justify-between border-b border-[var(--border-subtle)] px-3 py-2.5 text-start text-xs text-[var(--text-1)] hover:bg-[var(--bg-hover)] disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span>{s.label}</span>
            <kbd className="rq-mono text-[10px] text-[var(--text-3)]">{s.hotkey}</kbd>
          </button>
        ))}
        <button
          type="button"
          onClick={() => void run(() => api.reset())}
          className="flex w-full items-center justify-between px-3 py-2.5 text-start text-xs text-[var(--warn)] hover:bg-[var(--warn-soft)]"
        >
          <span>Reset demo</span>
          <kbd className="rq-mono text-[10px]">⇧R</kbd>
        </button>
      </div>
      {error && <p className="border-t border-[var(--border-subtle)] px-3 py-2 text-[11px] text-crit">{error}</p>}
    </div>
  );
}
