import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useOps } from '@/store/useOps';
import type { Focus } from '@/components/topology/DeviceNode';

type ReplayStep = {
  ts: number;
  kind: string;
  entityId?: string;
  label: string;
  value?: number | string;
};

interface Props {
  incidentId: string;
  onFocus?: (focus: Record<string, Focus>) => void;
}

export function IncidentReplay({ incidentId, onFocus }: Props) {
  const { t } = useTranslation();
  const select = useOps((s) => s.select);
  const [steps, setSteps] = useState<ReplayStep[]>([]);
  const [idx, setIdx] = useState(-1);
  const [playing, setPlaying] = useState(false);
  const timer = useRef<number | null>(null);

  useEffect(() => {
    void fetch(`/api/incidents/${incidentId}/replay`)
      .then((r) => r.json())
      .then((j: { steps: ReplayStep[] }) => setSteps(j.steps ?? []))
      .catch(() => setSteps([]));
  }, [incidentId]);

  useEffect(() => {
    if (!playing || steps.length === 0) return;
    let i = 0;
    setIdx(0);
    const tick = () => {
      const step = steps[i];
      if (!step) {
        setPlaying(false);
        onFocus?.({});
        return;
      }
      setIdx(i);
      if (step.entityId) {
        const kind = step.entityId.startsWith('link-') ? 'link' : 'node';
        select({ kind, id: step.entityId });
        onFocus?.({
          [step.entityId]: step.kind === 'root_cause' ? 'cause' : 'impact',
        });
      }
      i += 1;
      // 5×: original spacing compressed — fixed 200ms between steps
      timer.current = window.setTimeout(tick, 200);
    };
    tick();
    return () => {
      if (timer.current) window.clearTimeout(timer.current);
    };
  }, [playing, steps, select, onFocus]);

  const current = idx >= 0 ? steps[idx] : null;

  return (
    <div className="flex items-center gap-2 rounded-lg border border-noc-line bg-noc-bg/60 px-2 py-1.5">
      <button
        type="button"
        disabled={steps.length === 0 || playing}
        onClick={() => setPlaying(true)}
        className="rounded bg-info/20 px-2 py-1 text-xs text-info disabled:opacity-40"
      >
        ▶ {t('incident.replay')} 5×
      </button>
      {current && (
        <span className="truncate font-mono text-[11px] text-slate-400">
          <bdi>
            {current.label}
            {current.value != null ? ` = ${current.value}` : ''}
          </bdi>
        </span>
      )}
      <span className="ms-auto font-mono text-[10px] text-slate-500">
        {idx >= 0 ? `${idx + 1}/${steps.length}` : `${steps.length} steps`}
      </span>
    </div>
  );
}
