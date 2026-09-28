import { useMemo, useState } from 'react';
import { STATUS_COLOR } from '@/lib/colors';
import { useOps } from '@/store/useOps';

export function DevicesPage() {
  const topology = useOps((s) => s.topology);
  const [q, setQ] = useState('');

  const rows = useMemo(() => {
    if (!topology) return [];
    const needle = q.trim().toLowerCase();
    return topology.nodes.filter((n) => {
      if (!needle) return true;
      return (
        n.label.toLowerCase().includes(needle) ||
        n.id.toLowerCase().includes(needle) ||
        n.managementIp.includes(needle) ||
        n.type.includes(needle)
      );
    });
  }, [topology, q]);

  if (!topology) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">Loading devices…</div>
    );
  }

  return (
    <div className="flex h-full flex-col gap-3 p-4">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-lg font-semibold tracking-wide">Devices</h1>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search name, IP, type…"
          className="w-72 rounded-lg border border-noc-line bg-noc-bg px-3 py-1.5 text-sm outline-none focus:border-info"
        />
      </div>
      <div className="overflow-auto rounded-xl border border-noc-line">
        <table className="w-full text-left text-sm">
          <thead className="bg-noc-panel text-[11px] uppercase tracking-wider text-slate-500">
            <tr>
              <th className="px-3 py-2 font-normal">Name</th>
              <th className="px-3 py-2 font-normal">Type</th>
              <th className="px-3 py-2 font-normal">IP</th>
              <th className="px-3 py-2 font-normal">Status</th>
              <th className="px-3 py-2 font-normal">CPU</th>
              <th className="px-3 py-2 font-normal">Ports</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((n) => {
              const cpu = n.metrics?.cpu_percent;
              return (
                <tr key={n.id} className="border-t border-noc-line/70 hover:bg-white/[0.02]">
                  <td className="px-3 py-2 font-medium">{n.label}</td>
                  <td className="px-3 py-2 capitalize text-slate-400">{n.type}</td>
                  <td className="px-3 py-2 font-mono tabular-nums">{n.managementIp}</td>
                  <td className="px-3 py-2">
                    <span className="capitalize" style={{ color: STATUS_COLOR[n.status] }}>
                      {n.status}
                    </span>
                  </td>
                  <td className="px-3 py-2 font-mono tabular-nums text-slate-300">
                    {cpu != null ? `${Math.round(cpu)}%` : '—'}
                  </td>
                  <td className="px-3 py-2 font-mono tabular-nums">{n.interfaces.length}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="text-xs text-slate-500">{rows.length} / {topology.nodes.length} devices</div>
    </div>
  );
}
