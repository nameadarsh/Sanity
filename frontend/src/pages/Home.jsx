import { motion } from 'framer-motion'
import { UploadCard } from '../components/UploadCard'
import { ResultCard } from '../components/ResultCard'
import { VerificationCard } from '../components/VerificationCard'
import { CardSkeleton } from '../components/Loaders/Skeleton'
import { useUploadHandler } from '../hooks/useUploadHandler'
import { usePredictionStore } from '../store/usePredictionStore'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
}

export const Home = () => {
  const { handleTextSubmit, handleUrlSubmit, handleFileUpload, uploading } =
    useUploadHandler()
  const { prediction, isLoading, error } = usePredictionStore()

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="min-h-screen"
    >
      {/* Hero Section */}
      <motion.section
        variants={itemVariants}
        className="text-center py-16 px-4 sm:py-24"
      >
        <motion.h1
          variants={itemVariants}
          className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6"
        >
          <span className="text-gradient">Sanity</span>
        </motion.h1>
        <motion.p
          variants={itemVariants}
          className="text-xl sm:text-2xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-12"
        >
          Detect Real vs Fake News with AI-Powered Analysis
        </motion.p>
      </motion.section>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <motion.div variants={itemVariants}>
          {isLoading || uploading ? (
            <CardSkeleton />
          ) : (
            <UploadCard
              onTextSubmit={handleTextSubmit}
              onUrlSubmit={handleUrlSubmit}
              onFileUpload={handleFileUpload}
              loading={isLoading || uploading}
            />
          )}
        </motion.div>

        {/* Error Display */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 p-4 bg-danger-50 dark:bg-danger-900/20 border border-danger-200 dark:border-danger-800 rounded-xl text-danger-800 dark:text-danger-200"
          >
            <p className="text-sm font-medium">{error}</p>
          </motion.div>
        )}

        {/* Results Preview */}
        {prediction && !isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-8 space-y-6"
          >
            <ResultCard />
            <VerificationCard />
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

