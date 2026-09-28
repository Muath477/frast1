import { useEffect, useState } from 'react';

interface Entry {
  ts: string;
  actor: string;
  action: string;
  target: string;
  detail: Record<string, unknown>;
}

export function AuditPage() {
  const [rows, setRows] = useState<Entry[]>([]);

  useEffect(() => {
    const load = () => {
      void fetch('/api/audit')
        .then((r) => (r.ok ? r.json() : []))
        .then(setRows)
        .catch(() => undefined);
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="h-full overflow-auto p-4">
      <h1 className="mb-3 text-lg font-semibold">Audit log</h1>
      <table className="w-full text-left text-xs">
        <thead className="text-slate-500">
          <tr>
            <th className="pb-2 font-normal">Time</th>
            <th className="pb-2 font-normal">Actor</th>
            <th className="pb-2 font-normal">Action</th>
            <th className="pb-2 font-normal">Target</th>
            <th className="pb-2 font-normal">Detail</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={`${r.ts}-${i}`} className="border-t border-noc-line/60 font-mono">
              <td className="py-1.5 pr-2 text-slate-400">{r.ts.slice(11, 19)}</td>
              <td className="py-1.5 pr-2">{r.actor}</td>
              <td className="py-1.5 pr-2 text-info">{r.action}</td>
              <td className="py-1.5 pr-2">{r.target}</td>
              <td className="py-1.5 text-slate-500">{JSON.stringify(r.detail)}</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={5} className="py-8 text-center text-slate-500">
                No audit entries yet
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
