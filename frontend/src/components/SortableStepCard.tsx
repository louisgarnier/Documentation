'use client';

import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { TestStep } from '@/src/types';
import { StepCard } from './StepCard';

interface SortableStepCardProps {
  step: TestStep;
  totalSteps: number;
  onUpdate: (updatedStep: TestStep) => void;
  onDelete: (stepId: number) => void;
  onReorder: (stepId: number, newPosition: number) => void;
}

export const SortableStepCard: React.FC<SortableStepCardProps> = ({
  step,
  totalSteps,
  onUpdate,
  onDelete,
  onReorder,
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: step.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} className={`${isDragging ? 'z-50' : ''}`}>
      <div className="relative">
        {/* Drag handle - only this area is draggable */}
        <div
          {...attributes}
          {...listeners}
          className="absolute left-0 top-0 bottom-0 w-8 cursor-grab active:cursor-grabbing flex items-center justify-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          style={{ touchAction: 'none' }}
        >
          <div className="flex flex-col space-y-1">
            <span className="text-lg leading-none">⋮</span>
            <span className="text-lg leading-none">⋮</span>
          </div>
        </div>
        <div className="pl-10">
          <StepCard
            step={step}
            totalSteps={totalSteps}
            onUpdate={onUpdate}
            onDelete={onDelete}
            onReorder={onReorder}
          />
        </div>
      </div>
    </div>
  );
};

