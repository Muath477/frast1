import {
  BaseEdge,
  EdgeLabelRenderer,
  getSmoothStepPath,
  type Edge,
  type EdgeProps,
} from '@xyflow/react';
import type { TopoLink } from '@/lib/types';
import { CAUSE_COLOR, IMPACT_COLOR, STATUS_COLOR } from '@/lib/colors';
import type { Focus } from './DeviceNode';

export type PortEdgeT = Edge<{ link: TopoLink; focus: Focus }, 'port'>;

export function PortEdge(p: EdgeProps<PortEdgeT>) {
  const [path, lx, ly] = getSmoothStepPath({ ...p, borderRadius: 18 });
  const link = p.data!.link;
  const focus = p.data!.focus;
  const color =
    focus === 'cause' ? CAUSE_COLOR : focus === 'impact' ? IMPACT_COLOR : STATUS_COLOR[link.status];
  const width = 2 + Math.min(6, link.utilization / 18);
  const cycle = Math.max(0.35, 3 - link.utilization / 35);

  return (
    <>
      <BaseEdge id={p.id} path={path} style={{ stroke: color, strokeWidth: width, opacity: 0.35 }} />
      <path
        d={path}
        fill="none"
        stroke={color}
        strokeWidth={width}
        strokeDasharray="6 10"
        className={focus === 'cause' ? 'rootiq-flow rootiq-cause' : 'rootiq-flow'}
        style={{ animationDuration: `${cycle}s` }}
      />
      <EdgeLabelRenderer>
        <div
          className="nodrag nopan absolute rounded-md border bg-noc-bg/95 px-2 py-1 font-mono text-[11px] leading-tight"
          style={{
            transform: `translate(-50%,-50%) translate(${lx}px,${ly}px)`,
            borderColor: color,
            pointerEvents: 'all',
          }}
        >
          <div>
            {link.sourcePort} ⇄ {link.targetPort}
          </div>
          <div className="text-slate-400">
            {Math.round(link.utilization)}% · {link.latencyMs.toFixed(0)} ms
            {link.packetLoss > 0 && (
              <span className="text-crit"> · loss {link.packetLoss.toFixed(1)}%</span>
            )}
          </div>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
