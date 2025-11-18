'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Header } from '../../../src/components/Header';
import { TestCaseDetail } from '../../../src/components/TestCaseDetail';
import { testCasesAPI, stepsAPI } from '../../../src/api/client';
import type { TestCase, TestStep } from '../../../src/types';

export default function TestCaseDetailPage() {
  const params = useParams();
  const testCaseId = parseInt(params.id as string, 10);

  const [testCase, setTestCase] = useState<TestCase | null>(null);
  const [steps, setSteps] = useState<TestStep[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isNaN(testCaseId)) {
      setError('Invalid test case ID');
      setLoading(false);
      return;
    }

    loadTestCaseData();
  }, [testCaseId]);

  const loadTestCaseData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load test case and steps in parallel
      const [testCaseData, stepsData] = await Promise.all([
        testCasesAPI.getById(testCaseId),
        stepsAPI.getByTestCaseId(testCaseId),
      ]);

      setTestCase(testCaseData);
      setSteps(stepsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load test case');
      console.error('Error loading test case:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="flex-grow max-w-7xl mx-auto w-full">
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading test case...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error || !testCase) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="flex-grow max-w-7xl mx-auto w-full">
          <div className="text-center py-12">
            <p className="text-red-600 dark:text-red-400">Error: {error || 'Test case not found'}</p>
            <button
              onClick={() => window.location.href = '/'}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Back to List
            </button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full">
        <TestCaseDetail testCase={testCase} steps={steps} />
      </main>
    </div>
  );
}

