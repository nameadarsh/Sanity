import { useState } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

export const TextInput = ({ onSubmit, loading }) => {
  const [text, setText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (text.trim() && !loading) {
      onSubmit(text)
      setText('')
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
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste or type your news article here..."
          className="input-field min-h-[200px] resize-none"
          disabled={loading}
        />
        <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          {text.length} characters
        </div>
      </div>
      <motion.button
        type="submit"
        disabled={!text.trim() || loading}
        className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        whileHover={{ scale: loading ? 1 : 1.02 }}
        whileTap={{ scale: loading ? 1 : 0.98 }}
      >
        {loading ? (
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : (
          <>
            <PaperAirplaneIcon className="w-5 h-5" />
            <span>Analyze News</span>
          </>
        )}
      </motion.button>
    </motion.form>
  )
}

