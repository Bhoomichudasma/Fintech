import { useEffect, useMemo, useState } from 'react'
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Activity, BarChart2, Loader2, Sparkles } from 'lucide-react'
import { fetchCompanies, fetchCompare, fetchStockData } from '../api'
import Sidebar from '../components/Sidebar'
import MetricCard from '../components/MetricCard'
import Heatmap from '../components/Heatmap'
import RiskMeter from '../components/RiskMeter'
import SimulatorCard from '../components/SimulatorCard'
import TopMovers from '../components/TopMovers'
import NewsList from '../components/NewsList'
import MoveInsights from '../components/MoveInsights'
import PortfolioSimulator from '../components/PortfolioSimulator'
import ComparePicker from '../components/ComparePicker'

const ranges = ['7d', '30d', '90d', '1y']

export default function Dashboard() {
  const [companies, setCompanies] = useState([])
  const [selected, setSelected] = useState('AAPL')
  const [range, setRange] = useState('30d')
  const [data, setData] = useState(null)
  const [compare, setCompare] = useState({ items: [], symbols: [], correlation_matrix: [] })
  const [loading, setLoading] = useState(false)
  const [showMA7, setShowMA7] = useState(true)
  const [showMA30, setShowMA30] = useState(true)
  const [showPred, setShowPred] = useState(true)
  const [compareSelection, setCompareSelection] = useState([])

  useEffect(() => {
    const init = async () => {
      const list = await fetchCompanies()
      setCompanies(list)
      setSelected(list[0]?.symbol || 'AAPL')
    }
    init()
  }, [])

  useEffect(() => {
    if (companies.length && compareSelection.length === 0) {
      const base = companies.slice(0, 2).map((c) => c.symbol)
      setCompareSelection(base.length >= 2 ? base : ['AAPL', 'MSFT'])
    }
  }, [companies, compareSelection.length])

  useEffect(() => {
    if (!selected) return
    const load = async () => {
      setLoading(true)
      try {
        const res = await fetchStockData(selected, range)
        setData(res)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [selected, range])

  useEffect(() => {
    const symbols = compareSelection.length >= 2 ? compareSelection : ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    const load = async () => {
      try {
        const comp = await fetchCompare(symbols)
        setCompare(comp)
      } catch (_) {}
    }
    load()
  }, [compareSelection])

  const chartData = useMemo(() => {
    if (!data) return []
    return data.points.map((p) => ({
      date: new Date(p.date).toLocaleDateString(),
      close: p.close,
      ma7: p.ma7,
      ma30: p.ma30,
      prediction: undefined,
    }))
  }, [data])

  const predictionLine = useMemo(() => {
    if (!data?.predictions) return []
    return data.predictions.map((p) => ({
      date: new Date(p.date).toLocaleDateString(),
      prediction: p.predicted_close,
    }))
  }, [data])

  const metrics = data?.metrics

  const handleAddSymbol = (entry) => {
    const sym = typeof entry === 'string' ? entry : entry.symbol
    const name = typeof entry === 'string' ? entry : entry.name || entry.symbol
    if (companies.some((c) => c.symbol === sym)) {
      setSelected(sym)
      return
    }
    const newCompany = { symbol: sym, name }
    const next = [...companies, newCompany]
    setCompanies(next)
    setSelected(sym)
    if (!compareSelection.includes(sym)) {
      setCompareSelection((prev) => [...prev, sym].slice(0, 8))
    }
  }

  return (
    <section id="dashboard" className="-mt-16 bg-gradient-to-b from-transparent via-[#0f1020] to-[#0a0b16] pb-16 pt-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 sm:px-10">
        <div className="flex flex-col gap-3">
          <p className="text-sm uppercase tracking-[0.3em] text-white/60">Dashboard</p>
          <div className="flex items-center justify-between">
            <h2 className="text-3xl font-semibold">Live Market Console</h2>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1 rounded-full bg-white/10 px-3 py-1 text-xs text-white/70">
                <Sparkles className="h-4 w-4 text-accent" /> AI forecast on
              </span>
              <span className="inline-flex items-center gap-1 rounded-full bg-accent/20 px-3 py-1 text-xs text-accent">
                {selected}
              </span>
            </div>
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-[260px,1fr]">
          <Sidebar companies={companies} active={selected} onSelect={setSelected} onAdd={handleAddSymbol} />

          <div className="flex flex-col gap-4">
            <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent/15 text-accent">
                  <Activity className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm text-white/60">Filters</p>
                  <p className="text-lg font-semibold">{selected} · {range.toUpperCase()}</p>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {ranges.map((r) => (
                  <button
                    key={r}
                    onClick={() => setRange(r)}
                    className={`rounded-full px-3 py-1 text-sm transition ${
                      range === r ? 'bg-accent text-midnight' : 'bg-white/10 text-white/70 hover:bg-white/20'
                    }`}
                  >
                    {r}
                  </button>
                ))}
                <button
                  onClick={() => setShowMA7((v) => !v)}
                  className={`rounded-full px-3 py-1 text-sm ${showMA7 ? 'bg-accent/20 text-accent' : 'bg-white/10 text-white/60'}`}
                >
                  7D MA
                </button>
                <button
                  onClick={() => setShowMA30((v) => !v)}
                  className={`rounded-full px-3 py-1 text-sm ${showMA30 ? 'bg-accent2/20 text-accent2' : 'bg-white/10 text-white/60'}`}
                >
                  30D MA
                </button>
                <button
                  onClick={() => setShowPred((v) => !v)}
                  className={`rounded-full px-3 py-1 text-sm ${showPred ? 'bg-warning/20 text-warning' : 'bg-white/10 text-white/60'}`}
                >
                  Prediction
                </button>
              </div>
            </div>

            <div className="grid gap-4 lg:grid-cols-3">
              <MetricCard label="52-week High" value={metrics ? `$${metrics.high_52_week.toFixed(2)}` : '--'} />
              <MetricCard label="52-week Low" value={metrics ? `$${metrics.low_52_week.toFixed(2)}` : '--'} />
              <MetricCard label="Volatility" value={metrics ? `${metrics.volatility.toFixed(2)}%` : '--'} />
            </div>

            <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
              <div className="mb-3 flex items-center justify-between">
                <div className="flex items-center gap-2 text-white/80">
                  <BarChart2 className="h-5 w-5 text-accent" />
                  <span className="font-semibold">Price action & overlays</span>
                </div>
                {loading && (
                  <span className="inline-flex items-center gap-2 text-xs text-white/60">
                    <Loader2 className="h-4 w-4 animate-spin" /> Updating
                  </span>
                )}
              </div>
              <div className="h-[360px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData} margin={{ left: 0, right: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                    <XAxis dataKey="date" stroke="#74778f" />
                    <YAxis stroke="#74778f" domain={['auto', 'auto']} />
                    <Tooltip
                      contentStyle={{ background: '#121526', border: '1px solid rgba(255,255,255,0.1)' }}
                      labelStyle={{ color: '#fff' }}
                    />
                    <Legend />
                    <Area type="monotone" dataKey="close" name="Close" stroke="#8ef5b9" fill="#8ef5b915" strokeWidth={2} />
                    {showMA7 && <Line type="monotone" dataKey="ma7" name="7D MA" stroke="#8c7bff" dot={false} strokeWidth={2} />}
                    {showMA30 && <Line type="monotone" dataKey="ma30" name="30D MA" stroke="#f9cf58" dot={false} strokeWidth={2} />}
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {showPred && predictionLine.length > 0 && (
              <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
                <div className="mb-2 flex items-center justify-between text-white/80">
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-warning" />
                    <span className="font-semibold">AI 7-day outlook</span>
                  </div>
                  <span className="text-xs text-white/60">Linear regression</span>
                </div>
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={predictionLine}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                      <XAxis dataKey="date" stroke="#74778f" />
                      <YAxis stroke="#74778f" domain={['auto', 'auto']} />
                      <Tooltip
                        contentStyle={{ background: '#121526', border: '1px solid rgba(255,255,255,0.1)' }}
                        formatter={(v) => `$${Number(v).toFixed(2)}`}
                      />
                      <Line type="monotone" dataKey="prediction" stroke="#f9cf58" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            <div className="grid gap-4 lg:grid-cols-3">
              <RiskMeter level={metrics?.risk_level} volatility={metrics?.volatility || 0} />
              <SimulatorCard data={data?.points || []} symbol={selected} />
              <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
                <p className="text-sm font-semibold text-white/80">Signal Board</p>
                <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
                  <div className="rounded-xl bg-white/5 p-3">
                    <p className="text-white/60">Momentum</p>
                    <p className="text-lg font-semibold text-accent">{metrics ? metrics.momentum.toFixed(2) : '--'}%</p>
                  </div>
                  <div className="rounded-xl bg-white/5 p-3">
                    <p className="text-white/60">Health Score</p>
                    <p className="text-lg font-semibold text-accent2">{metrics ? metrics.health_score.toFixed(0) : '--'}</p>
                  </div>
                  <div className="rounded-xl bg-white/5 p-3">
                    <p className="text-white/60">Avg Close</p>
                    <p className="text-lg font-semibold">{metrics ? `$${metrics.average_close.toFixed(2)}` : '--'}</p>
                  </div>
                  <div className="rounded-xl bg-white/5 p-3">
                    <p className="text-white/60">Volatility</p>
                    <p className="text-lg font-semibold">{metrics ? `${metrics.volatility.toFixed(2)}%` : '--'}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid gap-4 lg:grid-cols-2">
              <MoveInsights metrics={metrics} />
              <PortfolioSimulator defaultSymbols={[selected, ...(companies.slice(0, 2).map((c) => c.symbol))]} />
            </div>

            <div>
              <NewsList items={data?.news || []} />
            </div>

            <div className="grid gap-4 lg:grid-cols-3">
              <div className="lg:col-span-2">
                <Heatmap symbols={compare.symbols} matrix={compare.correlation_matrix} />
              </div>
              <TopMovers items={compare.items} />
            </div>

            <ComparePicker companies={companies} selection={compareSelection} onChange={setCompareSelection} />
          </div>
        </div>
      </div>
    </section>
  )
}
