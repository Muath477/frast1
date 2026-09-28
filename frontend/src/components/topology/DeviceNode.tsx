import type { CSSProperties } from 'react';
import { Handle, Position, type Node, type NodeProps } from '@xyflow/react';
import { Router, Network, Server, Radar } from 'lucide-react';
import clsx from 'clsx';
import type { Iface, Side, TopoNode } from '@/lib/types';
import { STATUS_COLOR } from '@/lib/colors';

export type Focus = 'cause' | 'impact' | null;
export type DeviceNodeT = Node<{ device: TopoNode; focus: Focus }, 'device'>;

const ICON = { router: Router, switch: Network, server: Server, collector: Radar } as const;
const POS: Record<Side, Position> = {
  top: Position.Top,
  bottom: Position.Bottom,
  left: Position.Left,
  right: Position.Right,
};

function handleStyle(side: Side, idx: number, total: number): CSSProperties {
  const pct = `${((idx + 1) / (total + 1)) * 100}%`;
  return side === 'top' || side === 'bottom' ? { left: pct } : { top: pct };
}

export function DeviceNode({ data, selected }: NodeProps<DeviceNodeT>) {
  const { device, focus } = data;
  const Icon = ICON[device.type];
  const bySide = device.interfaces.reduce<Partial<Record<Side, Iface[]>>>((acc, i) => {
    (acc[i.side] ??= []).push(i);
    return acc;
  }, {});

  return (
    <div
      className={clsx(
        'min-w-[160px] rounded-xl border-2 bg-noc-panel/95 px-4 py-3 shadow-lg transition-colors',
        selected && 'ring-2 ring-info',
        focus === 'cause' && 'rootiq-cause',
      )}
      style={{
        borderColor:
          focus === 'cause'
            ? '#ef4444'
            : focus === 'impact'
              ? '#f59e0b'
              : STATUS_COLOR[device.status],
      }}
    >
      <div className="flex items-center gap-2">
        <Icon className="size-5" style={{ color: STATUS_COLOR[device.status] }} />
        <span className="font-semibold tracking-wide">{device.label}</span>
      </div>
      <div className="mt-1 font-mono text-[11px] text-slate-400">{device.managementIp}</div>
      {(Object.keys(bySide) as Side[]).flatMap((side) =>
        (bySide[side] ?? []).map((i, idx) => (
          <Handle
            key={i.name}
            id={i.name}
            type="source"
            position={POS[side]}
            style={handleStyle(side, idx, bySide[side]!.length)}
            className="!size-2.5 !border-0 !bg-slate-300"
            title={i.name}
          />
        )),
      )}
    </div>
  );
}
