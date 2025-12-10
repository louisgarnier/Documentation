'use client';

import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { TestCase, Project } from '@/src/types';
import { TestCaseItem } from './TestCaseItem';

interface SortableTestCaseItemProps {
  testCase: TestCase;
  isSelected: boolean;
  onSelect: (id: number) => void;
  onViewDetail: (testCase: TestCase) => void;
  onDuplicate?: (testCaseId: number, targetProjectId?: number) => void;
  onMove?: (testCaseId: number, targetProjectId: number | null) => void;
  currentProjectId?: number;
  allProjects?: Project[];
  onRefreshProjects?: () => void;
}

export const SortableTestCaseItem: React.FC<SortableTestCaseItemProps> = ({
  testCase,
  isSelected,
  onSelect,
  onViewDetail,
  onDuplicate,
  onMove,
  currentProjectId,
  allProjects,
  onRefreshProjects,
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: testCase.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} className={`${isDragging ? 'z-50' : ''}`}>
      <div className="relative">
        {/* Drag handle - vertical dots on the left */}
        <div
          {...attributes}
          {...listeners}
          className="absolute left-0 top-0 bottom-0 w-8 cursor-grab active:cursor-grabbing flex items-center justify-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          style={{ touchAction: 'none' }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col space-y-1">
            <span className="text-lg leading-none">⋮</span>
            <span className="text-lg leading-none">⋮</span>
          </div>
        </div>
        <div className="pl-10">
          <TestCaseItem
            testCase={testCase}
            isSelected={isSelected}
            onSelect={onSelect}
            onViewDetail={onViewDetail}
            onDuplicate={onDuplicate}
            onMove={onMove}
            currentProjectId={currentProjectId}
            allProjects={allProjects}
            onRefreshProjects={onRefreshProjects}
          />
        </div>
      </div>
    </div>
  );
};

