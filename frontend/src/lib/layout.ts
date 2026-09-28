import type { DeviceNodeT, Focus } from '@/components/topology/DeviceNode';
import type { PortEdgeT } from '@/components/topology/PortEdge';
import type { Topology } from './types';

export function toFlow(t: Topology, focus: Record<string, Focus> = {}) {
  const nodes: DeviceNodeT[] = t.nodes.map((n) => ({
    id: n.id,
    type: 'device',
    position: n.position,
    data: { device: n, focus: focus[n.id] ?? null },
  }));
  const edges: PortEdgeT[] = t.links.map((l) => ({
    id: l.id,
    type: 'port',
    source: l.source,
    target: l.target,
    sourceHandle: l.sourcePort,
    targetHandle: l.targetPort,
    data: { link: l, focus: focus[l.id] ?? null },
  }));
  return { nodes, edges };
}
