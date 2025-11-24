import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ChatBubble } from '../components/ChatBubble'
import { CardSkeleton } from '../components/Loaders/Skeleton'
import { usePredictionStore } from '../store/usePredictionStore'
import { askQuestion } from '../lib/api'
import { PaperAirplaneIcon, ArrowLeftIcon } from '@heroicons/react/24/outline'

export const Chat = () => {
  const { prediction, contextId, chatHistory, addChatMessage, setLoading, setError } =
    usePredictionStore()
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const chatEndRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Initialize chat with prediction context if available
    if (prediction && chatHistory.length === 0) {
      // Use LLM prediction if available, otherwise use model prediction
      const finalPrediction = prediction.auto_verification?.prediction || prediction.label
      const isLLMVerified = !!prediction.auto_verification
      const verificationNote = isLLMVerified ? ' (verified by AI)' : ''
      
      addChatMessage({
        role: 'assistant',
        message: `I've analyzed your news article and determined it's ${finalPrediction}${verificationNote}. How can I help you understand this better?`,
        timestamp: new Date().toISOString(),
      })
    }
  }, [prediction, chatHistory.length, addChatMessage])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || sending) return

    const userMessage = input.trim()
    setInput('')

    // Add user message
    addChatMessage({
      role: 'user',
      message: userMessage,
      timestamp: new Date().toISOString(),
    })

    setSending(true)
    setLoading(true)

    try {
      // Determine if this is a follow-up question or direct question
      const payload = contextId
        ? {
            context_id: contextId,
            question: userMessage,
          }
        : {
            question: userMessage,
          }

      const response = await askQuestion(payload)

      // Add AI response
      addChatMessage({
        role: 'assistant',
        message: response.answer,
        timestamp: new Date().toISOString(),
      })
    } catch (error) {
      addChatMessage({
        role: 'assistant',
        message: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        timestamp: new Date().toISOString(),
      })
      setError(error.message)
    } finally {
      setSending(false)
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen flex flex-col"
    >
      <div className="max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 flex flex-col flex-1">
        {/* Header */}
        <motion.button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 mb-6 transition-colors self-start"
          whileHover={{ x: -5 }}
        >
          <ArrowLeftIcon className="w-5 h-5" />
          <span>Back</span>
        </motion.button>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col min-h-0">
          <div className="flex-1 overflow-y-auto mb-4 space-y-4 p-4">
            {chatHistory.length === 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center text-gray-500 dark:text-gray-400 py-12"
              >
                <p className="text-lg mb-2">Start a conversation</p>
                <p className="text-sm">
                  {prediction
                    ? 'Ask me anything about the analyzed article!'
                    : 'Ask me any general question, or analyze a news article first.'}
                </p>
              </motion.div>
            )}

            <AnimatePresence>
              {chatHistory.map((msg, index) => (
                <ChatBubble
                  key={index}
                  message={msg.message}
                  isUser={msg.role === 'user'}
                  timestamp={msg.timestamp}
                />
              ))}
            </AnimatePresence>

            {sending && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center space-x-2 text-gray-500 dark:text-gray-400"
              >
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </motion.div>
            )}

            <div ref={chatEndRef} />
          </div>

          {/* Input Area */}
          <motion.form
            onSubmit={handleSubmit}
            className="flex items-end space-x-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                prediction
                  ? 'Ask a follow-up question about the article...'
                  : 'Ask me anything...'
              }
              className="input-field flex-1"
              disabled={sending}
            />
            <motion.button
              type="submit"
              disabled={!input.trim() || sending}
              className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
              whileHover={{ scale: sending ? 1 : 1.05 }}
              whileTap={{ scale: sending ? 1 : 0.95 }}
            >
              {sending ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <PaperAirplaneIcon className="w-5 h-5" />
              )}
            </motion.button>
          </motion.form>
        </div>
      </div>
    </motion.div>
  )
}

