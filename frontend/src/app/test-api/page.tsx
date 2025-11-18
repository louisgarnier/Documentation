'use client';

/**
 * Test page to verify API connection
 * This is a temporary page for testing the API client
 */

import { useEffect, useState } from 'react';
import { testCasesAPI, healthAPI } from '@/api/client';
import type { TestCase } from '@/types';

export default function TestAPIPage() {
  const [healthStatus, setHealthStatus] = useState<string>('Checking...');
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function testConnection() {
      try {
        // Test health endpoint
        const health = await healthAPI.check();
        setHealthStatus(health.status);

        // Test test cases endpoint
        const cases = await testCasesAPI.getAll();
        setTestCases(cases);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setHealthStatus('Error');
      } finally {
        setLoading(false);
      }
    }

    testConnection();
  }, []);

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">API Connection Test</h1>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Health Check</h2>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              healthStatus === 'healthy' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {healthStatus}
            </span>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <h3 className="text-red-800 font-semibold mb-2">Error</h3>
            <p className="text-red-700">{error}</p>
            <p className="text-sm text-red-600 mt-2">
              Make sure the backend API is running on http://localhost:8000
            </p>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Cases</h2>
          {loading ? (
            <p>Loading...</p>
          ) : testCases.length > 0 ? (
            <div className="space-y-2">
              <p className="text-sm text-gray-600 mb-4">
                Found {testCases.length} test case(s)
              </p>
              <div className="space-y-2">
                {testCases.map((tc) => (
                  <div
                    key={tc.id}
                    className="border border-gray-200 rounded p-3 hover:bg-gray-50"
                  >
                    <div className="font-semibold">{tc.test_number}</div>
                    <div className="text-sm text-gray-600">{tc.description}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      Created: {new Date(tc.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-gray-600">No test cases found</p>
          )}
        </div>

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> This is a test page. Once API connection is verified,
            you can delete this page and continue with the main implementation.
          </p>
        </div>
      </div>
    </div>
  );
}

