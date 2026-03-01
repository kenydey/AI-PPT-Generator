/**
 * 素材拾取器 - 搜索 Pexels/Unsplash/Iconfinder
 */
import { useState } from 'react'
import { searchImages } from '../../api/client'

export default function MediaPicker() {
  const [q, setQ] = useState('')
  const [results, setResults] = useState<{ thumb?: string; url?: string }[]>([])
  const [loading, setLoading] = useState(false)
  const search = async () => {
    if (!q.trim()) return
    setLoading(true)
    try {
      const { results: r } = await searchImages(q)
      setResults(r || [])
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="rounded border p-4">
      <h3 className="font-medium text-sm mb-2">图片搜索</h3>
      <input type="text" value={q} onChange={(e) => setQ(e.target.value)} placeholder="关键词" className="w-full border rounded px-2 py-1 text-sm" />
      <button onClick={search} disabled={loading} className="mt-2 w-full py-1 bg-gray-200 rounded text-sm">搜索</button>
      <div className="mt-2 grid grid-cols-2 gap-1">
        {results.slice(0, 4).map((r, i) => (
          <a key={i} href={r.url} target="_blank" rel="noreferrer" className="block">
            {r.thumb ? <img src={r.thumb} alt="" className="w-full h-16 object-cover rounded" /> : <span className="text-xs text-gray-400">无缩略图</span>}
          </a>
        ))}
      </div>
    </div>
  )
}
