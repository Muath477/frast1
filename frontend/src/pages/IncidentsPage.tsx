import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router';
import { IncidentPanel } from '@/components/incidents/IncidentPanel';
import { useOps } from '@/store/useOps';
import type { IncidentStatus } from '@/lib/types';

const FILTERS: Array<IncidentStatus | 'all'> = [
  'all',
  'open',
  'investigating',
  'recommendation_ready',
  'awaiting_approval',
  'approved',
  'resolved',
];

export function IncidentsPage() {
  const { id } = useParams();
  const incidents = useOps((s) => s.incidents);
  const [status, setStatus] = useState<(typeof FILTERS)[number]>('all');
  const [selected, setSelected] = useState<string | null>(id ?? null);

  useEffect(() => {
    if (id) setSelected(id);
  }, [id]);

  const rows = useMemo(() => {
    const list = Object.values(incidents).sort(
      (a, b) => new Date(b.openedAt).getTime() - new Date(a.openedAt).getTime(),
    );
    return status === 'all' ? list : list.filter((i) => i.status === status);
  }, [incidents, status]);

  const active = selected ? incidents[selected] ?? null : null;

  return (
    <div className="relative flex h-full flex-col gap-3 p-4">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-lg font-semibold tracking-wide">Incidents</h1>
        <div className="flex flex-wrap gap-1">
          {FILTERS.map((f) => (
            <button
              key={f}
              type="button"
              onClick={() => setStatus(f)}
              className={
                status === f
                  ? 'rounded px-2 py-1 text-[11px] uppercase tracking-wider bg-info/20 text-info'
                  : 'rounded px-2 py-1 text-[11px] uppercase tracking-wider text-slate-500 hover:bg-white/5'
              }
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-auto rounded-xl border border-noc-line">
        <table className="w-full text-left text-sm">
          <thead className="bg-noc-panel text-[11px] uppercase tracking-wider text-slate-500">
            <tr>
              <th className="px-3 py-2 font-normal">ID</th>
              <th className="px-3 py-2 font-normal">Title</th>
              <th className="px-3 py-2 font-normal">Status</th>
              <th className="px-3 py-2 font-normal">Severity</th>
              <th className="px-3 py-2 font-normal">Opened</th>
              <th className="px-3 py-2 font-normal">Root cause</th>
              <th className="px-3 py-2 font-normal">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((i) => (
              <tr
                key={i.id}
                className="cursor-pointer border-t border-noc-line/70 hover:bg-white/[0.02]"
                onClick={() => setSelected(i.id)}
              >
                <td className="px-3 py-2 font-mono text-info">
                  <Link to={`/incidents/${i.id}`} onClick={(e) => e.stopPropagation()}>
                    {i.id}
                  </Link>
                </td>
                <td className="px-3 py-2">{i.title}</td>
                <td className="px-3 py-2 capitalize text-slate-400">{i.status.replaceAll('_', ' ')}</td>
                <td className="px-3 py-2 capitalize">{i.severity}</td>
                <td className="px-3 py-2 font-mono text-xs tabular-nums text-slate-400">
                  {new Date(i.openedAt).toLocaleString()}
                </td>
                <td className="px-3 py-2 font-mono text-xs">{i.rootCause?.entityId ?? '—'}</td>
                <td className="px-3 py-2 font-mono tabular-nums">
                  {i.rootCause?.confidence != null
                    ? `${Math.round(i.rootCause.confidence * 100)}%`
                    : '—'}
                </td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={7} className="px-3 py-8 text-center text-slate-500">
                  No incidents
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {active && (
        <div className="absolute inset-y-0 right-0 w-[420px]">
          <IncidentPanel incident={active} onClose={() => setSelected(null)} />
        </div>
      )}
    </div>
  );
}
