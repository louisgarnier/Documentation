"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Test Case Models
class TestCaseBase(BaseModel):
    """Base model for test case."""
    test_number: str
    description: str


class TestCaseCreate(TestCaseBase):
    """Model for creating a test case."""
    project_id: Optional[int] = None


class TestCaseUpdate(BaseModel):
    """Model for updating a test case."""
    test_number: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None


class TestCaseResponse(TestCaseBase):
    """Model for test case response."""
    id: int
    project_id: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True


class TestCaseDuplicateRequest(BaseModel):
    """Model for duplicating a test case."""
    new_test_number: str
    target_project_id: Optional[int] = None


class TestCaseMoveRequest(BaseModel):
    """Model for moving a test case to another project."""
    target_project_id: Optional[int] = None


# Test Step Models
class TestStepBase(BaseModel):
    """Base model for test step."""
    step_number: int
    description: str
    modules: Optional[str] = None
    calculation_logic: Optional[str] = None
    configuration: Optional[str] = None


class TestStepCreate(TestStepBase):
    """Model for creating a test step."""
    pass


class TestStepUpdate(BaseModel):
    """Model for updating a test step."""
    step_number: Optional[int] = None
    description: Optional[str] = None
    modules: Optional[str] = None
    calculation_logic: Optional[str] = None
    configuration: Optional[str] = None


class TestStepResponse(TestStepBase):
    """Model for test step response."""
    id: int
    test_case_id: int
    created_at: str

    class Config:
        from_attributes = True


# Reorder Model
class StepReorderRequest(BaseModel):
    """Model for step reordering request."""
    new_position: int


# Screenshot Models
class ScreenshotResponse(BaseModel):
    """Model for screenshot response."""
    id: int
    step_id: int
    file_path: str
    uploaded_at: str

    class Config:
        from_attributes = True


# Export Models
class ExportRequest(BaseModel):
    """Model for export request."""
    test_case_ids: Optional[List[int]] = None
    project_ids: Optional[List[int]] = None


# Load Step Models
class LoadStepRequest(BaseModel):
    """Model for loading a step from Capture_TC/ directory."""
    description: str
    image_paths: List[str]
    description_file_path: Optional[str] = None


# Project Models
class ProjectBase(BaseModel):
    """Base model for project."""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Model for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Model for updating a project."""
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Model for project response."""
    id: int
    test_case_count: Optional[int] = 0
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

