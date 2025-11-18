#!/usr/bin/env python3
"""
View Screenshot Capture Service Logs
Shows recent log entries with filtering options
"""
import sys
from pathlib import Path
import config
from datetime import datetime

def view_logs(lines=50, component=None, level=None, follow=False):
    """View log entries"""
    log_file = Path(config.LOG_FILE)
    
    if not log_file.exists():
        print(f"❌ Log file not found: {log_file}")
        print(f"   The service may not have been started yet.")
        return
    
    print(f"📋 Viewing logs from: {log_file}")
    print(f"   File size: {log_file.stat().st_size / 1024:.1f} KB")
    print(f"{'='*80}\n")
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            
            # Filter by component and level if specified
            filtered_lines = []
            for line in all_lines:
                if component and f"[{component}]" not in line:
                    continue
                if level and f"[{level}]" not in line:
                    continue
                filtered_lines.append(line)
            
            # Show last N lines
            if lines > 0:
                lines_to_show = filtered_lines[-lines:] if filtered_lines else all_lines[-lines:]
            else:
                lines_to_show = filtered_lines if filtered_lines else all_lines
            
            if not lines_to_show:
                print("No log entries found matching the criteria.")
                return
            
            for line in lines_to_show:
                print(line.rstrip())
            
            if follow:
                print("\n--- Following log (Ctrl+C to stop) ---")
                import time
                try:
                    while True:
                        new_lines = f.readlines()
                        for line in new_lines:
                            if component and f"[{component}]" not in line:
                                continue
                            if level and f"[{level}]" not in line:
                                continue
                            print(line.rstrip())
                        time.sleep(0.5)
                except KeyboardInterrupt:
                    print("\n--- Stopped following ---")
                    
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        sys.exit(1)

def show_summary():
    """Show log summary"""
    log_file = Path(config.LOG_FILE)
    
    if not log_file.exists():
        print("Log file not found.")
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"\n📊 Log Summary for: {log_file.name}")
        print(f"{'='*80}")
        print(f"Total lines: {len(lines)}")
        
        # Count by component
        components = {}
        levels = {}
        
        for line in lines:
            # Extract component
            if "[INFO]" in line or "[WARNING]" in line or "[ERROR]" in line or "[DEBUG]" in line:
                parts = line.split("]")
                if len(parts) >= 3:
                    component = parts[2].strip().split()[0] if len(parts[2].strip().split()) > 0 else "UNKNOWN"
                    components[component] = components.get(component, 0) + 1
                    
                    # Extract level
                    level = parts[1].strip().replace("[", "")
                    levels[level] = levels.get(level, 0) + 1
        
        print(f"\nBy Component:")
        for comp, count in sorted(components.items(), key=lambda x: x[1], reverse=True):
            print(f"  {comp}: {count}")
        
        print(f"\nBy Level:")
        for level, count in sorted(levels.items(), key=lambda x: x[1], reverse=True):
            print(f"  {level}: {count}")
        
        # Show first and last entries
        if lines:
            print(f"\nFirst entry: {lines[0].rstrip()[:80]}")
            print(f"Last entry:  {lines[-1].rstrip()[:80]}")
            
    except Exception as e:
        print(f"Error reading log: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="View Screenshot Capture Service logs")
    parser.add_argument("-n", "--lines", type=int, default=50, help="Number of lines to show (default: 50, 0 for all)")
    parser.add_argument("-c", "--component", help="Filter by component (SERVICE, WATCHER, API, etc.)")
    parser.add_argument("-l", "--level", help="Filter by level (INFO, WARNING, ERROR, DEBUG)")
    parser.add_argument("-f", "--follow", action="store_true", help="Follow log file (like tail -f)")
    parser.add_argument("-s", "--summary", action="store_true", help="Show log summary")
    
    args = parser.parse_args()
    
    if args.summary:
        show_summary()
    else:
        view_logs(lines=args.lines, component=args.component, level=args.level, follow=args.follow)

