import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export default function SimulatorCard({ data = [], symbol }) {
  const formatted = data.map((point) => ({
    date: new Date(point.date).toLocaleDateString(),
    value: Number(point.close) * (10000 / (data[0]?.close || 1)),
  }))

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-white/60">If you invested ₹10,000</p>
          <p className="text-lg font-semibold">{symbol}</p>
        </div>
        {formatted.length > 0 && (
          <p className="text-sm text-accent">₹{formatted.at(-1).value.toFixed(0)}</p>
        )}
      </div>
      <div className="mt-3 h-40">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={formatted}>
            <defs>
              <linearGradient id="simColor" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8ef5b9" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#8ef5b9" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="date" hide interval="preserveStartEnd" />
            <YAxis hide />
            <Tooltip
              contentStyle={{ background: '#121526', border: '1px solid rgba(255,255,255,0.08)' }}
              formatter={(v) => `₹${Number(v).toFixed(0)}`}
            />
            <Area type="monotone" dataKey="value" stroke="#8ef5b9" fill="url(#simColor)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
