'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { TestCase, TestStep } from '@/src/types';
import { ChevronLeftIcon } from './icons/ChevronLeftIcon';
import { testCasesAPI } from '@/src/api/client';
import { StepCard } from './StepCard';
import { AddStepForm } from './AddStepForm';

interface TestCaseDetailProps {
  testCase: TestCase;
  steps: TestStep[];
  onUpdate?: (updatedTestCase: TestCase) => void;
  onStepsChange?: () => void;
}

export const TestCaseDetail: React.FC<TestCaseDetailProps> = ({ 
  testCase: initialTestCase, 
  steps: initialSteps, 
  onUpdate,
  onStepsChange 
}) => {
  const router = useRouter();
  const [testCase, setTestCase] = useState<TestCase>(initialTestCase);
  const [steps, setSteps] = useState<TestStep[]>(initialSteps);
  const [isEditing, setIsEditing] = useState(false);
  const [testNumber, setTestNumber] = useState(testCase.test_number);
  const [description, setDescription] = useState(testCase.description);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formattedDate = new Date(testCase.created_at).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  const handleGoBack = () => {
    router.push('/');
  };

  const handleSave = async () => {
    if (!testNumber.trim() || !description.trim()) {
      setError('Test Number and Description are required');
      return;
    }

    try {
      setSaving(true);
      setError(null);
      const updated = await testCasesAPI.update(testCase.id, {
        test_number: testNumber.trim(),
        description: description.trim(),
      });
      setTestCase(updated);
      setIsEditing(false);
      if (onUpdate) {
        onUpdate(updated);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update test case');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setTestNumber(testCase.test_number);
    setDescription(testCase.description);
    setIsEditing(false);
    setError(null);
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8">
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={handleGoBack}
          className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold transition-colors duration-200"
        >
          <ChevronLeftIcon className="w-5 h-5" />
          <span>Back to List</span>
        </button>
        {!isEditing ? (
          <button
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Edit
          </button>
        ) : (
          <div className="flex space-x-2">
            <button
              onClick={handleCancel}
              disabled={saving}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="flex flex-col sm:flex-row justify-between sm:items-center border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
          <div className="flex-1 space-y-4">
            {isEditing ? (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Test Number *
                  </label>
                  <input
                    type="text"
                    value={testNumber}
                    onChange={(e) => setTestNumber(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Description *
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </>
            ) : (
              <>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{testCase.test_number}</h2>
                <p className="text-gray-600 dark:text-gray-400 mt-1">{testCase.description}</p>
              </>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Test Steps</h3>
            
            {steps.length === 0 ? (
              <p className="text-gray-500 dark:text-gray-500 mb-4">No steps yet. Add steps to document this test case.</p>
            ) : (
              <div className="space-y-4 mb-4">
                {steps
                  .sort((a, b) => a.step_number - b.step_number)
                  .map((step) => (
                    <StepCard
                      key={step.id}
                      step={step}
                      totalSteps={steps.length}
                      onUpdate={(updatedStep) => {
                        setSteps(steps.map(s => s.id === updatedStep.id ? updatedStep : s));
                        if (onStepsChange) onStepsChange();
                      }}
                      onDelete={(stepId) => {
                        setSteps(steps.filter(s => s.id !== stepId));
                        if (onStepsChange) onStepsChange();
                      }}
                      onReorder={async (stepId, newPosition) => {
                        if (onStepsChange) {
                          onStepsChange();
                        }
                      }}
                    />
                  ))}
              </div>
            )}

            <AddStepForm
              testCaseId={testCase.id}
              currentStepCount={steps.length}
              onStepAdded={(newStep) => {
                setSteps([...steps, newStep]);
                if (onStepsChange) onStepsChange();
              }}
            />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">Details</h3>
            <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-md">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                <span className="font-medium">Created:</span> {formattedDate}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

