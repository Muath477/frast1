import { useEffect, useState } from 'react';
import { useOps } from '@/store/useOps';
import clsx from 'clsx';

export function TopBar() {
  const wsStatus = useOps((s) => s.wsStatus);
  const lastUpdate = useOps((s) => s.lastUpdate);
  const demo = useOps((s) => s.demo);
  const [, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const ageSec = lastUpdate ? Math.max(0, Math.round((Date.now() - lastUpdate) / 1000)) : null;
  const dot =
    wsStatus === 'open' ? 'bg-ok' : wsStatus === 'connecting' ? 'bg-warn' : 'bg-crit';

  return (
    <header className="flex items-center justify-between border-b border-noc-line bg-noc-panel px-4">
      <div className="flex items-center gap-3">
        <span className="text-lg font-semibold tracking-wide text-info">RootIQ</span>
        <span className="text-xs text-slate-400">Operations</span>
        <span
          className={clsx(
            'rounded px-1.5 py-0.5 text-[10px] uppercase tracking-wider',
            demo.mode === 'sim' ? 'bg-warn/20 text-warn' : 'bg-ok/20 text-ok',
          )}
        >
          {demo.mode}
        </span>
      </div>
      <div className="flex items-center gap-3 text-xs text-slate-400">
        <span className="flex items-center gap-1.5">
          <span className={clsx('inline-block size-2 rounded-full', dot)} />
          {wsStatus}
        </span>
        <span>{ageSec === null ? '—' : `updated ${ageSec}s ago`}</span>
      </div>
    </header>
  );
}
