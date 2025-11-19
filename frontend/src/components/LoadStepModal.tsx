'use client';

import React, { useState, useEffect, useRef } from 'react';
import { captureServiceAPI, stepsAPI } from '@/src/api/client';
import type { TestStep } from '@/src/types';

interface LoadStepModalProps {
  testCaseId: number;
  isOpen: boolean;
  onClose: () => void;
  onStepLoaded: (step: TestStep) => void;
}

export const LoadStepModal: React.FC<LoadStepModalProps> = ({
  testCaseId,
  isOpen,
  onClose,
  onStepLoaded,
}) => {
  const [captureFiles, setCaptureFiles] = useState<Array<{name: string; path: string; size: number; modified: number}>>([]);
  const [textFiles, setTextFiles] = useState<Array<{name: string; path: string; size: number; modified: number}>>([]);
  const [selectedImages, setSelectedImages] = useState<Set<string>>(new Set());
  const [selectedTextFile, setSelectedTextFile] = useState<string | null>(null);
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingFiles, setLoadingFiles] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingDescription, setLoadingDescription] = useState(false);
  const [captureDirectory, setCaptureDirectory] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<Array<{name: string; path: string; file: File}>>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load files when modal opens
  useEffect(() => {
    if (isOpen) {
      loadFiles();
      // Get capture directory path
      captureServiceAPI.getCaptureDirectory().then(dir => {
        setCaptureDirectory(dir.capture_directory_expanded);
      }).catch(() => {
        setCaptureDirectory('~/Desktop/Capture_TC/');
      });
    } else {
      // Reset state when closing
      setSelectedImages(new Set());
      setSelectedTextFile(null);
      setDescription('');
      setError(null);
      setUploadedFiles([]);
    }
  }, [isOpen]);

  const loadFiles = async () => {
    setLoadingFiles(true);
    setError(null);
    try {
      const filesData = await captureServiceAPI.listCaptureFiles();
      const images = filesData.files.filter(f => 
        f.name.toLowerCase().endsWith('.png') || 
        f.name.toLowerCase().endsWith('.jpg') || 
        f.name.toLowerCase().endsWith('.jpeg')
      );
      const texts = filesData.files.filter(f => 
        f.name.toLowerCase().endsWith('.txt')
      );
      setCaptureFiles(images);
      setTextFiles(texts);
    } catch (err) {
      console.error('Failed to load files:', err);
      setError('Failed to load files from capture directory');
    } finally {
      setLoadingFiles(false);
    }
  };

  const handleImageToggle = (imagePath: string) => {
    const newSelected = new Set(selectedImages);
    if (newSelected.has(imagePath)) {
      newSelected.delete(imagePath);
    } else {
      newSelected.add(imagePath);
    }
    setSelectedImages(newSelected);
  };

  const handleTextFileSelect = async (textPath: string) => {
    // If clicking the same file, deselect it
    if (selectedTextFile === textPath) {
      setSelectedTextFile(null);
      setDescription('');
      return;
    }
    
    setSelectedTextFile(textPath);
    setLoadingDescription(true);
    setError(null);
    try {
      // Fetch the text file content
      const blob = await captureServiceAPI.getCaptureFile(textPath);
      const text = await blob.text();
      setDescription(text);
    } catch (err) {
      console.error('Failed to load text file:', err);
      setError('Failed to load text file content');
      setSelectedTextFile(null);
    } finally {
      setLoadingDescription(false);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setError(null);
    const newImagePaths: string[] = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const fileName = file.name;
      const isImage = fileName.toLowerCase().endsWith('.png') || 
                     fileName.toLowerCase().endsWith('.jpg') || 
                     fileName.toLowerCase().endsWith('.jpeg') ||
                     fileName.toLowerCase().endsWith('.gif') ||
                     fileName.toLowerCase().endsWith('.bmp');
      const isText = fileName.toLowerCase().endsWith('.txt');

      if (isImage || isText) {
        try {
          // Upload file to Capture_TC/ directory
          const formData = new FormData();
          formData.append('file', file);
          
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/capture-service/upload-file`, {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error(`Failed to upload file: ${response.statusText}`);
          }

          const result = await response.json();
          const uploadedPath = result.file_path;

          if (isImage) {
            newImagePaths.push(uploadedPath);
          } else if (isText && !selectedTextFile) {
            // If it's a text file and no text file is selected yet, load it
            setSelectedTextFile(uploadedPath);
            const text = await file.text();
            setDescription(text);
          }
        } catch (err) {
          console.error('Error uploading file:', err);
          setError(`Failed to upload ${fileName}: ${err instanceof Error ? err.message : 'Unknown error'}`);
        }
      }
    }

    if (newImagePaths.length > 0) {
      // Add to selected images
      setSelectedImages(prev => new Set([...Array.from(prev), ...newImagePaths]));
      // Refresh file list to show newly uploaded files
      await loadFiles();
    }

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (selectedImages.size === 0) {
      setError('Please select at least one image');
      return;
    }

    if (!description.trim()) {
      setError('Description is required');
      return;
    }

    try {
      setLoading(true);
      const newStep = await stepsAPI.load(testCaseId, {
        description: description.trim(),
        image_paths: Array.from(selectedImages),
        description_file_path: selectedTextFile || undefined,
      });
      onStepLoaded(newStep);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load step');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Load Step</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              ✕
            </button>
          </div>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-2 rounded text-sm mb-4">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Image Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Select Images (one or more) *
              </label>
              {loadingFiles ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  Loading files...
                </div>
              ) : captureFiles.length === 0 ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  No images found in Capture_TC/
                </div>
              ) : (
                <div className="grid grid-cols-4 gap-3 border border-gray-300 dark:border-gray-600 rounded-lg p-3 bg-gray-50 dark:bg-gray-900 max-h-64 overflow-y-auto">
                  {captureFiles.map((file) => {
                    const isSelected = selectedImages.has(file.path);
                    return (
                      <button
                        key={file.path}
                        type="button"
                        onClick={() => handleImageToggle(file.path)}
                        className={`relative aspect-square rounded border-2 transition-colors overflow-hidden ${
                          isSelected
                            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                            : 'border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 hover:border-blue-400'
                        }`}
                      >
                        <img
                          src={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/capture-service/get-file?path=${encodeURIComponent(file.path)}`}
                          alt={file.name}
                          className="w-full h-full object-cover"
                          loading="lazy"
                          onError={(e) => {
                            (e.target as HTMLImageElement).style.display = 'none';
                            const parent = (e.target as HTMLImageElement).parentElement;
                            if (parent) {
                              parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-2xl">📸</div>';
                            }
                          }}
                        />
                        {isSelected && (
                          <div className="absolute top-1 right-1 bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                            ✓
                          </div>
                        )}
                        <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-[10px] px-1 py-0.5 truncate">
                          {file.name}
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
              
              {/* Or select from computer */}
              <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Or select from computer</span>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept="image/png,image/jpeg,image/jpg,image/gif,image/bmp,.txt"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="load-step-file-input"
                  />
                  <label
                    htmlFor="load-step-file-input"
                    className="cursor-pointer text-xs text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    📁 Browse Files
                  </label>
                </div>
              </div>
            </div>

            {/* Text File Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Select Description File (optional)
              </label>
              {captureDirectory && (
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">
                  Files from: <span className="font-mono">{captureDirectory}</span>
                </div>
              )}
              {textFiles.length === 0 ? (
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  No text files found in Capture_TC/
                </div>
              ) : (
                <div className="space-y-2 max-h-32 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-lg p-2 bg-gray-50 dark:bg-gray-900">
                  {textFiles.map((file) => (
                    <button
                      key={file.path}
                      type="button"
                      onClick={() => handleTextFileSelect(file.path)}
                      className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                        selectedTextFile === file.path
                          ? 'bg-blue-100 dark:bg-blue-900/30 border border-blue-500'
                          : 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
                      }`}
                    >
                      📄 {file.name}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Description Editor */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description *
              </label>
              {loadingDescription ? (
                <div className="text-center py-4 text-gray-500 dark:text-gray-400">
                  Loading description...
                </div>
              ) : (
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                  placeholder="Enter step description or select a text file above"
                  required
                />
              )}
            </div>

            {/* Actions */}
            <div className="flex justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading || selectedImages.size === 0 || !description.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Loading Step...' : 'Create Step'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

