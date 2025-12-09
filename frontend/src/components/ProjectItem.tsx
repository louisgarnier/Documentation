'use client';

import React from 'react';
import type { Project } from '@/types';
import { useRouter } from 'next/navigation';

interface ProjectItemProps {
  project: Project;
  selected?: boolean;
  onSelect?: (projectId: number) => void;
}

export const ProjectItem: React.FC<ProjectItemProps> = ({ project, selected = false, onSelect }) => {
  const router = useRouter();
  const { id, name, description, test_case_count, created_at } = project;

  const handleCardClick = (e: React.MouseEvent) => {
    // If clicking on checkbox, don't navigate
    if ((e.target as HTMLElement).closest('input[type="checkbox"]')) {
      return;
    }
    router.push(`/project/${id}`);
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.stopPropagation();
    if (onSelect) {
      onSelect(id);
    }
  };

  const formattedDate = new Date(created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div 
      onClick={handleCardClick}
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-blue-500/20 hover:ring-2 hover:ring-blue-500/50 ${
        selected ? 'ring-2 ring-green-500 bg-green-50 dark:bg-green-900/20' : ''
      }`}
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-3 flex-1">
          {onSelect && (
            <input
              type="checkbox"
              checked={selected}
              onChange={handleCheckboxChange}
              onClick={(e) => e.stopPropagation()}
              className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
            />
          )}
          <h3 className="font-bold text-xl text-gray-900 dark:text-gray-100">{name}</h3>
        </div>
        <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-semibold">
          {test_case_count || 0} {test_case_count === 1 ? 'test case' : 'test cases'}
        </span>
      </div>
      {description && (
        <p className="text-gray-600 dark:text-gray-400 mt-2 mb-3">{description}</p>
      )}
      <p className="text-sm text-gray-500 dark:text-gray-500">Created: {formattedDate}</p>
    </div>
  );
};

