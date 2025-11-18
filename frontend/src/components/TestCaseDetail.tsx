'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { TestCase, TestStep } from '@/src/types';
import { ChevronLeftIcon } from './icons/ChevronLeftIcon';

interface TestCaseDetailProps {
  testCase: TestCase;
  steps: TestStep[];
}

export const TestCaseDetail: React.FC<TestCaseDetailProps> = ({ testCase, steps }) => {
  const router = useRouter();

  const formattedDate = new Date(testCase.created_at).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  const handleGoBack = () => {
    router.push('/');
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8">
      <button
        onClick={handleGoBack}
        className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 mb-6 font-semibold transition-colors duration-200"
      >
        <ChevronLeftIcon className="w-5 h-5" />
        <span>Back to List</span>
      </button>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="flex flex-col sm:flex-row justify-between sm:items-center border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{testCase.test_number}</h2>
            <p className="text-gray-600 dark:text-gray-400 mt-1">{testCase.description}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">Test Steps</h3>
            {steps.length === 0 ? (
              <p className="text-gray-500 dark:text-gray-500">No steps yet. Add steps to document this test case.</p>
            ) : (
              <ol className="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400">
                {steps
                  .sort((a, b) => a.step_number - b.step_number)
                  .map((step) => (
                    <li key={step.id}>
                      <span className="font-medium">Step {step.step_number}:</span> {step.description}
                    </li>
                  ))}
              </ol>
            )}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">Details</h3>
            <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-md">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                <span className="font-medium">Created:</span> {formattedDate}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

