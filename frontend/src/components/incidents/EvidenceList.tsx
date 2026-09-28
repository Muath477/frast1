import type { Evidence } from '@/lib/types';

export function EvidenceList({
  evidence,
  firstAnomalyAt,
}: {
  evidence: Evidence[];
  firstAnomalyAt?: string;
}) {
  const t0 = firstAnomalyAt ? new Date(firstAnomalyAt).getTime() : null;
  const unique = evidence.reduce<Evidence[]>((acc, e) => {
    if (!acc.some((x) => x.entityId === e.entityId && x.metric === e.metric)) acc.push(e);
    return acc;
  }, []);

  return (
    <ul className="space-y-1.5">
      {unique.slice(0, 8).map((e) => {
        const rel =
          t0 != null ? `+${Math.max(0, Math.round((new Date(e.ts).getTime() - t0) / 1000))}s` : '';
        const pct =
          e.baseline > 0 ? Math.min(100, Math.round((e.value / Math.max(e.baseline, 1)) * 20)) : 50;
        return (
          <li
            key={e.id}
            className="rounded border border-noc-line bg-noc-bg/50 px-2 py-1.5 text-[11px]"
          >
            <div className="flex justify-between font-mono">
              <span>
                {e.entityId} · {e.metric}
              </span>
              <span className="text-slate-500">{rel}</span>
            </div>
            <div className="mt-0.5 text-slate-400">
              {e.value} vs baseline {e.baseline}
            </div>
            <div className="mt-1 h-1 overflow-hidden rounded bg-noc-line">
              <div className="h-full bg-crit/70" style={{ width: `${pct}%` }} />
            </div>
          </li>
        );
      })}
    </ul>
  );
}
