export default function TopMovers({ items = [] }) {
  const sorted = [...items].sort((a, b) => b.momentum - a.momentum)
  const top = sorted.slice(0, 3)
  const bottom = sorted.slice(-3).reverse()

  return (
    <div id="gainers" className="grid grid-cols-1 gap-3 2xl:grid-cols-2">
      <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
        <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
          <p className="text-sm font-semibold text-white/80">Top Gainers</p>
          <span className="shrink-0 text-xs text-accent">Momentum</span>
        </div>
        <div className="flex flex-col gap-2">
          {top.map((i) => (
            <div key={i.symbol} className="rounded-xl bg-white/5 px-3 py-2">
              <div className="flex items-center justify-between gap-2">
                <p className="min-w-0 truncate text-sm font-semibold">{i.symbol}</p>
                <span className="shrink-0 text-sm text-accent">{i.momentum.toFixed(2)}%</span>
              </div>
              <p className="mt-1 text-xs text-white/60">Health {i.health_score.toFixed(0)}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
        <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
          <p className="text-sm font-semibold text-white/80">Top Losers</p>
          <span className="shrink-0 text-xs text-danger">Momentum</span>
        </div>
        <div className="flex flex-col gap-2">
          {bottom.map((i) => (
            <div key={i.symbol} className="rounded-xl bg-white/5 px-3 py-2">
              <div className="flex items-center justify-between gap-2">
                <p className="min-w-0 truncate text-sm font-semibold">{i.symbol}</p>
                <span className="shrink-0 text-sm text-danger">{i.momentum.toFixed(2)}%</span>
              </div>
              <p className="mt-1 text-xs text-white/60">Health {i.health_score.toFixed(0)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
