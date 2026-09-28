function Placeholder({ title }: { title: string }) {
  return (
    <div className="flex h-full items-center justify-center text-slate-400">
      {title} — Coming soon
    </div>
  );
}

export function IncidentsPage() {
  return <Placeholder title="Incidents" />;
}

export function DevicesPage() {
  return <Placeholder title="Devices" />;
}

export function ServicesPage() {
  return <Placeholder title="Services" />;
}

export function AnalyticsPage() {
  return <Placeholder title="Analytics" />;
}

export function SettingsPage() {
  return <Placeholder title="Settings" />;
}
