'use client';

import KnowledgeBaseChat from '@/components/KnowledgeBaseChat';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-slate-900 dark:to-indigo-950">
      <KnowledgeBaseChat />
    </div>
  );
}
