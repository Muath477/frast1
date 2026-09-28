import { Outlet } from 'react-router';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { useOpsSocket } from '@/hooks/useOpsSocket';

export function Shell() {
  useOpsSocket();

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

      <TopBar />

      <main className="relative min-h-0 overflow-hidden">
        <Outlet />
      </main>

      <footer className="col-start-2 border-t border-noc-line bg-noc-panel px-4 py-2 text-xs text-slate-500">
        Timeline — coming day 6+
      </footer>
    </div>
  );
}
