'use client';

import React, { useState, useEffect } from 'react';
import { TestCase } from '@/src/types';

interface TestCaseFormProps {
  testCase?: TestCase | null;
  onSave: (data: { test_number: string; description: string }) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

export const TestCaseForm: React.FC<TestCaseFormProps> = ({
  testCase,
  onSave,
  onCancel,
  loading = false,
}) => {
  const [testNumber, setTestNumber] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (testCase) {
      setTestNumber(testCase.test_number);
      setDescription(testCase.description);
    } else {
      setTestNumber('');
      setDescription('');
    }
    setError(null);
  }, [testCase]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!testNumber.trim()) {
      setError('Test Number is required');
      return;
    }

    if (!description.trim()) {
      setError('Description is required');
      return;
    }

    try {
      await onSave({ test_number: testNumber.trim(), description: description.trim() });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save test case');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="test_number" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Test Number *
        </label>
        <input
          type="text"
          id="test_number"
          value={testNumber}
          onChange={(e) => setTestNumber(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="e.g., TC01, TC02"
          required
          disabled={loading}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description *
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Describe the test case..."
          required
          disabled={loading}
        />
      </div>

      <div className="flex justify-end space-x-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="px-6 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Saving...' : testCase ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  );
};

