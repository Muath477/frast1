import { TopologyCanvas } from '@/components/topology/TopologyCanvas';
import { DeviceInspector } from '@/components/topology/DeviceInspector';
import { LinkInspector } from '@/components/topology/LinkInspector';
import { useOps } from '@/store/useOps';

async function saveLayout(positions: Record<string, { x: number; y: number }>) {
  try {
    await fetch('/api/topology/layout', {
      method: 'PUT',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ positions }),
    });
  } catch {
    // Backend may be offline
  }
}

export function OperationsPage() {
  const topology = useOps((s) => s.topology);
  const selection = useOps((s) => s.selection);
  const select = useOps((s) => s.select);

  if (!topology) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        Connecting to operations feed…
      </div>
    );
  }

  const selectedNode =
    selection?.kind === 'node' ? topology.nodes.find((n) => n.id === selection.id) : undefined;
  const selectedLink =
    selection?.kind === 'link' ? topology.links.find((l) => l.id === selection.id) : undefined;

  return (
    <div className="relative h-full w-full">
      <TopologyCanvas
        topology={topology}
        onSelect={select}
        onLayoutSaved={(positions) => void saveLayout(positions)}
      />

      {selectedNode && (
        <DeviceInspector
          device={selectedNode}
          services={topology.services}
          onClose={() => select(null)}
        />
      )}

      {selectedLink && (
        <LinkInspector
          link={selectedLink}
          sourceLabel={
            topology.nodes.find((n) => n.id === selectedLink.source)?.label ?? selectedLink.source
          }
          targetLabel={
            topology.nodes.find((n) => n.id === selectedLink.target)?.label ?? selectedLink.target
          }
          onClose={() => select(null)}
        />
      )}
    </div>
  );
}
