import { useState } from 'react'
import { TextInput } from './TextInput'
import { FileUpload } from './FileUpload'
import { UrlInput } from './UrlInput'
import { DocumentTextIcon, LinkIcon, DocumentIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'

const tabs = [
  { id: 'text', label: 'Text', icon: DocumentTextIcon },
  { id: 'url', label: 'URL', icon: LinkIcon },
  { id: 'pdf', label: 'PDF', icon: DocumentIcon },
]

export const UploadCard = ({ onTextSubmit, onUrlSubmit, onFileUpload, loading }) => {
  const [activeTab, setActiveTab] = useState('text')

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="card"
    >
      <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">
        Upload News Content
      </h2>

      {/* Tabs */}
      <div className="flex space-x-2 mb-6 bg-gray-100 dark:bg-gray-700 p-1 rounded-xl">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = activeTab === tab.id
          return (
            <motion.button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-lg font-medium transition-all duration-200 ${
                isActive
                  ? 'bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Icon className="w-5 h-5" />
              <span className="hidden sm:inline">{tab.label}</span>
            </motion.button>
          )
        })}
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        {activeTab === 'text' && (
          <TextInput onSubmit={onTextSubmit} loading={loading} />
        )}
        {activeTab === 'url' && (
          <UrlInput onSubmit={onUrlSubmit} loading={loading} />
        )}
        {activeTab === 'pdf' && (
          <FileUpload onSubmit={onFileUpload} loading={loading} />
        )}
      </motion.div>
    </motion.div>
  )
}

