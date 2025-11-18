'use client';

import React from 'react';
import { TestCase } from '@/src/types';
import { CheckIcon } from './icons/CheckIcon';

interface TestCaseItemProps {
  testCase: TestCase;
  isSelected: boolean;
  onSelect: (id: number) => void;
  onViewDetail: (testCase: TestCase) => void;
}

export const TestCaseItem: React.FC<TestCaseItemProps> = ({ 
  testCase, 
  isSelected, 
  onSelect, 
  onViewDetail 
}) => {
  const { id, test_number, description, created_at } = testCase;

  const handleCheckboxClick = (e: React.MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    onSelect(id);
  };
  
  const handleCardClick = () => {
    onViewDetail(testCase);
  };

  const formattedDate = new Date(created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

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
        </div>
        <p className="text-gray-600 dark:text-gray-400 mt-1">{description}</p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mt-3">Created: {formattedDate}</p>
      </div>
    </div>
  );
};

