import { useOps } from '@/store/useOps';

export function KpiStrip() {
  const topology = useOps((s) => s.topology);
  const incidents = useOps((s) => s.incidents);
  if (!topology) return null;
  const all = [...topology.nodes, ...topology.links, ...topology.services];
  const healthy = all.filter((x) => x.status === 'healthy').length;
  const active = Object.values(incidents).filter((i) => i.status !== 'resolved').length;
  const cards = [
    { label: 'Infra Health', value: `${Math.round((100 * healthy) / Math.max(all.length, 1))}%` },
    { label: 'Active Incidents', value: String(active) },
    {
      label: 'Devices Online',
      value: String(topology.nodes.filter((n) => n.status !== 'unknown').length),
    },
    {
      label: 'Services Affected',
      value: String(topology.services.filter((s) => s.status !== 'healthy').length),
    },
    { label: 'MTTD', value: '—' },
    { label: 'MTTR', value: '—' },
  ];
  return (
    <div className="grid grid-cols-6 gap-2 border-b border-noc-line bg-noc-panel/80 px-3 py-2">
      {cards.map((c) => (
        <div key={c.label} className="rounded-lg border border-noc-line bg-noc-bg/40 px-2 py-1.5">
          <div className="text-[10px] uppercase tracking-wider text-slate-500">{c.label}</div>
          <div className="font-mono text-lg tabular-nums">{c.value}</div>
        </div>
      ))}
    </div>
  );
}
