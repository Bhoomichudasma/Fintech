export default function RiskMeter({ level = 'Medium', volatility = 0 }) {
  const levelColor = {
    Low: 'bg-accent',
    Medium: 'bg-warning',
    High: 'bg-danger',
  }[level] || 'bg-accent'

  const pct = Math.min(100, Math.max(0, volatility * 10))

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Risk Meter</p>
        <span className="text-xs text-white/60">Volatility tuned</span>
      </div>
      <div className="mt-4 h-3 w-full overflow-hidden rounded-full bg-white/10">
        <div className={`h-full ${levelColor}`} style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-2 flex justify-between text-xs text-white/60">
        <span>Calm</span>
        <span>{level}</span>
        <span>Stormy</span>
      </div>
    </div>
  )
}
