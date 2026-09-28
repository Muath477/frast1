import { useCallback, useState } from 'react';
import { TopologyCanvas } from '@/components/topology/TopologyCanvas';
import { DeviceInspector } from '@/components/topology/DeviceInspector';
import { LinkInspector } from '@/components/topology/LinkInspector';
import { staticTopology } from '@/lib/staticTopology';
import type { Topology } from '@/lib/types';

type Selection = { kind: 'node' | 'link'; id: string } | null;

async function saveLayout(positions: Record<string, { x: number; y: number }>) {
  try {
    await fetch('/api/topology/layout', {
      method: 'PUT',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ positions }),
    });
  } catch {
    // Backend may be offline during pure FE work
  }
}

export function OperationsPage() {
  const [topology] = useState<Topology>(staticTopology);
  const [selection, setSelection] = useState<Selection>(null);

  const onLayoutSaved = useCallback((positions: Record<string, { x: number; y: number }>) => {
    void saveLayout(positions);
  }, []);

  const selectedNode =
    selection?.kind === 'node' ? topology.nodes.find((n) => n.id === selection.id) : undefined;
  const selectedLink =
    selection?.kind === 'link' ? topology.links.find((l) => l.id === selection.id) : undefined;

  return (
    <div className="relative h-full w-full">
      <TopologyCanvas
        topology={topology}
        onSelect={setSelection}
        onLayoutSaved={onLayoutSaved}
      />

      {selectedNode && (
        <DeviceInspector
          device={selectedNode}
          services={topology.services}
          onClose={() => setSelection(null)}
        />
      )}

      {selectedLink && (
        <LinkInspector
          link={selectedLink}
          sourceLabel={topology.nodes.find((n) => n.id === selectedLink.source)?.label ?? selectedLink.source}
          targetLabel={topology.nodes.find((n) => n.id === selectedLink.target)?.label ?? selectedLink.target}
          onClose={() => setSelection(null)}
        />
      )}
    </div>
  );
}
