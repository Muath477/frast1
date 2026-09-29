import { useState } from 'react';
import type { VendorCommands, VendorDiagnose } from '@/lib/types';

function DeviceBlock({ d, label }: { d: VendorDiagnose; label: string }) {
  const usable = d.checks.filter((c) => c.available);
  return (
    <div className="rounded border border-noc-line/60 px-2 py-1.5">
      <p className="text-slate-300">
        <span className="font-semibold">{label}</span>
        {d.interface && <span className="ms-1 font-mono text-[10px] text-slate-500">{d.interface}</span>}
        <span className="ms-2 text-slate-500">
          {d.vendor ? `${d.vendor}${d.os ? ` / ${d.os}` : ''}` : 'vendor not identified'}
        </span>
      </p>
      {usable.length === 0 && <p className="text-slate-500">{d.note || 'No curated commands for this vendor yet.'}</p>}
      <ul className="mt-1 space-y-1">
        {usable.map((c) => (
          <li key={c.capability}>
            <span className="text-slate-500">{c.why}</span>
            {c.commands.map((cmd) => (
              <code key={cmd} className="block break-all text-[10px] text-info">
                {cmd}
              </code>
            ))}
          </li>
        ))}
      </ul>
    </div>
  );
}

/** Vendor-specific reference commands for the devices involved. Read-only; RootIQ does not run them. */
export function VendorCommandsView({ vc }: { vc: VendorCommands }) {
  const [open, setOpen] = useState(false);
  const labels = Object.fromEntries(vc.devices.map((d) => [d.id, d.label]));
  return (
    <div className="rounded border border-noc-line/60 bg-noc-bg/30" data-testid="vendor-commands">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-center justify-between px-2 py-1 text-start text-violet-300 hover:bg-white/5"
      >
        <span>
          Vendor diagnostics · {vc.title} · {vc.diagnose.length} device(s)
        </span>
        <span aria-hidden>{open ? '▾' : '▸'}</span>
      </button>
      {open && (
        <div className="space-y-1.5 border-t border-noc-line/60 px-2 py-2">
          {vc.diagnose.map((d) => (
            <DeviceBlock key={d.device} d={d} label={labels[d.device] ?? d.device} />
          ))}
          {vc.fixes
            .filter((f) => f.commands.length > 0)
            .map((f) => (
              <p key={f.id} className="text-warn">
                Fix option (needs approval): {f.title}
              </p>
            ))}
          <p className="text-slate-500">{vc.note}</p>
        </div>
      )}
    </div>
  );
}
