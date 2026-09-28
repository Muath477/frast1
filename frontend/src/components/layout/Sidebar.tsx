import { NavLink } from 'react-router';
import {
  Network,
  Siren,
  Server,
  Boxes,
  BarChart3,
  ShieldCheck,
  Settings,
} from 'lucide-react';
import clsx from 'clsx';

const items: { to: string; label: string; icon: typeof Network; end?: boolean }[] = [
  { to: '/', label: 'Topology', icon: Network, end: true },
  { to: '/incidents', label: 'Incidents', icon: Siren },
  { to: '/devices', label: 'Devices', icon: Server },
  { to: '/services', label: 'Services', icon: Boxes },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/audit', label: 'Automation', icon: ShieldCheck },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export function Sidebar() {
  return (
    <nav className="flex h-full flex-col items-center gap-1 py-3">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-info/15 text-sm font-bold text-info">
        RQ
      </div>
      {items.map(({ to, label, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          title={label}
          className={({ isActive }) =>
            clsx(
              'flex h-11 w-11 items-center justify-center rounded-lg transition-colors',
              isActive
                ? 'bg-info/20 text-info'
                : 'text-slate-400 hover:bg-white/5 hover:text-slate-200',
            )
          }
        >
          <Icon size={20} />
        </NavLink>
      ))}
    </nav>
  );
}
