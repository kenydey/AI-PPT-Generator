import { create } from 'zustand'
import type { PPTOutline, SlideOutline } from '../types'

interface PPTState {
  outline: PPTOutline
  setOutline: (outline: PPTOutline) => void
  updateSlide: (index: number, slide: Partial<SlideOutline>) => void
}

export const usePPTStore = create<PPTState>((set) => ({
  outline: { slides: [] },
  setOutline: (outline) => set({ outline }),
  updateSlide: (index, slide) =>
    set((state) => {
      const slides = [...state.outline.slides]
      if (slides[index]) slides[index] = { ...slides[index], ...slide }
      return { outline: { slides } }
    }),
}))
