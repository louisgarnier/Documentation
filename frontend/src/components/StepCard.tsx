'use client';

import React, { useState } from 'react';
import { TestStep } from '@/src/types';
import { stepsAPI } from '@/src/api/client';
import { ScreenshotGallery } from './ScreenshotGallery';
import { ScreenshotUpload } from './ScreenshotUpload';

interface StepCardProps {
  step: TestStep;
  totalSteps: number;
  onUpdate: (updatedStep: TestStep) => void;
  onDelete: (stepId: number) => void;
  onReorder: (stepId: number, newPosition: number) => void;
}

export const StepCard: React.FC<StepCardProps> = ({
  step,
  totalSteps,
  onUpdate,
  onDelete,
  onReorder,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [description, setDescription] = useState(step.description);
  const [stepNumber, setStepNumber] = useState(step.step_number);
  const [modules, setModules] = useState(step.modules || '');
  const [calculationLogic, setCalculationLogic] = useState(step.calculation_logic || '');
  const [configuration, setConfiguration] = useState(step.configuration || '');
  const [newPosition, setNewPosition] = useState(step.step_number);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [screenshotRefreshTrigger, setScreenshotRefreshTrigger] = useState(0);

  const handleSave = async () => {
    if (!description.trim()) {
      setError('Description is required');
      return;
    }

    try {
      setSaving(true);
      setError(null);
      const updated = await stepsAPI.update(step.id, {
        step_number: stepNumber,
        description: description.trim(),
        modules: modules.trim() || null,
        calculation_logic: calculationLogic.trim() || null,
        configuration: configuration.trim() || null,
      });
      onUpdate(updated);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update step');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setDescription(step.description);
    setStepNumber(step.step_number);
    setModules(step.modules || '');
    setCalculationLogic(step.calculation_logic || '');
    setConfiguration(step.configuration || '');
    setIsEditing(false);
    setError(null);
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this step?')) {
      try {
        await stepsAPI.delete(step.id);
        onDelete(step.id);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to delete step');
      }
    }
  };

  const handleReorder = async (position: number) => {
    if (position === step.step_number) return;

    try {
      setError(null);
      await stepsAPI.reorder(step.id, { new_position: position });
      onReorder(step.id, position);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reorder step');
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 p-4">
      {error && (
        <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-2 rounded text-sm">
          {error}
        </div>
      )}

      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-4 flex-1">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-lg text-blue-600 dark:text-blue-400">
              Step {step.step_number}
            </span>
            <select
              value={newPosition}
              onChange={async (e) => {
                const pos = parseInt(e.target.value);
                setNewPosition(pos);
                if (pos !== step.step_number) {
                  await handleReorder(pos);
                }
              }}
              className="ml-4 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              {Array.from({ length: totalSteps }, (_, i) => i + 1).map((pos) => (
                <option key={pos} value={pos}>
                  Move to position {pos}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex space-x-2">
          {!isEditing ? (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700"
              >
                Delete
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleCancel}
                disabled={saving}
                className="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save'}
              </button>
            </>
          )}
        </div>
      </div>

      {isEditing ? (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Step Number
            </label>
            <input
              type="number"
              min="1"
              value={stepNumber}
              onChange={(e) => setStepNumber(parseInt(e.target.value) || 1)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Modules (Optional)
            </label>
            <textarea
              value={modules}
              onChange={(e) => setModules(e.target.value)}
              rows={2}
              placeholder="e.g., Order Entry, Portfolio Management"
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Calculation Logic (Optional)
            </label>
            <textarea
              value={calculationLogic}
              onChange={(e) => setCalculationLogic(e.target.value)}
              rows={2}
              placeholder="e.g., Cost = Quantity × Price"
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Configuration (Optional)
            </label>
            <textarea
              value={configuration}
              onChange={(e) => setConfiguration(e.target.value)}
              rows={2}
              placeholder="e.g., Enable auto-execution in settings"
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>
        </div>
      ) : (
        <div className="space-y-2">
          <p className="text-gray-700 dark:text-gray-300">{step.description}</p>
          {step.modules && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <span className="font-medium">Modules:</span> {step.modules}
            </div>
          )}
          {step.calculation_logic && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <span className="font-medium">Calculation:</span> {step.calculation_logic}
            </div>
          )}
          {step.configuration && (
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <span className="font-medium">Configuration:</span> {step.configuration}
            </div>
          )}
        </div>
      )}

      {/* Screenshots Section */}
      {!isEditing && (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-start gap-4">
            <div className="flex-1">
              <ScreenshotGallery
                stepId={step.id}
                refreshTrigger={screenshotRefreshTrigger}
                onScreenshotDeleted={() => {
                  setScreenshotRefreshTrigger(prev => prev + 1);
                }}
              />
            </div>
            <div className="w-1/2 flex-shrink-0">
              <ScreenshotUpload
                stepId={step.id}
                onScreenshotUploaded={() => {
                  setScreenshotRefreshTrigger(prev => prev + 1);
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

