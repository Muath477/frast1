import { useEffect, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  ConnectionMode,
  useNodesState,
} from '@xyflow/react';
import { DeviceNode, type DeviceNodeT, type Focus } from './DeviceNode';
import { PortEdge } from './PortEdge';
import { toFlow } from '@/lib/layout';
import type { Topology } from '@/lib/types';

const nodeTypes = { device: DeviceNode };
const edgeTypes = { port: PortEdge };
const NO_FOCUS: Record<string, Focus> = {};

interface Props {
  topology: Topology;
  focus?: Record<string, Focus>;
  onSelect?: (sel: { kind: 'node' | 'link'; id: string } | null) => void;
  onLayoutSaved?: (positions: Record<string, { x: number; y: number }>) => void;
}

export function TopologyCanvas({
  topology,
  focus = NO_FOCUS,
  onSelect,
  onLayoutSaved,
}: Props) {
  const flow = useMemo(() => toFlow(topology, focus), [topology, focus]);
  const [nodes, setNodes, onNodesChange] = useNodesState<DeviceNodeT>(flow.nodes);

  useEffect(() => {
    setNodes((cur) =>
      flow.nodes.map((n) => ({
        ...n,
        position: cur.find((c) => c.id === n.id)?.position ?? n.position,
      })),
    );
  }, [flow.nodes, setNodes]);

  return (
    <div dir="ltr" className="h-full w-full">
      <ReactFlow
        nodes={nodes}
        edges={flow.edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesChange={onNodesChange}
        connectionMode={ConnectionMode.Loose}
        nodesConnectable={false}
        fitView
        minZoom={0.4}
        maxZoom={2}
        onNodeClick={(_, n) => onSelect?.({ kind: 'node', id: n.id })}
        onEdgeClick={(_, e) => onSelect?.({ kind: 'link', id: e.id })}
        onPaneClick={() => onSelect?.(null)}
        onNodeDragStop={(_, dragged) =>
          onLayoutSaved?.({
            ...Object.fromEntries(nodes.map((n) => [n.id, n.position])),
            [dragged.id]: dragged.position,
          })
        }
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1f2a4d" gap={24} />
        <MiniMap pannable zoomable className="!bg-noc-panel" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
