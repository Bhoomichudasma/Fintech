export default function ComparisonTable({ items = [] }) {
  if (!items || items.length === 0) return null

  const sortedByHealth = [...items].sort((a, b) => b.health_score - a.health_score)
  const sortedByMomentum = [...items].sort((a, b) => b.momentum - a.momentum)
  const sortedByVolatility = [...items].sort((a, b) => a.volatility - b.volatility)

  const getHealthColor = (score) => {
    if (score >= 70) return 'text-accent'
    if (score >= 40) return 'text-warning'
    return 'text-danger'
  }

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'low': return 'text-accent'
      case 'medium': return 'text-warning'
      case 'high': return 'text-danger'
      default: return 'text-white/70'
    }
  }

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Stock Comparison</p>
        <span className="text-xs text-white/60">{items.length} stocks</span>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/10">
              <th className="py-2 text-left text-white/60">Symbol</th>
              <th className="py-2 text-right text-white/60">Avg Price</th>
              <th className="py-2 text-right text-white/60">Volatility</th>
              <th className="py-2 text-right text-white/60">Momentum</th>
              <th className="py-2 text-right text-white/60">Health Score</th>
              <th className="py-2 text-right text-white/60">Risk Level</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.symbol} className="border-b border-white/5 last:border-0">
                <td className="py-3 font-semibold text-white">{item.symbol}</td>
                <td className="py-3 text-right text-white/70">${item.average_close.toFixed(2)}</td>
                <td className="py-3 text-right text-white/70">{item.volatility.toFixed(2)}%</td>
                <td className={`py-3 text-right ${item.momentum >= 0 ? 'text-accent' : 'text-danger'}`}>
                  {item.momentum >= 0 ? '+' : ''}{item.momentum.toFixed(2)}%
                </td>
                <td className={`py-3 text-right font-medium ${getHealthColor(item.health_score)}`}>
                  {item.health_score.toFixed(0)}
                </td>
                <td className={`py-3 text-right ${getRiskColor(item.risk_level || 'Medium')}`}>
                  {item.risk_level || 'Medium'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Quick rankings */}
      <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
        <div className="rounded-xl bg-white/5 p-2">
          <p className="text-white/60">Healthiest</p>
          <p className="font-semibold text-accent">{sortedByHealth[0]?.symbol}</p>
        </div>
        <div className="rounded-xl bg-white/5 p-2">
          <p className="text-white/60">Best Momentum</p>
          <p className="font-semibold text-accent">{sortedByMomentum[0]?.symbol}</p>
        </div>
        <div className="rounded-xl bg-white/5 p-2">
          <p className="text-white/60">Safest</p>
          <p className="font-semibold text-accent">{sortedByVolatility[0]?.symbol}</p>
        </div>
      </div>
    </div>
  )
}
