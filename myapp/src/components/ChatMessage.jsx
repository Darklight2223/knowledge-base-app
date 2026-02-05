'use client';

import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { UserCircleIcon, SparklesIcon, DocumentTextIcon } from '@heroicons/react/24/solid';

export default function ChatMessage({ message }) {
  const isUser = message.type === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
        isUser
          ? 'bg-gradient-to-br from-purple-500 to-pink-500'
          : 'bg-gradient-to-br from-blue-500 to-indigo-600'
      }`}>
        {isUser ? (
          <UserCircleIcon className="w-6 h-6 text-white" />
        ) : (
          <SparklesIcon className="w-6 h-6 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        <div
          className={`max-w-3xl rounded-2xl px-5 py-4 ${
            isUser
              ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
              : message.isError
              ? 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-900 dark:text-red-200'
              : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 shadow-sm'
          }`}
        >
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        </div>

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-3 space-y-2"
          >
            <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 font-medium">
              <DocumentTextIcon className="w-4 h-4" />
              <span>Sources ({message.sources.length})</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-3xl">
              {message.sources.map((source, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className="p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-xs"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-gray-900 dark:text-gray-100 truncate">
                      <span className="bg-indigo-500 text-white px-2 py-0.5 rounded-full mr-2 text-[10px]">
                        {idx + 1}
                      </span>
                      📄 {source.document_name}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 mb-1 flex-wrap">
                    {source.page_number && (
                      <span className="bg-blue-100 dark:bg-blue-900/30 px-2 py-0.5 rounded">
                        📖 Page {source.page_number}
                      </span>
                    )}
                    <span>📍 Lines {source.start_line || 1}-{source.end_line || source.start_line || 1}</span>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 line-clamp-2">
                    {source.chunk_text}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
