/**
 * 幻灯片实时预览沙盒
 */
import { usePPTStore } from '../../store/pptStore'
import { useState } from 'react'

export default function SlidePreview() {
  const { outline } = usePPTStore()
  const [idx, setIdx] = useState(0)
  const slide = outline.slides[idx]
  if (!slide) {
    return (
      <div className="aspect-video rounded border bg-gray-50 flex items-center justify-center text-gray-500">
        暂无幻灯片
      </div>
    )
  }
  return (
    <div className="flex flex-col gap-2">
      <div className="flex gap-2">
        {outline.slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setIdx(i)}
            className={`px-2 py-1 rounded text-sm ${i === idx ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            {i + 1}
          </button>
        ))}
      </div>
      <div className="aspect-video rounded border bg-white p-8 shadow">
        <h3 className="text-2xl font-bold">{slide.title}</h3>
        <ul className="mt-4 list-disc list-inside space-y-1">
          {slide.bullets.map((b, j) => (
            <li key={j}>{b}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
