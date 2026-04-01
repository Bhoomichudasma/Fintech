import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchCompanies() {
  const res = await axios.get(`${API_BASE}/companies`)
  return res.data.companies
}

export async function fetchStockData(symbol, range = '30d') {
  const res = await axios.get(`${API_BASE}/data/${symbol}`, { params: { range } })
  return res.data
}

export async function fetchSummary(symbol) {
  const res = await axios.get(`${API_BASE}/summary/${symbol}`)
  return res.data
}

export async function fetchCompare(symbols) {
  const res = await axios.get(`${API_BASE}/compare`, { params: { symbols: symbols.join(',') } })
  return res.data
}

export async function searchSymbols(query) {
  if (!query) return []
  const res = await axios.get(`${API_BASE}/search`, { params: { q: query } })
  return res.data.results || []
}
