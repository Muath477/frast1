import { STATUS_COLOR } from '@/lib/colors';
import type { Health } from '@/lib/types';

export function AffectedServices({
  services,
  statuses,
}: {
  services: string[];
  statuses?: Record<string, Health>;
}) {
  if (!services.length) return <p className="text-xs text-slate-500">None yet</p>;
  return (
    <div className="flex flex-wrap gap-1.5">
      {services.map((id) => {
        const st = statuses?.[id] ?? 'degraded';
        return (
          <span
            key={id}
            className="rounded-full border px-2 py-0.5 text-[11px]"
            style={{ borderColor: STATUS_COLOR[st], color: STATUS_COLOR[st] }}
          >
            {id}
          </span>
        );
      })}
    </div>
  );
}
