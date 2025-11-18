'use client';

import React, { useState, useCallback } from 'react';
import * as XLSX from 'xlsx';

interface ExcelCalculationEditorProps {
  value: string | null; // Base64 encoded XLSX or null
  onChange: (value: string | null) => void; // Callback with base64 XLSX
  readOnly?: boolean;
  rows?: number;
  cols?: number;
}

interface CellData {
  value: string;
  formula?: string;
}

type GridData = CellData[][];

// Simple formula parser for basic Excel functions
const evaluateFormula = (formula: string, grid: GridData, rows: number, cols: number): string => {
  if (!formula || !formula.startsWith('=')) {
    console.log('Not a formula:', formula);
    return formula || '';
  }

  const formulaBody = formula.substring(1).trim();
  console.log('Evaluating formula body:', formulaBody, 'Length:', formulaBody.length);

  // Handle simple cell reference FIRST (e.g., =A1) - this is the most common case
  const cellRefMatch = formulaBody.match(/^([A-Z]+\d+)$/i);
  if (cellRefMatch) {
    console.log('Cell reference match:', cellRefMatch[1]);
    const addr = parseCellAddress(cellRefMatch[1]);
    console.log('Parsed address:', addr);
    if (addr.row >= 0 && addr.row < rows && addr.col >= 0 && addr.col < cols) {
      const cell = grid[addr.row]?.[addr.col];
      console.log('Referenced cell:', cell);
      // If the referenced cell has a formula, return its calculated value
      // Otherwise return the value
      return cell?.value || '0';
    }
    console.log('Cell reference out of bounds');
    return '#REF!';
  }

  // Handle =SUM(range) - e.g., =SUM(A1:A5) or =SUM(A1:A5) with spaces
  const sumMatch = formulaBody.match(/^SUM\s*\(\s*([A-Z]+\d+)\s*:\s*([A-Z]+\d+)\s*\)$/i);
  if (sumMatch) {
    console.log('SUM match:', sumMatch[1], 'to', sumMatch[2]);
    const start = parseCellAddress(sumMatch[1]);
    const end = parseCellAddress(sumMatch[2]);
    console.log('SUM range:', start, 'to', end);
    
    let sum = 0;
    for (let r = start.row; r <= end.row && r < rows; r++) {
      for (let c = start.col; c <= end.col && c < cols; c++) {
        const cell = grid[r]?.[c];
        // Skip if it's a formula (to avoid circular references)
        if (!cell?.formula) {
          const val = parseFloat(cell?.value || '0');
          if (!isNaN(val)) sum += val;
        }
      }
    }
    console.log('SUM result:', sum);
    return sum.toString();
  }
  
  // Handle =SUM(A:A) - entire column
  const sumColMatch = formulaBody.match(/^SUM\(([A-Z]+):([A-Z]+)\)$/i);
  if (sumColMatch && sumColMatch[1] === sumColMatch[2]) {
    const colStr = sumColMatch[1].toUpperCase();
    const col = parseCellAddress(`${colStr}1`).col;
    let sum = 0;
    for (let r = 0; r < rows; r++) {
      const cell = grid[r]?.[col];
      if (!cell?.formula) {
        const val = parseFloat(cell?.value || '0');
        if (!isNaN(val)) sum += val;
      }
    }
    return sum.toString();
  }

  // Handle =ABS(value)
  const absMatch = formulaBody.match(/^ABS\s*\(\s*([A-Z]+\d+)\s*\)$/i);
  if (absMatch) {
    const addr = parseCellAddress(absMatch[1]);
    const val = parseFloat(grid[addr.row]?.[addr.col]?.value || '0');
    return Math.abs(val).toString();
  }

  // Handle =AVG(range)
  const avgMatch = formulaBody.match(/^AVG\s*\(\s*([A-Z]+\d+)\s*:\s*([A-Z]+\d+)\s*\)$/i);
  if (avgMatch) {
    const start = parseCellAddress(avgMatch[1]);
    const end = parseCellAddress(avgMatch[2]);
    let sum = 0;
    let count = 0;
    for (let r = start.row; r <= end.row && r < rows; r++) {
      for (let c = start.col; c <= end.col && c < cols; c++) {
        const cell = grid[r]?.[c];
        if (!cell?.formula) {
          const val = parseFloat(cell?.value || '0');
          if (!isNaN(val)) {
            sum += val;
            count++;
          }
        }
      }
    }
    return count > 0 ? (sum / count).toString() : '0';
  }

  // Handle =MAX(range)
  const maxMatch = formulaBody.match(/^MAX\s*\(\s*([A-Z]+\d+)\s*:\s*([A-Z]+\d+)\s*\)$/i);
  if (maxMatch) {
    const start = parseCellAddress(maxMatch[1]);
    const end = parseCellAddress(maxMatch[2]);
    let max = -Infinity;
    for (let r = start.row; r <= end.row && r < rows; r++) {
      for (let c = start.col; c <= end.col && c < cols; c++) {
        const cell = grid[r]?.[c];
        if (!cell?.formula) {
          const val = parseFloat(cell?.value || '0');
          if (!isNaN(val) && val > max) max = val;
        }
      }
    }
    return max !== -Infinity ? max.toString() : '0';
  }

  // Handle =MIN(range)
  const minMatch = formulaBody.match(/^MIN\s*\(\s*([A-Z]+\d+)\s*:\s*([A-Z]+\d+)\s*\)$/i);
  if (minMatch) {
    const start = parseCellAddress(minMatch[1]);
    const end = parseCellAddress(minMatch[2]);
    let min = Infinity;
    for (let r = start.row; r <= end.row && r < rows; r++) {
      for (let c = start.col; c <= end.col && c < cols; c++) {
        const cell = grid[r]?.[c];
        if (!cell?.formula) {
          const val = parseFloat(cell?.value || '0');
          if (!isNaN(val) && val < min) min = val;
        }
      }
    }
    return min !== Infinity ? min.toString() : '0';
  }


  // Handle simple arithmetic with cell references (e.g., =A1+B2, =A1*B2)
  const arithmeticMatch = formulaBody.match(/^([A-Z]+\d+)\s*([+\-*/])\s*([A-Z]+\d+)$/i);
  if (arithmeticMatch) {
    const addr1 = parseCellAddress(arithmeticMatch[1]);
    const addr2 = parseCellAddress(arithmeticMatch[3]);
    const op = arithmeticMatch[2];
    
    const cell1 = grid[addr1.row]?.[addr1.col];
    const cell2 = grid[addr2.row]?.[addr2.col];
    
    const val1 = parseFloat(cell1?.value || '0');
    const val2 = parseFloat(cell2?.value || '0');
    
    if (isNaN(val1) || isNaN(val2)) return '#N/A';
    
    switch (op) {
      case '+': return (val1 + val2).toString();
      case '-': return (val1 - val2).toString();
      case '*': return (val1 * val2).toString();
      case '/': return val2 !== 0 ? (val1 / val2).toString() : '#DIV/0!';
      default: return '#N/A';
    }
  }

  // Handle complex formulas like =SUM(A1:A5)+B1
  const complexMatch = formulaBody.match(/^SUM\s*\(\s*([A-Z]+\d+)\s*:\s*([A-Z]+\d+)\s*\)\s*([+\-*/])\s*([A-Z]+\d+)$/i);
  if (complexMatch) {
    const start = parseCellAddress(complexMatch[1]);
    const end = parseCellAddress(complexMatch[2]);
    const op = complexMatch[3];
    const addr2 = parseCellAddress(complexMatch[4]);
    
    let sum = 0;
    for (let r = start.row; r <= end.row && r < rows; r++) {
      for (let c = start.col; c <= end.col && c < cols; c++) {
        const cell = grid[r]?.[c];
        if (!cell?.formula) {
          const val = parseFloat(cell?.value || '0');
          if (!isNaN(val)) sum += val;
        }
      }
    }
    
    const cell2 = grid[addr2.row]?.[addr2.col];
    const val2 = parseFloat(cell2?.value || '0');
    if (isNaN(val2)) return '#N/A';
    
    switch (op) {
      case '+': return (sum + val2).toString();
      case '-': return (sum - val2).toString();
      case '*': return (sum * val2).toString();
      case '/': return val2 !== 0 ? (sum / val2).toString() : '#DIV/0!';
      default: return '#N/A';
    }
  }

  console.log('No formula match found for:', formulaBody);
  return '#N/A';
};

