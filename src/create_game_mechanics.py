#!/usr/bin/env python3
"""
Phase 5 Task 05: Define Simulation Game Mechanics
Specify detailed game mechanics for Phase 6 simulation.
"""

import json
from pathlib import Path
from datetime import datetime


def load_action_planner(processed_dir: Path) -> dict:
    """Load the action planner."""
    with open(processed_dir / "action_planner.json", 'r') as f:
        return json.load(f)


def load_virtual_map(processed_dir: Path) -> dict:
    """Load the virtual map."""
    with open(processed_dir / "virtual_map.json", 'r') as f:
        return json.load(f)


def create_game_mechanics_spec(action_planner: dict, virtual_map: dict) -> dict:
    """Create comprehensive game mechanics specification."""
    
    spec = {
        "title": "USA Business Journey - Simulation Game Mechanics",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "Detailed game mechanics for the USA business formation simulation game",
        
        "1_core_game_loop": {
            "description": "The fundamental cycle of gameplay",
            "phases": [
                {
                    "phase": "Select Action",
                    "description": "Player chooses an action from available options in current region"
                },
                {
                    "phase": "Check Requirements",
                    "description": "Verify player has required resources and prerequisites"
                },
                {
                    "phase": "Execute Action",
                    "description": "Player completes the action, spending resources and time"
                },
                {
                    "phase": "Resolve Outcomes",
                    "description": "Apply effects, gain rewards, trigger events"
                },
                {
                    "phase": "Update State",
                    "description": "Update progress, resources, and unlock new actions"
                }
            ]
        },
        
        "2_resource_system": {
            "description": "Resources that players manage throughout the game",
            "resources": [
                {
                    "name": "Capital",
                    "symbol": "💰",
                    "description": "Financial resources for business formation",
                    "starting_amount": {"min": 5000, "max": 50000, "default": 15000},
                    "max_capacity": 1000000,
                    "acquisition_methods": [
                        "Personal savings (starting amount)",
                        "Business loan (unlocks in Phase 2)",
                        "Investor funding (unlocks in Phase 4)",
                        "Revenue generation (unlocks in Phase 5)",
                        "Grants and incentives (random events)"
                    ],
                    "spending_categories": [
                        "Filing fees ($50-500 per action)",
                        "Legal services ($500-5000)",
                        "Insurance premiums ($100-1000/month)",
                        "Equipment and supplies (variable)",
                        "Marketing and advertising (variable)"
                    ],
                    "depletion_penalty": "Game over if capital reaches $0 for 3 consecutive turns"
                },
                {
                    "name": "Time",
                    "symbol": "⏰",
                    "description": "Available time for completing actions",
                    "unit": "weeks",
                    "starting_amount": 52,
                    "max_capacity": 104,
                    "acquisition_methods": [
                        "Weekly time allocation (1 week per turn)",
                        "Hiring help (converts Capital to Time efficiency)",
                        "Automation tools (reduces action time requirements)"
                    ],
                    "spending_categories": [
                        "Action completion (varies by action)",
                        "Learning and research (optional)",
                        "Networking (optional)",
                        "Recovery from setbacks (penalty)"
                    ],
                    "depletion_penalty": "Opportunity cost - competitors gain advantage"
                },
                {
                    "name": "Knowledge",
                    "symbol": "📚",
                    "description": "Understanding of business formation requirements",
                    "starting_amount": 10,
                    "max_capacity": 100,
                    "acquisition_methods": [
                        "Research actions (+5-10 per action)",
                        "Consulting experts (+10-20, costs Capital)",
                        "Completing actions successfully (+2-5)",
                        "Learning from failures (+5-15)"
                    ],
                    "spending_categories": [
                        "Unlock advanced actions (requires Knowledge threshold)",
                        "Reduce action failure chance",
                        "Identify optimal paths"
                    ],
                    "depletion_penalty": "None - Knowledge only grows"
                },
                {
                    "name": "Network",
                    "symbol": "🤝",
                    "description": "Professional connections and relationships",
                    "starting_amount": 5,
                    "max_capacity": 100,
                    "acquisition_methods": [
                        "Networking events (+5-10)",
                        "Mentor relationships (+10-20)",
                        "Industry associations (+5-15)",
                        "Successful partnerships (+10-25)"
                    ],
                    "spending_categories": [
                        "Access to investors (requires Network threshold)",
                        "Finding co-founders or partners",
                        "Getting referrals and recommendations",
                        "Crisis support (reduces penalty severity)"
                    ],
                    "depletion_penalty": "Limited access to opportunities"
                },
                {
                    "name": "Reputation",
                    "symbol": "⭐",
                    "description": "Business credibility and trustworthiness",
                    "starting_amount": 0,
                    "max_capacity": 100,
                    "acquisition_methods": [
                        "Completing compliance actions (+5-10)",
                        "Successful business milestones (+10-20)",
                        "Positive customer interactions (+5-15)",
                        "Community involvement (+5-10)"
                    ],
                    "spending_categories": [
                        "Attract investors (requires Reputation threshold)",
                        "Secure partnerships",
                        "Premium pricing power",
                        "Crisis mitigation"
                    ],
                    "depletion_penalty": "Reduced opportunities, higher scrutiny"
                }
            ]
        },
        
        "3_progression_system": {
            "description": "How players advance through the game",
            "type": "phase_gated_with_requirements",
            "phases": [
                {
                    "phase": 1,
                    "name": "Planning Peaks",
                    "entry_requirements": {"capital": 5000, "knowledge": 0},
                    "completion_requirements": {
                        "actions_completed": ["action_1_1", "action_1_2", "action_1_3", "action_1_4", "action_1_5"],
                        "minimum_knowledge": 25
                    },
                    "unlocks": ["Phase 2: Legal Labyrinth", "Business loan option"]
                },
                {
                    "phase": 2,
                    "name": "Legal Labyrinth",
                    "entry_requirements": {"capital": 3000, "knowledge": 25},
                    "completion_requirements": {
                        "actions_completed": ["action_2_1", "action_2_2", "action_2_3", "action_2_4", "action_2_5"],
                        "business_structure_selected": True
                    },
                    "unlocks": ["Phase 3: Compliance Canyon", "Business bank account"]
                },
                {
                    "phase": 3,
                    "name": "Compliance Canyon",
                    "entry_requirements": {"capital": 2000, "knowledge": 40},
                    "completion_requirements": {
                        "actions_completed": ["action_3_1", "action_3_2", "action_3_3", "action_3_4"],
                        "compliance_score": 80
                    },
                    "unlocks": ["Phase 4: Operations Ocean", "Revenue generation"]
                },
                {
                    "phase": 4,
                    "name": "Operations Ocean",
                    "entry_requirements": {"capital": 5000, "reputation": 10},
                    "completion_requirements": {
                        "actions_completed": ["action_4_1", "action_4_2", "action_4_3", "action_4_4", "action_4_5"],
                        "operational_readiness": 100
                    },
                    "unlocks": ["Phase 5: Growth Galaxy", "Investor funding option"]
                },
                {
                    "phase": 5,
                    "name": "Growth Galaxy",
                    "entry_requirements": {"capital": 10000, "reputation": 25},
                    "completion_requirements": {
                        "actions_completed": ["action_5_1", "action_5_2", "action_5_3", "action_5_4", "action_5_5"],
                        "growth_metrics": {"revenue": 100000, "customers": 100}
                    },
                    "unlocks": ["Endgame: Sustainable Business", "Expansion options"]
                }
            ],
            "gating_rules": [
                "Cannot access Phase N+1 actions until Phase N is complete",
                "Failed requirements allow retry with penalty",
                "Optional actions can be skipped but may affect ending"
            ]
        },
        
        "4_challenge_system": {
            "description": "Obstacles and difficulties players must overcome",
            "challenge_types": [
                {
                    "type": "environmental",
                    "description": "Challenges from the business environment",
                    "examples": [
                        {
                            "name": "Fog of Uncertainty",
                            "effect": "Reduces visibility of optimal action paths",
                            "mitigation": "Research actions clear fog temporarily",
                            "severity": "low"
                        },
                        {
                            "name": "Regulation Rapids",
                            "effect": "Fast-changing rules require constant attention",
                            "mitigation": "Compliance system reduces impact",
                            "severity": "medium"
                        },
                        {
                            "name": "Cash Flow Currents",
                            "effect": "Strong currents affect business movement",
                            "mitigation": "Maintain 3-month operating reserve",
                            "severity": "high"
                        }
                    ]
                },
                {
                    "type": "enemy",
                    "description": "Active threats that attack the player",
                    "examples": [
                        {
                            "name": "Deadline Dragons",
                            "effect": "Attack if filing deadlines are missed",
                            "damage": "Capital -500, Reputation -10 per missed deadline",
                            "mitigation": "Calendar reminders, automated filing",
                            "severity": "high"
                        },
                        {
                            "name": "Liability Leviathan",
                            "effect": "Emerges without proper insurance",
                            "damage": "Capital -5000 to -50000 (based on incident)",
                            "mitigation": "Appropriate insurance coverage",
                            "severity": "critical"
                        },
                        {
                            "name": "Competition Comets",
                            "effect": "Rival businesses crossing your path",
                            "damage": "Market share -5% to -20%",
                            "mitigation": "Differentiation, speed to market",
                            "severity": "medium"
                        }
                    ]
                },
                {
                    "type": "resource",
                    "description": "Challenges requiring resource expenditure",
                    "examples": [
                        {
                            "name": "Fee Toll Bridges",
                            "effect": "Require payment to cross",
                            "cost": "Capital -50 to -500 per action",
                            "mitigation": "Budget planning, fee waivers for qualifying businesses",
                            "severity": "low"
                        },
                        {
                            "name": "Paperwork Golems",
                            "effect": "Slow progress with documentation requirements",
                            "cost": "Time -1 to -4 weeks per action",
                            "mitigation": "Templates, professional services, automation",
                            "severity": "medium"
                        }
                    ]
                }
            ],
            "difficulty_scaling": {
                "easy": {"challenge_frequency": 0.1, "severity_modifier": 0.5},
                "normal": {"challenge_frequency": 0.25, "severity_modifier": 1.0},
                "hard": {"challenge_frequency": 0.4, "severity_modifier": 1.5},
                "expert": {"challenge_frequency": 0.6, "severity_modifier": 2.0}
            }
        },
        
        "5_reward_system": {
            "description": "Rewards and achievements for player accomplishments",
            "reward_types": [
                {
                    "type": "milestone",
                    "description": "Rewards for completing major milestones",
                    "examples": [
                        {
                            "milestone": "First Phase Complete",
                            "reward": {"capital": 1000, "knowledge": 10, "achievement": "Planner"}
                        },
                        {
                            "milestone": "Business Registered",
                            "reward": {"capital": 500, "reputation": 5, "achievement": "Founder"}
                        },
                        {
                            "milestone": "All Compliance Met",
                            "reward": {"knowledge": 20, "reputation": 15, "achievement": "Compliant"}
                        },
                        {
                            "milestone": "First Revenue",
                            "reward": {"capital": 5000, "reputation": 10, "achievement": "Earner"}
                        },
                        {
                            "milestone": "Game Complete",
                            "reward": {"achievement": "Entrepreneur", "ending_variant": "based_on_performance"}
                        }
                    ]
                },
                {
                    "type": "achievement",
                    "description": "Special accomplishments with badges",
                    "examples": [
                        {"name": "Bootstrapper", "condition": "Complete game without external funding"},
                        {"name": "Speed Runner", "condition": "Complete game in under 26 weeks"},
                        {"name": "Perfectionist", "condition": "Complete all actions with 100% compliance"},
                        {"name": "Networker", "condition": "Reach Network stat of 75+"},
                        {"name": "Knowledge Seeker", "condition": "Reach Knowledge stat of 75+"},
                        {"name": "Phoenix", "condition": "Recover from near-bankruptcy to success"}
                    ]
                },
                {
                    "type": "unlock",
                    "description": "New options and capabilities",
                    "examples": [
                        {"unlock": "Investor Meetings", "condition": "Reach Phase 4 with Reputation 30+"},
                        {"unlock": "Media Coverage", "condition": "Reach Reputation 50+"},
                        {"unlock": "Acquisition Offers", "condition": "Reach revenue milestone"},
                        {"unlock": "Franchise Option", "condition": "Complete game with high scores"}
                    ]
                }
            ]
        },
        
        "6_scoring_system": {
            "description": "How player performance is evaluated",
            "score_categories": [
                {
                    "category": "Financial Performance",
                    "weight": 0.30,
                    "metrics": [
                        {"metric": "Final Capital", "max_score": 100, "formula": "min(100, capital / 10000)"},
                        {"metric": "Revenue Generated", "max_score": 100, "formula": "min(100, revenue / 100000)"},
                        {"metric": "Capital Efficiency", "max_score": 100, "formula": "revenue / starting_capital"}
                    ]
                },
                {
                    "category": "Speed",
                    "weight": 0.20,
                    "metrics": [
                        {"metric": "Time to Complete", "max_score": 100, "formula": "max(0, 100 - weeks_taken)"},
                        {"metric": "Actions per Week", "max_score": 100, "formula": "actions_completed / weeks_taken * 10"}
                    ]
                },
                {
                    "category": "Compliance",
                    "weight": 0.25,
                    "metrics": [
                        {"metric": "Compliance Score", "max_score": 100, "formula": "compliance_percentage"},
                        {"metric": "Deadlines Met", "max_score": 100, "formula": "on_time_filings / total_filings * 100"}
                    ]
                },
                {
                    "category": "Growth",
                    "weight": 0.15,
                    "metrics": [
                        {"metric": "Network Size", "max_score": 100, "formula": "network_stat"},
                        {"metric": "Reputation", "max_score": 100, "formula": "reputation_stat"},
                        {"metric": "Knowledge", "max_score": 100, "formula": "knowledge_stat"}
                    ]
                },
                {
                    "category": "Achievements",
                    "weight": 0.10,
                    "metrics": [
                        {"metric": "Achievements Unlocked", "max_score": 100, "formula": "achievements / total_achievements * 100"}
                    ]
                }
            ],
            "grade_scale": {
                "S": {"min": 90, "title": "Visionary Entrepreneur"},
                "A": {"min": 80, "title": "Successful Founder"},
                "B": {"min": 70, "title": "Solid Business Owner"},
                "C": {"min": 60, "title": "Struggling Entrepreneur"},
                "D": {"min": 50, "title": "At-Risk Business"},
                "F": {"min": 0, "title": "Business Failure"}
            }
        },
        
        "7_decision_system": {
            "description": "Meaningful choices players must make",
            "key_decisions": [
                {
                    "decision_id": "business_structure",
                    "location": "loc_2_1",
                    "question": "What business structure will you choose?",
                    "options": [
                        {
                            "choice": "LLC",
                            "immediate_effects": {"capital": -200, "time": -2},
                            "long_term_effects": "Pass-through taxation, flexible management, moderate liability protection",
                            "best_for": "Small to medium businesses, real estate, consulting"
                        },
                        {
                            "choice": "C-Corporation",
                            "immediate_effects": {"capital": -500, "time": -4},
                            "long_term_effects": "Double taxation, investor-friendly, unlimited shareholders",
                            "best_for": "Startups seeking VC funding, companies planning IPO"
                        },
                        {
                            "choice": "S-Corporation",
                            "immediate_effects": {"capital": -400, "time": -4},
                            "long_term_effects": "Pass-through taxation, limited to 100 shareholders",
                            "best_for": "Profitable small businesses, family businesses"
                        },
                        {
                            "choice": "Sole Proprietorship",
                            "immediate_effects": {"capital": -50, "time": -1},
                            "long_term_effects": "Simple, personal liability, no separation",
                            "best_for": "Low-risk businesses, testing ideas, side hustles"
                        }
                    ]
                },
                {
                    "decision_id": "funding_strategy",
                    "location": "loc_1_4",
                    "question": "How will you fund your business?",
                    "options": [
                        {
                            "choice": "Bootstrapping",
                            "requirements": {"capital": 10000},
                            "effects": "Full ownership, slower growth, no debt",
                            "risk": "low"
                        },
                        {
                            "choice": "Bank Loan",
                            "requirements": {"credit_score": 680, "business_plan": True},
                            "effects": "Debt obligation, retain ownership, interest payments",
                            "risk": "medium"
                        },
                        {
                            "choice": "Angel Investor",
                            "requirements": {"pitch_deck": True, "network": 20},
                            "effects": "Equity dilution (10-25%), mentorship, faster growth",
                            "risk": "medium"
                        },
                        {
                            "choice": "Venture Capital",
                            "requirements": {"high_growth_potential": True, "traction": True},
                            "effects": "Significant equity dilution (20-50%), pressure for exit",
                            "risk": "high"
                        }
                    ]
                },
                {
                    "decision_id": "market_entry",
                    "location": "loc_5_1",
                    "question": "What is your market entry strategy?",
                    "options": [
                        {
                            "choice": "MVP Launch",
                            "effects": {"time": -4, "capital": -2000},
                            "outcome": "Fast feedback, iterate based on customer input",
                            "risk": "medium"
                        },
                        {
                            "choice": "Soft Launch",
                            "effects": {"time": -8, "capital": -5000},
                            "outcome": "Limited market testing, refine before full launch",
                            "risk": "low"
                        },
                        {
                            "choice": "Big Bang Launch",
                            "effects": {"time": -12, "capital": -20000},
                            "outcome": "Maximum impact, high risk if not ready",
                            "risk": "high"
                        }
                    ]
                }
            ]
        },
        
        "8_endgame_system": {
            "description": "How the game concludes",
            "ending_types": [
                {
                    "ending": "Sustainable Success",
                    "conditions": {
                        "all_phases_complete": True,
                        "capital": {"min": 50000},
                        "reputation": {"min": 50},
                        "compliance_score": {"min": 90}
                    },
                    "narrative": "Your business is thriving with strong fundamentals and growth trajectory."
                },
                {
                    "ending": "Acquisition Target",
                    "conditions": {
                        "all_phases_complete": True,
                        "revenue": {"min": 500000},
                        "reputation": {"min": 60}
                    },
                    "narrative": "Your successful business attracts acquisition offers from larger companies."
                },
                {
                    "ending": "Lifestyle Business",
                    "conditions": {
                        "phases_complete": {"min": 4},
                        "capital": {"min": 30000},
                        "work_life_balance": {"min": 70}
                    },
                    "narrative": "You've built a comfortable business that supports your desired lifestyle."
                },
                {
                    "ending": "Pivot Success",
                    "conditions": {
                        "phases_complete": {"min": 3},
                        "pivots": {"min": 1},
                        "final_revenue": {"min": 100000}
                    },
                    "narrative": "Your willingness to pivot led to unexpected success in a new direction."
                },
                {
                    "ending": "Gradual Decline",
                    "conditions": {
                        "capital": {"max": 5000},
                        "reputation": {"max": 20},
                        "turns_without_revenue": {"min": 10}
                    },
                    "narrative": "Despite your efforts, the business struggles to gain traction."
                },
                {
                    "ending": "Bankruptcy",
                    "conditions": {
                        "capital": {"max": 0},
                        "debt": {"min": 10000}
                    },
                    "narrative": "The business has failed due to insolvency. Time to learn and try again."
                }
            ],
            "new_game_plus": {
                "description": "Unlockable features for subsequent playthroughs",
                "unlocks": [
                    "Harder difficulty modes",
                    "Alternative starting scenarios",
                    "Industry-specific challenges",
                    "Historical business scenarios"
                ]
            }
        }
    }
    
    return spec


