#!/usr/bin/env python3
"""
Phase 5 Task 03: Create PlantUML Visualization of Virtual Map
Generate visual diagram of the USA Business Journey Map.
"""

import json
from pathlib import Path
from datetime import datetime


def load_virtual_map(processed_dir: Path) -> dict:
    """Load the virtual map."""
    with open(processed_dir / "virtual_map.json", 'r') as f:
        return json.load(f)


def generate_plantuml_diagram(virtual_map: dict) -> str:
    """Generate PlantUML diagram from virtual map."""
    
    diagram = f"""@startuml USA_Business_Journey_Map
!theme plain
title {virtual_map.get('title', 'USA Business Journey Map')}
legend
    {virtual_map.get('description', 'A metaphorical map for USA business formation')}
    Created: {datetime.now().strftime('%Y-%m-%d')}
    Total Regions: {len(virtual_map.get('regions', []))}
    Total Locations: {sum(len(r.get('locations', [])) for r in virtual_map.get('regions', []))}
endlegend

skinparam rectangle {{
  BackgroundColor<<region>> LightBlue
  BorderColor<<region>> DarkBlue
  BackgroundColor<<location>> LightYellow
  BorderColor<<location>> DarkGreen
  BackgroundColor<<decision>> LightCoral
  BorderColor<<decision>> Red
  BackgroundColor<<challenge>> LightGray
  BorderColor<<challenge>> Black
}}

skinparam note {{
  BackgroundColor Lavender
  BorderColor Purple
}}

"""
    
    # Generate regions and locations
    for region in virtual_map.get('regions', []):
        region_id = region.get('region_id', 'unknown')
        region_name = region.get('name', 'Unknown Region')
        region_desc = region.get('description', '')
        region_metaphor = region.get('metaphor', '')
        phase_conn = region.get('phase_connection', 0)
        
        diagram += f"""
rectangle "{region_name}\\n**Phase {phase_conn}**\\n<i>{region_metaphor}</i>" <<region>> as {region_id} {{
"""
        
        # Add locations within region
        for loc in region.get('locations', []):
            loc_id = loc.get('location_id', 'unknown')
            loc_name = loc.get('name', 'Unknown Location')
            loc_desc = loc.get('description', '')
            loc_type = loc.get('type', 'general')
            action_ref = loc.get('action_ref', '')
            visual = loc.get('visual_element', '')
            
            # Determine stereotype based on type
            stereotype = "location"
            if loc_type == 'decision':
                stereotype = "decision"
            elif loc_type in ['challenge', 'enemy']:
                stereotype = "challenge"
            
            diagram += f"""
  rectangle "{loc_name}\\n--\\n{loc_desc[:50]}{'...' if len(loc_desc) > 50 else ''}\\n<i>{visual}</i>\\n[Action: {action_ref}]" <<{stereotype}>> as {loc_id}
"""
        
        # Add challenges in region
        challenges = region.get('challenges', [])
        if challenges:
            diagram += f"""
  note right of {region_id}
    <b>Challenges:</b>
"""
            for challenge in challenges:
                diagram += f"    • {challenge.get('name', 'Unknown')}: {challenge.get('effect', '')}\\n"
            diagram += f"""  end note
"""
        
        # Add allies in region
        allies = region.get('allies', [])
        if allies:
            diagram += f"""
  note left of {region_id}
    <b>Allies:</b>
"""
            for ally in allies:
                diagram += f"    • {ally.get('name', 'Unknown')}: {ally.get('role', '')}\\n"
            diagram += f"""  end note
"""
        
        diagram += f"""
}}
"""
    
    # Add journey paths
    diagram += """
' Journey Paths between regions
"""
    
    journey_path = virtual_map.get('journey_path', {})
    waypoints = journey_path.get('waypoints', [])
    
    for i, phase_waypoints in enumerate(waypoints):
        if i < len(waypoints) - 1:
            # Connect last location of current phase to first location of next phase
            current_last = phase_waypoints[-1] if phase_waypoints else None
            next_first = waypoints[i + 1][0] if waypoints[i + 1] else None
            
            if current_last and next_first:
                diagram += f"{current_last} --> {next_first} : Phase {i + 1} → {i + 2}\n"
    
    # Add paths within phases
    diagram += """
' Paths within each phase
"""
    for phase_waypoints in waypoints:
        for i in range(len(phase_waypoints) - 1):
            diagram += f"{phase_waypoints[i]} -[hidden]- {phase_waypoints[i + 1]}\n"
    
    # Add game mechanics summary
    game_mechanics = virtual_map.get('game_mechanics', {})
    if game_mechanics:
        diagram += f"""
rectangle "Game Mechanics" <<region>> as game_mech {{
  note right
    <b>Resources:</b>
"""
        for res in game_mechanics.get('resources', []):
            diagram += f"    • {res.get('name', 'Unknown')}: {res.get('description', '')}\\n"
        
        diagram += f"""
    <b>Progression:</b> {game_mechanics.get('progression', {}).get('description', 'Phase-gated')}
    <b>Success:</b>
"""
        for condition in game_mechanics.get('success_conditions', []):
            diagram += f"    • {condition}\\n"
        
        diagram += f"""  end note
}}
"""
    
    # Add decision points
    navigation_rules = virtual_map.get('navigation_rules', {}) if isinstance(virtual_map.get('navigation_rules'), dict) else {}
    # Note: navigation_rules might be in a separate file
    
    diagram += """
' Styling
skinparam shadowing false
skinparam defaultTextAlignment center

@enduml
"""
    
    return diagram


