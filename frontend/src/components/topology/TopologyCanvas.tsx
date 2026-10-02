import { useEffect, useMemo, useState } from 'react';
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
import { cssToken } from '@/lib/theme';

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
  const [grid, setGrid] = useState(() => cssToken('--topo-grid', 'rgba(169, 176, 224, .07)'));

  useEffect(() => {
    const sync = () => setGrid(cssToken('--topo-grid', 'rgba(169, 176, 224, .07)'));
    sync();
    const mo = new MutationObserver(sync);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => mo.disconnect();
  }, []);

  useEffect(() => {
    setNodes((cur) =>
      flow.nodes.map((n) => ({
        ...n,
        position: cur.find((c) => c.id === n.id)?.position ?? n.position,
      })),
    );
  }, [flow.nodes, setNodes]);

  return (
    <div dir="ltr" className="h-full w-full bg-[var(--bg-canvas)]">
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
        <Background color={grid} gap={24} />
        <MiniMap pannable zoomable className="!bg-noc-panel" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
