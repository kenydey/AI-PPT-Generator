/**
 * 与后端 Pydantic PPTOutline 对齐
 */
export interface SlideOutline {
  title: string
  bullets: string[]
  chart_type?: 'bar' | 'line' | 'pie' | 'bubble' | 'none'
  chart_data?: { categories: string[]; series: { name: string; values: number[] }[] }
  image_urls?: string[]
}

export interface PPTOutline {
  slides: SlideOutline[]
}
