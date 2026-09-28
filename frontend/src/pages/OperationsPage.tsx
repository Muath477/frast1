import { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  type Node,
  type Edge,
} from '@xyflow/react';
import { staticTopology } from '@/lib/staticTopology';

export function OperationsPage() {
  const nodes: Node[] = useMemo(
    () =>
      staticTopology.nodes.map((n) => ({
        id: n.id,
        position: n.position,
        data: { label: `${n.label}\n${n.managementIp}` },
        style: {
          background: '#111831',
          color: '#e2e8f0',
          border: '1px solid #1f2a4d',
          borderRadius: 8,
          padding: 10,
          fontSize: 12,
          whiteSpace: 'pre-line' as const,
          textAlign: 'center' as const,
          minWidth: 110,
        },
      })),
    [],
  );

  const edges: Edge[] = useMemo(
    () =>
      staticTopology.links.map((l) => ({
        id: l.id,
        source: l.source,
        target: l.target,
        label: `${l.sourcePort} ↔ ${l.targetPort}`,
        style: { stroke: '#22c55e' },
        labelStyle: { fill: '#94a3b8', fontSize: 10 },
      })),
    [],
  );

  return (
    <div className="h-full w-full">
      <ReactFlow nodes={nodes} edges={edges} fitView proOptions={{ hideAttribution: true }}>
        <Background color="#1f2a4d" gap={20} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
