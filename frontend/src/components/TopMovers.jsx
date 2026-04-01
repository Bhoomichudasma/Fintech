export default function TopMovers({ items = [] }) {
  const sorted = [...items].sort((a, b) => b.momentum - a.momentum)
  const top = sorted.slice(0, 3)
  const bottom = sorted.slice(-3).reverse()

  return (
    <div id="gainers" className="grid gap-3 md:grid-cols-2">
      <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-sm font-semibold text-white/80">Top Gainers</p>
          <span className="text-xs text-accent">Momentum</span>
        </div>
        <div className="flex flex-col gap-2">
          {top.map((i) => (
            <div key={i.symbol} className="flex items-center justify-between rounded-xl bg-white/5 px-3 py-2">
              <div>
                <p className="text-sm font-semibold">{i.symbol}</p>
                <p className="text-xs text-white/60">Health {i.health_score.toFixed(0)}</p>
              </div>
              <span className="text-sm text-accent">{i.momentum.toFixed(2)}%</span>
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-sm font-semibold text-white/80">Top Losers</p>
          <span className="text-xs text-danger">Momentum</span>
        </div>
        <div className="flex flex-col gap-2">
          {bottom.map((i) => (
            <div key={i.symbol} className="flex items-center justify-between rounded-xl bg-white/5 px-3 py-2">
              <div>
                <p className="text-sm font-semibold">{i.symbol}</p>
                <p className="text-xs text-white/60">Health {i.health_score.toFixed(0)}</p>
              </div>
              <span className="text-sm text-danger">{i.momentum.toFixed(2)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
