import { useEffect, useState } from 'react';
import clsx from 'clsx';

interface Props {
  injectedAt?: string | null;
  analyzedAt?: string | null;
}

export function MttdStopwatch({ injectedAt, analyzedAt }: Props) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!injectedAt || analyzedAt) return;
    let raf = 0;
    const tick = () => {
      setNow(Date.now());
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [injectedAt, analyzedAt]);

  if (!injectedAt) return null;

  const start = new Date(injectedAt).getTime();
  const end = analyzedAt ? new Date(analyzedAt).getTime() : now;
  const seconds = Math.max(0, (end - start) / 1000);
  const frozen = Boolean(analyzedAt);
  const underTarget = seconds < 60;

  return (
    <div
      className={clsx(
        'absolute left-1/2 top-3 z-30 -translate-x-1/2 rounded-2xl border px-6 py-3 text-center shadow-2xl',
        frozen
          ? underTarget
            ? 'border-ok/50 bg-ok/15'
            : 'border-warn/50 bg-warn/15'
          : 'border-info/50 bg-noc-panel/95',
      )}
    >
      <div className="text-[10px] uppercase tracking-[0.2em] text-slate-400">MTTD Stopwatch</div>
      <div
        className={clsx(
          'font-mono text-4xl font-bold tabular-nums',
          frozen ? (underTarget ? 'text-ok' : 'text-warn') : 'text-info',
        )}
      >
        {seconds.toFixed(1)}
        <span className="text-lg">s</span>
      </div>
      {frozen ? (
        <div className={clsx('mt-1 text-xs', underTarget ? 'text-ok' : 'text-warn')}>
          Root cause in {seconds.toFixed(1)} s · target &lt; 60 s
        </div>
      ) : (
        <div className="mt-1 text-xs text-slate-500">Detecting…</div>
      )}
    </div>
  );
}
