#!/usr/bin/env python3
"""Fix Phase 4 task README files to match actual processed files."""

import os
from pathlib import Path

# Configuration
EXPORT_DIR = Path("/home/sblo/Dev/UsaCom/books/export")
TASKS_DIR = Path("/home/sblo/Dev/UsaCom/plan/development/phase4")
PROCESSED_DIR = Path("/home/sblo/Dev/UsaCom/processed")

# Get all markdown files from export directory (sorted, excluding _fixed)
export_files = sorted([f.stem for f in EXPORT_DIR.glob("*.md") if not f.name.endswith("_fixed.md")])

# Get all processed JSON files
processed_files = [f.stem.replace("_parsed", "").replace("_processed", "") 
                   for f in list(PROCESSED_DIR.glob("*_parsed.json")) + list(PROCESSED_DIR.glob("*_processed.json"))]
processed_files = [f for f in processed_files if not f.startswith("sample_")]

print(f"Export files: {len(export_files)}")
print(f"Processed files: {len(processed_files)}")
print(f"Processed: {sorted(processed_files)}")

# Create mapping: processed file -> task number
# We need to reorganize tasks so that processed files come first

# First, let's identify which export files have been processed
processed_set = set(processed_files)

# Create ordered list: processed files first, then unprocessed
ordered_files = []
for f in export_files:
    if f in processed_set:
        ordered_files.append((f, True))  # (filename, is_processed)
    else:
        ordered_files.append((f, False))

# Sort: processed files first (maintaining export order within each group)
processed_first = [x for x in ordered_files if x[1]]
unprocessed_second = [x for x in ordered_files if not x[1]]
final_order = processed_first + unprocessed_second

print(f"\nReorganized task order:")
print(f"Processed files (tasks 1-{len(processed_first)}): {[x[0] for x in processed_first]}")
print(f"Unprocessed files (tasks {len(processed_first)+1}-{len(final_order)}): {[x[0] for x in unprocessed_second][:5]}...")

# Now create/update task READMEs
for i, (filename, is_processed) in enumerate(final_order, start=1):
    task_num = i
    task_dir = TASKS_DIR / f"task{task_num:02d}"
    task_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if actual output file exists (try both suffixes)
    output_file_parsed = f"{filename}_parsed.json"
    output_file_processed = f"{filename}_processed.json"
    output_path_parsed = PROCESSED_DIR / output_file_parsed
    output_path_processed = PROCESSED_DIR / output_file_processed
    actually_exists = output_path_parsed.exists() or output_path_processed.exists()
    
    # Use the correct output file name
    output_file = output_file_parsed if output_path_parsed.exists() else output_file_processed
    
    # Create README content
    status = "completed" if actually_exists else "pending"
    objective = "Parse" if not is_processed else "Process"
    
    readme_content = f"""# Phase 4 Task {task_num:02d}: {objective.title()} Export File {task_num:02d}

## Status: {status.upper()}

## Objective
{objective.lower()} the markdown file `{filename}.md` using the methodology from PARSING_TECH.md and create structured data in ./processed/ directory.

## Input
- File: books/export/{filename}.md

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
- {"Successfully parsed the markdown file" if actually_exists else "Pending: Parse the markdown file"}
- Output follows the schema described in PARSING_TECH.md
- {"Ready for next task in sequence" if actually_exists else "Task pending execution"}
"""
    
    # Write README file
    readme_path = task_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

print(f"\nDone! Updated all {len(final_order)} task README files.")
print(f"Tasks 1-{len(processed_first)}: Completed (processed files)")
print(f"Tasks {len(processed_first)+1}-{len(final_order)}: Pending (unprocessed files)")
