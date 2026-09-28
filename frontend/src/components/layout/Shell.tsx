import { NavLink, Outlet } from 'react-router';
import { Sidebar } from './Sidebar';

export function Shell() {
  return (
    <div
      className="h-full grid"
      style={{
        gridTemplateColumns: '72px 1fr',
        gridTemplateRows: '56px 1fr 180px',
      }}
    >
      <aside className="row-span-3 border-r border-noc-line bg-noc-panel">
        <Sidebar />
      </aside>

      <header className="flex items-center justify-between px-4 border-b border-noc-line bg-noc-panel">
        <div className="flex items-center gap-3">
          <span className="text-lg font-semibold tracking-wide text-info">RootIQ</span>
          <span className="text-xs text-slate-400">Operations</span>
        </div>
        <NavLink to="/settings" className="text-xs text-slate-400 hover:text-slate-200">
          Settings
        </NavLink>
      </header>

      <main className="min-h-0 overflow-hidden">
        <Outlet />
      </main>

      <footer className="col-start-2 border-t border-noc-line bg-noc-panel px-4 py-2 text-xs text-slate-500">
        Timeline — coming day 6+
      </footer>
    </div>
  );
}
