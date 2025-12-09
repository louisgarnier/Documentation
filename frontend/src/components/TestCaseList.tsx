'use client';

import React from 'react';
import { TestCase, Project } from '@/src/types';
import { TestCaseItem } from './TestCaseItem';

interface TestCaseListProps {
  testCases: TestCase[];
  selectedTestCaseIds: Set<number>;
  onSelectTestCase: (id: number) => void;
  onViewDetail: (testCase: TestCase) => void;
  onDuplicate?: (testCaseId: number, targetProjectId?: number) => void;
  onMove?: (testCaseId: number, targetProjectId: number | null) => void;
  currentProjectId?: number;
  allProjects?: Project[];
  onRefreshProjects?: () => void;
}

export const TestCaseList: React.FC<TestCaseListProps> = ({ 
  testCases, 
  selectedTestCaseIds, 
  onSelectTestCase, 
  onViewDetail,
  onDuplicate,
  onMove,
  currentProjectId,
  allProjects = [],
  onRefreshProjects
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
          onDuplicate={onDuplicate}
          onMove={onMove}
          currentProjectId={currentProjectId}
          allProjects={allProjects}
          onRefreshProjects={onRefreshProjects}
        />
      ))}
    </div>
  );
};

