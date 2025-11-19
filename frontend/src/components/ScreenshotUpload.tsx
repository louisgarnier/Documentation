'use client';

import React, { useState, useRef, useEffect } from 'react';
import { screenshotsAPI, captureServiceAPI } from '@/src/api/client';
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
  const [captureDirectory, setCaptureDirectory] = useState<string | null>(null);
  const [captureFiles, setCaptureFiles] = useState<Array<{name: string; path: string; size: number; modified: number}>>([]);
  const [showFileList, setShowFileList] = useState(false);
  const [loadingFiles, setLoadingFiles] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Get capture directory and files on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const dir = await captureServiceAPI.getCaptureDirectory();
        setCaptureDirectory(dir.capture_directory_expanded);
        
        // Load files from capture directory
        const filesData = await captureServiceAPI.listCaptureFiles();
        setCaptureFiles(filesData.files);
      } catch (err) {
        // If it fails, use default
        setCaptureDirectory('~/Desktop/Capture_TC/');
      }
    };
    fetchData();
  }, []);

  // Load files when showing file list
  const loadCaptureFiles = async () => {
    setLoadingFiles(true);
    try {
      const filesData = await captureServiceAPI.listCaptureFiles();
      setCaptureFiles(filesData.files);
      setShowFileList(true);
    } catch (err) {
      console.error('Failed to load files:', err);
      setError('Failed to load files from capture directory');
    } finally {
      setLoadingFiles(false);
    }
  };

  const handleSelectFileFromList = async (filePath: string) => {
    try {
      setUploading(true);
      setError(null);
      
      // Fetch the file from the backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/capture-service/get-file?path=${encodeURIComponent(filePath)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch file');
      }
      
      const blob = await response.blob();
      const file = new File([blob], filePath.split('/').pop() || 'screenshot.png', { type: blob.type });
      
      await screenshotsAPI.upload(stepId, file);
      if (onScreenshotUploaded) {
        // Refresh the screenshot list
        window.location.reload();
      }
      
      setShowFileList(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload screenshot');
    } finally {
      setUploading(false);
    }
  };

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

  const handleClickOrDrag = () => {
    // Show file list from Capture_TC/ directory
    loadCaptureFiles();
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
        <button
          type="button"
          onClick={handleClickOrDrag}
          disabled={uploading || loadingFiles}
          className="cursor-pointer w-full"
        >
          <div className="space-y-1">
            <div className="text-2xl">📸</div>
            <div className="text-xs text-gray-600 dark:text-gray-400">
              {uploading ? (
                <span>Uploading...</span>
              ) : loadingFiles ? (
                <span>Loading files...</span>
              ) : (
                <span className="text-blue-600 dark:text-blue-400 font-medium">Click or drag</span>
              )}
            </div>
            <div className="text-[10px] text-gray-500 dark:text-gray-500">
              Max 200MB
            </div>
          </div>
        </button>
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
          className="text-[10px] text-blue-600 dark:text-blue-400 hover:underline cursor-pointer mt-1 block text-center"
        >
          Or select from computer
        </label>
      </div>
      {showFileList && (
        <div className="mt-3 border border-gray-300 dark:border-gray-600 rounded-lg p-3 bg-gray-50 dark:bg-gray-900 max-h-64 overflow-y-auto">
          <div className="flex items-center justify-between mb-2">
            <div className="text-xs font-medium text-gray-700 dark:text-gray-300">
              Files in Capture_TC/
            </div>
            <button
              type="button"
              onClick={() => setShowFileList(false)}
              className="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
            >
              ✕
            </button>
          </div>
          {captureFiles.length === 0 ? (
            <div className="text-xs text-gray-500 dark:text-gray-400 text-center py-4">
              No files found in {captureDirectory || '~/Desktop/Capture_TC/'}
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-2">
              {captureFiles.map((file) => (
                <button
                  key={file.path}
                  type="button"
                  onClick={() => handleSelectFileFromList(file.path)}
                  disabled={uploading}
                  className="relative aspect-square rounded border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-colors overflow-hidden bg-gray-100 dark:bg-gray-700 group"
                  title={file.name}
                >
                  <img
                    src={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/capture-service/get-file?path=${encodeURIComponent(file.path)}`}
                    alt={file.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).style.display = 'none';
                      const parent = (e.target as HTMLImageElement).parentElement;
                      if (parent) {
                        parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-2xl">📸</div>';
                      }
                    }}
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-[10px] px-1 py-0.5 truncate opacity-0 group-hover:opacity-100 transition-opacity">
                    {file.name}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
      <div className="mt-1.5 text-[10px] text-gray-500 dark:text-gray-500 text-center">
        💡 Screenshots saved to: <span className="font-mono">{captureDirectory || '~/Desktop/Capture_TC/'}</span>
      </div>
      {error && (
        <div className="mt-1.5 text-xs text-red-600 dark:text-red-400">{error}</div>
      )}
    </div>
  );
};

