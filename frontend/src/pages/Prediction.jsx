import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ResultCard } from '../components/ResultCard'
import { VerificationCard } from '../components/VerificationCard'
import { CardSkeleton } from '../components/Loaders/Skeleton'
import { usePredictionStore } from '../store/usePredictionStore'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'

export const Prediction = () => {
  const { prediction, isLoading } = usePredictionStore()
  const navigate = useNavigate()

  useEffect(() => {
    if (!prediction && !isLoading) {
      navigate('/')
    }
  }, [prediction, isLoading, navigate])

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <CardSkeleton />
      </div>
    )
  }

  if (!prediction) return null

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen"
    >
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 mb-8 transition-colors"
          whileHover={{ x: -5 }}
        >
          <ArrowLeftIcon className="w-5 h-5" />
          <span>Back to Home</span>
        </motion.button>

        <div className="space-y-6">
          <ResultCard />
          <VerificationCard />
        </div>
      </div>
    </motion.div>
  )
}

