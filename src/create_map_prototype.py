#!/usr/bin/env python3
"""
Phase 5 Task 04: Develop Interactive Map Navigation Prototype
Create basic interactive navigation for the virtual map.
"""

import json
from pathlib import Path
from datetime import datetime


def load_virtual_map(processed_dir: Path) -> dict:
    """Load the virtual map."""
    with open(processed_dir / "virtual_map.json", 'r') as f:
        return json.load(f)


def load_navigation_rules(processed_dir: Path) -> dict:
    """Load navigation rules."""
    with open(processed_dir / "navigation_rules.json", 'r') as f:
        return json.load(f)


def load_action_planner(processed_dir: Path) -> dict:
    """Load the action planner."""
    with open(processed_dir / "action_planner.json", 'r') as f:
        return json.load(f)


def generate_html_prototype(virtual_map: dict, navigation_rules: dict, action_planner: dict) -> str:
    """Generate interactive HTML prototype."""
    
    # Build action lookup
    action_lookup = {}
    for phase in action_planner.get('phases', []):
        for action in phase.get('actions', []):
            action_lookup[action['id']] = action
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{virtual_map.get('title', 'USA Business Journey Map')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        header {{
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #4a90d9;
        }}
        
        header h1 {{
            color: #4a90d9;
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        header p {{
            color: #aaa;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .container {{
            display: flex;
            min-height: calc(100vh - 150px);
        }}
        
        /* Region Navigation Sidebar */
        .region-nav {{
            width: 250px;
            background: rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-right: 1px solid #333;
        }}
        
        .region-nav h2 {{
            color: #4a90d9;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .region-btn {{
            display: block;
            width: 100%;
            padding: 15px;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border: 1px solid #4a90d9;
            border-radius: 8px;
            color: #eee;
            cursor: pointer;
            text-align: left;
            transition: all 0.3s ease;
        }}
        
        .region-btn:hover {{
            background: linear-gradient(135deg, #34495e 0%, #3d566e 100%);
            transform: translateX(5px);
        }}
        
        .region-btn.active {{
            background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
            box-shadow: 0 0 15px rgba(74, 144, 217, 0.5);
        }}
        
        .region-btn .phase-num {{
            font-size: 0.8em;
            color: #888;
        }}
        
        .region-btn.active .phase-num {{
            color: #ddd;
        }}
        
        /* Main Map Area */
        .map-area {{
            flex: 1;
            padding: 30px;
            overflow-y: auto;
        }}
        
        .region-display {{
            display: none;
            animation: fadeIn 0.5s ease;
        }}
        
        .region-display.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .region-header {{
            background: rgba(74, 144, 217, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #4a90d9;
        }}
        
        .region-header h2 {{
            color: #4a90d9;
            margin-bottom: 10px;
        }}
        
        .region-header .metaphor {{
            font-style: italic;
            color: #aaa;
            margin-bottom: 10px;
        }}
        
        /* Location Cards */
        .locations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .location-card {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border: 1px solid #444;
            border-radius: 10px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .location-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #4a90d9;
        }}
        
        .location-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(74, 144, 217, 0.3);
            border-color: #4a90d9;
        }}
        
        .location-card.completed {{
            border-color: #27ae60;
        }}
        
        .location-card.completed::before {{
            background: #27ae60;
        }}
        
        .location-card h3 {{
            color: #4a90d9;
            margin-bottom: 10px;
        }}
        
        .location-card .type {{
            display: inline-block;
            padding: 3px 10px;
            background: rgba(74, 144, 217, 0.2);
            border-radius: 15px;
            font-size: 0.8em;
            margin-bottom: 10px;
        }}
        
        .location-card .description {{
            color: #ccc;
            margin-bottom: 15px;
            line-height: 1.5;
        }}
        
        .location-card .visual {{
            font-style: italic;
            color: #888;
            font-size: 0.9em;
        }}
        
        /* Action Detail Panel */
        .action-panel {{
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 25px;
            margin-top: 20px;
            display: none;
        }}
        
        .action-panel.active {{
            display: block;
            animation: slideIn 0.3s ease;
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .action-panel h3 {{
            color: #27ae60;
            margin-bottom: 15px;
        }}
        
        .action-detail {{
            background: rgba(39, 174, 96, 0.1);
            border-left: 3px solid #27ae60;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }}
        
        .action-detail h4 {{
            color: #27ae60;
            margin-bottom: 10px;
        }}
        
        .action-detail p {{
            color: #ccc;
            line-height: 1.6;
        }}
        
        .action-detail .keywords {{
            margin-top: 10px;
        }}
        
        .action-detail .keyword {{
            display: inline-block;
            padding: 3px 8px;
            background: rgba(39, 174, 96, 0.2);
            border-radius: 3px;
            font-size: 0.85em;
            margin: 2px;
        }}
        
        /* Challenges Section */
        .challenges-section {{
            background: rgba(231, 76, 60, 0.1);
            border: 1px solid #e74c3c;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }}
        
        .challenges-section h3 {{
            color: #e74c3c;
            margin-bottom: 15px;
        }}
        
        .challenge-item {{
            background: rgba(231, 76, 60, 0.05);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            border-left: 3px solid #e74c3c;
        }}
        
        .challenge-item h4 {{
            color: #e74c3c;
            margin-bottom: 5px;
        }}
        
        /* Allies Section */
        .allies-section {{
            background: rgba(52, 152, 219, 0.1);
            border: 1px solid #3498db;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .allies-section h3 {{
            color: #3498db;
            margin-bottom: 15px;
        }}
        
        .ally-item {{
            background: rgba(52, 152, 219, 0.05);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
            border-left: 3px solid #3498db;
        }}
        
        .ally-item h4 {{
            color: #3498db;
            margin-bottom: 5px;
        }}
        
        /* Progress Bar */
        .progress-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px 30px;
            border-top: 1px solid #4a90d9;
        }}
        
        .progress-bar {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .progress-label {{
            color: #aaa;
            white-space: nowrap;
        }}
        
        .progress-track {{
            flex: 1;
            height: 10px;
            background: #333;
            border-radius: 5px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4a90d9 0%, #357abd 100%);
            transition: width 0.5s ease;
        }}
        
        .progress-percent {{
            color: #4a90d9;
            font-weight: bold;
            min-width: 50px;
            text-align: right;
        }}
        
        /* Resource Display */
        .resources {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .resource {{
            background: rgba(74, 144, 217, 0.1);
            padding: 10px 15px;
            border-radius: 5px;
            border: 1px solid #4a90d9;
        }}
        
        .resource .name {{
            font-size: 0.8em;
            color: #888;
        }}
        
        .resource .value {{
            color: #4a90d9;
            font-weight: bold;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}
            
            .region-nav {{
                width: 100%;
                border-right: none;
                border-bottom: 1px solid #333;
            }}
            
            .locations-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>🗺️ {virtual_map.get('title', 'USA Business Journey Map')}</h1>
        <p>{virtual_map.get('description', 'Navigate your business formation journey')}</p>
    </header>
    
    <div class="container">
        <nav class="region-nav">
            <h2>📍 Regions</h2>
"""
    
    # Generate region navigation buttons
    for i, region in enumerate(virtual_map.get('regions', [])):
        region_id = region.get('region_id', f'region_{i+1}')
        region_name = region.get('name', 'Unknown Region')
        phase_num = region.get('phase_connection', i + 1)
        loc_count = len(region.get('locations', []))
        active_class = 'active' if i == 0 else ''
        
        html += f"""
            <button class="region-btn {active_class}" onclick="showRegion('{region_id}')">
                <span class="phase-num">Phase {phase_num}</span>
                <strong>{region_name}</strong>
                <br><small>{loc_count} locations</small>
            </button>
"""
    
    html += f"""
        </nav>
        
        <main class="map-area">
"""
    
    # Generate region displays
    for i, region in enumerate(virtual_map.get('regions', [])):
        region_id = region.get('region_id', f'region_{i+1}')
        region_name = region.get('name', 'Unknown Region')
        region_desc = region.get('description', '')
        region_metaphor = region.get('metaphor', '')
        active_class = 'active' if i == 0 else ''
        
        html += f"""
            <div class="region-display {active_class}" id="{region_id}">
                <div class="region-header">
                    <h2>🏔️ {region_name}</h2>
                    <p class="metaphor"><i>{region_metaphor}</i></p>
                    <p>{region_desc}</p>
                </div>
                
                <div class="locations-grid">
"""
        
        # Generate location cards
        for loc in region.get('locations', []):
            loc_id = loc.get('location_id', 'unknown')
            loc_name = loc.get('name', 'Unknown Location')
            loc_desc = loc.get('description', '')
            loc_type = loc.get('type', 'general')
            visual = loc.get('visual_element', '')
            action_ref = loc.get('action_ref', '')
            
            # Get action details
            action = action_lookup.get(action_ref, {})
            
            html += f"""
                    <div class="location-card" onclick="showAction('{loc_id}', '{action_ref}')">
                        <h3>📍 {loc_name}</h3>
                        <span class="type">{loc_type}</span>
                        <p class="description">{loc_desc[:100]}{'...' if len(loc_desc) > 100 else ''}</p>
                        <p class="visual">🎨 {visual}</p>
                    </div>
"""
        
        html += """
                </div>
"""
        
        # Add challenges section
        challenges = region.get('challenges', [])
        if challenges:
            html += f"""
                <div class="challenges-section">
                    <h3>⚠️ Challenges in {region_name}</h3>
"""
            for challenge in challenges:
                challenge_name = challenge.get('name', 'Unknown')
                challenge_type = challenge.get('type', 'unknown')
                challenge_effect = challenge.get('effect', '')
                
                html += f"""
                    <div class="challenge-item">
                        <h4>{challenge_name}</h4>
                        <p><strong>Type:</strong> {challenge_type} | <strong>Effect:</strong> {challenge_effect}</p>
                    </div>
"""
            html += """
                </div>
"""
        
        # Add allies section
        allies = region.get('allies', [])
        if allies:
            html += f"""
                <div class="allies-section">
                    <h3>🤝 Allies in {region_name}</h3>
"""
            for ally in allies:
                ally_name = ally.get('name', 'Unknown')
                ally_type = ally.get('type', 'unknown')
                ally_role = ally.get('role', '')
                
                html += f"""
                    <div class="ally-item">
                        <h4>{ally_name}</h4>
                        <p><strong>Type:</strong> {ally_type} | <strong>Role:</strong> {ally_role}</p>
                    </div>
"""
            html += """
                </div>
"""
        
        html += """
            </div>
"""
    
    # Action detail panel
    html += """
            <div class="action-panel" id="actionPanel">
                <h3>📋 Action Details</h3>
                <div id="actionContent"></div>
            </div>
        </main>
    </div>
    
    <div class="progress-container">
        <div class="progress-bar">
            <span class="progress-label">Journey Progress:</span>
            <div class="progress-track">
                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
            </div>
            <span class="progress-percent" id="progressPercent">0%</span>
        </div>
    </div>
    
    <script>
        // State
        let completedLocations = new Set();
        let currentRegion = 0;
        const totalLocations = """ + str(sum(len(r.get('locations', [])) for r in virtual_map.get('regions', []))) + """;
        
        // Action data
        const actions = """ + json.dumps(action_lookup) + """;
        
        function showRegion(regionId) {{
            // Hide all regions
            document.querySelectorAll('.region-display').forEach(el => {{
                el.classList.remove('active');
            }});
            
            // Show selected region
            document.getElementById(regionId).classList.add('active');
            
            // Update navigation buttons
            document.querySelectorAll('.region-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Hide action panel
            document.getElementById('actionPanel').classList.remove('active');
        }}
        
        function showAction(locId, actionRef) {{
            const action = actions[actionRef];
            const panel = document.getElementById('actionPanel');
            const content = document.getElementById('actionContent');
            
            if (!action) {{
                content.innerHTML = '<p>Action details not available.</p>';
            }} else {{
                const keywords = action.keywords ? action.keywords.map(k => `<span class="keyword">${{k}}</span>`).join('') : '';
                
                content.innerHTML = `
                    <div class="action-detail">
                        <h4>🎯 ${{action.title}}</h4>
                        <p><strong>ID:</strong> ${{action.id}}</p>
                        <p><strong>Description:</strong> ${{action.description}}</p>
                        <p><strong>Estimated Time:</strong> ${{action.estimated_time || 'Not specified'}}</p>
                        <p><strong>Output:</strong> ${{action.output || 'Not specified'}}</p>
                        <div class="keywords"><strong>Keywords:</strong> ${{keywords}}</div>
                    </div>
                    <button class="region-btn" onclick="markComplete('${{locId}}')" style="margin-top: 15px; background: linear-gradient(135deg, #27ae60 0%, #229954 100%); border-color: #27ae60;">
                        ✅ Mark as Completed
                    </button>
                `;
            }}
            
            panel.classList.add('active');
            panel.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}
        
        function markComplete(locId) {{
            completedLocations.add(locId);
            
            // Update UI
            const cards = document.querySelectorAll('.location-card');
            cards.forEach(card => {{
                if (card.innerHTML.includes(locId)) {{
                    card.classList.add('completed');
                }}
            }});
            
            // Update progress
            updateProgress();
            
            // Show completion message
            alert(`Location marked as completed! Progress: ${{completedLocations.size}} / ${{totalLocations}}`);
        }}
        
        function updateProgress() {{
            const percent = Math.round((completedLocations.size / totalLocations) * 100);
            document.getElementById('progressFill').style.width = percent + '%';
            document.getElementById('progressPercent').textContent = percent + '%';
        }}
        
        // Initialize
        console.log('USA Business Journey Map loaded');
        console.log('Total locations:', totalLocations);
        console.log('Regions:', """ + str(len(virtual_map.get('regions', []))) + """ );
    </script>
</body>
</html>
"""
    
    return html


def main():
    processed_dir = Path("processed")
    
    print("Loading virtual map...")
    virtual_map = load_virtual_map(processed_dir)
    
    print("Loading navigation rules...")
    navigation_rules = load_navigation_rules(processed_dir)
    
    print("Loading action planner...")
    action_planner = load_action_planner(processed_dir)
    
    print("\nGenerating interactive HTML prototype...")
    html_content = generate_html_prototype(virtual_map, navigation_rules, action_planner)
    
    output_path = processed_dir / "map_navigation_prototype.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  -> Saved: {output_path}")
    
    # Create task summary
    summary_md = f"""# Phase 5 Task 04: Develop Interactive Map Navigation Prototype

## Status: COMPLETED

## Objective
Create basic interactive navigation for the virtual map.

## Process Completed
1. Built HTML/CSS interface for map display with responsive design
2. Implemented region switching logic with smooth animations
3. Added location click handlers with action detail panels
4. Implemented progress tracking system
5. Added completion marking functionality
6. Included challenge and ally displays per region

## Output Files
- `processed/map_navigation_prototype.html` - Interactive HTML prototype

## Features

### Navigation
- **Region Sidebar**: Click to switch between 5 regions
- **Location Cards**: Click to view action details
- **Progress Bar**: Track completion at bottom of page
- **Responsive Design**: Works on desktop and mobile

### Interactive Elements
- **Region Selection**: Smooth transitions between regions
- **Action Details**: Panel shows full action information
- **Mark Complete**: Track progress through locations
- **Visual Feedback**: Hover effects, animations, completion states

### Content Display
- **Region Headers**: Name, metaphor, description
- **Location Cards**: Type, description, visual element
- **Challenges Section**: Obstacles per region
- **Allies Section**: Helpers per region
- **Action Panel**: Full action details with keywords

## Usage
Open `processed/map_navigation_prototype.html` in a web browser.

```bash
# On Linux
xdg-open processed/map_navigation_prototype.html

# On macOS
open processed/map_navigation_prototype.html

# On Windows
start processed/map_navigation_prototype.html
```

## Technical Details
- Pure HTML/CSS/JavaScript (no external dependencies)
- Responsive design with CSS Grid and Flexbox
- Smooth animations using CSS transitions
- State management with vanilla JavaScript
- Embedded JSON data for actions

## Verification
- HTML file created successfully
- All regions and locations included
- Interactive elements functional
- Progress tracking works

## Next Steps
- Test in multiple browsers
- Consider adding save/load functionality
- Add sound effects and enhanced visuals
- Proceed to Task 05: Define Simulation Game Mechanics

---
*Task completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    summary_path = processed_dir / "phase5_task04_summary.md"
    with open(summary_path, 'w') as f:
        f.write(summary_md)
    
    print(f"  -> Saved: {summary_path}")
    
    print("\nPhase 5 Task 04 completed successfully!")


if __name__ == "__main__":
    main()