def generate_markdown_spec(spec: dict) -> str:
    """Generate human-readable markdown specification."""
    
    md = f"""# USA Business Journey - Simulation Game Mechanics Specification

## Overview
- **Title**: {spec['title']}
- **Version**: {spec['version']}
- **Created**: {spec['created']}
- **Description**: {spec['description']}

---

## 1. Core Game Loop

{spec['1_core_game_loop']['description']}

"""
    
    for i, phase in enumerate(spec['1_core_game_loop']['phases'], 1):
        md += f"**{i}. {phase['phase']}**: {phase['description']}\n\n"
    
    md += f"""---

## 2. Resource System

{spec['2_resource_system']['description']}

### Resources

"""
    
    for resource in spec['2_resource_system']['resources']:
        md += f"""### {resource['symbol']} {resource['name']}
- **Description**: {resource['description']}
- **Starting Amount**: {resource['starting_amount']}
- **Max Capacity**: {resource['max_capacity']}
- **Acquisition**: {', '.join(resource['acquisition_methods'][:3])}...
- **Spending**: {', '.join(resource['spending_categories'][:3])}...
- **Depletion Penalty**: {resource.get('depletion_penalty', 'None')}

"""
    
    md += f"""---

## 3. Progression System

{spec['3_progression_system']['description']}

**Type**: {spec['3_progression_system']['type']}

### Phase Requirements

| Phase | Name | Entry Requirements | Completion Requirements | Unlocks |
|-------|------|-------------------|------------------------|---------|
"""
    
    for phase in spec['3_progression_system']['phases']:
        entry = phase['entry_requirements']
        comp = phase['completion_requirements']
        md += f"| {phase['phase']} | {phase['name']} | {entry} | {comp['actions_completed'][:2]}... | {phase['unlocks'][0]} |\n"
    
    md += f"""
---

## 4. Challenge System

{spec['4_challenge_system']['description']}

"""
    
    for ctype in spec['4_challenge_system']['challenge_types']:
        md += f"""### {ctype['type'].title()} Challenges
{ctype['description']}

"""
        for example in ctype['examples'][:2]:
            md += f"""- **{example['name']}**: {example['effect']}
  - Mitigation: {example['mitigation']}
  - Severity: {example['severity']}

"""
    
    md += f"""---

## 5. Reward System

{spec['5_reward_system']['description']}

"""
    
    for rtype in spec['5_reward_system']['reward_types']:
        md += f"""### {rtype['type'].title()} Rewards
{rtype['description']}

"""
        for example in rtype['examples'][:3]:
            if 'milestone' in example:
                md += f"- **{example['milestone']}**: {example['reward']}\n"
            elif 'name' in example:
                md += f"- **{example['name']}**: {example['condition']}\n"
            elif 'unlock' in example:
                md += f"- **{example['unlock']}**: {example['condition']}\n"
        md += "\n"
    
    md += f"""---

## 6. Scoring System

{spec['6_scoring_system']['description']}

### Score Categories

| Category | Weight | Metrics |
|----------|--------|---------|
"""
    
    for cat in spec['6_scoring_system']['score_categories']:
        metrics = [m['metric'] for m in cat['metrics']]
        md += f"| {cat['category']} | {cat['weight']*100:.0f}% | {', '.join(metrics[:2])}... |\n"
    
    md += f"""
### Grade Scale

| Grade | Min Score | Title |
|-------|-----------|-------|
"""
    
    for grade, data in spec['6_scoring_system']['grade_scale'].items():
        md += f"| {grade} | {data['min']}+ | {data['title']} |\n"
    
    md += f"""
---

## 7. Decision System

{spec['7_decision_system']['description']}

"""
    
    for decision in spec['7_decision_system']['key_decisions']:
        md += f"""### {decision['decision_id'].replace('_', ' ').title()}
**Location**: {decision['location']}
**Question**: {decision['question']}

"""
        for opt in decision['options'][:3]:
            md += f"""- **{opt['choice']}**: {opt.get('effects', opt.get('immediate_effects', 'N/A'))}
  - {opt.get('long_term_effects', opt.get('outcome', 'N/A'))}

"""
    
    md += f"""---

## 8. Endgame System

{spec['8_endgame_system']['description']}

### Ending Types

"""
    
    for ending in spec['8_endgame_system']['ending_types']:
        md += f"""#### {ending['ending']}
- **Conditions**: {ending['conditions']}
- **Narrative**: {ending['narrative']}

"""
    
    md += f"""---

## Implementation Notes for Phase 6

1. **Resource Management**: Implement resource tracking with visual indicators
2. **Phase Gating**: Enforce progression requirements before unlocking new areas
3. **Challenge Timing**: Scale challenge frequency based on difficulty setting
4. **Save System**: Allow players to save progress at any point
5. **Tutorial**: Include guided tutorial for first-time players
6. **Accessibility**: Ensure UI is accessible to all players

---

*Specification generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return md


def main():
    processed_dir = Path("processed")
    
    print("Loading action planner...")
    action_planner = load_action_planner(processed_dir)
    
    print("Loading virtual map...")
    virtual_map = load_virtual_map(processed_dir)
    
    print("\nCreating game mechanics specification...")
    spec = create_game_mechanics_spec(action_planner, virtual_map)
    
    # Save JSON spec
    json_path = processed_dir / "game_mechanics_spec.json"
    with open(json_path, 'w') as f:
        json.dump(spec, f, indent=2)
    print(f"  -> Saved: {json_path}")
    
    # Save markdown spec
    md_spec = generate_markdown_spec(spec)
    md_path = processed_dir / "game_mechanics_spec.md"
    with open(md_path, 'w') as f:
        f.write(md_spec)
    print(f"  -> Saved: {md_path}")
    
    # Create task summary
    summary_md = f"""# Phase 5 Task 05: Define Simulation Game Mechanics

