/**
 * 大纲拖拽编辑器 - @dnd-kit 可后续增强拖拽排序
 */
import { usePPTStore } from '../../store/pptStore'

export default function OutlineEditor() {
  const { outline } = usePPTStore()
  if (!outline.slides.length) {
    return <p className="text-sm text-gray-500">生成大纲后将在此显示，支持拖拽调整顺序</p>
  }
  return (
    <ul className="space-y-2">
      {outline.slides.map((s, i) => (
        <li key={i} className="text-sm border-l-2 border-blue-400 pl-2">
          <span className="font-medium">{s.title}</span>
          {s.bullets.length ? <ul className="mt-1 text-gray-600 list-disc list-inside">{s.bullets.slice(0, 2).map((b, j) => <li key={j}>{b}</li>)}</ul> : null}
        </li>
      ))}
    </ul>
  )
}
