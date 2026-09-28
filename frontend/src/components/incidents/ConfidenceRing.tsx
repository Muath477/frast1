export function ConfidenceRing({ value }: { value: number }) {
  const r = 40;
  const c = 2 * Math.PI * r;
  const pct = Math.round(value * 100);
  const color = value >= 0.8 ? '#22c55e' : value >= 0.55 ? '#eab308' : '#f97316';
  return (
    <svg width="96" height="96" viewBox="0 0 96 96" role="img" aria-label={`confidence ${pct}%`}>
      <circle cx="48" cy="48" r={r} stroke="#1f2a4d" strokeWidth="8" fill="none" />
      <circle
        cx="48"
        cy="48"
        r={r}
        stroke={color}
        strokeWidth="8"
        fill="none"
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={c * (1 - value)}
        transform="rotate(-90 48 48)"
        style={{ transition: 'stroke-dashoffset 900ms ease' }}
      />
      <text
        x="48"
        y="54"
        textAnchor="middle"
        className="fill-slate-100 font-mono text-xl font-bold"
      >
        {pct}%
      </text>
    </svg>
  );
}
