import type { ReactNode } from 'react';
import type { Service, TopoNode } from '@/lib/types';
import { STATUS_COLOR } from '@/lib/colors';
import { X } from 'lucide-react';

interface Props {
  device: TopoNode;
  services: Service[];
  onClose: () => void;
}

export function DeviceInspector({ device, services, onClose }: Props) {
  const hosted = services.filter((s) => s.host === device.id);

  return (
    <aside className="absolute right-0 top-0 z-10 flex h-full w-[360px] flex-col border-l border-noc-line bg-noc-panel/98 shadow-xl">
      <header className="flex items-center justify-between border-b border-noc-line px-4 py-3">
        <div>
          <div className="text-xs uppercase tracking-wider text-slate-500">{device.type}</div>
          <div className="font-semibold">{device.label}</div>
        </div>
        <button type="button" onClick={onClose} className="rounded p-1 text-slate-400 hover:bg-white/5 hover:text-white">
          <X size={18} />
        </button>
      </header>

      <div className="flex-1 space-y-4 overflow-y-auto p-4 text-sm">
        <Row label="Vendor" value={device.vendor ?? '—'} />
        <Row label="Management IP" value={device.managementIp} mono />
        <Row
          label="Status"
          value={
            <span style={{ color: STATUS_COLOR[device.status] }} className="capitalize">
              {device.status}
            </span>
          }
        />

        <section>
          <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">Interfaces</h3>
          <table className="w-full text-left text-xs">
            <thead className="text-slate-500">
              <tr>
                <th className="pb-1 font-normal">Name</th>
                <th className="pb-1 font-normal">Side</th>
                <th className="pb-1 font-normal">Speed</th>
                <th className="pb-1 font-normal">State</th>
              </tr>
            </thead>
            <tbody className="font-mono">
              {device.interfaces.map((i) => (
                <tr key={i.name} className="border-t border-noc-line/60">
                  <td className="py-1.5">{i.name}</td>
                  <td className="py-1.5 text-slate-400">{i.side}</td>
                  <td className="py-1.5">{i.speedMbps}</td>
                  <td className="py-1.5 capitalize">{i.operState ?? 'up'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section>
          <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">Hosted services</h3>
          {hosted.length === 0 ? (
            <p className="text-slate-500">None</p>
          ) : (
            <ul className="space-y-1">
              {hosted.map((s) => (
                <li key={s.id} className="flex justify-between">
                  <span>{s.label}</span>
                  <span className="font-mono text-slate-400">:{s.port}</span>
                </li>
              ))}
            </ul>
          )}
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
