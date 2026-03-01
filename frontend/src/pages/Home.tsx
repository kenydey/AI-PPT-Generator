import { useState } from 'react'
import { usePPTStore } from '../store/pptStore'
import { uploadFile, generateOutline, generateOneShot, exportPptx } from '../api/client'
import OutlineEditor from '../components/editor/OutlineEditor'
import SlidePreview from '../components/preview/SlidePreview'
import VibeChat from '../components/vibe/VibeChat'
import MediaPicker from '../components/media/MediaPicker'

export default function Home() {
  const { outline, setOutline } = usePPTStore()
  const [markdown, setMarkdown] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [nSlides, setNSlides] = useState(8)
  const [webSearch, setWebSearch] = useState(false)

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    setLoading(true)
    setError('')
    try {
      const res = await uploadFile(f)
      setMarkdown(res.markdown)
    } catch (err: unknown) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    const content = markdown || '机器学习入门简介'
    setLoading(true)
    setError('')
    try {
      const res = await generateOneShot({
        content,
        markdown: markdown || undefined,
        n_slides: nSlides,
        web_search: webSearch,
      })
      setOutline(res.outline)
    } catch (err: unknown) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    if (!outline.slides.length) {
      setError('请先生成大纲')
      return
    }
    setLoading(true)
    setError('')
    try {
      const blob = await exportPptx(outline)
      const url = URL.createObjectURL(blob as Blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'presentation.pptx'
      a.click()
      URL.revokeObjectURL(url)
    } catch (err: unknown) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white shadow p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">AI PPT Generator</h1>
        <a href="/docs" target="_blank" rel="noreferrer" className="text-sm text-blue-600 hover:underline">
          API 文档
        </a>
      </header>

      <main className="flex-1 flex gap-4 p-4 overflow-hidden">
        <aside className="w-80 flex flex-col gap-4 overflow-y-auto">
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="font-semibold mb-2">输入</h2>
            <label className="block text-sm text-gray-600 mb-1">上传文件 (PDF/Word/PPTX/TXT)</label>
            <input type="file" accept=".pdf,.docx,.pptx,.txt,.md" onChange={handleUpload} className="block w-full text-sm" />
            <textarea
              className="mt-2 w-full h-24 border rounded p-2 text-sm"
              placeholder="或直接输入关键词 / Markdown..."
              value={markdown}
              onChange={(e) => setMarkdown(e.target.value)}
            />
            <div className="flex items-center gap-2 mt-2">
              <label className="text-sm">页数</label>
              <input type="number" min={3} max={20} value={nSlides} onChange={(e) => setNSlides(Number(e.target.value))} className="w-16 border rounded px-2" />
              <label className="flex items-center gap-1 text-sm">
                <input type="checkbox" checked={webSearch} onChange={(e) => setWebSearch(e.target.checked)} />
                联网搜索
              </label>
            </div>
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="mt-2 w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? '生成中…' : '生成大纲'}
            </button>
            <button
              onClick={handleExport}
              disabled={!outline.slides.length || loading}
              className="mt-2 w-full py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            >
              导出 PPTX
            </button>
            {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          </div>
          <MediaPicker />
        </aside>

        <section className="flex-1 flex gap-4 min-w-0">
          <div className="w-72 bg-white rounded-lg shadow overflow-hidden flex flex-col">
            <h2 className="p-2 font-semibold border-b">大纲</h2>
            <div className="flex-1 overflow-y-auto p-2">
              <OutlineEditor />
            </div>
          </div>
          <div className="flex-1 bg-white rounded-lg shadow overflow-hidden flex flex-col">
            <h2 className="p-2 font-semibold border-b">预览</h2>
            <div className="flex-1 overflow-auto p-4">
              <SlidePreview />
            </div>
          </div>
        </section>

        <aside className="w-80 bg-white rounded-lg shadow overflow-hidden flex flex-col">
          <h2 className="p-2 font-semibold border-b">Vibe 编辑</h2>
          <div className="flex-1 overflow-y-auto p-2">
            <VibeChat />
          </div>
        </aside>
      </main>
    </div>
  )
}
