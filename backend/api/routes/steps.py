"""
Routes for test step operations.
"""

from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path
from typing import List

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.models import (
    get_steps_by_test_case,
    get_step_by_id,
    create_test_step as create_test_step_db,
    update_test_step as update_test_step_db,
    delete_test_step as delete_test_step_db,
    reorder_steps as reorder_steps_db
)
from api.models import TestStepCreate, TestStepUpdate, TestStepResponse, StepReorderRequest

router = APIRouter(prefix="/api", tags=["steps"])


@router.get("/test-cases/{test_case_id}/steps", response_model=List[TestStepResponse])
async def list_steps(test_case_id: int):
    """
    Get all steps for a test case.
    
    Args:
        test_case_id: The ID of the test case
        
    Returns:
        List of steps for the test case
    """
    try:
        steps = get_steps_by_test_case(test_case_id)
        return steps
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching steps: {str(e)}")


@router.get("/steps/{step_id}", response_model=TestStepResponse)
async def get_step(step_id: int):
    """
    Get a specific step by ID.
    
    Args:
        step_id: The ID of the step to retrieve
        
    Returns:
        Step details
    """
    try:
        step = get_step_by_id(step_id)
        if not step:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        return step
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching step: {str(e)}")


@router.post("/test-cases/{test_case_id}/steps", response_model=TestStepResponse, status_code=201)
async def create_step(test_case_id: int, step: TestStepCreate):
    """
    Create a new step for a test case.
    
    Args:
        test_case_id: The ID of the test case
        step: Step data
        
    Returns:
        Created step details
    """
    try:
        step_id = create_test_step_db(
            test_case_id=test_case_id,
            step_number=step.step_number,
            description=step.description,
            modules=step.modules,
            calculation_logic=step.calculation_logic,
            configuration=step.configuration
        )
        if not step_id:
            raise HTTPException(status_code=400, detail="Failed to create step")
        
        # Fetch and return the created step
        created = get_step_by_id(step_id)
        if not created:
            raise HTTPException(status_code=500, detail="Step created but could not be retrieved")
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating step: {str(e)}")


@router.put("/steps/{step_id}", response_model=TestStepResponse)
async def update_step(step_id: int, step: TestStepUpdate):
    """
    Update an existing step.
    
    Args:
        step_id: The ID of the step to update
        step: Updated step data (only provided fields will be updated)
        
    Returns:
        Updated step details
    """
    try:
        # Check if step exists
        existing = get_step_by_id(step_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        
        # Prepare update data (use existing values if not provided)
        step_number = step.step_number if step.step_number is not None else existing['step_number']
        description = step.description if step.description is not None else existing['description']
        modules = step.modules if step.modules is not None else existing.get('modules')
        calculation_logic = step.calculation_logic if step.calculation_logic is not None else existing.get('calculation_logic')
        configuration = step.configuration if step.configuration is not None else existing.get('configuration')
        
        # Update the step
        success = update_test_step_db(
            step_id=step_id,
            step_number=step_number,
            description=description,
            modules=modules,
            calculation_logic=calculation_logic,
            configuration=configuration
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update step")
        
        # Fetch and return the updated step
        updated = get_step_by_id(step_id)
        if not updated:
            raise HTTPException(status_code=500, detail="Step updated but could not be retrieved")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating step: {str(e)}")


@router.delete("/steps/{step_id}", status_code=204)
async def delete_step(step_id: int):
    """
    Delete a step.
    
    Args:
        step_id: The ID of the step to delete
        
    Returns:
        No content (204)
    """
    try:
        # Check if step exists
        existing = get_step_by_id(step_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        
        # Delete the step
        success = delete_test_step_db(step_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete step")
        
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting step: {str(e)}")


@router.post("/steps/{step_id}/reorder", response_model=TestStepResponse)
async def reorder_step(step_id: int, reorder_request: StepReorderRequest):
    """
    Reorder a step to a new position.
    
    Args:
        step_id: The ID of the step to reorder
        reorder_request: New position for the step
        
    Returns:
        Updated step details
    """
    try:
        # Get the step to find its test_case_id
        step = get_step_by_id(step_id)
        if not step:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        
        test_case_id = step['test_case_id']
        
        # Get all steps for this test case
        all_steps = get_steps_by_test_case(test_case_id)
        
        # Create new order: move step_id to new_position
        step_ids = [s['id'] for s in all_steps]
        
        # Remove step_id from current position
        if step_id not in step_ids:
            raise HTTPException(status_code=400, detail="Step not found in test case")
        
        step_ids.remove(step_id)
        
        # Insert at new position
        new_position = reorder_request.new_position
        if new_position < 1:
            new_position = 1
        if new_position > len(step_ids) + 1:
            new_position = len(step_ids) + 1
        
        step_ids.insert(new_position - 1, step_id)
        
        # Reorder using the shared function
        success = reorder_steps_db(test_case_id, step_ids)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to reorder steps")
        
        # Fetch and return the updated step
        updated = get_step_by_id(step_id)
        if not updated:
            raise HTTPException(status_code=500, detail="Step reordered but could not be retrieved")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reordering step: {str(e)}")

