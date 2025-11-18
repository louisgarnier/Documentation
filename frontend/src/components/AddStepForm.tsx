'use client';

import React, { useState } from 'react';
import { stepsAPI } from '@/src/api/client';
import type { TestStep } from '@/src/types';

interface AddStepFormProps {
  testCaseId: number;
  currentStepCount: number;
  onStepAdded: (step: TestStep) => void;
}

export const AddStepForm: React.FC<AddStepFormProps> = ({
  testCaseId,
  currentStepCount,
  onStepAdded,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [stepNumber, setStepNumber] = useState(currentStepCount + 1);
  const [description, setDescription] = useState('');
  const [modules, setModules] = useState('');
  const [calculationLogic, setCalculationLogic] = useState('');
  const [configuration, setConfiguration] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!description.trim()) {
      setError('Description is required');
      return;
    }

    try {
      setSaving(true);
      const newStep = await stepsAPI.create(testCaseId, {
        step_number: stepNumber,
        description: description.trim(),
        modules: modules.trim() || null,
        calculation_logic: calculationLogic.trim() || null,
        configuration: configuration.trim() || null,
      });
      onStepAdded(newStep);
      // Reset form
      setStepNumber(currentStepCount + 2);
      setDescription('');
      setModules('');
      setCalculationLogic('');
      setConfiguration('');
      setIsExpanded(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create step');
    } finally {
      setSaving(false);
    }
  };

  if (!isExpanded) {
    return (
      <button
        onClick={() => setIsExpanded(true)}
        className="w-full py-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg text-gray-600 dark:text-gray-400 hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
      >
        ➕ Add New Step
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-700 space-y-4">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-2 rounded text-sm">
          {error}
        </div>
      )}

      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Add New Step</h3>
        <button
          type="button"
          onClick={() => {
            setIsExpanded(false);
            setError(null);
          }}
          className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ✕
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-3">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description *
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            placeholder="e.g., Navigate to Order Entry module and create a new order"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Step #
          </label>
          <input
            type="number"
            min="1"
            value={stepNumber}
            onChange={(e) => setStepNumber(parseInt(e.target.value) || 1)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>
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

      <div className="flex justify-end space-x-2">
        <button
          type="button"
          onClick={() => {
            setIsExpanded(false);
            setError(null);
          }}
          disabled={saving}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={saving}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? 'Adding...' : 'Add Step'}
        </button>
      </div>
    </form>
  );
};

