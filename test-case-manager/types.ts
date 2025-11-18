
export interface TestCase {
  id: string;
  description: string;
  createdDate: string;
  steps: string[];
  expectedResult: string;
  status: 'Pass' | 'Fail' | 'Untested';
}
