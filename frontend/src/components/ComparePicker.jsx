export default function ComparePicker({ companies = [], selection = [], onChange }) {
  const toggle = (sym) => {
    const exists = selection.includes(sym)
    const next = exists ? selection.filter((s) => s !== sym) : [...selection, sym]
    onChange(next.slice(0, 8))
  }

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Compare symbols</p>
        <span className="text-xs text-white/60">Select 2-8</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {companies.slice(0, 12).map((c) => {
          const active = selection.includes(c.symbol)
          return (
            <button
              key={c.symbol}
              onClick={() => toggle(c.symbol)}
              className={`rounded-full px-3 py-1 text-sm transition ${
                active ? 'bg-accent text-midnight' : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              {c.symbol}
            </button>
          )
        })}
        {selection.length === 0 && (
          <span className="text-xs text-white/50">Pick at least two symbols</span>
        )}
      </div>
    </div>
  )
}
