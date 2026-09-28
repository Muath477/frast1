import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import type { Incident, IncidentStatus } from '@/lib/types';
import clsx from 'clsx';
import { ConfidenceRing } from './ConfidenceRing';
import { CandidateRanking } from './CandidateRanking';
import { EvidenceList } from './EvidenceList';
import { AffectedServices } from './AffectedServices';
import { ActionCard } from './ActionCard';

const STEPS: IncidentStatus[] = [
  'open',
  'investigating',
  'recommendation_ready',
  'awaiting_approval',
  'approved',
  'resolved',
];

interface Props {
  incident: Incident | null;
  onClose?: () => void;
}

export function IncidentPanel({ incident, onClose }: Props) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const elapsed = useMemo(() => {
    if (!incident) return '00:00';
    const ms = now - new Date(incident.openedAt).getTime();
    const s = Math.max(0, Math.floor(ms / 1000));
    return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  }, [incident, now]);

  const conf = incident?.rootCause?.confidence ?? 0;

  return (
    <AnimatePresence>
      {incident && (
        <motion.aside
          initial={{ x: 40, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 40, opacity: 0 }}
          className="absolute right-0 top-0 z-20 flex h-full w-[420px] flex-col border-l border-noc-line bg-noc-panel/98 shadow-2xl"
        >
          <header className="border-b border-noc-line px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="font-mono text-sm text-info">{incident.id}</div>
              <div className="flex items-center gap-2">
                <span
                  className={clsx(
                    'rounded px-1.5 py-0.5 text-[10px] uppercase',
                    incident.severity === 'critical' || incident.severity === 'high'
                      ? 'bg-crit/20 text-crit'
                      : 'bg-warn/20 text-warn',
                  )}
                >
                  {incident.severity}
                </span>
                <span className="font-mono text-lg tabular-nums">{elapsed}</span>
                {onClose && (
                  <button type="button" onClick={onClose} className="text-slate-500 hover:text-white">
                    ✕
                  </button>
                )}
              </div>
            </div>
            <h2 className="mt-1 text-base font-semibold">{incident.title}</h2>
          </header>

          <div className="flex gap-1 overflow-x-auto border-b border-noc-line px-3 py-2">
            {STEPS.map((step) => {
              const idx = STEPS.indexOf(step);
              const cur = STEPS.indexOf(
                incident.status === 'rejected' ? 'awaiting_approval' : incident.status,
              );
              return (
                <div
                  key={step}
                  className={clsx(
                    'rounded px-1.5 py-1 text-[9px] uppercase tracking-wide',
                    idx <= cur ? 'bg-info/20 text-info' : 'text-slate-600',
                  )}
                >
                  {step.replaceAll('_', ' ')}
                </div>
              );
            })}
          </div>

          <div className="flex-1 space-y-4 overflow-y-auto p-4 text-sm">
            {incident.rootCause ? (
              <section className="flex items-start gap-3">
                <ConfidenceRing value={conf} />
                <div className="min-w-0 flex-1">
                  <div className="text-xs uppercase tracking-wider text-slate-500">
                    Root cause ·{" "}
                    {incident.rootCause.entityId.startsWith("link-")
                      ? "Network"
                      : incident.rootCause.entityId === "svc-dns"
                        ? "DNS"
                        : "Server"}
                  </div>
                  <div className="font-semibold text-crit">{incident.rootCause.label}</div>
                  <div className="font-mono text-[11px] text-slate-400">
                    {incident.rootCause.entityId}
                  </div>
                  {incident.needsInvestigation && (
                    <div className="mt-2 rounded border border-warn/40 bg-warn/10 px-2 py-1 text-[11px] text-warn">
                      Low confidence — more investigation required
                    </div>
                  )}
                </div>
              </section>
            ) : (
              <section>
                <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">Root cause</h3>
                <p className="text-slate-500">Analyzing…</p>
              </section>
            )}

            {incident.candidates?.length > 0 && (
              <section>
                <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">
                  Why this cause?
                </h3>
                <CandidateRanking candidates={incident.candidates} />
              </section>
            )}

            {incident.explanation && (
              <section>
                <h3 className="mb-1 text-xs uppercase tracking-wider text-slate-500">
                  Explanation{' '}
                  <span className="normal-case text-slate-600">· {incident.explanation.source}</span>
                </h3>
                <p className="text-xs leading-relaxed text-slate-300">{incident.explanation.en}</p>
              </section>
            )}

            <section>
              <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">
                Evidence
              </h3>
              <EvidenceList
                evidence={incident.evidence}
                firstAnomalyAt={incident.timings.firstAnomalyAt}
              />
            </section>

            <section>
              <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">
                Affected services
              </h3>
              <AffectedServices services={incident.affectedServices} />
            </section>

            <section>
              <h3 className="mb-2 text-xs uppercase tracking-wider text-slate-500">
                Recommended action
              </h3>
              {incident.action ? (
                <ActionCard
                  action={incident.action}
                  engineer={
                    typeof window !== 'undefined'
                      ? localStorage.getItem('rootiq.engineer') || 'Ahmed'
                      : 'Ahmed'
                  }
                  incidentStatus={incident.status}
                  needsInvestigation={incident.needsInvestigation}
                />
              ) : (
                <p className="text-slate-500">Waiting for recommendation…</p>
              )}
            </section>

            <div className="rounded-lg border border-ok/30 bg-ok/10 px-3 py-2 text-xs text-ok">
              Noise reduction:{' '}
              <span className="font-mono text-base">
                {incident.rawAlertCount > 0
                  ? `${Math.min(99, Math.round((1 - 1 / Math.max(incident.rawAlertCount, 1)) * 100))}%`
                  : '—'}
              </span>{' '}
              ({incident.rawAlertCount} alerts → 1 incident)
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
