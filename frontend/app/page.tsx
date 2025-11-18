'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '../src/components/Header';
import { TestCaseList } from '../src/components/TestCaseList';
import { Footer } from '../src/components/Footer';
import { testCasesAPI, exportAPI } from '../src/api/client';
import type { TestCase } from '../src/types';

export default function HomePage() {
  const router = useRouter();
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [selectedTestCaseIds, setSelectedTestCaseIds] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTestCases();
  }, []);

  const loadTestCases = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await testCasesAPI.getAll();
      setTestCases(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load test cases');
      console.error('Error loading test cases:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTestCase = (id: number) => {
    setSelectedTestCaseIds(prevIds => {
      const newIds = new Set(prevIds);
      if (newIds.has(id)) {
        newIds.delete(id);
      } else {
        newIds.add(id);
      }
      return newIds;
    });
  };

  const handleViewDetail = (testCase: TestCase) => {
    router.push(`/test-case/${testCase.id}`);
  };

  const handleExport = async () => {
    if (selectedTestCaseIds.size === 0) {
      alert('No test cases selected for export.');
      return;
    }

    try {
      const testCaseIds = Array.from(selectedTestCaseIds);
      const blob = await exportAPI.exportToExcel({ test_case_ids: testCaseIds });
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Generate filename with timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
      link.download = `test_cases_export_${timestamp}.xlsx`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to export test cases');
      console.error('Error exporting test cases:', err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full">
        {loading && (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading test cases...</p>
          </div>
        )}
        {error && (
          <div className="text-center py-12">
            <p className="text-red-600 dark:text-red-400">Error: {error}</p>
            <button 
              onClick={loadTestCases}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Retry
            </button>
          </div>
        )}
        {!loading && !error && (
          <TestCaseList
            testCases={testCases}
            selectedTestCaseIds={selectedTestCaseIds}
            onSelectTestCase={handleSelectTestCase}
            onViewDetail={handleViewDetail}
          />
        )}
      </main>
      <Footer 
        selectedCount={selectedTestCaseIds.size} 
        onExport={handleExport}
      />
    </div>
  );
}
