import { useState } from 'react'
import { predictNews } from '../lib/api'
import { usePredictionStore } from '../store/usePredictionStore'

export const useUploadHandler = () => {
  const [uploading, setUploading] = useState(false)
  const { setPrediction, setLoading, setError } = usePredictionStore()

  const handleTextSubmit = async (text) => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setUploading(true)
    setLoading(true)
    setError(null)

    try {
      const response = await predictNews({
        input_type: 'text',
        text: text.trim(),
      })
      setPrediction(response)
    } catch (error) {
      setError(error.message || 'Failed to predict. Please try again.')
    } finally {
      setUploading(false)
      setLoading(false)
    }
  }

  const handleUrlSubmit = async (url) => {
    if (!url.trim()) {
      setError('Please enter a URL')
      return
    }

    setUploading(true)
    setLoading(true)
    setError(null)

    try {
      const response = await predictNews({
        input_type: 'url',
        url: url.trim(),
      })
      setPrediction(response)
    } catch (error) {
      setError(error.message || 'Failed to extract and predict. Please check the URL.')
    } finally {
      setUploading(false)
      setLoading(false)
    }
  }

  const handleFileUpload = async (file) => {
    if (!file) {
      setError('Please select a PDF file')
      return
    }

    setUploading(true)
    setLoading(true)
    setError(null)

    try {
      const reader = new FileReader()
      reader.onload = async (e) => {
        const base64 = e.target.result.split(',')[1]
        try {
          const response = await predictNews({
            input_type: 'pdf',
            pdf_base64: base64,
          })
          setPrediction(response)
        } catch (error) {
          setError(error.message || 'Failed to process PDF. Please try again.')
        } finally {
          setUploading(false)
          setLoading(false)
        }
      }
      reader.readAsDataURL(file)
    } catch (error) {
      setError(error.message || 'Failed to read file')
      setUploading(false)
      setLoading(false)
    }
  }

  return {
    uploading,
    handleTextSubmit,
    handleUrlSubmit,
    handleFileUpload,
  }
}

