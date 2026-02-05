'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import DocumentManager from './DocumentManager';
import { SparklesIcon, DocumentTextIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function KnowledgeBaseChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: '👋 Hello! I\'m your AI Knowledge Base Assistant. I can help you find information from your uploaded documents. Ask me anything!',
      sources: [],
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showDocuments, setShowDocuments] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/`);
      setApiStatus(response.data.gemini_configured ? 'ready' : 'warning');
    } catch (error) {
      setApiStatus('error');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/query`, {
        query: input,
        top_k: 5
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources || [],
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `❌ Sorry, I encountered an error: ${error.response?.data?.detail || error.message}. Please make sure the backend is running and configured correctly.`,
        sources: [],
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQuestions = [
    "What are the pricing plans available?",
    "How do I integrate the API?",
    "What's the refund policy?",
    "How to troubleshoot authentication issues?"
  ];

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col"
      >
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg">
              <SparklesIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                AI Knowledge Base
              </h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Powered by Gemini & RAG
              </p>
            </div>
          </div>

          {/* API Status */}
          <div className="flex items-center gap-2 text-sm">
            <div className={`w-2 h-2 rounded-full ${
              apiStatus === 'ready' ? 'bg-green-500 animate-pulse' :
              apiStatus === 'warning' ? 'bg-yellow-500' :
              apiStatus === 'error' ? 'bg-red-500' : 'bg-gray-400'
            }`} />
            <span className="text-gray-600 dark:text-gray-300">
              {apiStatus === 'ready' ? 'API Connected' :
               apiStatus === 'warning' ? 'API Key Not Set' :
               apiStatus === 'error' ? 'API Offline' : 'Checking...'}
            </span>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex-1 overflow-y-auto p-4">
          <nav className="space-y-2">
            <button
              onClick={() => setShowDocuments(false)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                !showDocuments
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <SparklesIcon className="w-5 h-5" />
              <span className="font-medium">Chat</span>
            </button>
            
            <button
              onClick={() => setShowDocuments(true)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                showDocuments
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <DocumentTextIcon className="w-5 h-5" />
              <span className="font-medium">Documents</span>
            </button>
          </nav>

          {/* Suggested Questions */}
          {!showDocuments && messages.length <= 1 && (
            <div className="mt-8">
              <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 px-2">
                💡 Try asking:
              </h3>
              <div className="space-y-2">
                {suggestedQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => setInput(question)}
                    className="w-full text-left text-sm p-3 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400">
          <p>🚀 Built with Next.js & FastAPI</p>
          <p className="mt-1">🤖 Powered by Google Gemini</p>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {showDocuments ? (
          <DocumentManager />
        ) : (
          <>
            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6">
              <div className="max-w-4xl mx-auto space-y-6">
                <AnimatePresence>
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                </AnimatePresence>

                {isLoading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center gap-3 text-gray-500"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                      <SparklesIcon className="w-5 h-5 text-white animate-pulse" />
                    </div>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                      <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </motion.div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
              <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about your documents..."
                    className="flex-1 px-4 py-3 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
                  >
                    Send
                  </button>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                  Press Enter to send • Powered by Gemini
                </p>
              </form>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
