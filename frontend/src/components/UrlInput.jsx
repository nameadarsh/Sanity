import { useState } from 'react'
import { LinkIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

export const UrlInput = ({ onSubmit, loading }) => {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim() && !loading) {
      onSubmit(url)
      setUrl('')
    }
  }

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <LinkIcon className="w-5 h-5 text-gray-400" />
        </div>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/news-article"
          className="input-field pl-12"
          disabled={loading}
        />
      </div>
      <motion.button
        type="submit"
        disabled={!url.trim() || loading}
        className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        whileHover={{ scale: loading ? 1 : 1.02 }}
        whileTap={{ scale: loading ? 1 : 0.98 }}
      >
        {loading ? (
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : (
          <>
            <PaperAirplaneIcon className="w-5 h-5" />
            <span>Extract & Analyze</span>
          </>
        )}
      </motion.button>
    </motion.form>
  )
}

