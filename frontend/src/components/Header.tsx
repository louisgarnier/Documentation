'use client';

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';

export const Header: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();
  const isHomePage = pathname === '/';

  const handleCreateNew = () => {
    router.push('/test-case/new');
  };

  return (
    <header className="py-6 px-4 sm:px-6 lg:px-8 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm sticky top-0 z-10 border-b border-gray-200 dark:border-gray-700/50">
      <div className="max-w-7xl mx-auto flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
            Test Case Manager
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Review, select, and manage your test cases with ease.
          </p>
        </div>
        {isHomePage && (
          <div className="flex items-center">
            <button
              onClick={handleCreateNew}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors"
            >
              ➕ Create New Test Case
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

