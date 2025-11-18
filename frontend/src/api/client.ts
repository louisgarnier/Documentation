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

