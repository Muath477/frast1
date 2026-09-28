import { useState } from 'react';

interface Props {
  onCancel: () => void;
  onConfirm: (reason: string) => void;
}

export function RejectDialog({ onCancel, onConfirm }: Props) {
  const [reason, setReason] = useState('');
  const ok = reason.trim().length >= 5;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-xl border border-noc-line bg-noc-panel p-4 shadow-2xl">
        <h3 className="text-sm font-semibold">Reject remediation</h3>
        <p className="mt-1 text-xs text-slate-500">Reason is required (min 5 characters).</p>
        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Outside change window"
          rows={3}
          className="mt-3 w-full rounded-lg border border-noc-line bg-noc-bg px-3 py-2 text-sm outline-none focus:border-info"
        />
        <div className="mt-3 flex justify-end gap-2">
          <button
            type="button"
            onClick={onCancel}
            className="rounded-lg px-3 py-1.5 text-xs text-slate-400 hover:bg-white/5"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={!ok}
            onClick={() => onConfirm(reason.trim())}
            className="rounded-lg bg-crit/90 px-3 py-1.5 text-xs font-semibold text-white disabled:opacity-40"
          >
            Confirm reject
          </button>
        </div>
      </div>
    </div>
  );
}
