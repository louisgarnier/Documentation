'use client';

import React, { useState, useEffect } from 'react';
import { Screenshot } from '@/src/types';
import { screenshotsAPI } from '@/src/api/client';

interface ScreenshotGalleryProps {
  stepId: number;
  onScreenshotDeleted?: () => void;
  refreshTrigger?: number; // Trigger reload when this changes
}

interface ScreenshotModalProps {
  screenshot: Screenshot;
  isOpen: boolean;
  onClose: () => void;
  onDelete: (id: number) => void;
}

const ScreenshotModal: React.FC<ScreenshotModalProps> = ({ screenshot, isOpen, onClose, onDelete }) => {
  if (!isOpen) return null;

  const imageUrl = screenshotsAPI.getFileUrl(screenshot.id);
  const uploadDate = new Date(screenshot.uploaded_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this screenshot?')) {
      onDelete(screenshot.id);
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
      onClick={onClose}
    >
      <div
        className="relative max-w-5xl max-h-[90vh] bg-white dark:bg-gray-800 rounded-lg p-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start mb-2">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Uploaded: {uploadDate}</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleDelete}
              className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              🗑️ Delete
            </button>
            <button
              onClick={onClose}
              className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 text-sm"
            >
              ✕ Close
            </button>
          </div>
        </div>
        <img
          src={imageUrl}
          alt={`Screenshot ${screenshot.id}`}
          className="max-w-full max-h-[80vh] object-contain rounded"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ddd" width="200" height="200"/%3E%3Ctext fill="%23999" font-family="sans-serif" font-size="14" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3EImage not found%3C/text%3E%3C/svg%3E';
          }}
        />
      </div>
    </div>
  );
};

export const ScreenshotGallery: React.FC<ScreenshotGalleryProps> = ({
  stepId,
  onScreenshotDeleted,
  refreshTrigger,
}) => {
  const [screenshots, setScreenshots] = useState<Screenshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [selectedScreenshot, setSelectedScreenshot] = useState<Screenshot | null>(null);

  useEffect(() => {
    loadScreenshots();
  }, [stepId, refreshTrigger]);

  const loadScreenshots = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await screenshotsAPI.getByStepId(stepId);
      setScreenshots(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load screenshots');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (screenshotId: number) => {
    try {
      setDeletingId(screenshotId);
      await screenshotsAPI.delete(screenshotId);
      setScreenshots(screenshots.filter(s => s.id !== screenshotId));
      if (onScreenshotDeleted) {
        onScreenshotDeleted();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete screenshot');
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return null; // Don't show loading state
  }

  if (error) {
    return <div className="text-sm text-red-600 dark:text-red-400">Error: {error}</div>;
  }

  if (screenshots.length === 0) {
    return null; // Don't show anything if no screenshots
  }

  return (
    <>
      <div className="mt-4">
        <div className="flex items-start gap-4">
          <div className="flex-1">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Screenshots:</h4>
            <div className="flex flex-wrap gap-2">
              {screenshots.map((screenshot) => {
                const imageUrl = screenshotsAPI.getFileUrl(screenshot.id);

                return (
                  <button
                    key={screenshot.id}
                    onClick={() => setSelectedScreenshot(screenshot)}
                    className="relative w-16 h-16 rounded border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-colors overflow-hidden bg-gray-100 dark:bg-gray-700"
                  >
                    <img
                      src={imageUrl}
                      alt={`Screenshot ${screenshot.id}`}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        (e.target as HTMLImageElement).style.display = 'none';
                        const parent = (e.target as HTMLImageElement).parentElement;
                        if (parent) {
                          parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-2xl">📸</div>';
                        }
                      }}
                    />
                    <div className="absolute top-0 right-0 bg-red-600 text-white text-xs px-1 rounded-bl">
                      {screenshots.length > 1 ? screenshots.indexOf(screenshot) + 1 : ''}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {selectedScreenshot && (
        <ScreenshotModal
          screenshot={selectedScreenshot}
          isOpen={true}
          onClose={() => setSelectedScreenshot(null)}
          onDelete={handleDelete}
        />
      )}
    </>
  );
};

