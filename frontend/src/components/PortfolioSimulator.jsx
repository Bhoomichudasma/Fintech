import { useState } from 'react'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function PortfolioSimulator({ defaultSymbols = [] }) {
  const [holdings, setHoldings] = useState(defaultSymbols.map((s) => ({ symbol: s, weight: 1 })))
  const [initial, setInitial] = useState(10000)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const onSimulate = async () => {
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/portfolio`, { holdings, initial, range: '180d' })
      setData(res.data)
    } finally {
      setLoading(false)
    }
  }

  const updateHolding = (idx, field, value) => {
    const next = holdings.slice()
    next[idx] = { ...next[idx], [field]: field === 'weight' ? Number(value) : value }
    setHoldings(next)
  }

  const addHolding = () => setHoldings([...holdings, { symbol: '', weight: 1 }])

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Portfolio Simulator</p>
        <button
          onClick={onSimulate}
          className="rounded-full bg-accent px-4 py-2 text-sm font-semibold text-midnight disabled:opacity-60"
          disabled={loading}
        >
          {loading ? 'Simulating...' : 'Run'}
        </button>
      </div>
      <div className="flex flex-col gap-2">
        {holdings.map((h, idx) => (
          <div key={idx} className="flex gap-2">
            <input
              value={h.symbol}
              onChange={(e) => updateHolding(idx, 'symbol', e.target.value.toUpperCase())}
              className="w-24 rounded-lg bg-white/10 px-2 py-1 text-sm text-white focus:outline-none"
              placeholder="SYMB"
            />
            <input
              type="number"
              value={h.weight}
              onChange={(e) => updateHolding(idx, 'weight', e.target.value)}
              className="w-20 rounded-lg bg-white/10 px-2 py-1 text-sm text-white focus:outline-none"
              placeholder="Weight"
            />
          </div>
        ))}
        <div className="flex gap-3 items-center">
          <button onClick={addHolding} className="text-xs text-accent">+ Add</button>
          <label className="text-xs text-white/60">
            Initial (₹)
            <input
              type="number"
              value={initial}
              onChange={(e) => setInitial(Number(e.target.value))}
              className="ml-2 w-28 rounded-lg bg-white/10 px-2 py-1 text-sm text-white focus:outline-none"
            />
          </label>
        </div>
      </div>

      {data && (
        <div className="mt-4">
          <p className="text-sm text-white/70">Total return: {data.total_return_pct.toFixed(2)}%</p>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.points}>
                <defs>
                  <linearGradient id="portColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8ef5b9" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#8ef5b9" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" tickFormatter={(d) => new Date(d).toLocaleDateString()} stroke="#777" />
                <YAxis stroke="#777" domain={['auto', 'auto']} />
                <Tooltip contentStyle={{ background: '#121526', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Area type="monotone" dataKey="value" stroke="#8ef5b9" fill="url(#portColor)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}
