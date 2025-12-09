'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Header } from '../../../src/components/Header';
import { TestCaseForm } from '../../../src/components/TestCaseForm';
import { testCasesAPI } from '../../../src/api/client';

export default function CreateTestCasePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const projectId = searchParams.get('project_id');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async (data: { test_number: string; description: string }) => {
    try {
      setLoading(true);
      setError(null);
      const projectIdNum = projectId ? parseInt(projectId) : undefined;
      const newTestCase = await testCasesAPI.create({
        ...data,
        project_id: projectIdNum || null
      });
      
      // Redirect to project page if project_id was provided, otherwise to test case detail
      if (projectIdNum) {
        router.push(`/project/${projectIdNum}`);
      } else {
        router.push(`/test-case/${newTestCase.id}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create test case');
      throw err; // Re-throw to let the form handle it
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (projectId) {
      router.push(`/project/${projectId}`);
    } else {
      router.push('/');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            Create New Test Case
          </h1>
          {error && (
            <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
              {error}
            </div>
          )}
          <TestCaseForm
            onSave={handleSave}
            onCancel={handleCancel}
            loading={loading}
          />
        </div>
      </main>
    </div>
  );
}

