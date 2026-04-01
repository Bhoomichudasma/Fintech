import { ArrowRight, BarChart3, ShieldCheck, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

const features = [
  {
    icon: <BarChart3 className="h-5 w-5 text-accent" />,
    title: 'Market-grade analytics',
    desc: 'Institutional-grade signals like volatility, momentum, and a bespoke health score.',
  },
  {
    icon: <Sparkles className="h-5 w-5 text-warning" />,
    title: 'AI-assisted outlook',
    desc: 'Quick linear-regression forecasts overlayed on live charts to sense short-term drift.',
  },
  {
    icon: <ShieldCheck className="h-5 w-5 text-accent2" />,
    title: 'Risk-aware decisions',
    desc: 'Correlation heatmaps, risk meters, and scenario simulations keep you ahead.',
  },
]

export default function Landing() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-[#13162b] via-[#0f1020] to-[#0b0c18]">
      <div className="absolute inset-0 opacity-40" aria-hidden>
        <div className="absolute -left-20 top-10 h-64 w-64 rounded-full bg-accent blur-[120px]" />
        <div className="absolute right-0 top-0 h-80 w-80 rounded-full bg-accent2 blur-[140px]" />
      </div>
      <div className="relative mx-auto flex max-w-6xl flex-col gap-12 px-6 py-16 sm:px-10">
        <div className="flex flex-col gap-6 sm:gap-8">
          <p className="inline-flex w-fit items-center gap-2 rounded-full bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.24em] text-white/70 ring-1 ring-white/10">
            Stock Data Intelligence Dashboard
          </p>
          <div className="flex flex-col gap-4 sm:max-w-3xl">
            <h1 className="text-4xl font-bold leading-tight sm:text-5xl">
              A mini Bloomberg-style cockpit for decisive equity moves.
            </h1>
            <p className="text-lg text-white/80 sm:text-xl">
              Blend quant-grade metrics, crisp visualizations, and playful simulations. Designed for
              teams who want clarity without the clutter.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <a
              href="#dashboard"
              className="group inline-flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-midnight font-semibold transition hover:-translate-y-0.5 hover:shadow-soft"
            >
              Launch Dashboard
              <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
            </a>
            <Link
              to="#gainers"
              className="inline-flex items-center gap-2 rounded-full border border-white/15 px-6 py-3 text-white/80 transition hover:border-accent hover:text-white"
            >
              See market movers
            </Link>
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-3">
          {features.map((f) => (
            <div
              key={f.title}
              className="rounded-2xl bg-white/5 p-4 shadow-soft ring-1 ring-white/10 backdrop-blur"
            >
              <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/5">
                {f.icon}
              </div>
              <p className="text-lg font-semibold">{f.title}</p>
              <p className="text-sm text-white/70">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
