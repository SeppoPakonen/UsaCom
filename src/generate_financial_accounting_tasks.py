#!/usr/bin/env python3
"""Generate README files for Financial Accounting track tasks."""

from pathlib import Path

BASE = Path("/home/sblo/Dev/UsaCom/plan/financial-accounting")

# Phase 3: Manual Conversion Tasks (28 tasks)
phase3_template = """# Phase 3 Task {task_num:02d}: Convert Financial Accounting Chunk {chunk_name}

## Status: PENDING

## Objective
Manually read and convert the OCR text chunk to clean markdown format.

## Input
- File: books/rawtxt/financial_accounting/financial_accounting_chunk_{chunk_name}

## Process
1. Read the raw OCR text chunk
2. Clean up OCR errors and formatting issues
3. Convert to structured markdown format
4. Preserve financial accounting terminology accurately
5. Add appropriate headers and structure

## Output
- File: books/export/financial_accounting/financial_accounting_chunk_{chunk_name}.md

## Guidelines
- Fix OCR misreadings (e.g., "0" vs "O", "1" vs "l")
- Preserve tables as markdown tables where possible
- Keep financial formulas and equations intact
- Add section headers for better navigation
- Remove page numbers and headers/footers from OCR

## Verification
- Review converted markdown for accuracy
- Check financial terms are correctly spelled
- Ensure numbers and figures are accurate

## Next Steps
- Proceed to next chunk in sequence
- After all chunks complete, proceed to Phase 4

"""

# Phase 4: Parsing Tasks (28 tasks)
phase4_template = """# Phase 4 Task {task_num:02d}: Parse Financial Accounting Chunk {chunk_name}

## Status: PENDING

## Objective
Parse the markdown file and create structured JSON data.

## Input
- File: books/export/financial_accounting/financial_accounting_chunk_{chunk_name}.md

## Process
1. Apply parsing methodology from PARSING_TECH.md
2. Extract keywords with relevance scoring
3. Identify ECS (Entity-Component-System) elements
4. Extract business constraints
5. Generate metadata with financial accounting context
6. Create structured JSON output

## Output
- File: processed/financial_accounting/financial_accounting_chunk_{chunk_name}_parsed.json
- Contains: keywords, ECS elements, constraints, metadata

## Verification
- Successfully parsed the markdown file
- Output follows schema from PARSING_TECH.md
- Ready for next task in sequence

## Next Steps
- Proceed to next chunk in sequence
- After all chunks complete, proceed to Phase 5

"""

# Phase 5: Integration Tasks
phase5_tasks = {
    "01": ("Create Unified Action Planner and Virtual Map", """
## Objective
Develop a unified action planner based on processed financial accounting data and create metaphorical map elements.

## Process
1. Analyze processed financial accounting data
2. Extract key accounting concepts for action planner
3. Create virtual map regions for accounting journey
4. Design accounting-specific challenges and allies
5. Document navigation rules

## Output
- processed/financial_accounting_action_planner.json
- processed/financial_accounting_virtual_map.json
"""),
    "02": ("Validate Financial Accounting Integration", """
## Objective
Cross-reference financial accounting content with existing business formation content.

## Process
1. Compare accounting concepts with business phases
2. Identify integration points
3. Validate completeness of accounting coverage
4. Create gap analysis report

## Output
- processed/financial_accounting_validation_report.md
"""),
    "03": ("Create Accounting Decision Trees", """
## Objective
Design decision trees for accounting method selection.

## Process
1. Map accounting method choices (cash vs accrual)
2. Create depreciation method decision tree
3. Design inventory valuation decision tree
4. Add tax implication branches

## Output
- processed/accounting_decision_trees.json
"""),
    "04": ("Integrate Accounting Metrics into Game", """
## Objective
Add financial accounting metrics to simulation game.

## Process
1. Define accounting KPIs for game
2. Create balance sheet tracking
3. Implement income statement calculations
4. Add financial ratio analysis

## Output
- src/accounting_metrics.py
- processed/accounting_game_metrics.json
"""),
    "05": ("Create Financial Statement Challenges", """
## Objective
Design accounting-specific challenges for the game.

## Process
1. Create cash flow management challenges
2. Design accounts receivable scenarios
3. Add inventory management challenges
4. Implement depreciation tracking challenges

## Output
- src/accounting_challenges.py
"""),
    "06": ("Add Accounting Tutorial Content", """
## Objective
Create tutorial content for financial accounting concepts.

## Process
1. Write basic accounting tutorials
2. Create debits/credits interactive lessons
3. Design financial statement reading guides
4. Add ratio analysis tutorials

## Output
- src/accounting_tutorial.py
"""),
    "07": ("Create Accounting Scenarios", """
## Objective
Develop business scenarios with accounting focus.

## Process
1. Create retail accounting scenario
2. Design service business scenario
3. Add manufacturing accounting scenario
4. Include nonprofit accounting scenario

## Output
- processed/accounting_scenarios.json
"""),
    "08": ("Integrate Tax Planning Content", """
## Objective
Add tax planning based on accounting data.

## Process
1. Map accounting methods to tax implications
2. Create depreciation tax strategies
3. Design entity selection tax analysis
4. Add quarterly tax estimation

## Output
- processed/tax_planning_integration.json
"""),
    "09": ("Create Financial Reporting System", """
## Objective
Implement financial reporting for game sessions.

## Process
1. Design session financial reports
2. Create performance dashboards
3. Add trend analysis
4. Implement benchmark comparisons

## Output
- src/financial_reporting.py
"""),
    "10": ("Prepare Phase 6 Handoff for Accounting", """
## Objective
Compile all accounting integration artifacts.

## Process
1. Catalog accounting artifacts
2. Create integration documentation
3. Document data structures
4. Provide implementation guide

## Output
- processed/financial_accounting_handoff.md
""")
}


def main():
    # Phase 3 README files
    chunk_names = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am',
                   'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba']
    
    for i, chunk in enumerate(chunk_names, start=1):
        task_dir = BASE / f"phase3/task{i:02d}"
        readme_path = task_dir / "README.md"
        
        content = phase3_template.format(task_num=i, chunk_name=chunk)
        with open(readme_path, 'w') as f:
            f.write(content)
    
    print(f"Created {len(chunk_names)} Phase 3 README files")
    
    # Phase 4 README files
    for i, chunk in enumerate(chunk_names, start=1):
        task_dir = BASE / f"phase4/task{i:02d}"
        readme_path = task_dir / "README.md"
        
        content = phase4_template.format(task_num=i, chunk_name=chunk)
        with open(readme_path, 'w') as f:
            f.write(content)
    
    print(f"Created {len(chunk_names)} Phase 4 README files")
    
    # Phase 5 README files
    for task_num, (title, content) in phase5_tasks.items():
        task_dir = BASE / f"phase5/task{task_num}"
        readme_path = task_dir / "README.md"
        
        full_content = f"""# Phase 5 Task {task_num}: {title}

## Status: PENDING
{content}
## Verification
- Output files created and validated
- Meets Phase 5 requirements
- Ready for next task or Phase 6 integration

"""
        with open(readme_path, 'w') as f:
            f.write(full_content)
    
    print(f"Created {len(phase5_tasks)} Phase 5 README files")
    print("\nAll README files created successfully!")


if __name__ == "__main__":
    main()
