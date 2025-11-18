"""
Routes for screenshot operations.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import sys
from pathlib import Path
import os
from typing import List
from datetime import datetime

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.models import (
    get_step_by_id,
    add_screenshot_to_step as add_screenshot_to_step_db,
    get_screenshots_by_step,
    delete_screenshot as delete_screenshot_db
)
from api.models import ScreenshotResponse

router = APIRouter(prefix="/api", tags=["screenshots"])


def save_uploaded_file(uploaded_file: UploadFile, test_case_id: int, step_id: int) -> str:
    """
    Save uploaded file to the appropriate directory and return the file path.
    
    Args:
        uploaded_file: The uploaded file
        test_case_id: The test case ID
        step_id: The step ID
        
    Returns:
        Path to the saved file
    """
    # Create directory structure: uploads/test_{id}/step_{id}/
    upload_dir = project_root / f"uploads/test_{test_case_id}/step_{step_id}"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(uploaded_file.filename).suffix if uploaded_file.filename else ".png"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}{file_extension}"
    file_path = upload_dir / filename
    
    # Save the file
    with open(file_path, "wb") as f:
        content = uploaded_file.file.read()
        f.write(content)
    
    return str(file_path)


@router.post("/steps/{step_id}/screenshots", response_model=ScreenshotResponse, status_code=201)
async def upload_screenshot(step_id: int, file: UploadFile = File(...)):
    """
    Upload a screenshot for a step.
    
    Args:
        step_id: The ID of the step
        file: The image file to upload
        
    Returns:
        Created screenshot details
    """
    try:
        # Check if step exists
        step = get_step_by_id(step_id)
        if not step:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        
        test_case_id = step['test_case_id']
        
        # Save the file
        file_path = save_uploaded_file(file, test_case_id, step_id)
        
        # Add to database
        screenshot_id = add_screenshot_to_step_db(step_id, file_path)
        if not screenshot_id:
            # If database insert fails, try to delete the file
            try:
                os.remove(file_path)
            except:
                pass
            raise HTTPException(status_code=500, detail="Failed to save screenshot to database")
        
        # Fetch and return the created screenshot
        screenshots = get_screenshots_by_step(step_id)
        created = next((s for s in screenshots if s['id'] == screenshot_id), None)
        if not created:
            raise HTTPException(status_code=500, detail="Screenshot created but could not be retrieved")
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading screenshot: {str(e)}")


@router.get("/steps/{step_id}/screenshots", response_model=List[ScreenshotResponse])
async def list_screenshots(step_id: int):
    """
    Get all screenshots for a step.
    
    Args:
        step_id: The ID of the step
        
    Returns:
        List of screenshots for the step
    """
    try:
        # Check if step exists
        step = get_step_by_id(step_id)
        if not step:
            raise HTTPException(status_code=404, detail=f"Step {step_id} not found")
        
        screenshots = get_screenshots_by_step(step_id)
        return screenshots
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching screenshots: {str(e)}")


@router.get("/screenshots/{screenshot_id}/file")
async def get_screenshot_file(screenshot_id: int):
    """
    Get the actual image file for a screenshot.
    
    Args:
        screenshot_id: The ID of the screenshot
        
    Returns:
        The image file
    """
    try:
        # Get screenshot from any step (we need to find which step has this screenshot)
        # This is a bit inefficient, but we don't have a get_screenshot_by_id function
        # For now, we'll search through steps
        # TODO: Add get_screenshot_by_id to models.py if needed
        
        # Get all test cases and search
        from shared.models import get_all_test_cases, get_steps_by_test_case
        
        all_test_cases = get_all_test_cases()
        screenshot = None
        file_path = None
        
        for tc in all_test_cases:
            steps = get_steps_by_test_case(tc['id'])
            for step in steps:
                screenshots = get_screenshots_by_step(step['id'])
                for s in screenshots:
                    if s['id'] == screenshot_id:
                        screenshot = s
                        file_path = s['file_path']
                        break
                if screenshot:
                    break
            if screenshot:
                break
        
        if not screenshot or not file_path:
            raise HTTPException(status_code=404, detail=f"Screenshot {screenshot_id} not found")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Screenshot file not found: {file_path}")
        
        return FileResponse(file_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching screenshot file: {str(e)}")


@router.delete("/screenshots/{screenshot_id}", status_code=204)
async def delete_screenshot(screenshot_id: int):
    """
    Delete a screenshot.
    
    Args:
        screenshot_id: The ID of the screenshot to delete
        
    Returns:
        No content (204)
    """
    try:
        # Get screenshot info before deleting (to delete the file)
        from shared.models import get_all_test_cases, get_steps_by_test_case
        
        all_test_cases = get_all_test_cases()
        screenshot = None
        file_path = None
        
        for tc in all_test_cases:
            steps = get_steps_by_test_case(tc['id'])
            for step in steps:
                screenshots = get_screenshots_by_step(step['id'])
                for s in screenshots:
                    if s['id'] == screenshot_id:
                        screenshot = s
                        file_path = s['file_path']
                        break
                if screenshot:
                    break
            if screenshot:
                break
        
        if not screenshot:
            raise HTTPException(status_code=404, detail=f"Screenshot {screenshot_id} not found")
        
        # Delete from database
        success = delete_screenshot_db(screenshot_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete screenshot from database")
        
        # Delete the file if it exists
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log error but don't fail the request
                print(f"Warning: Could not delete file {file_path}: {e}")
        
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting screenshot: {str(e)}")

