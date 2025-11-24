import { create } from 'zustand'

export const usePredictionStore = create((set) => ({
  prediction: null,
  contextId: null,
  isLoading: false,
  error: null,
  chatHistory: [],

  setPrediction: (data) =>
    set({
      prediction: data,
      contextId: data?.context_id || null,
      error: null,
    }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error, isLoading: false }),

  addChatMessage: (message) =>
    set((state) => ({
      chatHistory: [...state.chatHistory, message],
    })),

  clearChat: () => set({ chatHistory: [] }),

  reset: () =>
    set({
      prediction: null,
      contextId: null,
      isLoading: false,
      error: null,
      chatHistory: [],
    }),
}))

