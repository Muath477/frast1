import { Outlet } from 'react-router';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { useOpsSocket } from '@/hooks/useOpsSocket';
import { useHotkeys } from '@/hooks/useHotkeys';
import { useCallback } from 'react';

export function Shell() {
  useOpsSocket();
  const onTogglePresenter = useCallback(() => {
    // Presenter mode — Day 10
  }, []);
  useHotkeys(onTogglePresenter);

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
        Timeline — inject ▲ · alerts · incident ● (full Day 6 polish)
      </footer>
    </div>
  );
}
