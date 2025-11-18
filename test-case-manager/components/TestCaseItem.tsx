
import React from 'react';
import { TestCase } from '../types';
import { CheckIcon } from './icons/CheckIcon';

interface TestCaseItemProps {
  testCase: TestCase;
  isSelected: boolean;
  onSelect: (id: string) => void;
  onViewDetail: (testCase: TestCase) => void;
}

const StatusBadge: React.FC<{ status: TestCase['status'] }> = ({ status }) => {
  const baseClasses = 'px-2 py-1 text-xs font-bold rounded-full';
  const statusClasses = {
    Pass: 'bg-green-500/20 text-green-300',
    Fail: 'bg-red-500/20 text-red-300',
    Untested: 'bg-yellow-500/20 text-yellow-300',
  };
  return <span className={`${baseClasses} ${statusClasses[status]}`}>{status}</span>;
};


export const TestCaseItem: React.FC<TestCaseItemProps> = ({ testCase, isSelected, onSelect, onViewDetail }) => {
  const { id, description, createdDate, status } = testCase;

  const handleCheckboxClick = (e: React.MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    onSelect(id);
  };
  
  const handleCardClick = () => {
    onViewDetail(testCase);
  }

  const formattedDate = new Date(createdDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div 
      onClick={handleCardClick}
      className="bg-surface rounded-lg shadow-lg flex items-start p-4 space-x-4 cursor-pointer transition-all duration-200 hover:shadow-primary/20 hover:ring-2 hover:ring-primary/50"
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
            <h3 className="font-bold text-lg text-text">{id}</h3>
            <StatusBadge status={status} />
        </div>
        <p className="text-text-secondary mt-1">{description}</p>
        <p className="text-sm text-muted mt-3">Created: {formattedDate}</p>
      </div>
    </div>
  );
};
