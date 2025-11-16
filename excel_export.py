"""
Excel Export Module for Test Case Documentation Tool

This module handles exporting test cases and their data to Excel workbooks.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from models import (
    get_all_test_cases,
    get_test_case_by_id,
    get_steps_by_test_case,
    get_screenshots_by_step
)
from datetime import datetime
import os


def create_excel_export(output_path="test_cases_export.xlsx", selected_test_case_ids=None):
    """
    Create an Excel workbook with test case documentation.
    
    Args:
        output_path: Path where the Excel file should be saved
        selected_test_case_ids: Optional list of test case IDs to export. If None, exports all.
        
    Returns:
        str: Path to the created Excel file
    """
    # Create workbook
    wb = Workbook()
    
    # Remove default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    
    # Get test cases (filtered if IDs provided)
    if selected_test_case_ids:
        all_test_cases = get_all_test_cases()
        test_cases = [tc for tc in all_test_cases if tc['id'] in selected_test_case_ids]
    else:
        test_cases = get_all_test_cases()
    
    # Create Summary sheet
    summary_sheet = wb.create_sheet("Summary", 0)
    create_summary_sheet(summary_sheet, test_cases)
    
    # Create a sheet for each test case
    for test_case in test_cases:
        sheet_name = f"{test_case['test_number']}"
        # Excel sheet names have a 31 character limit
        if len(sheet_name) > 31:
            sheet_name = sheet_name[:28] + "..."
        
        # Check if sheet name already exists (handle duplicates)
        base_name = sheet_name
        counter = 1
        while sheet_name in [s.title for s in wb.worksheets]:
            sheet_name = f"{base_name[:26]}_{counter}"
            counter += 1
        
        test_sheet = wb.create_sheet(sheet_name)
        create_test_case_sheet(test_sheet, test_case)
    
    # Save workbook
    wb.save(output_path)
    return output_path


def create_summary_sheet(sheet, test_cases=None):
    """Create the summary sheet with all test cases matching the reference format."""
    # Get test cases if not provided
    if test_cases is None:
        test_cases = get_all_test_cases()
    
    # Row 2: Title (centered in column B)
    title_cell = sheet.cell(row=2, column=2)
    title_cell.value = "Test Case Documentation"
    title_cell.font = Font(bold=True, size=14)
    
    # Row 4: Headers (starting in column B to match reference format)
    headers = ["Test Case ID", "Test Case Name", "Execution Status", "Outcome"]
    header_font = Font(bold=True, size=11)
    
    for col_num, header in enumerate(headers, 2):  # Start from column B (2)
        cell = sheet.cell(row=4, column=col_num)
        cell.value = header
        cell.font = header_font
    
    # Row 5 onwards: Test case data
    for row_num, test_case in enumerate(test_cases, 5):
        # Column B: Test Case ID
        sheet.cell(row=row_num, column=2).value = test_case['test_number']
        # Column C: Test Case Name (Description)
        sheet.cell(row=row_num, column=3).value = test_case['description']
        # Column D: Execution Status (default to "Completed" or leave empty)
        sheet.cell(row=row_num, column=4).value = "Completed"
        # Column E: Outcome (default to "Pass" or leave empty)
        sheet.cell(row=row_num, column=5).value = "Pass"
    
    # Auto-adjust column widths
    sheet.column_dimensions['B'].width = 20
    sheet.column_dimensions['C'].width = 60
    sheet.column_dimensions['D'].width = 18
    sheet.column_dimensions['E'].width = 15


def create_test_case_sheet(sheet, test_case):
    """Create a sheet for a specific test case matching the reference format with embedded screenshots."""
    # Row 2: Title linking to Summary (formula format like reference)
    # Format: =Summary!B6&" - "&Summary!C6
    # For now, we'll use a simple title format
    title_cell = sheet.cell(row=2, column=2)
    title_cell.value = f"{test_case['test_number']} - {test_case['description']}"
    title_cell.font = Font(bold=True, size=12)
    
    # Row 10: Navigation links (matching reference format)
    sheet.cell(row=10, column=10).value = "Go to"
    sheet.cell(row=10, column=11).value = "[Summary]"
    
    # Get steps
    steps = get_steps_by_test_case(test_case['id'])
    
    if steps:
        # Start steps from row 6 (matching reference format)
        current_row = 6
        
        for step in steps:
            # Step description in column B (format: "1  Description")
            step_cell = sheet.cell(row=current_row, column=2)
            step_cell.value = f"{step['step_number']}  {step['description']}"
            step_cell.font = Font(bold=True, size=11)
            
            # Add metadata in adjacent columns if available
            if step.get('modules'):
                sheet.cell(row=current_row, column=3).value = f"Modules: {step['modules']}"
            if step.get('calculation_logic'):
                sheet.cell(row=current_row, column=4).value = f"Calculation: {step['calculation_logic']}"
            if step.get('configuration'):
                sheet.cell(row=current_row, column=5).value = f"Config: {step['configuration']}"
            
            # Get screenshots for this step
            screenshots = get_screenshots_by_step(step['id'])
            
            # Add screenshots below the step description
            if screenshots:
                image_row = current_row + 1
                image_col = 2  # Start in column B
                
                for screenshot in screenshots:
                    screenshot_path = screenshot['file_path']
                    
                    # Check if file exists
                    if os.path.exists(screenshot_path):
                        try:
                            # Load and resize image if needed
                            img = XLImage(screenshot_path)
                            
                            # Resize image to fit nicely (max width 500px, maintain aspect ratio)
                            max_width = 500
                            if img.width > max_width:
                                ratio = max_width / img.width
                                img.width = int(img.width * ratio)
                                img.height = int(img.height * ratio)
                            
                            # Anchor image to cell (column B)
                            cell_ref = f"{get_column_letter(image_col)}{image_row}"
                            img.anchor = cell_ref
                            
                            # Add image to sheet
                            sheet.add_image(img)
                            
                            # Adjust row height to accommodate image (convert pixels to points: 1 point ≈ 1.33 pixels)
                            row_height = max(int(img.height * 0.75), 100)
                            sheet.row_dimensions[image_row].height = row_height
                            
                            # Move to next row for next image (stack vertically)
                            image_row += 1
                            
                        except Exception as e:
                            # If image can't be loaded, add text reference
                            sheet.cell(row=image_row, column=image_col).value = f"[Image: {os.path.basename(screenshot_path)}]"
                            image_row += 1
                    else:
                        # File doesn't exist, add text reference
                        sheet.cell(row=image_row, column=image_col).value = f"[Image not found: {os.path.basename(screenshot_path)}]"
                        image_row += 1
                
                # Move to next step (leave space after images)
                current_row = image_row + 2
            else:
                # No screenshots, just move to next step
                current_row += 2
        
        # Auto-adjust column widths
        sheet.column_dimensions['B'].width = 50
        sheet.column_dimensions['C'].width = 30
        sheet.column_dimensions['D'].width = 30
        sheet.column_dimensions['E'].width = 30
    else:
        # No steps
        sheet.cell(row=6, column=2).value = "No steps defined for this test case."
        sheet.cell(row=6, column=2).font = Font(italic=True)


if __name__ == "__main__":
    # Test the export function
    print("Creating Excel export...")
    output_file = create_excel_export("test_export.xlsx")
    print(f"Excel file created: {output_file}")

