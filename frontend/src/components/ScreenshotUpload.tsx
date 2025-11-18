'use client';

import React, { useState, useRef } from 'react';
import { screenshotsAPI } from '@/src/api/client';
import { Screenshot } from '@/src/types';

interface ScreenshotUploadProps {
  stepId: number;
  onScreenshotUploaded?: (screenshot: Screenshot) => void;
}

export const ScreenshotUpload: React.FC<ScreenshotUploadProps> = ({
  stepId,
  onScreenshotUploaded,
}) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (file: File) => {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
      setError('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP.');
      return;
    }

    // Validate file size (200MB max)
    const maxSize = 200 * 1024 * 1024; // 200MB in bytes
    if (file.size > maxSize) {
      setError('File size exceeds 200MB limit.');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      const screenshot = await screenshotsAPI.upload(stepId, file);
      if (onScreenshotUploaded) {
        onScreenshotUploaded(screenshot);
      }
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload screenshot');
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  return (
    <div>
      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1.5">
        Add Screenshot
      </label>
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-3 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
            : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-900'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/jpg,image/gif,image/bmp"
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
          id={`screenshot-upload-${stepId}`}
        />
        <label
          htmlFor={`screenshot-upload-${stepId}`}
          className="cursor-pointer"
        >
          <div className="space-y-1">
            <div className="text-2xl">📸</div>
            <div className="text-xs text-gray-600 dark:text-gray-400">
              {uploading ? (
                <span>Uploading...</span>
              ) : (
                <span className="text-blue-600 dark:text-blue-400 font-medium">Click or drag</span>
              )}
            </div>
            <div className="text-[10px] text-gray-500 dark:text-gray-500">
              Max 200MB
            </div>
          </div>
        </label>
      </div>
      {error && (
        <div className="mt-1.5 text-xs text-red-600 dark:text-red-400">{error}</div>
      )}
    </div>
  );
};

