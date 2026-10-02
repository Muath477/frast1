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
        'rq-float absolute left-1/2 top-3 z-30 -translate-x-1/2 px-6 py-3 text-center',
        frozen
          ? underTarget
            ? 'border-[color:var(--ok)]'
            : 'border-[color:var(--warn)]'
          : 'border-[color:var(--brand)]',
      )}
    >
      <div className="text-[length:var(--fs-2xs)] text-[var(--text-3)]">MTTD Stopwatch</div>
      <div
        className={clsx(
          'rq-stopwatch',
          frozen ? (underTarget ? 'text-ok' : 'text-warn') : 'text-[var(--brand-text)]',
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
        <div className="mt-1 text-xs text-[var(--text-3)]">Detecting…</div>
      )}
    </div>
  );
}
