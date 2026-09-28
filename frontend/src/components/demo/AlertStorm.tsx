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
      <div className="absolute left-3 top-3 z-20 w-[340px] overflow-hidden rounded-xl border border-noc-line bg-noc-panel/95 shadow-xl">
        <div className="grid grid-cols-[1fr_auto_1fr] gap-1 p-3">
          <div className="rounded-lg border border-crit/30 bg-crit/10 p-2">
            <div className="text-[10px] uppercase tracking-wider text-crit/80">Traditional NMS</div>
            <div className="font-mono text-3xl font-bold tabular-nums text-crit">{raw}</div>
            <div className="text-[11px] text-slate-400">alerts</div>
          </div>
          <div className="flex items-center justify-center px-1">
            <motion.span
              animate={{ x: [0, 6, 0] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
              className="text-xl text-info"
            >
              →
            </motion.span>
          </div>
          <div className="rounded-lg border border-ok/30 bg-ok/10 p-2">
            <div className="text-[10px] uppercase tracking-wider text-ok/80">RootIQ</div>
            <div className="font-mono text-3xl font-bold tabular-nums text-ok">1</div>
            <div className="truncate text-[11px] text-slate-300">
              {incident?.rootCause?.label ?? 'incident'}
            </div>
          </div>
        </div>
        {noise != null && (
          <div className="border-t border-noc-line bg-noc-bg/60 px-3 py-2 text-center">
            <span className="text-[10px] uppercase tracking-wider text-slate-500">
              Noise reduction
            </span>
            <div className="font-mono text-2xl tabular-nums text-info">{noise.toFixed(1)}%</div>
          </div>
        )}
        <ul className="max-h-40 space-y-1 overflow-y-auto border-t border-noc-line p-2">
          <AnimatePresence initial={false}>
            {alerts.slice(0, 12).map((a) => (
              <motion.li
                key={a.id}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                className={clsx(
                  'rounded-md border px-2 py-1 font-mono text-[10px]',
                  a.severity === 'critical'
                    ? 'border-crit/40 bg-crit/10 text-crit'
                    : 'border-warn/40 bg-warn/10 text-warn',
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
    <div className="absolute left-3 top-3 z-20 flex h-[45%] w-[260px] flex-col overflow-hidden rounded-xl border border-noc-line bg-noc-panel/95 shadow-xl">
      <header className="border-b border-noc-line px-3 py-2">
        <div className="text-[10px] uppercase tracking-wider text-slate-500">
          What a traditional NMS shows you
        </div>
        <div className="mt-1 flex items-baseline justify-between">
          <span className="text-sm font-semibold">Raw alerts</span>
          <span className="font-mono text-2xl tabular-nums text-crit">{alerts.length}</span>
        </div>
      </header>
      <ul className="flex-1 space-y-1 overflow-y-auto p-2">
        <AnimatePresence initial={false}>
          {alerts.slice(0, 40).map((a) => (
            <motion.li
              key={a.id}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0 }}
              className={clsx(
                'rounded-md border px-2 py-1.5 font-mono text-[11px]',
                a.severity === 'critical'
                  ? 'border-crit/40 bg-crit/10 text-crit'
                  : 'border-warn/40 bg-warn/10 text-warn',
              )}
            >
              <div className="truncate">{a.sourceId}</div>
              <div className="text-slate-400">
                {a.metric} = {a.value}
              </div>
            </motion.li>
          ))}
        </AnimatePresence>
        {alerts.length === 0 && (
          <li className="px-2 py-6 text-center text-xs text-slate-500">
            Waiting for threshold crossings…
          </li>
        )}
      </ul>
    </div>
  );
}
