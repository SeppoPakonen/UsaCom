#!/usr/bin/env python3
"""Generate Phase 4 task README files for all export markdown files."""

import os
from pathlib import Path

# Configuration
EXPORT_DIR = Path("/home/sblo/Dev/UsaCom/books/export")
TASKS_DIR = Path("/home/sblo/Dev/UsaCom/plan/development/phase4")

# Get all markdown files from export directory (sorted)
export_files = sorted([f.name for f in EXPORT_DIR.glob("*.md")])

# Skip the _fixed file as it's a corrected version
export_files = [f for f in export_files if not f.endswith("_fixed.md")]

print(f"Found {len(export_files)} export files to process")

# Already have tasks 01-07 with README files
# Task 01 = techventure_chunk_aa (already processed)
# Task 07 = techventure_chunk_af (already processed)
# Start from task 08 = techventure_chunk_ag

# Create task directories and README files
for i, filename in enumerate(export_files, start=1):
    task_num = i
    task_dir = TASKS_DIR / f"task{task_num:02d}"
    
    # Create task directory if it doesn't exist
    task_dir.mkdir(parents=True, exist_ok=True)
    
    # Get base name without .md extension
    base_name = filename.replace(".md", "")
    
    # Determine output filename
    output_file = f"{base_name}_parsed.json"
    
    # Check if this is already processed (tasks 01-07)
    readme_path = task_dir / "README.md"
    
    if readme_path.exists():
        print(f"Task {task_num:02d}: {filename} - README exists (skipping)")
        continue
    
    # Create README content
    readme_content = f"""# Phase 4 Task {task_num:02d}: Process Export File {task_num:02d}

## Objective
Parse the markdown file `{filename}` using the methodology from PARSING_TECH.md and create structured data in ./processed/ directory.

## Input
- File: books/export/{filename}

## Process
- Apply parsing methodology from PARSING_TECH.md
- Extract keywords with relevance scoring
- Identify ECS (Entity-Component-System) elements
- Extract business constraints
- Generate metadata with USA business context
- Create structured JSON output

## Output
- File: processed/{output_file}
- Contains structured data with keywords, ECS elements, constraints, and metadata

## Verification
- Successfully parsed the markdown file
- Output follows the schema described in PARSING_TECH.md
- Ready for next task in sequence
"""
    
    # Write README file
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Task {task_num:02d}: {filename} - README created")

print(f"\nDone! Created task README files for all {len(export_files)} export files.")
