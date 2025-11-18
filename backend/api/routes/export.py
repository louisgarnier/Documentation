"""
Routes for Excel export operations.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import sys
from pathlib import Path
import os
import tempfile

# Add project root to path to import shared modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.excel_export import create_excel_export
from api.models import ExportRequest

router = APIRouter(prefix="/api", tags=["export"])


@router.post("/export")
async def export_test_cases(export_request: ExportRequest):
    """
    Export selected test cases to Excel.
    
    Args:
        export_request: Request containing list of test case IDs to export
        
    Returns:
        Excel file download
    """
    try:
        if not export_request.test_case_ids:
            raise HTTPException(status_code=400, detail="No test case IDs provided")
        
        # Create temporary file for Excel export
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Generate Excel file
            excel_path = create_excel_export(
                output_path=tmp_path,
                selected_test_case_ids=export_request.test_case_ids
            )
            
            if not excel_path or not os.path.exists(excel_path):
                raise HTTPException(status_code=500, detail="Failed to generate Excel file")
            
            # Generate filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_cases_export_{timestamp}.xlsx"
            
            # Return file as download
            return FileResponse(
                excel_path,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=filename,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
            raise HTTPException(status_code=500, detail=f"Error generating Excel export: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting test cases: {str(e)}")

