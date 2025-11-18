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
    pass


class TestCaseUpdate(BaseModel):
    """Model for updating a test case."""
    test_number: Optional[str] = None
    description: Optional[str] = None


class TestCaseResponse(TestCaseBase):
    """Model for test case response."""
    id: int
    created_at: str

    class Config:
        from_attributes = True


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
    test_case_ids: List[int]

