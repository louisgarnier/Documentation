'use client';

import { Header } from '@/components/Header';

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Welcome to Test Case Documentation Tool
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Interface en cours de développement...
          </p>
        </div>
      </main>
    </div>
  );
}

