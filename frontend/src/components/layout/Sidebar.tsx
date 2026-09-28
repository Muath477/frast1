import { NavLink } from 'react-router';
import {
  Network,
  Siren,
  Server,
  Boxes,
  Bot,
  BarChart3,
  ShieldCheck,
  Settings,
} from 'lucide-react';
import clsx from 'clsx';
import { useTranslation } from 'react-i18next';

const items: { to: string; labelKey: string; icon: typeof Network; end?: boolean }[] = [
  { to: '/', labelKey: 'nav.topology', icon: Network, end: true },
  { to: '/incidents', labelKey: 'nav.incidents', icon: Siren },
  { to: '/devices', labelKey: 'nav.devices', icon: Server },
  { to: '/services', labelKey: 'nav.services', icon: Boxes },
  { to: '/agents', labelKey: 'nav.agents', icon: Bot },
  { to: '/analytics', labelKey: 'nav.analytics', icon: BarChart3 },
  { to: '/audit', labelKey: 'nav.audit', icon: ShieldCheck },
  { to: '/settings', labelKey: 'nav.settings', icon: Settings },
];

export function Sidebar() {
  const { t } = useTranslation();
  return (
    <nav className="presenter-hide flex h-full flex-col items-center gap-1 py-3">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-info/15 text-sm font-bold text-info">
        RQ
      </div>
      {items.map(({ to, labelKey, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          title={t(labelKey)}
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
