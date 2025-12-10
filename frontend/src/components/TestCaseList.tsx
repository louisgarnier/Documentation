'use client';

import React from 'react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { TestCase, Project } from '@/src/types';
import { SortableTestCaseItem } from './SortableTestCaseItem';
import { TestCaseItem } from './TestCaseItem';

interface TestCaseListProps {
  testCases: TestCase[];
  selectedTestCaseIds: Set<number>;
  onSelectTestCase: (id: number) => void;
  onViewDetail: (testCase: TestCase) => void;
  onDuplicate?: (testCaseId: number, targetProjectId?: number) => void;
  onMove?: (testCaseId: number, targetProjectId: number | null) => void;
  onReorder?: (testCaseIds: number[]) => void;
  currentProjectId?: number;
  allProjects?: Project[];
  onRefreshProjects?: () => void;
  reordering?: boolean;
}

export const TestCaseList: React.FC<TestCaseListProps> = ({ 
  testCases, 
  selectedTestCaseIds, 
  onSelectTestCase, 
  onViewDetail,
  onDuplicate,
  onMove,
  onReorder,
  currentProjectId,
  allProjects = [],
  onRefreshProjects,
  reordering = false
}) => {
  // Configure sensors for drag and drop
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over || active.id === over.id || !onReorder) {
      return;
    }

    const activeId = active.id as number;
    const overId = over.id as number;

    // Find the test cases
    const activeTestCase = testCases.find(tc => tc.id === activeId);
    const overTestCase = testCases.find(tc => tc.id === overId);

    if (!activeTestCase || !overTestCase) {
      return;
    }

    // Calculate new order
    const sortedTestCases = [...testCases].sort((a, b) => {
      const orderA = a.display_order ?? 999999;
      const orderB = b.display_order ?? 999999;
      return orderA - orderB;
    });
    
    const activeIndex = sortedTestCases.findIndex(tc => tc.id === activeId);
    const overIndex = sortedTestCases.findIndex(tc => tc.id === overId);

    // Create new order array
    const newOrder = [...sortedTestCases];
    const [removed] = newOrder.splice(activeIndex, 1);
    newOrder.splice(overIndex, 0, removed);

    // Extract IDs in new order
    const newOrderIds = newOrder.map(tc => tc.id);

    // Call reorder callback
    onReorder(newOrderIds);
  };

  if (testCases.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          No test cases yet. Create your first test case to get started!
        </p>
      </div>
    );
  }

  // Sort test cases by display_order
  const sortedTestCases = [...testCases].sort((a, b) => {
    const orderA = a.display_order ?? 999999;
    const orderB = b.display_order ?? 999999;
    return orderA - orderB;
  });

  return (
    <div className="space-y-4 p-4 sm:p-6 lg:p-8">
      {onReorder ? (
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={sortedTestCases.map(tc => tc.id)}
            strategy={verticalListSortingStrategy}
          >
            {sortedTestCases.map((testCase) => (
              <SortableTestCaseItem
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
          </SortableContext>
        </DndContext>
      ) : (
        sortedTestCases.map((testCase) => (
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
        ))
      )}
    </div>
  );
};

