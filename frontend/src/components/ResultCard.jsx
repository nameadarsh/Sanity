import { CheckCircleIcon, XCircleIcon, ShieldCheckIcon } from '@heroicons/react/24/solid'
import { motion } from 'framer-motion'
import { usePredictionStore } from '../store/usePredictionStore'
import { useNavigate } from 'react-router-dom'

export const ResultCard = () => {
  const { prediction } = usePredictionStore()
  const navigate = useNavigate()

  if (!prediction) return null

  // When LLM auto-verification exists, use its prediction; otherwise use model's prediction
  const finalPrediction = prediction.auto_verification?.prediction || prediction.label
  const isReal = finalPrediction === 'Real'
  const isLLMVerified = !!prediction.auto_verification
  const reasoning = prediction.auto_verification?.reasoning

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          {isLLMVerified ? 'AI Verification Result' : 'Prediction Result'}
        </h2>
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
        >
          {isLLMVerified ? (
            <ShieldCheckIcon className={`w-12 h-12 ${isReal ? 'text-success-500' : 'text-danger-500'}`} />
          ) : (
            isReal ? (
              <CheckCircleIcon className="w-12 h-12 text-success-500" />
            ) : (
              <XCircleIcon className="w-12 h-12 text-danger-500" />
            )
          )}
        </motion.div>
      </div>

      <div className="space-y-6">
        {/* Final Prediction Label */}
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <span
              className={`text-3xl font-bold ${
                isReal ? 'text-success-600' : 'text-danger-600'
              }`}
            >
              {finalPrediction}
            </span>
            {isLLMVerified && (
              <span className="px-3 py-1 text-xs font-semibold bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 rounded-full">
                AI Verified
              </span>
            )}
          </div>
        </div>

        {/* LLM Reasoning (only shown when auto-verification exists) */}
        {isLLMVerified && reasoning && (
          <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl border border-gray-200 dark:border-gray-600">
            <div className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Verification Reasoning
            </div>
            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              {reasoning}
            </p>
          </div>
        )}

        {/* Action Button */}
        <motion.button
          onClick={() => navigate('/chat')}
          className="btn-primary w-full"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          Ask Follow-up Questions
        </motion.button>
      </div>
    </motion.div>
  )
}

