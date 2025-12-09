/**
 * TypeScript types for the Test Case Documentation Tool
 * These types match the API response models
 */

export interface Project {
  id: number;
  name: string;
  description?: string | null;
  created_at: string;
  updated_at: string;
  test_case_count?: number;
}

export interface TestCase {
  id: number;
  test_number: string;
  description: string;
  project_id?: number | null;
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
export interface CreateProjectRequest {
  name: string;
  description?: string | null;
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string | null;
}

export interface CreateTestCaseRequest {
  test_number: string;
  description: string;
  project_id?: number | null;
}

export interface UpdateTestCaseRequest {
  test_number?: string;
  description?: string;
  project_id?: number | null;
}

export interface MoveTestCaseRequest {
  target_project_id?: number | null;
}

export interface DuplicateTestCaseRequest {
  new_test_number: string;
  target_project_id?: number | null;
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
  test_case_ids?: number[];
  project_ids?: number[];
}

