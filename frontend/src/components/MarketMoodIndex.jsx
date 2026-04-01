export default function MarketMoodIndex({ metrics, data }) {
  if (!metrics || !data) return null

  const latestClose = data.points.length > 0 ? data.points[data.points.length - 1].close : 0
  const avgClose = metrics.average_close
  const momentum = metrics.momentum
  const volatility = metrics.volatility
  const healthScore = metrics.health_score

  // Calculate market mood based on multiple factors
  let bullishScore = 0
  let bearishScore = 0

  // Trend analysis (MA7 vs MA30)
  const latestMA7 = data.points.length > 0 ? data.points[data.points.length - 1].ma7 : 0
  const latestMA30 = data.points.length > 0 ? data.points[data.points.length - 1].ma30 : 0
  
  if (latestMA7 > latestMA30) {
    bullishScore += 2
  } else {
    bearishScore += 2
  }

  // Momentum analysis
  if (momentum > 5) {
    bullishScore += 2
  } else if (momentum > 0) {
    bullishScore += 1
  } else if (momentum < -5) {
    bearishScore += 2
  } else {
    bearishScore += 1
  }

  // Price vs Average
  if (latestClose > avgClose) {
    bullishScore += 1
  } else {
    bearishScore += 1
  }

  // Health score
  if (healthScore > 60) {
    bullishScore += 1
  } else if (healthScore < 40) {
    bearishScore += 1
  }

  // Volatility consideration
  if (volatility > 3) {
    bearishScore += 1 // High volatility adds uncertainty
  }

  const totalScore = bullishScore + bearishScore
  const bullishPercent = totalScore > 0 ? (bullishScore / totalScore) * 100 : 50
  
  let mood = 'Neutral'
  let color = 'text-white/70'
  let bgColor = 'bg-white/10'
  
  if (bullishPercent > 65) {
    mood = 'Bullish 🚀'
    color = 'text-accent'
    bgColor = 'bg-accent/20'
  } else if (bullishPercent < 35) {
    mood = 'Bearish 📉'
    color = 'text-danger'
    bgColor = 'bg-danger/20'
  } else {
    mood = 'Neutral ⏸️'
    color = 'text-warning'
    bgColor = 'bg-warning/20'
  }

  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Market Mood Index</p>
        <span className={`rounded-full px-2 py-1 text-xs ${bgColor} ${color}`}>{mood}</span>
      </div>
      
      <div className="space-y-3">
        {/* Sentiment Bar */}
        <div className="relative h-4 w-full overflow-hidden rounded-full bg-white/10">
          <div 
            className="absolute left-0 top-0 h-full bg-gradient-to-r from-accent to-warning transition-all duration-500"
            style={{ width: `${bullishPercent}%` }}
          />
          <div 
            className="absolute right-0 top-0 h-full bg-gradient-to-l from-danger to-white/20 transition-all duration-500"
            style={{ width: `${100 - bullishPercent}%` }}
          />
        </div>
        
        {/* Labels */}
        <div className="flex justify-between text-xs text-white/60">
          <span>Bearish</span>
          <span>Neutral</span>
          <span>Bullish</span>
        </div>
        
        {/* Metrics breakdown */}
        <div className="grid grid-cols-2 gap-2 pt-2">
          <div className="rounded-xl bg-white/5 p-2 text-center">
            <p className="text-xs text-white/60">Bullish Signals</p>
            <p className="text-lg font-semibold text-accent">{bullishScore}</p>
          </div>
          <div className="rounded-xl bg-white/5 p-2 text-center">
            <p className="text-xs text-white/60">Bearish Signals</p>
            <p className="text-lg font-semibold text-danger">{bearishScore}</p>
          </div>
        </div>
        
        {/* Analysis details */}
        <div className="mt-2 space-y-1 text-xs text-white/70">
          <div className="flex justify-between">
            <span>Trend (MA7 vs MA30):</span>
            <span className={latestMA7 > latestMA30 ? 'text-accent' : 'text-danger'}>
              {latestMA7 > latestMA30 ? 'Bullish' : 'Bearish'}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Momentum:</span>
            <span className={momentum > 0 ? 'text-accent' : 'text-danger'}>
              {momentum > 0 ? '+' : ''}{momentum.toFixed(2)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span>Health Score:</span>
            <span className={healthScore > 60 ? 'text-accent' : healthScore < 40 ? 'text-danger' : 'text-warning'}>
              {healthScore.toFixed(0)}/100
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
