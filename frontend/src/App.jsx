import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'

function Navbar() {
  return (
    <header className="sticky top-0 z-20 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 sm:px-10">
        <div className="flex items-center gap-2 text-lg font-semibold">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-accent/20 text-accent">Σ</span>
          <span>Stock Intelligence</span>
        </div>
        <div className="flex items-center gap-3 text-sm text-white/70">
          <a href="#dashboard" className="hover:text-white">
            Dashboard
          </a>
          <a href="#gainers" className="hover:text-white">
            Movers
          </a>
          <a href="#contact" className="rounded-full bg-white/10 px-4 py-2 hover:bg-white/20">
            Get early access
          </a>
        </div>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <main className="min-h-screen text-white">
      <Navbar />
      <Landing />
      <Dashboard />
    </main>
  )
}
