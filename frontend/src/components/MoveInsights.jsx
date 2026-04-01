export default function MoveInsights({ metrics }) {
  if (!metrics) return null
  const { anomaly, move_reason, price_spike, volume_spike } = metrics
  const chips = []
  if (anomaly) chips.push(anomaly)
  if (move_reason) chips.push(move_reason)
  if (price_spike !== null && price_spike !== undefined) chips.push(`Price spike: ${price_spike.toFixed(2)}%`)
  if (volume_spike) chips.push(`Volume x${volume_spike.toFixed(2)}`)
  if (!chips.length) return null

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Why did this stock move?</p>
        <span className="text-xs text-white/60">Anomaly detector</span>
      </div>
      <div className="flex flex-wrap gap-2 text-sm">
        {chips.map((c) => (
          <span key={c} className="rounded-full bg-accent/15 px-3 py-1 text-accent">
            {c}
          </span>
        ))}
      </div>
    </div>
  )
}
