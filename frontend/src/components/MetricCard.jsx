export default function MetricCard({ label, value, delta, positive, accent = 'accent' }) {
  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <p className="text-sm text-white/60">{label}</p>
      <div className="mt-2 flex items-end justify-between">
        <p className="text-2xl font-semibold">{value}</p>
        {delta !== undefined && (
          <span
            className={`text-xs font-semibold ${positive ? 'text-accent' : 'text-danger'} rounded-full bg-white/5 px-2 py-1`}
          >
            {positive ? '▲' : '▼'} {delta}
          </span>
        )}
      </div>
    </div>
  )
}
