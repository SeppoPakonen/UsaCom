#!/usr/bin/env python3
"""Generate Phase 5 task README files for tasks 02-10."""

from pathlib import Path
from datetime import datetime

TASKS_DIR = Path("plan/testing/phase5")

# Task definitions based on Phase 5 scope
tasks = {
    "task02": {
        "title": "Validate Action Planner Against Source Data",
        "objective": "Cross-reference action planner with original book content to ensure completeness",
        "input": ["processed/action_planner.json", "processed/*.json"],
        "output": "validation_report.md",
        "process": [
            "Compare action planner phases against source document keywords",
            "Verify all major business formation steps are covered",
            "Check for missing regulatory requirements",
            "Validate time estimates against source material"
        ]
    },
    "task03": {
        "title": "Create PlantUML Visualization of Virtual Map",
        "objective": "Generate visual diagram of the USA Business Journey Map",
        "input": ["processed/virtual_map.json"],
        "output": "usa_business_journey_map.puml",
        "process": [
            "Convert virtual map regions to PlantUML components",
            "Add location nodes with coordinates",
            "Draw journey paths between locations",
            "Include challenge and ally annotations"
        ]
    },
    "task04": {
        "title": "Develop Interactive Map Navigation Prototype",
        "objective": "Create basic interactive navigation for the virtual map",
        "input": ["processed/virtual_map.json", "processed/navigation_rules.json"],
        "output": "map_navigation_prototype.html",
        "process": [
            "Build HTML/CSS interface for map display",
            "Implement region switching logic",
            "Add location click handlers",
            "Display action details on selection"
        ]
    },
    "task05": {
        "title": "Define Simulation Game Mechanics",
        "objective": "Specify detailed game mechanics for Phase 6 simulation",
        "input": ["processed/action_planner.json", "processed/virtual_map.json"],
        "output": "game_mechanics_spec.md",
        "process": [
            "Define resource management system",
            "Specify scoring and progression mechanics",
            "Create challenge difficulty scaling",
            "Design reward and achievement system"
        ]
    },
    "task06": {
        "title": "Create USA Business Regulation Database",
        "objective": "Extract and structure regulatory requirements from processed data",
        "input": ["processed/*_parsed.json"],
        "output": "regulation_database.json",
        "process": [
            "Extract all compliance-related constraints",
            "Categorize by jurisdiction (federal, state, local)",
            "Add filing frequencies and deadlines",
            "Link to action planner phases"
        ]
    },
    "task07": {
        "title": "Design Decision Tree for Business Structure Selection",
        "objective": "Create interactive decision tree for choosing business entity type",
        "input": ["processed/action_planner.json", "processed/virtual_map.json"],
        "output": "entity_decision_tree.json",
        "process": [
            "Map entity selection criteria from source data",
            "Create branching logic for different scenarios",
            "Add tax implication comparisons",
            "Include liability and management considerations"
        ]
    },
    "task08": {
        "title": "Generate Sample Business Scenarios",
        "objective": "Create realistic business scenarios for testing the simulation",
        "input": ["processed/action_planner.json", "processed/virtual_map.json"],
        "output": "sample_scenarios.json",
        "process": [
            "Define diverse business types (tech, retail, service)",
            "Create scenario parameters (funding, team, market)",
            "Map scenarios to journey paths",
            "Add success metrics for each scenario"
        ]
    },
    "task09": {
        "title": "Create Assessment and Feedback System",
        "objective": "Design system for evaluating player progress and providing feedback",
        "input": ["processed/action_planner.json", "processed/navigation_rules.json"],
        "output": "assessment_system.md",
        "process": [
            "Define progress tracking metrics",
            "Create feedback message templates",
            "Design milestone celebrations",
            "Implement corrective guidance system"
        ]
    },
    "task10": {
        "title": "Prepare Phase 6 Handoff Documentation",
        "objective": "Compile all Phase 5 artifacts for simulation game development",
        "input": ["processed/*.json", "processed/*.md", "processed/*.puml"],
        "output": "phase6_handoff_package.md",
        "process": [
            "Catalog all generated artifacts",
            "Create integration guidelines",
            "Document data structures and APIs",
            "Provide implementation recommendations"
        ]
    }
}

for task_num, task_data in tasks.items():
    task_dir = TASKS_DIR / task_num
    task_dir.mkdir(parents=True, exist_ok=True)
    
    readme_content = f"""# Phase 5 {task_num.replace('task', ' Task ').replace('0', '')}: {task_data['title']}

## Status: PENDING

## Objective
{task_data['objective']}

## Input
"""
    for inp in task_data['input']:
        readme_content += f"- {inp}\n"
    
    readme_content += """
## Process
"""
    for i, step in enumerate(task_data['process'], 1):
        readme_content += f"{i}. {step}\n"
    
    readme_content += f"""
## Output
- {task_data['output']}

## Verification
- Output file created and validated
- Meets Phase 5 requirements
- Ready for next task or Phase 6 integration
"""
    
    readme_path = task_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Created {task_num}/README.md")

print(f"\nCreated {len(tasks)} task README files in Phase 5.")
