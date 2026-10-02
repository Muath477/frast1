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
    <div className="absolute left-1/2 top-16 z-30 -translate-x-1/2">
      <div
        className={clsx(
          'rq-panel px-8 py-3 text-center',
          frozen ? (underTarget ? 'rq-panel--ok' : 'rq-panel--warn') : 'rq-panel--quiet',
        )}
      >
        <div className="rq-kicker">Time to root cause</div>
        <div
          className={clsx(
            'rq-stopwatch mt-1',
            frozen ? (underTarget ? 'text-ok' : 'text-warn') : 'text-[var(--brand-text)]',
          )}
        >
          {seconds.toFixed(1)}
          <span className="ms-1 text-lg font-normal opacity-70">s</span>
        </div>
        {frozen ? (
          <div className={clsx('mt-1 text-[11px]', underTarget ? 'text-ok' : 'text-warn')}>
            target &lt; 60s
          </div>
        ) : (
          <div className="mt-1 text-[11px] text-[var(--text-3)]">detecting…</div>
        )}
      </div>
    </div>
  );
}
