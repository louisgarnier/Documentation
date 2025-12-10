"""
FastAPI main application for Test Case Documentation Tool API.
"""

import sys
from pathlib import Path

# Add project root to path for shared imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.models import init_database
from api.routes import test_cases, steps, screenshots, export, capture_service, projects

# Create FastAPI app
app = FastAPI(
    title="Test Case Documentation API",
    description="REST API for managing SimCorp Dimension test case documentation",
    version="1.0.0"
)

# Configure CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(test_cases.router)
app.include_router(steps.router)
app.include_router(screenshots.router)
app.include_router(export.router)
app.include_router(capture_service.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_database()


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {"status": "ok", "message": "Test Case Documentation API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