const parseCellAddress = (address: string): { row: number; col: number } => {
  const match = address.match(/^([A-Z]+)(\d+)$/i);
  if (!match) {
    console.log('parseCellAddress: No match for', address);
    return { row: 0, col: 0 };
  }
  
  const colStr = match[1].toUpperCase();
  const row = parseInt(match[2]) - 1; // Convert to 0-based
  
  let col = 0;
  for (let i = 0; i < colStr.length; i++) {
    col = col * 26 + (colStr.charCodeAt(i) - 64);
  }
  col -= 1; // Convert to 0-based
  
  console.log('parseCellAddress:', address, '->', { row, col });
  return { row, col };
};

const getCellAddress = (row: number, col: number): string => {
  let colStr = '';
  let colNum = col + 1;
  while (colNum > 0) {
    colNum--;
    colStr = String.fromCharCode(65 + (colNum % 26)) + colStr;
    colNum = Math.floor(colNum / 26);
  }
  return `${colStr}${row + 1}`;
};

export const ExcelCalculationEditor: React.FC<ExcelCalculationEditorProps> = ({
  value,
  onChange,
  readOnly = false,
  rows = 15,
  cols = 10,
}) => {
  const [grid, setGrid] = useState<GridData>(() => {
    const initialGrid: GridData = [];
    for (let r = 0; r < rows; r++) {
      initialGrid[r] = [];
      for (let c = 0; c < cols; c++) {
        initialGrid[r][c] = { value: '' };
      }
    }
    return initialGrid;
  });

  const [editingCell, setEditingCell] = useState<{ row: number; col: number } | null>(null);
  const [editValue, setEditValue] = useState('');
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const isClickingCell = React.useRef<boolean>(false);

  // Load data from XLSX
  React.useEffect(() => {
    if (value) {
      try {
        const binaryString = atob(value);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        const workbook = XLSX.read(bytes, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const range = XLSX.utils.decode_range(worksheet['!ref'] || 'A1');
        
        const newGrid: GridData = [];
        for (let r = 0; r < rows; r++) {
          newGrid[r] = [];
          for (let c = 0; c < cols; c++) {
            if (r <= range.e.r && c <= range.e.c) {
              const cellAddress = XLSX.utils.encode_cell({ r, c });
              const cell = worksheet[cellAddress];
              newGrid[r][c] = {
                value: cell?.v?.toString() || '',
                formula: cell?.f || undefined,
              };
            } else {
              newGrid[r][c] = { value: '' };
            }
          }
        }
        setGrid(newGrid);
      } catch (error) {
        console.error('Error loading spreadsheet data:', error);
      }
    }
  }, [value, rows, cols]);

  // Recalculate formulas when grid changes
  const recalculateFormulas = useCallback((gridData: GridData): GridData => {
    const newGrid = gridData.map(row => row.map(cell => ({ ...cell })));
    
    // Evaluate formulas - may need multiple passes for dependencies
    let changed = true;
    let iterations = 0;
    const maxIterations = 10; // Prevent infinite loops
    
    while (changed && iterations < maxIterations) {
      changed = false;
      iterations++;
      
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const cell = newGrid[r][c];
          if (cell.formula) {
            const oldValue = cell.value;
            cell.value = evaluateFormula(cell.formula, newGrid, rows, cols);
            if (oldValue !== cell.value) {
              changed = true;
            }
          }
        }
      }
    }
    
    return newGrid;
  }, [rows, cols]);

  const handleCellChange = (row: number, col: number, newValue: string) => {
    const newGrid = grid.map(r => r.map(c => ({ ...c })));
    const trimmedValue = newValue.trim();
    const isFormula = trimmedValue.startsWith('=');
    
    console.log('Cell change:', { row, col, newValue, trimmedValue, isFormula });
    
    if (isFormula) {
      // It's a formula - store it and calculate
      newGrid[row][col] = {
        value: '', // Will be calculated
        formula: trimmedValue,
      };
      console.log('Formula detected:', trimmedValue);
    } else if (trimmedValue === '') {
      // Empty cell
      newGrid[row][col] = {
        value: '',
        formula: undefined,
      };
    } else {
      // Regular value
      newGrid[row][col] = {
        value: trimmedValue,
        formula: undefined,
      };
    }
    
    const recalculated = recalculateFormulas(newGrid);
    console.log('Recalculated grid:', recalculated[row][col]);
    setGrid(recalculated);
    
    // Save to XLSX
    saveToXLSX(recalculated);
  };

  const saveToXLSX = (gridData: GridData) => {
    try {
      const workbook = XLSX.utils.book_new();
      const worksheet: any = {};
      
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const cell = gridData[r][c];
          if (cell.value || cell.formula) {
            const cellAddress = XLSX.utils.encode_cell({ r, c });
            worksheet[cellAddress] = {
              v: cell.formula ? cell.value : cell.value,
              f: cell.formula || undefined,
              t: cell.formula ? 'n' : 's',
            };
          }
        }
      }
      
      worksheet['!ref'] = XLSX.utils.encode_range({
        s: { r: 0, c: 0 },
        e: { r: rows - 1, c: cols - 1 },
      });
      
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
      
      const xlsxBuffer = XLSX.write(workbook, { type: 'array', bookType: 'xlsx' });
      const base64 = btoa(
        String.fromCharCode.apply(null, Array.from(new Uint8Array(xlsxBuffer)))
      );
      
      onChange(base64);
    } catch (error) {
      console.error('Error saving spreadsheet data:', error);
    }
  };

  const handleCellClick = (row: number, col: number, e?: React.MouseEvent) => {
    if (readOnly) return;
    
    // If we're already editing a cell, clicking another cell should insert its reference
    if (editingCell && (editingCell.row !== row || editingCell.col !== col)) {
      isClickingCell.current = true;
      const cellAddress = getCellAddress(row, col);
      const input = inputRef.current;
      if (input) {
        const start = input.selectionStart || 0;
        const end = input.selectionEnd || 0;
        const currentValue = editValue || '';
        // Insert cell reference at cursor position
        const newValue = currentValue.substring(0, start) + cellAddress + currentValue.substring(end);
        setEditValue(newValue);
        // Restore focus and cursor position
        setTimeout(() => {
          input.focus();
          const newCursorPos = start + cellAddress.length;
          input.setSelectionRange(newCursorPos, newCursorPos);
          isClickingCell.current = false;
        }, 10);
      } else {
        // Fallback: append if input not available
        setEditValue((editValue || '') + cellAddress);
        isClickingCell.current = false;
      }
      e?.stopPropagation();
      e?.preventDefault();
      return;
    }
    
    // Normal click - start editing this cell
    setEditingCell({ row, col });
    const cell = grid[row]?.[col];
    setEditValue(cell?.formula || cell?.value || '');
  };

  const handleCellBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    // Don't save if we're clicking on another cell to insert reference
    if (isClickingCell.current) {
      return;
    }
    
    if (editingCell) {
      // Use the current input value, not the state (which might be outdated)
      const finalValue = e.currentTarget.value.trim();
      console.log('Cell blur - final value:', finalValue);
      handleCellChange(editingCell.row, editingCell.col, finalValue);
      setEditingCell(null);
      setEditValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const input = e.currentTarget;
      const finalValue = input.value;
      if (editingCell) {
        handleCellChange(editingCell.row, editingCell.col, finalValue);
        setEditingCell(null);
        setEditValue('');
      }
    } else if (e.key === 'Escape') {
      setEditingCell(null);
      setEditValue('');
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // Allow tab to move to next cell or finish editing
      if (editingCell) {
        const finalValue = e.currentTarget.value;
        handleCellChange(editingCell.row, editingCell.col, finalValue);
        setEditingCell(null);
        setEditValue('');
      }
    }
  };

  return (
    <div className="w-full border border-gray-300 dark:border-gray-600 rounded-md overflow-auto" style={{ maxHeight: '400px' }}>
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="w-12 h-8 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-center text-xs font-medium"></th>
            {Array.from({ length: cols }, (_, i) => (
              <th key={i} className="w-20 h-8 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-center text-xs font-medium">
                {getCellAddress(0, i).replace(/\d/g, '')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: rows }, (_, rowIndex) => (
            <tr key={rowIndex}>
              <td className="w-12 h-8 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-center text-xs font-medium">
                {rowIndex + 1}
              </td>
              {Array.from({ length: cols }, (_, colIndex) => {
                const cell = grid[rowIndex][colIndex];
                const isEditing = editingCell?.row === rowIndex && editingCell?.col === colIndex;
                const cellAddress = getCellAddress(rowIndex, colIndex);
                const hasFormula = !!cell.formula;
                const isError = cell.value.startsWith('#');
                
                return (
                  <td
                    key={colIndex}
                    className={`h-8 border border-gray-300 dark:border-gray-600 p-0 ${
                      isEditing ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                    } ${hasFormula ? 'bg-yellow-50 dark:bg-yellow-900/20' : ''} ${
                      isError ? 'text-red-600 dark:text-red-400' : ''
                    }`}
                    onClick={(e) => {
                      // Always allow clicks - handleCellClick will decide what to do
                      handleCellClick(rowIndex, colIndex, e);
                    }}
                  >
                    {isEditing ? (
                      <input
                        ref={inputRef}
                        type="text"
                        value={editValue}
                        onChange={(e) => {
                          setEditValue(e.target.value);
                        }}
                        onBlur={handleCellBlur}
                        onKeyDown={handleKeyDown}
                        className="w-full h-full px-1 text-xs border-0 outline-none bg-transparent text-gray-900 dark:text-gray-100"
                        autoFocus
                        placeholder="Enter value or formula (e.g., =A1, =SUM(A1:A5))"
                      />
                ) : (
                  <div className="px-1 py-1 text-xs text-gray-900 dark:text-gray-100">
                    {cell.value || ''}
                    {hasFormula && (
                      <span className="ml-1 text-xs text-gray-400 dark:text-gray-500" title={cell.formula}>
                        📐
                      </span>
                    )}
                  </div>
                )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
