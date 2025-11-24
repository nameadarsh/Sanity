import { ShieldCheckIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'
import { usePredictionStore } from '../store/usePredictionStore'

/**
 * VerificationCard is now deprecated - verification results are shown in ResultCard.
 * This component is kept for backward compatibility but returns null.
 */
export const VerificationCard = () => {
  // Verification is now integrated into ResultCard
  // This component is hidden to avoid duplicate display
  return null
}

