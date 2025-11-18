/**
 * TypeScript types for the Test Case Documentation Tool
 * These types match the API response models
 */

export interface TestCase {
  id: number;
  test_number: string;
  description: string;
  created_at: string;
}

export interface TestStep {
  id: number;
  test_case_id: number;
  step_number: number;
  description: string;
  modules?: string | null;
  calculation_logic?: string | null;
  configuration?: string | null;
  created_at: string;
}

export interface Screenshot {
  id: number;
  step_id: number;
  file_path: string;
  screenshot_name?: string | null;
  uploaded_at: string;
}

export interface TestCaseWithSteps extends TestCase {
  steps?: TestStep[];
}

export interface TestStepWithScreenshots extends TestStep {
  screenshots?: Screenshot[];
}

// Request types
export interface CreateTestCaseRequest {
  test_number: string;
  description: string;
}

export interface UpdateTestCaseRequest {
  test_number?: string;
  description?: string;
}

export interface CreateStepRequest {
  step_number: number;
  description: string;
  modules?: string | null;
  calculation_logic?: string | null;
  configuration?: string | null;
}

export interface UpdateStepRequest {
  step_number?: number;
  description?: string;
  modules?: string | null;
  calculation_logic?: string | null;
  configuration?: string | null;
}

export interface ReorderStepRequest {
  new_position: number;
}

export interface ExportRequest {
  test_case_ids: number[];
}

