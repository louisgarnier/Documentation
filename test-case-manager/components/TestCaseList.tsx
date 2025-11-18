
import React from 'react';
import { TestCase } from '../types';
import { TestCaseItem } from './TestCaseItem';

interface TestCaseListProps {
  testCases: TestCase[];
  selectedTestCaseIds: Set<string>;
  onSelectTestCase: (id: string) => void;
  onViewDetail: (testCase: TestCase) => void;
}

export const TestCaseList: React.FC<TestCaseListProps> = ({ testCases, selectedTestCaseIds, onSelectTestCase, onViewDetail }) => {
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
