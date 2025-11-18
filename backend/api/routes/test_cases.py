"""
Routes for test case operations.
"""

from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.models import (
    get_all_test_cases,
    get_test_case_by_id,
    create_test_case as create_test_case_db,
    update_test_case as update_test_case_db,
    delete_test_case as delete_test_case_db
)
from api.models import TestCaseCreate, TestCaseUpdate, TestCaseResponse

router = APIRouter(prefix="/api/test-cases", tags=["test-cases"])


@router.get("", response_model=list[TestCaseResponse])
async def list_test_cases():
    """
    Get all test cases.
    
    Returns a list of all test cases in the database.
    """
    try:
        test_cases = get_all_test_cases()
        return test_cases
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching test cases: {str(e)}")


@router.get("/{test_case_id}", response_model=TestCaseResponse)
async def get_test_case(test_case_id: int):
    """
    Get a specific test case by ID.
    
    Args:
        test_case_id: The ID of the test case to retrieve
        
    Returns:
        Test case details
    """
    try:
        test_case = get_test_case_by_id(test_case_id)
        if not test_case:
            raise HTTPException(status_code=404, detail=f"Test case {test_case_id} not found")
        return test_case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching test case: {str(e)}")


@router.post("", response_model=TestCaseResponse, status_code=201)
async def create_test_case(test_case: TestCaseCreate):
    """
    Create a new test case.
    
    Args:
        test_case: Test case data (test_number, description)
        
    Returns:
        Created test case details
    """
    try:
        test_case_id = create_test_case_db(
            test_number=test_case.test_number,
            description=test_case.description
        )
        if not test_case_id:
            raise HTTPException(status_code=400, detail="Failed to create test case")
        
        # Fetch and return the created test case
        created = get_test_case_by_id(test_case_id)
        if not created:
            raise HTTPException(status_code=500, detail="Test case created but could not be retrieved")
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating test case: {str(e)}")


@router.put("/{test_case_id}", response_model=TestCaseResponse)
async def update_test_case(test_case_id: int, test_case: TestCaseUpdate):
    """
    Update an existing test case.
    
    Args:
        test_case_id: The ID of the test case to update
        test_case: Updated test case data (only provided fields will be updated)
        
    Returns:
        Updated test case details
    """
    try:
        # Check if test case exists
        existing = get_test_case_by_id(test_case_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Test case {test_case_id} not found")
        
        # Prepare update data (only include fields that are provided)
        update_data = {}
        if test_case.test_number is not None:
            update_data['test_number'] = test_case.test_number
        if test_case.description is not None:
            update_data['description'] = test_case.description
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Update the test case
        # Get existing values if not provided
        test_number = update_data.get('test_number', existing['test_number'])
        description = update_data.get('description', existing['description'])
        
        success = update_test_case_db(
            test_case_id=test_case_id,
            test_number=test_number,
            description=description
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update test case")
        
        # Fetch and return the updated test case
        updated = get_test_case_by_id(test_case_id)
        if not updated:
            raise HTTPException(status_code=500, detail="Test case updated but could not be retrieved")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating test case: {str(e)}")


@router.delete("/{test_case_id}", status_code=204)
async def delete_test_case(test_case_id: int):
    """
    Delete a test case.
    
    Args:
        test_case_id: The ID of the test case to delete
        
    Returns:
        No content (204)
    """
    try:
        # Check if test case exists
        existing = get_test_case_by_id(test_case_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Test case {test_case_id} not found")
        
        # Delete the test case
        success = delete_test_case_db(test_case_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete test case")
        
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting test case: {str(e)}")

