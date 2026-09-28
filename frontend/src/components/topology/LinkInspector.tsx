import type { ReactNode } from 'react';
import type { TopoLink } from '@/lib/types';
import { STATUS_COLOR } from '@/lib/colors';
import { X } from 'lucide-react';

interface Props {
  link: TopoLink;
  sourceLabel: string;
  targetLabel: string;
  onClose: () => void;
}

export function LinkInspector({ link, sourceLabel, targetLabel, onClose }: Props) {
  return (
    <aside className="absolute right-0 top-0 z-10 flex h-full w-[360px] flex-col border-l border-noc-line bg-noc-panel/98 shadow-xl">
      <header className="flex items-center justify-between border-b border-noc-line px-4 py-3">
        <div>
          <div className="text-xs uppercase tracking-wider text-slate-500">Link</div>
          <div className="font-semibold">{link.id}</div>
        </div>
        <button type="button" onClick={onClose} className="rounded p-1 text-slate-400 hover:bg-white/5 hover:text-white">
          <X size={18} />
        </button>
      </header>

      <div className="flex-1 space-y-4 overflow-y-auto p-4 text-sm">
        <Row label="Endpoints" value={`${sourceLabel} → ${targetLabel}`} />
        <Row label="Ports" value={`${link.sourcePort} ⇄ ${link.targetPort}`} mono />
        <Row label="Role" value={link.role} />
        <Row label="Speed" value={`${link.speedMbps} Mbps`} />
        <Row
          label="Status"
          value={
            <span style={{ color: STATUS_COLOR[link.status] }} className="capitalize">
              {link.status}
            </span>
          }
        />
        <Row label="Utilization" value={`${link.utilization.toFixed(1)}%`} />
        <Row label="Latency" value={`${link.latencyMs.toFixed(1)} ms`} />
        <Row label="Packet loss" value={`${link.packetLoss.toFixed(2)}%`} />

        <section>
          <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">Recent events</h3>
          <p className="text-slate-500">No events yet — Day 3+</p>
        </section>
      </div>
    </aside>
  );
}

function Row({
  label,
  value,
  mono,
}: {
  label: string;
  value: ReactNode;
  mono?: boolean;
}) {
  return (
    <div className="flex items-start justify-between gap-3">
      <span className="text-slate-500">{label}</span>
      <span className={mono ? 'font-mono text-right' : 'text-right'}>{value}</span>
    </div>
  );
}
