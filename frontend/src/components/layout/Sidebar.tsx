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
import { RootIQMark } from '@/components/brand/Logo';

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
    <nav
      className="presenter-hide flex h-full flex-col items-center gap-1 py-3"
      style={{ width: 'var(--rail-w)' }}
    >
      <div className="mb-3 flex h-11 w-11 items-center justify-center">
        <RootIQMark size={40} />
      </div>
      {items.map(({ to, labelKey, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          title={t(labelKey)}
          className={({ isActive }) =>
            clsx(
              'relative flex h-11 w-11 items-center justify-center rounded-lg transition-colors',
              isActive
                ? 'bg-[var(--bg-selected)] text-[var(--brand-text)]'
                : 'text-[var(--text-3)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-1)]',
            )
          }
        >
          {({ isActive }) => (
            <>
              {isActive && (
                <span
                  aria-hidden
                  className="absolute inset-y-2 start-0 w-[3px] rounded-full bg-[var(--brand)]"
                />
              )}
              <Icon size={20} strokeWidth={1.75} />
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}
