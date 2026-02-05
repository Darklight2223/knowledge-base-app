'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { 
  DocumentTextIcon, 
  TrashIcon, 
  CloudArrowUpIcon,
  CheckCircleIcon,
  XCircleIcon 
} from '@heroicons/react/24/outline';
import { format } from 'date-fns';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function DocumentManager() {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/documents`);
      setDocuments(response.data);
    } catch (error) {
      showNotification('Failed to load documents', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type - Only PDF allowed
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      showNotification('Only PDF files are allowed', 'error');
      event.target.value = '';
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      showNotification('File size must be less than 10MB', 'error');
      event.target.value = '';
      return;
    }

    setUploadingFile(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      await axios.post(`${API_URL}/api/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      showNotification(`${file.name} uploaded successfully!`, 'success');
      loadDocuments();
    } catch (error) {
      showNotification(
        error.response?.data?.detail || 'Failed to upload document',
        'error'
      );
    } finally {
      setUploadingFile(false);
      event.target.value = ''; // Reset file input
    }
  };

  const handleDelete = async (docId, filename) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) return;

    try {
      await axios.delete(`${API_URL}/api/documents/${docId}`);
      showNotification('Document deleted successfully', 'success');
      loadDocuments();
    } catch (error) {
      showNotification('Failed to delete document', 'error');
    }
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const getFileIcon = (docType) => {
    switch (docType) {
      case 'pdf':
        return '📕';
      case 'text':
        return '📄';
      default:
        return '📄';
    }
  };

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Document Manager
              </h2>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Upload and manage your knowledge base documents
              </p>
            </div>

            {/* Upload Button */}
            <label className="cursor-pointer">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileUpload}
                className="hidden"
                disabled={uploadingFile}
              />
              <div className={`flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl ${
                uploadingFile ? 'opacity-50 cursor-not-allowed' : ''
              }`}>
                <CloudArrowUpIcon className="w-5 h-5" />
                {uploadingFile ? 'Uploading...' : 'Upload Document'}
              </div>
            </label>
          </div>
        </div>
      </div>

      {/* Notification */}
      <AnimatePresence>
        {notification && (
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="fixed top-4 right-4 z-50"
          >
            <div className={`flex items-center gap-3 px-6 py-4 rounded-xl shadow-lg ${
              notification.type === 'success'
                ? 'bg-green-500 text-white'
                : 'bg-red-500 text-white'
            }`}>
              {notification.type === 'success' ? (
                <CheckCircleIcon className="w-6 h-6" />
              ) : (
                <XCircleIcon className="w-6 h-6" />
              )}
              <span className="font-medium">{notification.message}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Documents List */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-6xl mx-auto">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
                <p className="text-gray-500 dark:text-gray-400">Loading documents...</p>
              </div>
            </div>
          ) : documents.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center justify-center h-64 text-center"
            >
              <div className="w-24 h-24 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
                <DocumentTextIcon className="w-12 h-12 text-gray-400 dark:text-gray-500" />
              </div>
              <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
                No documents yet
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mb-6">
                Upload your first document to get started with the AI assistant
              </p>
              <label className={`${uploadingFile ? 'pointer-events-none' : 'cursor-pointer'}`}>
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={uploadingFile}
                />
                <div className={`flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition-all shadow-lg ${
                  uploadingFile ? 'opacity-50 cursor-not-allowed' : ''
                }`}>
                  <CloudArrowUpIcon className="w-5 h-5" />
                  {uploadingFile ? 'Uploading...' : 'Upload Your First Document'}
                </div>
              </label>
            </motion.div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <AnimatePresence>
                {documents.map((doc, idx) => (
                  <motion.div
                    key={doc.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ delay: idx * 0.05 }}
                    className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 hover:shadow-lg transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <span className="text-3xl">{getFileIcon(doc.doc_type)}</span>
                        <div className="flex-1 min-w-0">
                          <h3 className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                            {doc.filename}
                          </h3>
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {doc.chunk_count} chunks
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDelete(doc.id, doc.filename)}
                        className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                        title="Delete document"
                      >
                        <TrashIcon className="w-5 h-5" />
                      </button>
                    </div>

                    <div className="border-t border-gray-200 dark:border-gray-700 pt-3 space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-500 dark:text-gray-400">Type</span>
                        <span className="text-gray-700 dark:text-gray-300 font-medium uppercase">
                          {doc.doc_type}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-gray-500 dark:text-gray-400">Uploaded</span>
                        <span className="text-gray-700 dark:text-gray-300 font-medium">
                          {doc.upload_date ? format(new Date(doc.upload_date), 'MMM d, yyyy') : 'N/A'}
                        </span>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          )}

          {/* Upload Instructions */}
          {documents.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-8 p-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl"
            >
              <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2 flex items-center gap-2">
                <DocumentTextIcon className="w-5 h-5" />
                Supported File Types
              </h3>
              <p className="text-sm text-blue-800 dark:text-blue-300">
                <strong>PDF:</strong> .pdf (max 10MB)
              </p>
              <p className="text-xs text-blue-700 dark:text-blue-400 mt-2">
                💡 Tip: Documents are automatically split into chunks and embedded for optimal retrieval.
              </p>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