## Status: COMPLETED

## Objective
Specify detailed game mechanics for Phase 6 simulation.

## Process Completed
1. Defined resource management system (5 resources: Capital, Time, Knowledge, Network, Reputation)
2. Specified scoring and progression mechanics (5 phases with requirements)
3. Created challenge difficulty scaling (4 difficulty levels)
4. Designed reward and achievement system (milestones, achievements, unlocks)
5. Defined decision system with meaningful choices
6. Created endgame system with 6 ending variants

## Output Files
- `processed/game_mechanics_spec.json` - Complete game mechanics in JSON format
- `processed/game_mechanics_spec.md` - Human-readable specification document

## Key Mechanics Defined

### Resources (5)
- 💰 **Capital**: $5,000-$50,000 starting, used for fees and expenses
- ⏰ **Time**: 52 weeks starting, spent on actions
- 📚 **Knowledge**: 0-100, unlocks advanced actions
- 🤝 **Network**: 0-100, access to opportunities
- ⭐ **Reputation**: 0-100, credibility and trust

### Progression
- 5 phase-gated regions with entry/completion requirements
- Sequential unlocking of actions and capabilities
- Optional actions affect ending variants

### Challenges
- 3 types: Environmental, Enemy, Resource
- 4 difficulty levels: Easy, Normal, Hard, Expert
- Mitigation strategies for each challenge

### Scoring
- 5 categories: Financial (30%), Speed (20%), Compliance (25%), Growth (15%), Achievements (10%)
- Grade scale: S (Visionary) to F (Failure)
- 6 ending variants based on performance

### Key Decisions
- Business structure selection (LLC, C-Corp, S-Corp, Sole Prop)
- Funding strategy (Bootstrap, Loan, Angel, VC)
- Market entry strategy (MVP, Soft Launch, Big Bang)

## Verification
- JSON specification complete and valid
- Markdown documentation comprehensive
- All game mechanics defined for Phase 6 implementation

## Next Steps
- Review mechanics for balance and fun factor
- Proceed to Task 06: Create USA Business Regulation Database

---
*Task completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    summary_path = processed_dir / "phase5_task05_summary.md"
    with open(summary_path, 'w') as f:
        f.write(summary_md)
    print(f"  -> Saved: {summary_path}")
    
    print("\nPhase 5 Task 05 completed successfully!")


if __name__ == "__main__":
    main()
