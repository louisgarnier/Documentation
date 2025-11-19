/**
 * API Client for Test Case Documentation Tool
 * Handles all communication with the backend API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

import type {
  TestCase,
  TestStep,
  Screenshot,
  CreateTestCaseRequest,
  UpdateTestCaseRequest,
  CreateStepRequest,
  UpdateStepRequest,
  ReorderStepRequest,
  ExportRequest,
} from '@/types';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}

/**
 * Test Cases API
 */
export const testCasesAPI = {
  /**
   * Get all test cases
   */
  getAll: async (): Promise<TestCase[]> => {
    return fetchAPI<TestCase[]>('/api/test-cases');
  },

  /**
   * Get a test case by ID
   */
  getById: async (id: number): Promise<TestCase> => {
    return fetchAPI<TestCase>(`/api/test-cases/${id}`);
  },

  /**
   * Create a new test case
   */
  create: async (data: CreateTestCaseRequest): Promise<TestCase> => {
    return fetchAPI<TestCase>('/api/test-cases', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a test case
   */
  update: async (id: number, data: UpdateTestCaseRequest): Promise<TestCase> => {
    return fetchAPI<TestCase>(`/api/test-cases/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a test case
   */
  delete: async (id: number): Promise<void> => {
    return fetchAPI<void>(`/api/test-cases/${id}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Steps API
 */
export const stepsAPI = {
  /**
   * Get all steps for a test case
   */
  getByTestCaseId: async (testCaseId: number): Promise<TestStep[]> => {
    return fetchAPI<TestStep[]>(`/api/test-cases/${testCaseId}/steps`);
  },

  /**
   * Get a step by ID
   */
  getById: async (id: number): Promise<TestStep> => {
    return fetchAPI<TestStep>(`/api/steps/${id}`);
  },

  /**
   * Create a new step
   */
  create: async (testCaseId: number, data: CreateStepRequest): Promise<TestStep> => {
    return fetchAPI<TestStep>(`/api/test-cases/${testCaseId}/steps`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update a step
   */
  update: async (id: number, data: UpdateStepRequest): Promise<TestStep> => {
    return fetchAPI<TestStep>(`/api/steps/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a step
   */
  delete: async (id: number): Promise<void> => {
    return fetchAPI<void>(`/api/steps/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Reorder a step
   */
  reorder: async (id: number, data: ReorderStepRequest): Promise<TestStep> => {
    return fetchAPI<TestStep>(`/api/steps/${id}/reorder`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

/**
 * Screenshots API
 */
export const screenshotsAPI = {
  /**
   * Get all screenshots for a step
   */
  getByStepId: async (stepId: number): Promise<Screenshot[]> => {
    return fetchAPI<Screenshot[]>(`/api/steps/${stepId}/screenshots`);
  },

  /**
   * Upload a screenshot
   */
  upload: async (stepId: number, file: File): Promise<Screenshot> => {
    const formData = new FormData();
    formData.append('file', file);

    const url = `${API_BASE_URL}/api/steps/${stepId}/screenshots`;
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  },

  /**
   * Get screenshot file URL
   */
  getFileUrl: (screenshotId: number): string => {
    return `${API_BASE_URL}/api/screenshots/${screenshotId}/file`;
  },

  /**
   * Delete a screenshot
   */
  delete: async (id: number): Promise<void> => {
    return fetchAPI<void>(`/api/screenshots/${id}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Export API
 */
export const exportAPI = {
  /**
   * Export test cases to Excel
   */
  exportToExcel: async (data: ExportRequest): Promise<Blob> => {
    const url = `${API_BASE_URL}/api/export`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.blob();
  },
};

/**
 * Health check
 */
export const healthAPI = {
  check: async (): Promise<{ status: string }> => {
    return fetchAPI<{ status: string }>('/health');
  },
};

/**
 * Screenshot Capture Service API
 * Handles communication with the local screenshot capture service (localhost:5001)
 */
const CAPTURE_SERVICE_URL = 'http://localhost:5001';

async function fetchCaptureService<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${CAPTURE_SERVICE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ 
        message: `HTTP error! status: ${response.status}` 
      }));
      throw new Error(error.message || error.detail || `HTTP error! status: ${response.status}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (error) {
    console.error(`Capture Service Error (${endpoint}):`, error);
    throw error;
  }
}

export const captureServiceAPI = {
  /**
   * Get current status of the capture service (via backend API)
   */
  getStatus: async (): Promise<{
    service_running: boolean;
    service_process_running: boolean;
    watcher_running: boolean;
    status: 'on' | 'off' | 'starting' | 'error';
  }> => {
    return fetchAPI<{
      service_running: boolean;
      service_process_running: boolean;
      watcher_running: boolean;
      status: 'on' | 'off' | 'starting' | 'error';
    }>('/api/capture-service/status');
  },

  /**
   * Start the capture service API
   */
  startService: async (): Promise<{
    success: boolean;
    message: string;
  }> => {
    return fetchAPI<{
      success: boolean;
      message: string;
    }>('/api/capture-service/start', {
      method: 'POST',
    });
  },

  /**
   * Stop the capture service API
   */
  stopService: async (): Promise<{
    success: boolean;
    message: string;
  }> => {
    return fetchAPI<{
      success: boolean;
      message: string;
    }>('/api/capture-service/stop', {
      method: 'POST',
    });
  },

  /**
   * Get watcher status (direct call to capture service)
   */
  getWatcherStatus: async (): Promise<{
    watcher_running: boolean;
    watcher_pid: number | null;
  }> => {
    return fetchCaptureService<{
      watcher_running: boolean;
      watcher_pid: number | null;
    }>('/status');
  },

  /**
   * Get capture directory path
   */
  getCaptureDirectory: async (): Promise<{
    capture_directory: string;
    capture_directory_expanded: string;
  }> => {
    return fetchAPI<{
      capture_directory: string;
      capture_directory_expanded: string;
    }>('/api/capture-service/capture-directory');
  },

  /**
   * List files in capture directory
   */
  listCaptureFiles: async (): Promise<{
    files: Array<{
      name: string;
      path: string;
      size: number;
      modified: number;
    }>;
    directory: string;
  }> => {
    return fetchAPI<{
      files: Array<{
        name: string;
        path: string;
        size: number;
        modified: number;
      }>;
      directory: string;
    }>('/api/capture-service/capture-files');
  },

  /**
   * Start/activate the capture mode
   */
  start: async (): Promise<{
    status: string;
    message: string;
  }> => {
    return fetchCaptureService<{
      status: string;
      message: string;
    }>('/start', {
      method: 'POST',
    });
  },

  /**
   * Stop/deactivate the capture mode
   */
  stop: async (): Promise<{
    status: string;
    message: string;
  }> => {
    return fetchCaptureService<{
      status: string;
      message: string;
    }>('/stop', {
      method: 'POST',
    });
  },

  /**
   * Health check for the capture service
   */
  health: async (): Promise<{
    status: string;
    service: string;
  }> => {
    return fetchCaptureService<{
      status: string;
      service: string;
    }>('/health');
  },
};

