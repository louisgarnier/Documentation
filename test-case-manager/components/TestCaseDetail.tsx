
import React from 'react';
import { TestCase } from '../types';
import { ChevronLeftIcon } from './icons/ChevronLeftIcon';

interface TestCaseDetailProps {
  testCase: TestCase;
  onGoBack: () => void;
}

const StatusBadge: React.FC<{ status: TestCase['status'] }> = ({ status }) => {
    const baseClasses = 'px-3 py-1 text-sm font-semibold rounded-full inline-block';
    const statusClasses = {
      Pass: 'bg-green-500/20 text-green-300',
      Fail: 'bg-red-500/20 text-red-300',
      Untested: 'bg-yellow-500/20 text-yellow-300',
    };
    return <span className={`${baseClasses} ${statusClasses[status]}`}>{status}</span>;
  };

export const TestCaseDetail: React.FC<TestCaseDetailProps> = ({ testCase, onGoBack }) => {
  const formattedDate = new Date(testCase.createdDate).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="p-4 sm:p-6 lg:p-8">
      <button
        onClick={onGoBack}
        className="flex items-center space-x-2 text-primary hover:text-primary-light mb-6 font-semibold transition-colors duration-200"
      >
        <ChevronLeftIcon className="w-5 h-5" />
        <span>Back to List</span>
      </button>

      <div className="bg-surface rounded-lg shadow-lg p-6">
        <div className="flex flex-col sm:flex-row justify-between sm:items-center border-b border-muted pb-4 mb-4">
          <div>
            <h2 className="text-2xl font-bold text-text">{testCase.id}</h2>
            <p className="text-text-secondary mt-1">{testCase.description}</p>
          </div>
          <div className="mt-4 sm:mt-0">
            <StatusBadge status={testCase.status} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h3 className="text-lg font-semibold text-text mb-3">Test Steps</h3>
                <ol className="list-decimal list-inside space-y-2 text-text-secondary">
                {testCase.steps.map((step, index) => (
                    <li key={index}>{step}</li>
                ))}
                </ol>
            </div>
            <div>
                <h3 className="text-lg font-semibold text-text mb-3">Expected Result</h3>
                <p className="bg-background p-3 rounded-md text-text-secondary">{testCase.expectedResult}</p>

                <h3 className="text-lg font-semibold text-text mt-6 mb-3">Details</h3>
                <p className="text-sm text-muted">Created: {formattedDate}</p>
            </div>
        </div>
      </div>
    </div>
  );
};
