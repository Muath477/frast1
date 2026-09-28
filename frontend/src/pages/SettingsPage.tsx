import { useEffect, useState } from 'react';
import { useOps } from '@/store/useOps';
import { api } from '@/lib/api';
import clsx from 'clsx';

const KEY = 'rootiq.engineer';

export function SettingsPage() {
  const [name, setName] = useState('Ahmed');
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const demo = useOps((s) => s.demo);

  useEffect(() => {
    setName(localStorage.getItem(KEY) || 'Ahmed');
  }, []);

  const setMode = async (mode: 'live' | 'sim') => {
    setBusy(true);
    setMsg(null);
    try {
      await api.setMode(mode);
      setMsg(
        mode === 'sim'
          ? 'Switched to SIMULATION — continue the demo (badge shows SIMULATION).'
          : 'Switched to LIVE LAB — ensure collector/agent are healthy.',
      );
    } catch (e) {
      setMsg(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg space-y-6 p-6">
      <h1 className="text-lg font-semibold">Settings</h1>
      <label className="block text-sm">
        <span className="text-slate-400">Engineer name (for Approve / Reject)</span>
        <input
          value={name}
          onChange={(e) => {
            setName(e.target.value);
            localStorage.setItem(KEY, e.target.value);
          }}
          className="mt-1 w-full rounded-lg border border-noc-line bg-noc-panel px-3 py-2 outline-none focus:border-info"
        />
      </label>

      <section className="space-y-3 rounded-lg border border-noc-line bg-noc-panel/60 p-4">
        <h2 className="text-sm font-semibold">Demo failover</h2>
        <p className="text-xs text-slate-500">
          If EVE-NG stalls mid-pitch: Presenter says «Let me switch to our recorded lab feed» →
          switch to Simulation here (or click the TopBar badge). Badge must show{' '}
          <span className="font-semibold text-info">SIMULATION</span>.
        </p>
        <div className="flex items-center gap-2">
          <span
            className={clsx(
              'rounded px-2 py-1 text-[10px] font-semibold uppercase tracking-wider',
              demo.mode === 'live' ? 'bg-ok/20 text-ok' : 'bg-info/20 text-info',
            )}
          >
            {demo.mode === 'live' ? 'LIVE LAB' : 'SIMULATION'}
          </span>
          <button
            type="button"
            disabled={busy || demo.mode === 'sim'}
            onClick={() => void setMode('sim')}
            className="rounded-lg bg-info/90 px-3 py-1.5 text-xs font-semibold text-black disabled:opacity-40"
          >
            Use Simulation feed
          </button>
          <button
            type="button"
            disabled={busy || demo.mode === 'live'}
            onClick={() => void setMode('live')}
            className="rounded-lg border border-noc-line px-3 py-1.5 text-xs text-slate-300 disabled:opacity-40"
          >
            Use Live lab
          </button>
        </div>
        {msg && <p className="text-[11px] text-slate-400">{msg}</p>}
      </section>
    </div>
  );
}
