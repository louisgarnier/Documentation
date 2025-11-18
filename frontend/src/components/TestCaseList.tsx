'use client';

import React from 'react';
import { TestCase } from '@/src/types';
import { TestCaseItem } from './TestCaseItem';

interface TestCaseListProps {
  testCases: TestCase[];
  selectedTestCaseIds: Set<number>;
  onSelectTestCase: (id: number) => void;
  onViewDetail: (testCase: TestCase) => void;
}

export const TestCaseList: React.FC<TestCaseListProps> = ({ 
  testCases, 
  selectedTestCaseIds, 
  onSelectTestCase, 
  onViewDetail 
}) => {
  if (testCases.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          No test cases yet. Create your first test case to get started!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4 sm:p-6 lg:p-8">
      {testCases.map((testCase) => (
        <TestCaseItem
          key={testCase.id}
          testCase={testCase}
          isSelected={selectedTestCaseIds.has(testCase.id)}
          onSelect={onSelectTestCase}
          onViewDetail={onViewDetail}
        />
      ))}
    </div>
  );
};

