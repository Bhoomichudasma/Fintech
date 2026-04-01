import React from 'react'

export default function Heatmap({ symbols = [], matrix = [] }) {
  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Correlation Heatmap</p>
        <span className="text-xs text-white/60">1 = highly correlated</span>
      </div>
      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full border-separate border-spacing-1 text-sm">
          <thead>
            <tr>
              <th className="text-left text-white/60">Pair</th>
              {symbols.map((s) => (
                <th key={s} className="text-center text-white/60">
                  {s}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={symbols[i]}>
                <td className="whitespace-nowrap px-2 py-1 text-white/70">{symbols[i]}</td>
                {row.map((cell, j) => {
                  const intensity = Math.abs(cell)
                  const bg = `rgba(140,123,255,${0.15 + intensity * 0.6})`
                  return (
                    <td
                      key={`${i}-${j}`}
                      className="rounded-md px-2 py-2 text-center text-xs font-semibold"
                      style={{ backgroundColor: bg }}
                    >
                      {cell.toFixed(2)}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
