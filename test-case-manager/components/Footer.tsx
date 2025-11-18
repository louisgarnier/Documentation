
import React from 'react';

interface FooterProps {
  selectedCount: number;
  onExport: () => void;
}

export const Footer: React.FC<FooterProps> = ({ selectedCount, onExport }) => {
  return (
    <footer className="sticky bottom-0 bg-surface/80 backdrop-blur-lg border-t border-muted/50 p-4 z-10">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="text-text-secondary">
          <span className="font-bold text-text">{selectedCount}</span> {selectedCount === 1 ? 'case' : 'cases'} selected
        </div>
        <button
          onClick={onExport}
          disabled={selectedCount === 0}
          className="px-6 py-2 bg-primary text-white font-semibold rounded-md shadow-md hover:bg-primary-light focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-background focus:ring-primary disabled:bg-muted disabled:cursor-not-allowed disabled:shadow-none transition-all duration-200"
        >
          Export Selected
        </button>
      </div>
    </footer>
  );
};
