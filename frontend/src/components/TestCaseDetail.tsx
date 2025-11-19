'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core';
import { SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { TestCase, TestStep } from '@/src/types';
import { ChevronLeftIcon } from './icons/ChevronLeftIcon';
import { testCasesAPI, stepsAPI, captureServiceAPI } from '@/src/api/client';
import { SortableStepCard } from './SortableStepCard';
import { AddStepForm } from './AddStepForm';
import { LoadStepModal } from './LoadStepModal';

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
  const [reordering, setReordering] = useState(false);
  const [loadStepModalOpen, setLoadStepModalOpen] = useState(false);
  
  // Capture service state
  const [captureModeActive, setCaptureModeActive] = useState(false);
  const [captureServiceStatus, setCaptureServiceStatus] = useState<'on' | 'off' | 'starting' | 'error'>('off');
  const [captureServiceAvailable, setCaptureServiceAvailable] = useState(false);
  const [captureLoading, setCaptureLoading] = useState(false);
  const [captureError, setCaptureError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  // Configure sensors for drag and drop
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const formattedDate = new Date(testCase.created_at).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  // Check capture service status on mount and periodically
  useEffect(() => {
    const checkCaptureServiceStatus = async () => {
      try {
        const status = await captureServiceAPI.getStatus();
        setCaptureServiceAvailable(status.service_running || status.service_process_running);
        setCaptureServiceStatus(status.status);
        setCaptureModeActive(status.watcher_running);
        setCaptureError(null);
        
        // Stop polling if service is fully on and watcher is running
        if (status.service_running && status.watcher_running && isPolling) {
          setIsPolling(false);
        }
      } catch (err) {
        setCaptureServiceAvailable(false);
        setCaptureServiceStatus('error');
        setCaptureModeActive(false);
        setCaptureError('Failed to check capture service status');
        console.error('Failed to check capture service status:', err);
      }
    };

    // Check immediately
    checkCaptureServiceStatus();

    // Poll more frequently if starting or if polling is active
    const pollInterval = isPolling ? 2000 : 5000;
    const interval = setInterval(checkCaptureServiceStatus, pollInterval);

    return () => clearInterval(interval);
  }, [isPolling]);

  const handleToggleCaptureMode = async () => {
    try {
      setCaptureLoading(true);
      setCaptureError(null);

      if (captureModeActive) {
        // Deactivate: Stop Watcher then Service API
        try {
          // Stop watcher first
          await captureServiceAPI.stop();
          setCaptureModeActive(false);
          
          // Then stop service API
          await captureServiceAPI.stopService();
          setCaptureServiceStatus('off');
          setCaptureServiceAvailable(false);
          
          console.log('Capture mode and service deactivated');
        } catch (err) {
          // Even if stop fails, try to stop service
          try {
            await captureServiceAPI.stopService();
          } catch (stopErr) {
            console.error('Error stopping service:', stopErr);
          }
          throw err;
        }
      } else {
        // Activate: Start Service API then Watcher
        try {
          // Start service API first
          setCaptureServiceStatus('starting');
          setIsPolling(true);
          const startResult = await captureServiceAPI.startService();
          
          if (!startResult.success) {
            throw new Error(startResult.message || 'Failed to start service');
          }
          
          // Wait a bit for service to start, then check status
          await new Promise(resolve => setTimeout(resolve, 2000));
          
          // Poll until service is ready
          let attempts = 0;
          const maxAttempts = 10;
          while (attempts < maxAttempts) {
            const status = await captureServiceAPI.getStatus();
            if (status.service_running) {
              setCaptureServiceStatus('on');
              setCaptureServiceAvailable(true);
              
              // Now start watcher
              await captureServiceAPI.start();
              setCaptureModeActive(true);
              console.log('Capture mode and service activated');
              break;
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
            attempts++;
          }
          
          if (attempts >= maxAttempts) {
            throw new Error('Service did not start in time');
          }
        } catch (err) {
          const errorMessage = err instanceof Error ? err.message : 'Failed to start service';
          setCaptureError(errorMessage);
          setCaptureServiceStatus('error');
          console.error('Error starting service:', err);
          throw err;
        } finally {
          setIsPolling(false);
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle capture mode';
      setCaptureError(errorMessage);
      console.error('Error toggling capture mode:', err);
      
      // Try to refresh status
      try {
        const status = await captureServiceAPI.getStatus();
        setCaptureServiceStatus(status.status);
        setCaptureModeActive(status.watcher_running);
        setCaptureServiceAvailable(status.service_running);
      } catch (statusErr) {
        setCaptureServiceAvailable(false);
        setCaptureServiceStatus('error');
      }
    } finally {
      setCaptureLoading(false);
    }
  };

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

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over || active.id === over.id) {
      return;
    }

    const activeId = active.id as number;
    const overId = over.id as number;

    // Find the steps
    const activeStep = steps.find(s => s.id === activeId);
    const overStep = steps.find(s => s.id === overId);

    if (!activeStep || !overStep) {
      return;
    }

    // Calculate new position
    const sortedSteps = [...steps].sort((a, b) => a.step_number - b.step_number);
    const activeIndex = sortedSteps.findIndex(s => s.id === activeId);
    const overIndex = sortedSteps.findIndex(s => s.id === overId);

    // Determine new position (insert at over position)
    const newPosition = overStep.step_number;

    try {
      setReordering(true);
      setError(null);
      
      // Call API to reorder
      await stepsAPI.reorder(activeId, { new_position: newPosition });
      
      // Reload steps to get updated step numbers
      if (onStepsChange) {
        onStepsChange();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reorder step');
      console.error('Error reordering step:', err);
    } finally {
      setReordering(false);
    }
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
        <div className="flex flex-col items-end space-y-2">
          <div className="flex items-center space-x-3">
            {/* Capture Mode Button */}
            <button
              onClick={handleToggleCaptureMode}
              disabled={captureLoading || captureServiceStatus === 'starting'}
              className={`px-4 py-2 rounded-md font-medium transition-colors duration-200 flex items-center space-x-2 ${
                captureModeActive
                  ? 'bg-green-600 text-white hover:bg-green-700'
                  : 'bg-gray-600 text-white hover:bg-gray-700'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
              title={
                captureServiceStatus === 'starting'
                  ? 'Service is starting, please wait...'
                  : captureModeActive
                  ? 'Click to disable capture mode'
                  : 'Click to enable capture mode'
              }
            >
              <span className={`w-2 h-2 rounded-full ${captureModeActive ? 'bg-green-300' : 'bg-gray-300'}`}></span>
              <span>
                {captureLoading
                  ? 'Loading...'
                  : captureModeActive
                  ? 'Capture Mode: ON'
                  : 'Capture Mode: OFF'}
              </span>
            </button>
            
            {/* Service API Status Indicator */}
            <div className="flex items-center space-x-2 px-3 py-2 rounded-md bg-gray-100 dark:bg-gray-800">
              <span className={`w-2 h-2 rounded-full ${
                captureServiceStatus === 'on' ? 'bg-green-500' :
                captureServiceStatus === 'starting' ? 'bg-yellow-500 animate-pulse' :
                captureServiceStatus === 'error' ? 'bg-red-500' :
                'bg-gray-400'
              }`}></span>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Service API: {
                  captureServiceStatus === 'on' ? 'ON' :
                  captureServiceStatus === 'starting' ? 'Starting...' :
                  captureServiceStatus === 'error' ? 'Error' :
                  'OFF'
                }
              </span>
            </div>
          </div>
          
          {/* Capture Mode Status Indicator */}
          <div className="flex items-center space-x-2 px-3 py-1 rounded-md bg-gray-100 dark:bg-gray-800">
            <span className={`w-2 h-2 rounded-full ${captureModeActive ? 'bg-green-500' : 'bg-gray-400'}`}></span>
            <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
              Capture Mode: {captureModeActive ? 'ACTIVE' : 'INACTIVE'}
            </span>
          </div>
          
          {/* Error Message */}
          {captureError && (
            <div className="text-xs text-red-600 dark:text-red-400 max-w-md text-right">
              {captureError}
            </div>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setLoadStepModalOpen(true)}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Load Step
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
      </div>

      {error && (
        <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {captureError && (
        <div className="mb-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 text-yellow-700 dark:text-yellow-400 px-4 py-3 rounded">
          <strong>Capture Service:</strong> {captureError}
        </div>
      )}

      {captureModeActive && (
        <div className="mb-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded">
          <strong>Capture Mode Active:</strong> Take a screenshot (Shift+Cmd+4) and a popup will appear to name and describe it.
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
              <DndContext
                sensors={sensors}
                collisionDetection={closestCenter}
                onDragEnd={handleDragEnd}
              >
                <SortableContext
                  items={steps.map(s => s.id)}
                  strategy={verticalListSortingStrategy}
                >
                  <div className="space-y-4 mb-4">
                    {steps
                      .sort((a, b) => a.step_number - b.step_number)
                      .map((step) => (
                        <SortableStepCard
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
                </SortableContext>
              </DndContext>
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

      <LoadStepModal
        testCaseId={testCase.id}
        isOpen={loadStepModalOpen}
        onClose={() => setLoadStepModalOpen(false)}
        onStepLoaded={(newStep) => {
          setSteps([...steps, newStep]);
          if (onStepsChange) {
            onStepsChange();
          }
        }}
      />
    </div>
  );
};

