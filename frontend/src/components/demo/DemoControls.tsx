import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { FlaskConical, Play, RotateCcw } from 'lucide-react';
import { api, type Scenario } from '@/lib/api';
import { useOps } from '@/store/useOps';

const SCENARIOS: Scenario[] = ['uplink-congestion', 'dns-failure', 'server-spike'];

export function DemoControls() {
  const { t } = useTranslation();
  const demo = useOps((s) => s.demo);
  const [scenario, setScenario] = useState<Scenario>('uplink-congestion');
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
    <div className="absolute start-3 top-3 z-20 max-w-[min(100%-1.5rem,420px)]">
      <div className="rq-panel rq-panel--quiet border border-[var(--border)] bg-[var(--bg-panel)]/95 shadow-lg backdrop-blur-sm">
        <div className="rq-slab-title gap-2 px-3 py-2">
          <span className="inline-flex items-center gap-1.5">
            <FlaskConical size={13} className="text-[var(--brand)]" />
            {t('demo.title')}
          </span>
          <span className="rq-mono !normal-case !tracking-normal text-[var(--text-2)]">
            {demo.scenario ? `${demo.scenario} · ${demo.state}` : demo.state}
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-2 px-3 pb-3">
          <label className="sr-only" htmlFor="demo-scenario">
            {t('demo.pick')}
          </label>
          <select
            id="demo-scenario"
            value={scenario}
            disabled={busy}
            onChange={(e) => setScenario(e.target.value as Scenario)}
            className="min-w-0 flex-1 border border-[var(--border)] bg-[var(--bg-canvas)] px-2.5 py-2 text-xs text-[var(--text-1)] outline-none focus:border-[var(--brand)] disabled:opacity-40"
          >
            {SCENARIOS.map((id) => (
              <option key={id} value={id}>
                {t(`demo.scenario.${id}`)}
              </option>
            ))}
          </select>

          <button
            type="button"
            disabled={busy}
            onClick={() => void run(() => api.inject(scenario))}
            className="rq-btn-primary inline-flex items-center gap-1.5 px-3 py-2 text-xs disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Play size={13} />
            {t('demo.run')}
          </button>

          <button
            type="button"
            onClick={() => void run(() => api.reset())}
            className="rq-btn-secondary inline-flex items-center gap-1.5 px-3 py-2 text-xs text-[var(--warn)]"
            title={t('demo.reset')}
          >
            <RotateCcw size={13} />
            {t('demo.reset')}
          </button>
        </div>

        {error && (
          <p className="border-t border-[var(--border-subtle)] px-3 py-2 text-[11px] text-crit">{error}</p>
        )}
      </div>
    </div>
  );
}
