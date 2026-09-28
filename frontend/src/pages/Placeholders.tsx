function Placeholder({ title }: { title: string }) {
  return (
    <div className="flex h-full items-center justify-center text-slate-400">
      {title} — Coming soon
    </div>
  );
}

export function ServicesPage() {
  return <Placeholder title="Services" />;
}
