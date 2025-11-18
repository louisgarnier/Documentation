
import { TestCase } from './types';

export const MOCK_TEST_CASES: TestCase[] = [
  {
    id: 'TC-001',
    description: 'User login with valid credentials',
    createdDate: '2023-10-26T10:00:00Z',
    steps: [
      'Navigate to the login page.',
      'Enter a valid username.',
      'Enter a valid password.',
      'Click the "Login" button.',
    ],
    expectedResult: 'User should be redirected to the dashboard page.',
    status: 'Pass',
  },
  {
    id: 'TC-002',
    description: 'User login with invalid credentials',
    createdDate: '2023-10-26T10:05:00Z',
    steps: [
      'Navigate to the login page.',
      'Enter a valid username.',
      'Enter an invalid password.',
      'Click the "Login" button.',
    ],
    expectedResult: 'An error message "Invalid credentials" should be displayed.',
    status: 'Pass',
  },
  {
    id: 'TC-003',
    description: 'Add item to shopping cart',
    createdDate: '2023-10-27T11:30:00Z',
    steps: [
      'Log in to the application.',
      'Navigate to a product page.',
      'Click the "Add to Cart" button.',
      'Navigate to the shopping cart page.',
    ],
    expectedResult: 'The selected product should be visible in the shopping cart with the correct quantity.',
    status: 'Untested',
  },
  {
    id: 'TC-004',
    description: 'User profile update with valid data',
    createdDate: '2023-10-28T14:00:00Z',
    steps: [
      'Log in to the application.',
      'Navigate to the user profile page.',
      'Update the "First Name" field.',
      'Click the "Save" button.',
    ],
    expectedResult: 'A success message should be displayed and the first name should be updated.',
    status: 'Pass',
  },
  {
    id: 'TC-005',
    description: 'Password reset functionality',
    createdDate: '2023-10-29T09:00:00Z',
    steps: [
        'Navigate to the login page.',
        'Click the "Forgot Password" link.',
        'Enter a registered email address.',
        'Click "Send Reset Link".',
    ],
    expectedResult: 'A password reset link should be sent to the registered email address.',
    status: 'Fail',
  },
  {
    id: 'TC-006',
    description: 'Search functionality with existing keyword',
    createdDate: '2023-10-30T16:20:00Z',
    steps: [
        'Navigate to the homepage.',
        'Enter an existing product name in the search bar.',
        'Press Enter or click the search icon.',
    ],
    expectedResult: 'A list of relevant products should be displayed.',
    status: 'Untested',
  },
  {
    id: 'TC-007',
    description: 'Logout functionality',
    createdDate: '2023-10-31T18:00:00Z',
    steps: [
        'Log in to the application.',
        'Click on the user avatar or menu.',
        'Click the "Logout" button.',
    ],
    expectedResult: 'User should be logged out and redirected to the login page.',
    status: 'Pass',
  }
];
