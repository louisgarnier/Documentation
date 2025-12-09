'use client';

import React, { useState } from 'react';
import { TestCase, Project } from '@/src/types';
import { CheckIcon } from './icons/CheckIcon';

interface TestCaseItemProps {
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

export const TestCaseItem: React.FC<TestCaseItemProps> = ({ 
  testCase, 
  isSelected, 
  onSelect, 
  onViewDetail,
  onDuplicate,
  onMove,
  currentProjectId,
  allProjects = [],
  onRefreshProjects
}) => {
  const { id, test_number, description, created_at } = testCase;
  const [showMoveMenu, setShowMoveMenu] = useState(false);

  const handleCheckboxClick = (e: React.MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    onSelect(id);
  };
  
  const handleCardClick = () => {
    onViewDetail(testCase);
  };

  const handleDuplicate = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDuplicate) {
      onDuplicate(id, currentProjectId);
    }
  };

  const handleMove = async (e: React.MouseEvent, targetProjectId: number | null) => {
    e.stopPropagation();
    setShowMoveMenu(false);
    if (onMove) {
      // Refresh projects before moving to ensure target still exists
      if (onRefreshProjects) {
        await onRefreshProjects();
      }
      await onMove(id, targetProjectId);
    }
  };

  const formattedDate = new Date(created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  // Filter out current project and ensure we only show projects that actually exist
  const otherProjects = allProjects.filter(p => p.id !== currentProjectId && p.id !== undefined && p.id !== null);

  return (
    <div 
      onClick={handleCardClick}
      className="bg-white dark:bg-gray-800 rounded-lg shadow-lg flex items-start p-4 space-x-4 cursor-pointer transition-all duration-200 hover:shadow-blue-500/20 hover:ring-2 hover:ring-blue-500/50"
    >
      <div
        onClick={handleCheckboxClick}
        className="flex-shrink-0 w-6 h-6 rounded-md border-2 flex items-center justify-center transition-all duration-200"
        style={{
          borderColor: isSelected ? 'hsl(210, 40%, 50%)' : 'hsl(222, 25%, 35%)',
          backgroundColor: isSelected ? 'hsl(210, 40%, 50%)' : 'transparent',
        }}
      >
        {isSelected && <CheckIcon className="w-4 h-4 text-white" />}
      </div>
      <div className="flex-grow">
        <div className="flex justify-between items-start">
          <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">{test_number}</h3>
          {(onDuplicate || onMove) && (
            <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
              {onDuplicate && (
                <button
                  onClick={handleDuplicate}
                  className="px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded hover:bg-blue-200 dark:hover:bg-blue-800 font-semibold transition-colors"
                  title="Duplicate test case"
                >
                  📋 Duplicate
                </button>
              )}
              {onMove && (
                <div className="relative">
                  <button
                    onClick={async (e) => {
                      e.stopPropagation();
                      // Always refresh projects list before showing menu to ensure we have latest data
                      if (onRefreshProjects) {
                        try {
                          await onRefreshProjects();
                        } catch (err) {
                          console.error('Error refreshing projects:', err);
                        }
                      }
                      setShowMoveMenu(!showMoveMenu);
                    }}
                    className="px-3 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded hover:bg-green-200 dark:hover:bg-green-800 font-semibold transition-colors"
                    title="Move test case"
                  >
                    ➡️ Move
                  </button>
                  {showMoveMenu && (
                    <div className="absolute right-0 mt-1 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-10">
                      <div className="py-1">
                        {otherProjects.length > 0 ? (
                          otherProjects.map((project) => (
                            <button
                              key={project.id}
                              onClick={(e) => handleMove(e, project.id)}
                              className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                            >
                              {project.name}
                            </button>
                          ))
                        ) : (
                          <div className="px-4 py-2 text-sm text-gray-500 dark:text-gray-400">
                            No other projects available
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
        <p className="text-gray-600 dark:text-gray-400 mt-1">{description}</p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mt-3">Created: {formattedDate}</p>
      </div>
      {showMoveMenu && (
        <div
          className="fixed inset-0 z-5"
          onClick={(e) => {
            e.stopPropagation();
            setShowMoveMenu(false);
          }}
        />
      )}
    </div>
  );
};

