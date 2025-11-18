'use client';

import React, { useState } from 'react';

interface FooterProps {
  selectedCount: number;
  onExport: () => Promise<void>;
}

export const Footer: React.FC<FooterProps> = ({ selectedCount, onExport }) => {
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    if (selectedCount === 0) {
      setError('Please select at least one test case to export.');
      return;
    }

    try {
      setExporting(true);
      setError(null);
      await onExport();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export test cases');
      console.error('Error exporting test cases:', err);
    } finally {
      setExporting(false);
    }
  };

  if (selectedCount === 0) {
    return null; // Don't show footer if nothing is selected
  }

  return (
    <footer className="sticky bottom-0 z-10 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
          <div className="flex items-center">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {selectedCount} {selectedCount === 1 ? 'test case' : 'test cases'} selected
            </span>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-4 w-full sm:w-auto">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-3 py-2 rounded text-sm">
                {error}
              </div>
            )}
            <button
              onClick={handleExport}
              disabled={exporting}
              className="px-4 sm:px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm sm:text-base"
            >
              {exporting ? 'Exporting...' : 'Export to Excel'}
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

