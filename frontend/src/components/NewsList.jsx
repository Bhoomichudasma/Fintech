export default function NewsList({ items = [] }) {
  if (!items.length) return null
  return (
    <div className="rounded-2xl bg-white/5 p-4 ring-1 ring-white/10">
      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm font-semibold text-white/80">Why did this move? (News)</p>
        <span className="text-xs text-white/50">Powered by NewsAPI / mock</span>
      </div>
      <div className="flex flex-col gap-2 text-sm">
        {items.map((n) => (
          <a
            key={n.url + n.title}
            href={n.url}
            target="_blank"
            rel="noreferrer"
            className="rounded-xl bg-white/5 px-3 py-2 transition hover:bg-white/10"
          >
            <p className="font-semibold text-white">{n.title}</p>
            <p className="text-xs text-white/60">{n.source || 'News'} · {n.published_at ? new Date(n.published_at).toLocaleString() : ''}</p>
          </a>
        ))}
      </div>
    </div>
  )
}