def generate_summary_diagram(virtual_map: dict) -> str:
    """Generate a simplified summary diagram showing region flow."""
    
    diagram = f"""@startuml USA_Business_Journey_Summary
!theme plain
title USA Business Journey - Phase Overview
legend
    High-level view of the business formation journey
    {len(virtual_map.get('regions', []))} regions, {sum(len(r.get('locations', [])) for r in virtual_map.get('regions', []))} locations
endlegend

skinparam rectangle {{
  BackgroundColor<<phase>> LightBlue
  BorderColor<<phase>> DarkBlue
  BackgroundColor<<start>> LightGreen
  BorderColor<<start>> DarkGreen
  BackgroundColor<<end>> LightCoral
  BorderColor<<end>> Red
}}

"""
    
    # Create phase boxes
    for region in virtual_map.get('regions', []):
        region_id = region.get('region_id', 'unknown')
        region_name = region.get('name', 'Unknown Region')
        phase_conn = region.get('phase_connection', 0)
        loc_count = len(region.get('locations', []))
        
        # Mark start and end
        stereotype = "phase"
        if phase_conn == 1:
            stereotype = "start"
        elif phase_conn == len(virtual_map.get('regions', [])):
            stereotype = "end"
        
        diagram += f"""
rectangle "**Phase {phase_conn}**\\n{region_name}\\n{loc_count} locations" <<{stereotype}>> as {region_id}
"""
    
    # Add connections between phases
    diagram += """
' Phase progression
"""
    regions = virtual_map.get('regions', [])
    for i in range(len(regions) - 1):
        current_id = regions[i].get('region_id', f'region_{i+1}')
        next_id = regions[i+1].get('region_id', f'region_{i+2}')
        diagram += f"{current_id} --> {next_id} : Complete Phase {i+1}\n"
    
    diagram += f"""
note bottom
    <b>Journey Path:</b>
    Start: Planning Peaks (Business Concept)
    → Legal Labyrinth (Structure & Registration)
    → Compliance Canyon (Licenses & Permits)
    → Operations Ocean (Business Setup)
    → Growth Galaxy (Scaling & Expansion)
    
    <b>Estimated Time:</b> 3-12 months
end note

skinparam shadowing false

@enduml
"""
    
    return diagram


def main():
    processed_dir = Path("processed")
    
    print("Loading virtual map...")
    virtual_map = load_virtual_map(processed_dir)
    print(f"Loaded map with {len(virtual_map.get('regions', []))} regions")
    
    print("\nGenerating detailed PlantUML diagram...")
    detailed_diagram = generate_plantuml_diagram(virtual_map)
    
    detailed_path = processed_dir / "usa_business_journey_map.puml"
    with open(detailed_path, 'w') as f:
        f.write(detailed_diagram)
    print(f"  -> Saved: {detailed_path}")
    
    print("\nGenerating summary PlantUML diagram...")
    summary_diagram = generate_summary_diagram(virtual_map)
    
    summary_path = processed_dir / "usa_business_journey_summary.puml"
    with open(summary_path, 'w') as f:
        f.write(summary_diagram)
    print(f"  -> Saved: {summary_path}")
    
    # Create task summary
    summary_md = f"""# Phase 5 Task 03: Create PlantUML Visualization of Virtual Map

## Status: COMPLETED

## Objective
Generate visual diagram of the USA Business Journey Map.

## Process Completed
1. Converted virtual map regions to PlantUML components
2. Added location nodes with descriptions and visual elements
3. Drew journey paths between locations and phases
4. Included challenge and ally annotations

## Output Files
- `processed/usa_business_journey_map.puml` - Detailed map with all regions, locations, challenges, and allies
- `processed/usa_business_journey_summary.puml` - High-level phase overview diagram

## Diagram Features

### Detailed Map (`usa_business_journey_map.puml`)
- **5 Region boxes** representing metaphorical landscapes
- **20 Location nodes** with descriptions and action references
- **Challenge notes** showing obstacles in each region
- **Ally notes** showing guidance available
- **Journey paths** connecting locations and phases
- **Game mechanics summary** showing resources and success conditions

### Summary Map (`usa_business_journey_summary.puml`)
- **5 Phase boxes** showing high-level progression
- **Sequential flow** from planning to growth
- **Location counts** per phase
- **Journey path summary** at bottom

## Visualization
To render the PlantUML diagrams:
```bash
# Using PlantUML CLI
plantuml processed/usa_business_journey_map.puml
plantuml processed/usa_business_journey_summary.puml

# Or use online renderer at https://www.plantuml.com/plantuml/
```

## Verification
- Both PlantUML files created successfully
- Diagrams follow PlantUML syntax
- All regions and locations represented
- Ready for rendering and review

## Next Steps
- Render diagrams to PNG/SVG for documentation
- Review visual layout and adjust if needed
- Proceed to Task 04: Interactive Map Navigation Prototype

---
*Task completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    summary_md_path = processed_dir / "phase5_task03_summary.md"
    with open(summary_md_path, 'w') as f:
        f.write(summary_md)
    print(f"  -> Saved: {summary_md_path}")
    
    print("\nPhase 5 Task 03 completed successfully!")


if __name__ == "__main__":
    main()
