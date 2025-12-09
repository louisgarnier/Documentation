'use client';

import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="py-4 sm:py-6 px-4 sm:px-6 lg:px-8 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm sticky top-0 z-10 border-b border-gray-200 dark:border-gray-700/50">
      <div className="max-w-7xl mx-auto">
        <div className="flex-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
            Test Case Manager
          </h1>
          <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 mt-1">
            Review, select, and manage your test cases with ease.
          </p>
        </div>
      </div>
    </header>
  );
};

