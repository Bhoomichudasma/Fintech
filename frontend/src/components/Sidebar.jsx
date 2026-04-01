import { useEffect, useState } from 'react'
import { searchSymbols } from '../api'

export default function Sidebar({ companies, onSelect, onAdd, active }) {
  const [draft, setDraft] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const t = setTimeout(async () => {
      if (!draft || draft.length < 2) {
        setResults([])
        return
      }
      setLoading(true)
      try {
        const res = await searchSymbols(draft)
        setResults(res)
      } finally {
        setLoading(false)
      }
    }, 250)
    return () => clearTimeout(t)
  }, [draft])

  const addSymbol = (symbol, name) => {
    const sym = (symbol || draft).trim().toUpperCase()
    if (!sym) return
    onAdd({ symbol: sym, name: name || sym })
    setDraft('')
    setResults([])
  }

  return (
    <aside className="flex h-full w-64 flex-col gap-3 rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-white/70">Watchlist</p>
        <span className="rounded-full bg-accent/20 px-3 py-1 text-xs text-accent">Live</span>
      </div>

      <div className="flex flex-col gap-2 rounded-xl bg-white/5 p-2">
        <div className="flex gap-2">
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addSymbol()}
            placeholder="Search company or symbol"
            className="w-full bg-transparent text-sm text-white placeholder:text-white/40 focus:outline-none"
          />
          <button onClick={() => addSymbol()} className="rounded-lg bg-accent px-3 text-sm font-semibold text-midnight">
            Add
          </button>
        </div>
        {loading && <p className="text-xs text-white/50">Searching...</p>}
        {!loading && results.length > 0 && (
          <div className="max-h-40 overflow-y-auto rounded-lg bg-white/5">
            {results.map((r) => (
              <button
                key={r.symbol}
                onClick={() => addSymbol(r.symbol, r.name)}
                className="flex w-full items-center justify-between px-3 py-2 text-left text-sm hover:bg-white/10"
              >
                <div>
                  <p className="font-semibold">{r.symbol}</p>
                  <p className="text-xs text-white/60">{r.name}</p>
                </div>
                <span className="text-[11px] text-white/50">{r.exchange}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="flex flex-col gap-2 overflow-y-auto pr-2">
        {companies.map((c) => (
          <button
            key={c.symbol}
            onClick={() => onSelect(c.symbol)}
            className={`flex w-full items-center justify-between rounded-xl px-3 py-3 text-left transition hover:bg-white/10 ${
              active === c.symbol ? 'bg-accent/15 ring-1 ring-accent/60' : 'bg-white/5'
            }`}
          >
            <div>
              <p className="text-sm font-semibold">{c.symbol}</p>
              <p className="text-xs text-white/60">{c.name}</p>
            </div>
            <span className="text-xs text-white/70">View</span>
          </button>
        ))}
      </div>
    </aside>
  )
}
