import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useOps } from '@/store/useOps';
import { api } from '@/lib/api';
import clsx from 'clsx';

export function TopBar() {
  const { t, i18n } = useTranslation();
  const wsStatus = useOps((s) => s.wsStatus);
  const lastUpdate = useOps((s) => s.lastUpdate);
  const demo = useOps((s) => s.demo);
  const [, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((x) => x + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const ageSec = lastUpdate ? Math.max(0, Math.round((Date.now() - lastUpdate) / 1000)) : null;
  const dot =
    wsStatus === 'open' ? 'bg-ok' : wsStatus === 'connecting' ? 'bg-warn' : 'bg-crit';

  const toggleLang = () => {
    void i18n.changeLanguage(i18n.language === 'ar' ? 'en' : 'ar');
  };

  const toggleMode = () => {
    void api.setMode(demo.mode === 'sim' ? 'live' : 'sim').catch(console.error);
  };

  return (
    <header className="flex items-center justify-between border-b border-noc-line bg-noc-panel px-4">
      <div className="flex items-center gap-3">
        <span className="text-lg font-semibold tracking-wide text-info">{t('appName')}</span>
        <span className="text-xs text-slate-400">{t('topbar.operations')}</span>
        <button
          type="button"
          onClick={toggleMode}
          title="Hot-switch mode"
          className={clsx(
            'rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider',
            demo.mode === 'live' ? 'animate-pulse bg-ok/20 text-ok' : 'bg-info/20 text-info',
          )}
        >
          {demo.mode === 'live' ? t('topbar.live') : t('topbar.sim')}
        </button>
      </div>
      <div className="flex items-center gap-3 text-xs text-slate-400">
        <span className="flex items-center gap-1.5">
          <span className={clsx('inline-block size-2 rounded-full', dot)} />
          <bdi>{wsStatus}</bdi>
        </span>
        <span>
          {ageSec === null ? '—' : t('topbar.lastUpdate', { sec: ageSec })}
        </span>
        <button
          type="button"
          onClick={toggleLang}
          className="rounded px-1.5 py-0.5 text-[10px] uppercase tracking-wider text-slate-300 hover:bg-white/5"
        >
          {i18n.language === 'ar' ? 'EN' : 'ع'}
        </button>
      </div>
    </header>
  );
}
