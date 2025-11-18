
import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="py-6 px-4 sm:px-6 lg:px-8 bg-surface/50 backdrop-blur-sm sticky top-0 z-10 border-b border-muted/50">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-text tracking-tight">
          Test Case Manager
        </h1>
        <p className="text-text-secondary mt-1">
          Review, select, and manage your test cases with ease.
        </p>
      </div>
    </header>
  );
};
