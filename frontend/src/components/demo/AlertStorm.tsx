import { motion, AnimatePresence } from 'motion/react';
import { useOps } from '@/store/useOps';
import clsx from 'clsx';
import type { Incident } from '@/lib/types';

interface Props {
  incident?: Incident | null;
}

export function AlertStorm({ incident }: Props) {
  const alerts = useOps((s) => s.alerts);
  const raw = Math.max(alerts.length, incident?.rawAlertCount ?? 0);
  const hasIncident = Boolean(incident);
  const noise =
    raw > 0 && hasIncident ? Math.min(99.9, (1 - 1 / raw) * 100) : null;

  if (hasIncident) {
    return (
      <div className="rq-panel rq-panel--quiet absolute start-3 top-3 z-20 w-[360px] overflow-hidden">
        <div className="rq-slab-title">
          <span>Alert storm → one cause</span>
          {noise != null && (
            <span className="rq-metric text-[var(--brand-text)]">{noise.toFixed(1)}%</span>
          )}
        </div>
        <div className="grid grid-cols-[1fr_24px_1fr] items-stretch">
          <div className="px-3 py-3">
            <div className="rq-kicker text-[var(--crit)]">NMS</div>
            <div className="rq-metric mt-2 text-3xl text-[var(--crit)] line-through decoration-1 opacity-80">
              {raw}
            </div>
            <div className="mt-1 text-[11px] text-[var(--text-3)]">raw alerts</div>
          </div>
          <div className="flex items-center justify-center text-[var(--brand-text)]">→</div>
          <div className="border-s border-[var(--border-subtle)] px-3 py-3">
            <div className="rq-kicker text-[var(--brand-text)]">RootIQ</div>
            <div className="rq-metric mt-2 text-3xl text-[var(--brand-text)]">1</div>
            <div className="mt-1 truncate text-[11px] text-[var(--text-2)]">
              {incident?.rootCause?.label ?? 'incident'}
            </div>
          </div>
        </div>
        <ul className="max-h-36 space-y-0 overflow-y-auto border-t border-[var(--border-subtle)]">
          <AnimatePresence initial={false}>
            {alerts.slice(0, 10).map((a) => (
              <motion.li
                key={a.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className={clsx(
                  'border-b border-[var(--border-subtle)] px-3 py-1.5 font-mono text-[10px]',
                  a.severity === 'critical' ? 'text-[var(--crit)]' : 'text-[var(--warn)]',
                )}
              >
                {a.sourceId} · {a.metric}={a.value}
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>
      </div>
    );
  }

  return (
    <div className="rq-panel rq-panel--quiet absolute start-3 top-3 z-20 flex h-[42%] w-[280px] flex-col overflow-hidden">
      <div className="rq-slab-title">
        <span>Traditional NMS feed</span>
        <span className="rq-metric text-[var(--crit)]">{alerts.length}</span>
      </div>
      <ul className="flex-1 space-y-0 overflow-y-auto">
        <AnimatePresence initial={false}>
          {alerts.slice(0, 40).map((a) => (
            <motion.li
              key={a.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className={clsx(
                'border-b border-[var(--border-subtle)] px-3 py-2 font-mono text-[11px]',
                a.severity === 'critical' ? 'text-[var(--crit)]' : 'text-[var(--warn)]',
              )}
            >
              <div className="truncate">{a.sourceId}</div>
              <div className="text-[var(--text-3)]">
                {a.metric} = {a.value}
              </div>
            </motion.li>
          ))}
        </AnimatePresence>
        {alerts.length === 0 && (
          <li className="px-3 py-8 text-center text-xs text-[var(--text-3)]">
            Waiting for threshold crossings…
          </li>
        )}
      </ul>
    </div>
  );
}
