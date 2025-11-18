
import React, { useState, useCallback } from 'react';
import { TestCase } from './types';
import { MOCK_TEST_CASES } from './constants';
import { Header } from './components/Header';
import { TestCaseList } from './components/TestCaseList';
import { TestCaseDetail } from './components/TestCaseDetail';
import { Footer } from './components/Footer';

type ViewState = 
  | { name: 'list' }
  | { name: 'detail'; testCase: TestCase };

const App: React.FC = () => {
  const [testCases] = useState<TestCase[]>(MOCK_TEST_CASES);
  const [selectedTestCaseIds, setSelectedTestCaseIds] = useState<Set<string>>(new Set());
  const [currentView, setCurrentView] = useState<ViewState>({ name: 'list' });

  const handleSelectTestCase = useCallback((id: string) => {
    setSelectedTestCaseIds(prevIds => {
      const newIds = new Set(prevIds);
      if (newIds.has(id)) {
        newIds.delete(id);
      } else {
        newIds.add(id);
      }
      return newIds;
    });
  }, []);

  const handleViewDetail = useCallback((testCase: TestCase) => {
    setCurrentView({ name: 'detail', testCase });
    window.scrollTo(0, 0);
  }, []);

  const handleGoBack = useCallback(() => {
    setCurrentView({ name: 'list' });
  }, []);

  const handleExport = useCallback(() => {
    if (selectedTestCaseIds.size === 0) {
      alert('No test cases selected for export.');
      return;
    }
    const idsToExport = Array.from(selectedTestCaseIds).join(', ');
    alert(`Exporting the following test cases:\n${idsToExport}`);
  }, [selectedTestCaseIds]);

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />
      <main className="flex-grow max-w-7xl mx-auto w-full">
        {currentView.name === 'list' ? (
          <TestCaseList
            testCases={testCases}
            selectedTestCaseIds={selectedTestCaseIds}
            onSelectTestCase={handleSelectTestCase}
            onViewDetail={handleViewDetail}
          />
        ) : (
          <TestCaseDetail
            testCase={currentView.testCase}
            onGoBack={handleGoBack}
          />
        )}
      </main>
      {currentView.name === 'list' && (
        <Footer 
            selectedCount={selectedTestCaseIds.size} 
            onExport={handleExport} 
        />
      )}
    </div>
  );
};

export default App;
