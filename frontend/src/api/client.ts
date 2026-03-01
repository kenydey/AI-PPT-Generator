import axios from 'axios'
import type { PPTOutline } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

export async function uploadFile(file: File) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<{ markdown: string; filename: string }>('/upload', form)
  return data
}

export async function generateOutline(params: { markdown: string; model?: string; n_slides?: number; web_search?: boolean }) {
  const { data } = await api.post<{ outline: PPTOutline }>('/generate-outline', {
    markdown: params.markdown,
    model: params.model ?? 'gpt-4o',
    n_slides: params.n_slides ?? 8,
    web_search: params.web_search ?? false,
  })
  return data
}

export async function generateOneShot(params: { content: string; markdown?: string; n_slides?: number; model?: string; web_search?: boolean }) {
  const { data } = await api.post<{ presentation_id: string; outline: PPTOutline }>('/v1/ppt/generate', params)
  return data
}

export async function exportPptx(outline: PPTOutline, template_path?: string): Promise<Blob> {
  const { data } = await api.post<Blob>('/export', { outline: outline as unknown as object, template_path }, { responseType: 'blob' })
  return data as Blob
}

export async function searchImages(q: string) {
  const { data } = await api.get<{ results: { thumb?: string; url?: string }[] }>('/images/search', { params: { q } })
  return data
}

export async function searchIcons(q: string) {
  const { data } = await api.get<{ results: { thumb?: string; url?: string }[] }>('/icons/search', { params: { q } })
  return data
}

export default api
