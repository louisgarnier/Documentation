"""
Routes for project operations.
"""

from fastapi import APIRouter, HTTPException, Query
import sys
from pathlib import Path
from typing import Optional

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.models import (
    get_all_projects,
    get_project_by_id,
    create_project as create_project_db,
    update_project as update_project_db,
    delete_project as delete_project_db,
    get_test_cases_by_project,
    reorder_test_cases as reorder_test_cases_db
)
from api.models import ProjectCreate, ProjectUpdate, ProjectResponse, TestCaseResponse, TestCaseReorderRequest

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[ProjectResponse])
async def list_projects():
    """
    Get all projects.
    
    Returns a list of all projects with their test case counts.
    """
    try:
        projects = get_all_projects()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """
    Get a specific project by ID.
    
    Args:
        project_id: The ID of the project to retrieve
        
    Returns:
        Project details with test case count
    """
    try:
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")


@router.get("/{project_id}/test-cases", response_model=list[TestCaseResponse])
async def get_project_test_cases(project_id: int):
    """
    Get all test cases for a specific project.
    
    Args:
        project_id: The ID of the project
        
    Returns:
        List of test cases in the project
    """
    try:
        # Verify project exists
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Get test cases for the project
        test_cases = get_test_cases_by_project(project_id)
        return test_cases
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching test cases for project: {str(e)}")


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """
    Create a new project.
    
    Args:
        project: Project creation data
        
    Returns:
        Created project details
    """
    try:
        project_id = create_project_db(project.name, project.description)
        if not project_id:
            raise HTTPException(status_code=400, detail="Failed to create project")
        
        # Fetch and return the created project
        created = get_project_by_id(project_id)
        if not created:
            raise HTTPException(status_code=500, detail="Project created but could not be retrieved")
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate):
    """
    Update an existing project.
    
    Args:
        project_id: The ID of the project to update
        project: Project update data
        
    Returns:
        Updated project details
    """
    try:
        # Verify project exists
        existing = get_project_by_id(project_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Use existing values if not provided
        name = project.name if project.name is not None else existing['name']
        description = project.description if project.description is not None else existing.get('description')
        
        # Update the project
        success = update_project_db(project_id, name, description)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update project")
        
        # Fetch and return the updated project
        updated = get_project_by_id(project_id)
        if not updated:
            raise HTTPException(status_code=500, detail="Project updated but could not be retrieved")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, move_to_project_id: Optional[int] = Query(None)):
    """
    Delete a project.
    
    Args:
        project_id: The ID of the project to delete
        move_to_project_id: Optional project ID to move test cases to. If not provided, test cases will be set to NULL.
        
    Returns:
        No content (204)
    """
    try:
        # Verify project exists
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Don't allow deleting the default "Unassigned" project
        if project['name'] == 'Unassigned':
            raise HTTPException(status_code=400, detail="Cannot delete the default 'Unassigned' project")
        
        # If moving to another project, verify it exists
        if move_to_project_id is not None:
            target_project = get_project_by_id(move_to_project_id)
            if not target_project:
                raise HTTPException(status_code=404, detail=f"Target project {move_to_project_id} not found")
        
        # Delete the project
        success = delete_project_db(project_id, move_to_project_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to delete project")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")


@router.post("/{project_id}/test-cases/reorder", response_model=dict)
async def reorder_test_cases(project_id: int, request: TestCaseReorderRequest):
    """
    Reorder test cases within a project.
    
    Args:
        project_id: The ID of the project
        request: Request containing list of test case IDs in the desired order
        
    Returns:
        Success message
    """
    try:
        # Verify project exists
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Validate request
        if not request.test_case_ids:
            raise HTTPException(status_code=400, detail="test_case_ids list cannot be empty")
        
        # Reorder test cases
        success = reorder_test_cases_db(project_id, request.test_case_ids)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to reorder test cases")
        
        return {"message": "Test cases reordered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reordering test cases: {str(e)}")

