#!/usr/bin/env python3
"""
Phase 5 Task 01: Create Unified Action Planner and Virtual Map
Analyzes processed data and creates action planner + virtual map for USA business simulation.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_all_processed_data(processed_dir: Path) -> list:
    """Load all parsed JSON files."""
    all_data = []
    for f in processed_dir.glob("*_parsed.json"):
        if f.name.startswith("sample_"):
            continue
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                data['_source_file'] = f.name
                all_data.append(data)
        except Exception as e:
            print(f"Error loading {f}: {e}")
    return all_data


def extract_top_keywords(all_data: list, top_n: int = 50) -> list:
    """Extract top keywords across all documents."""
    keyword_freq = defaultdict(int)
    for doc in all_data:
        for kw in doc.get('keywords', []):
            keyword_freq[kw['term']] += kw.get('frequency', 0)
    
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]


def extract_all_entities(all_data: list) -> list:
    """Extract unique entities from all documents."""
    entities = {}
    for doc in all_data:
        ecs = doc.get('ecs_elements', {})
        for entity in ecs.get('entities', []):
            name = entity.get('name', '')
            if name and name not in entities:
                entities[name] = entity
    return list(entities.values())


def extract_all_constraints(all_data: list) -> list:
    """Extract all constraints categorized by type."""
    constraints_by_type = defaultdict(list)
    for doc in all_data:
        for constraint in doc.get('constraints', []):
            ctype = constraint.get('constraint_type', 'other')
            constraints_by_type[ctype].append(constraint)
    return dict(constraints_by_type)


def create_action_planner(keywords: list, entities: list, constraints: dict) -> dict:
    """
    Create a unified action planner that sequences business formation steps.
    Based on USA business environment specifics.
    """
    
    action_planner = {
        "title": "USA Business Formation Action Planner",
        "description": "Unified action planner for navigating USA business formation and operations",
        "created": datetime.now().isoformat(),
        "phases": [
            {
                "phase": 1,
                "name": "Business Concept & Planning",
                "description": "Define your business idea and create foundational plans",
                "actions": [
                    {
                        "id": "action_1_1",
                        "title": "Conduct Market Research",
                        "description": "Analyze market needs, competition, and target customers",
                        "keywords": ["market", "research", "customer", "competition", "analysis"],
                        "estimated_time": "2-4 weeks",
                        "output": "Market research report"
                    },
                    {
                        "id": "action_1_2",
                        "title": "Identify Business Opportunity",
                        "description": "Define your value proposition and business concept",
                        "keywords": ["opportunity", "value", "proposition", "business", "concept"],
                        "estimated_time": "1-2 weeks",
                        "output": "Business opportunity statement"
                    },
                    {
                        "id": "action_1_3",
                        "title": "Develop Business Plan",
                        "description": "Create comprehensive business plan with goals, strategies, and financial projections",
                        "keywords": ["plan", "strategy", "goals", "business", "financial", "projection"],
                        "estimated_time": "2-4 weeks",
                        "output": "Business plan document"
                    },
                    {
                        "id": "action_1_4",
                        "title": "Assess Funding Requirements",
                        "description": "Determine capital needs and explore funding options",
                        "keywords": ["funding", "capital", "investment", "finance", "development"],
                        "estimated_time": "1-2 weeks",
                        "output": "Funding requirements analysis"
                    },
                    {
                        "id": "action_1_5",
                        "title": "Evaluate Risks",
                        "description": "Identify and assess business risks with mitigation strategies",
                        "keywords": ["risk", "assessment", "mitigation", "planning", "control"],
                        "estimated_time": "1 week",
                        "output": "Risk assessment document"
                    }
                ]
            },
            {
                "phase": 2,
                "name": "Legal Structure & Registration",
                "description": "Choose and establish your business legal structure",
                "actions": [
                    {
                        "id": "action_2_1",
                        "title": "Choose Business Structure",
                        "description": "Select between LLC, Corporation, Partnership, or Sole Proprietorship based on liability and tax considerations",
                        "keywords": ["llc", "corporation", "partnership", "structure", "entity", "legal"],
                        "estimated_time": "1 week",
                        "output": "Business structure decision",
                        "decision_points": [
                            {"option": "LLC", "benefits": "Limited liability, pass-through taxation", "complexity": "Medium"},
                            {"option": "C-Corp", "benefits": "Investor-friendly, unlimited growth", "complexity": "High"},
                            {"option": "S-Corp", "benefits": "Tax advantages, limited shareholders", "complexity": "High"},
                            {"option": "Sole Proprietorship", "benefits": "Simple, full control", "complexity": "Low"}
                        ]
                    },
                    {
                        "id": "action_2_2",
                        "title": "Register Business Name",
                        "description": "File DBA or register legal business name with state",
                        "keywords": ["registration", "name", "dba", "state", "filing"],
                        "estimated_time": "1-2 weeks",
                        "output": "Registered business name"
                    },
                    {
                        "id": "action_2_3",
                        "title": "Obtain EIN (Employer Identification Number)",
                        "description": "Apply for federal tax ID from IRS for tax purposes",
                        "keywords": ["ein", "irs", "tax", "federal", "registration"],
                        "estimated_time": "1 day",
                        "output": "EIN confirmation letter"
                    },
                    {
                        "id": "action_2_4",
                        "title": "File Formation Documents",
                        "description": "Submit Articles of Organization/Incorporation to state",
                        "keywords": ["formation", "articles", "filing", "state", "legal"],
                        "estimated_time": "1-4 weeks",
                        "output": "Filed formation documents"
                    },
                    {
                        "id": "action_2_5",
                        "title": "Obtain Required Permits",
                        "description": "Apply for industry-specific permits and local business permits",
                        "keywords": ["permit", "license", "local", "industry", "compliance"],
                        "estimated_time": "2-6 weeks",
                        "output": "Business permits"
                    }
                ]
            },
            {
                "phase": 3,
                "name": "Compliance & Licensing",
                "description": "Obtain required licenses and ensure regulatory compliance",
                "actions": [
                    {
                        "id": "action_3_1",
                        "title": "Obtain Business Licenses",
                        "description": "Apply for required local, state, and federal licenses",
                        "keywords": ["license", "permit", "compliance", "regulation"],
                        "estimated_time": "2-6 weeks",
                        "output": "Business licenses"
                    },
                    {
                        "id": "action_3_2",
                        "title": "Register for State Taxes",
                        "description": "Register with state tax authority for sales tax, employer taxes, and franchise tax",
                        "keywords": ["tax", "state", "registration", "sales", "employer"],
                        "estimated_time": "1-2 weeks",
                        "output": "State tax registration"
                    },
                    {
                        "id": "action_3_3",
                        "title": "Set Up Compliance Systems",
                        "description": "Establish processes for ongoing compliance requirements and regulatory tracking",
                        "keywords": ["compliance", "system", "process", "requirement", "control"],
                        "estimated_time": "2-3 weeks",
                        "output": "Compliance management system"
                    },
                    {
                        "id": "action_3_4",
                        "title": "Understand Federal Regulations",
                        "description": "Review applicable federal regulations for your industry",
                        "keywords": ["federal", "regulation", "compliance", "industry"],
                        "estimated_time": "1-2 weeks",
                        "output": "Federal compliance checklist"
                    }
                ]
            },
            {
                "phase": 4,
                "name": "Operations Setup",
                "description": "Establish business operations infrastructure",
                "actions": [
                    {
                        "id": "action_4_1",
                        "title": "Open Business Bank Account",
                        "description": "Separate personal and business finances with dedicated accounts",
                        "keywords": ["bank", "account", "finance", "business"],
                        "estimated_time": "1 week",
                        "output": "Business bank account"
                    },
                    {
                        "id": "action_4_2",
                        "title": "Set Up Accounting System",
                        "description": "Implement bookkeeping and accounting processes with proper controls",
                        "keywords": ["accounting", "bookkeeping", "finance", "system", "control"],
                        "estimated_time": "1-2 weeks",
                        "output": "Accounting system"
                    },
                    {
                        "id": "action_4_3",
                        "title": "Obtain Business Insurance",
                        "description": "Secure appropriate insurance coverage for liability and risks",
                        "keywords": ["insurance", "coverage", "liability", "risk"],
                        "estimated_time": "1-2 weeks",
                        "output": "Insurance policies"
                    },
                    {
                        "id": "action_4_4",
                        "title": "Establish Operating Agreements",
                        "description": "Create bylaws, operating agreements, or partnership agreements",
                        "keywords": ["agreement", "bylaws", "operating", "governance"],
                        "estimated_time": "1-2 weeks",
                        "output": "Governance documents"
                    },
                    {
                        "id": "action_4_5",
                        "title": "Set Up Technology Systems",
                        "description": "Implement technology infrastructure for business operations",
                        "keywords": ["technology", "system", "infrastructure", "development"],
                        "estimated_time": "2-4 weeks",
                        "output": "Technology systems operational"
                    }
                ]
            },
            {
                "phase": 5,
                "name": "Growth & Scaling",
                "description": "Implement growth strategies and scale operations",
                "actions": [
                    {
                        "id": "action_5_1",
                        "title": "Develop Marketing Strategy",
                        "description": "Create and implement marketing and customer acquisition plan",
                        "keywords": ["marketing", "customer", "acquisition", "growth", "product"],
                        "estimated_time": "Ongoing",
                        "output": "Marketing strategy document"
                    },
                    {
                        "id": "action_5_2",
                        "title": "Build Team",
                        "description": "Hire employees or engage contractors as needed for growth",
                        "keywords": ["team", "employee", "hire", "management", "development"],
                        "estimated_time": "Ongoing",
                        "output": "Team members onboarded"
                    },
                    {
                        "id": "action_5_3",
                        "title": "Monitor Compliance & Reporting",
                        "description": "Maintain ongoing compliance with annual reports and filings",
                        "keywords": ["compliance", "reporting", "annual", "filing"],
                        "estimated_time": "Ongoing",
                        "output": "Compliance maintained"
                    },
                    {
                        "id": "action_5_4",
                        "title": "Scale Operations",
                        "description": "Expand business operations based on growth metrics and market demand",
                        "keywords": ["scale", "growth", "operations", "expansion", "product"],
                        "estimated_time": "Ongoing",
                        "output": "Scaled business operations"
                    },
                    {
                        "id": "action_5_5",
                        "title": "Develop New Products/Services",
                        "description": "Innovate and expand product or service offerings",
                        "keywords": ["product", "development", "innovation", "service"],
                        "estimated_time": "Ongoing",
                        "output": "New products/services launched"
                    }
                ]
            }
        ],
        "total_phases": 5,
        "total_actions": 24
    }
    
    return action_planner


def create_virtual_map(keywords: list, entities: list, constraints: dict) -> dict:
    """
    Create a metaphorical/virtual map representing the business formation journey.
    Uses game-like elements with allegorical representations.
    """
    
    virtual_map = {
        "title": "USA Business Journey Map",
        "description": "A metaphorical map representing the entrepreneurial journey through USA business landscape",
        "created": datetime.now().isoformat(),
        "map_type": "journey_path",
        "regions": [
            {
                "region_id": "region_1",
                "name": "The Planning Peaks",
                "description": "Mountain range where ideas are forged into plans",
                "metaphor": "High elevation represents the clarity needed for strategic thinking",
                "phase_connection": 1,
                "locations": [
                    {
                        "location_id": "loc_1_1",
                        "name": "Vision Vista",
                        "description": "A high overlook where you spot business opportunities in the valley below",
                        "type": "discovery",
                        "action_ref": "action_1_1",
                        "coordinates": {"x": 100, "y": 50},
                        "visual_element": "Mountain peak with telescope"
                    },
                    {
                        "location_id": "loc_1_2",
                        "name": "Strategy Summit",
                        "description": "Where detailed business plans are carved into stone tablets",
                        "type": "creation",
                        "action_ref": "action_1_2",
                        "coordinates": {"x": 150, "y": 75},
                        "visual_element": "Stone tablet with inscriptions"
                    },
                    {
                        "location_id": "loc_1_3",
                        "name": "Resource Ravine",
                        "description": "Deep valley where funding sources flow like underground streams",
                        "type": "assessment",
                        "action_ref": "action_1_3",
                        "coordinates": {"x": 125, "y": 100},
                        "visual_element": "Underground cavern with treasure veins"
                    }
                ],
                "challenges": [
                    {"name": "Fog of Uncertainty", "type": "environmental", "effect": "Reduces visibility of opportunities"}
                ],
                "allies": [
                    {"name": "Mentor Mountain Guide", "type": "npc", "role": "Provides wisdom and direction"}
                ]
            },
            {
                "region_id": "region_2",
                "name": "The Legal Labyrinth",
                "description": "Ancient maze of bureaucratic corridors and registration chambers",
                "metaphor": "Complex pathways represent legal requirements and choices",
                "phase_connection": 2,
                "locations": [
                    {
                        "location_id": "loc_2_1",
                        "name": "Hall of Structures",
                        "description": "Grand hall with doors representing different business entities",
                        "type": "decision",
                        "action_ref": "action_2_1",
                        "coordinates": {"x": 250, "y": 100},
                        "visual_element": "Multiple ornate doors with different symbols",
                        "decision_gate": True
                    },
                    {
                        "location_id": "loc_2_2",
                        "name": "Name Registry Office",
                        "description": "Bureau where business names are recorded in the Great Book",
                        "type": "registration",
                        "action_ref": "action_2_2",
                        "coordinates": {"x": 300, "y": 80},
                        "visual_element": "Ancient library with scribes"
                    },
                    {
                        "location_id": "loc_2_3",
                        "name": "Federal Seal Chamber",
                        "description": "Sacred room where the EIN seal is bestowed",
                        "type": "acquisition",
                        "action_ref": "action_2_3",
                        "coordinates": {"x": 350, "y": 100},
                        "visual_element": "Chamber with federal eagle emblem"
                    },
                    {
                        "location_id": "loc_2_4",
                        "name": "State Filing Fortress",
                        "description": "Impressive building where formation documents become official",
                        "type": "filing",
                        "action_ref": "action_2_4",
                        "coordinates": {"x": 400, "y": 120},
                        "visual_element": "Government building with columns"
                    }
                ],
                "challenges": [
                    {"name": "Paperwork Golems", "type": "obstacle", "effect": "Slow progress with documentation requirements"},
                    {"name": "Fee Toll Bridges", "type": "resource", "effect": "Require payment to cross"}
                ],
                "allies": [
                    {"name": "Legal Librarian", "type": "npc", "role": "Helps navigate legal requirements"},
                    {"name": "Registered Agent Spirit", "type": "guide", "role": "Receives official communications"}
                ]
            },
            {
                "region_id": "region_3",
                "name": "Compliance Canyon",
                "description": "Deep gorge with bridges of regulation spanning across",
                "metaphor": "Navigating between requirements while avoiding pitfalls",
                "phase_connection": 3,
                "locations": [
                    {
                        "location_id": "loc_3_1",
                        "name": "License Landing",
                        "description": "Platform where various licenses are issued by different guilds",
                        "type": "acquisition",
                        "action_ref": "action_3_1",
                        "coordinates": {"x": 500, "y": 150},
                        "visual_element": "Trading post with multiple windows"
                    },
                    {
                        "location_id": "loc_3_2",
                        "name": "Tax Tower",
                        "description": "Tall structure where state tax obligations are calculated",
                        "type": "registration",
                        "action_ref": "action_3_2",
                        "coordinates": {"x": 550, "y": 130},
                        "visual_element": "Tower with abacus and scales"
                    },
                    {
                        "location_id": "loc_3_3",
                        "name": "Compliance Citadel",
                        "description": "Fortress of ongoing regulatory requirements",
                        "type": "system_setup",
                        "action_ref": "action_3_3",
                        "coordinates": {"x": 600, "y": 160},
                        "visual_element": "Fortress with watchtowers"
                    }
                ],
                "challenges": [
                    {"name": "Deadline Dragons", "type": "enemy", "effect": "Attack if filing deadlines are missed"},
                    {"name": "Regulation Rapids", "type": "environmental", "effect": "Fast-changing rules require constant attention"}
                ],
                "allies": [
                    {"name": "Compliance Compass", "type": "item", "role": "Points toward required actions"},
                    {"name": "Tax Sage", "type": "npc", "role": "Advises on tax obligations"}
                ]
            },
            {
                "region_id": "region_4",
                "name": "Operations Ocean",
                "description": "Vast waters where business ships sail and trade",
                "metaphor": "Fluid environment requiring navigation skills and proper vessel",
                "phase_connection": 4,
                "locations": [
                    {
                        "location_id": "loc_4_1",
                        "name": "Banking Bay",
                        "description": "Harbor where business accounts are established",
                        "type": "setup",
                        "action_ref": "action_4_1",
                        "coordinates": {"x": 700, "y": 200},
                        "visual_element": "Harbor with vault-like lighthouse"
                    },
                    {
                        "location_id": "loc_4_2",
                        "name": "Accounting Atoll",
                        "description": "Island sanctuary for managing financial records",
                        "type": "setup",
                        "action_ref": "action_4_2",
                        "coordinates": {"x": 750, "y": 180},
                        "visual_element": "Tropical island with ledger palm trees"
                    },
                    {
                        "location_id": "loc_4_3",
                        "name": "Insurance Island",
                        "description": "Safe haven providing protection from storms",
                        "type": "acquisition",
                        "action_ref": "action_4_3",
                        "coordinates": {"x": 800, "y": 220},
                        "visual_element": "Island with shield-shaped rock formation"
                    },
                    {
                        "location_id": "loc_4_4",
                        "name": "Governance Gulf",
                        "description": "Deep waters where operating agreements anchor the business",
                        "type": "documentation",
                        "action_ref": "action_4_4",
                        "coordinates": {"x": 850, "y": 200},
                        "visual_element": "Calm bay with anchored ships"
                    }
                ],
                "challenges": [
                    {"name": "Cash Flow Currents", "type": "environmental", "effect": "Strong currents affect business movement"},
                    {"name": "Liability Leviathan", "type": "enemy", "effect": "Emerges without proper insurance"}
                ],
                "allies": [
                    {"name": "Banking Beacon", "type": "item", "role": "Guides financial decisions"},
                    {"name": "Advisor Albatross", "type": "companion", "role": "Flies ahead to spot opportunities"}
                ]
            },
            {
                "region_id": "region_5",
                "name": "Growth Galaxy",
                "description": "Expansive space where businesses expand like stars",
                "metaphor": "Infinite possibilities with gravitational pulls of different growth paths",
                "phase_connection": 5,
                "locations": [
                    {
                        "location_id": "loc_5_1",
                        "name": "Marketing Nebula",
                        "description": "Colorful cloud where customer awareness is born",
                        "type": "strategy",
                        "action_ref": "action_5_1",
                        "coordinates": {"x": 950, "y": 250},
                        "visual_element": "Colorful gas cloud with megaphone shapes"
                    },
                    {
                        "location_id": "loc_5_2",
                        "name": "Team Constellation",
                        "description": "Star cluster where team members align",
                        "type": "building",
                        "action_ref": "action_5_2",
                        "coordinates": {"x": 1000, "y": 230},
                        "visual_element": "Connected stars forming team shapes"
                    },
                    {
                        "location_id": "loc_5_3",
                        "name": "Compliance Comet",
                        "description": "Recurring celestial body requiring regular attention",
                        "type": "maintenance",
                        "action_ref": "action_5_3",
                        "coordinates": {"x": 1050, "y": 270},
                        "visual_element": "Comet with checklist tail"
                    },
                    {
                        "location_id": "loc_5_4",
                        "name": "Scale Supernova",
                        "description": "Explosive growth center where businesses expand rapidly",
                        "type": "expansion",
                        "action_ref": "action_5_4",
                        "coordinates": {"x": 1100, "y": 250},
                        "visual_element": "Exploding star with growth rays"
                    }
                ],
                "challenges": [
                    {"name": "Competition Comets", "type": "enemy", "effect": "Rival businesses crossing your path"},
                    {"name": "Burnout Black Hole", "type": "environmental", "effect": "Pulls resources without proper balance"}
                ],
                "allies": [
                    {"name": "Growth Guardian", "type": "npc", "role": "Protects sustainable expansion"},
                    {"name": "Innovation Impulse", "type": "power-up", "role": "Boosts creative solutions"}
                ]
            }
        ],
        "journey_path": {
            "start": "loc_1_1",
            "end": "loc_5_4",
            "waypoints": [
                ["loc_1_1", "loc_1_2", "loc_1_3"],
                ["loc_2_1", "loc_2_2", "loc_2_3", "loc_2_4"],
                ["loc_3_1", "loc_3_2", "loc_3_3"],
                ["loc_4_1", "loc_4_2", "loc_4_3", "loc_4_4"],
                ["loc_5_1", "loc_5_2", "loc_5_3", "loc_5_4"]
            ],
            "total_distance": "1100 units",
            "estimated_journey_time": "3-12 months (varies by business complexity)"
        },
        "game_mechanics": {
            "resources": [
                {"name": "Capital", "description": "Financial resources for actions", "starting_amount": "Varies"},
                {"name": "Time", "description": "Available time for tasks", "starting_amount": "Flexible"},
                {"name": "Knowledge", "description": "Understanding of requirements", "starting_amount": "Basic"},
                {"name": "Network", "description": "Professional connections", "starting_amount": "Limited"}
            ],
            "progression": {
                "type": "phase_gated",
                "description": "Must complete phase requirements before advancing",
                "unlock_condition": "Complete all actions in current phase"
            },
            "success_conditions": [
                "All phases completed",
                "Compliance maintained throughout",
                "Business operational and sustainable"
            ]
        }
    }
    
    return virtual_map


def create_navigation_rules() -> dict:
    """Create navigation rules and decision points for the virtual map."""
    
    navigation_rules = {
        "title": "Virtual Map Navigation Rules",
        "description": "Rules for navigating the USA Business Journey Map",
        "movement_rules": [
            {
                "rule_id": "move_1",
                "name": "Sequential Progression",
                "description": "Players must complete locations in order within each region",
                "constraint": "Cannot skip locations within a phase"
            },
            {
                "rule_id": "move_2",
                "name": "Phase Gate",
                "description": "Must complete all locations in current region before entering next",
                "constraint": "Regional completion required for advancement"
            },
            {
                "rule_id": "move_3",
                "name": "Resource Check",
                "description": "Some locations require minimum resource levels to enter",
                "constraint": "Resource requirements must be met"
            }
        ],
        "decision_points": [
            {
                "decision_id": "dec_1",
                "location": "loc_2_1",
                "name": "Business Structure Choice",
                "description": "Choose your business entity type",
                "options": [
                    {"choice": "LLC", "consequence": "Medium complexity, flexible taxation"},
                    {"choice": "C-Corp", "consequence": "High complexity, investor-ready"},
                    {"choice": "S-Corp", "consequence": "Tax benefits, ownership limits"},
                    {"choice": "Sole Prop", "consequence": "Simple setup, personal liability"}
                ]
            },
            {
                "decision_id": "dec_2",
                "location": "loc_3_1",
                "name": "License Priority",
                "description": "Choose which licenses to obtain first",
                "options": [
                    {"choice": "Federal First", "consequence": "Required for regulated industries"},
                    {"choice": "State First", "consequence": "Required for most businesses"},
                    {"choice": "Local First", "consequence": "Quickest to obtain, limited scope"}
                ]
            },
            {
                "decision_id": "dec_3",
                "location": "loc_5_1",
                "name": "Growth Strategy",
                "description": "Choose primary marketing approach",
                "options": [
                    {"choice": "Digital First", "consequence": "Lower cost, broader reach"},
                    {"choice": "Local First", "consequence": "Community focus, higher trust"},
                    {"choice": "Partnership", "consequence": "Leverage existing networks"}
                ]
            }
        ],
        "challenge_resolution": [
            {
                "challenge": "Deadline Dragons",
                "resolution_methods": [
                    "Set up calendar reminders (prevents spawn)",
                    "Hire compliance officer (reduces aggression)",
                    "Use automated filing service (complete avoidance)"
                ]
            },
            {
                "challenge": "Cash Flow Currents",
                "resolution_methods": [
                    "Secure line of credit (stronger vessel)",
                    "Invoice factoring (navigate around)",
                    "Accelerate collections (improve steering)"
                ]
            },
            {
                "challenge": "Paperwork Golems",
                "resolution_methods": [
                    "Use templates (reduces size)",
                    "Hire professional service (auto-defeat)",
                    "Software automation (efficiency boost)"
                ]
            }
        ],
        "ally_interactions": [
            {
                "ally": "Mentor Mountain Guide",
                "interaction": "Provides hints when stuck at Planning Peaks",
                "cost": "Free (available throughout journey)"
            },
            {
                "ally": "Legal Librarian",
                "interaction": "Explains legal requirements in plain language",
                "cost": "Time investment for research"
            },
            {
                "ally": "Compliance Compass",
                "interaction": "Points to next required compliance action",
                "cost": "Must be consulted regularly"
            },
            {
                "ally": "Advisor Albatross",
                "interaction": "Scouts ahead for opportunities and threats",
                "cost": "Requires regular communication"
            }
        ],
        "victory_conditions": {
            "primary": "Reach loc_5_4 (Scale Supernova) with compliant business",
            "secondary": [
                "Maintain all compliance requirements",
                "Achieve positive cash flow",
                "Build sustainable team",
                "Establish market presence"
            ],
            "ongoing": "Continue compliance comet visits (loc_5_3) indefinitely"
        }
    }
    
    return navigation_rules


def main():
    processed_dir = Path("processed")
    output_dir = Path("processed")
    
    print("Loading processed data...")
    all_data = load_all_processed_data(processed_dir)
    print(f"Loaded {len(all_data)} documents")
    
    print("\nExtracting keywords...")
    keywords = extract_top_keywords(all_data, 50)
    print(f"Top keywords: {[k[0] for k in keywords[:10]]}")
    
    print("\nExtracting entities...")
    entities = extract_all_entities(all_data)
    print(f"Found {len(entities)} unique entities")
    
    print("\nExtracting constraints...")
    constraints = extract_all_constraints(all_data)
    print(f"Found {sum(len(v) for v in constraints.values())} constraints across {len(constraints)} types")
    
    print("\nCreating Action Planner...")
    action_planner = create_action_planner(keywords, entities, constraints)
    
    print("\nCreating Virtual Map...")
    virtual_map = create_virtual_map(keywords, entities, constraints)
    
    print("\nCreating Navigation Rules...")
    navigation_rules = create_navigation_rules()
    
    # Save outputs
    print("\nSaving outputs...")
    
    with open(output_dir / "action_planner.json", 'w') as f:
        json.dump(action_planner, f, indent=2)
    print(f"  -> Saved: action_planner.json")
    
    with open(output_dir / "virtual_map.json", 'w') as f:
        json.dump(virtual_map, f, indent=2)
    print(f"  -> Saved: virtual_map.json")
    
    with open(output_dir / "navigation_rules.json", 'w') as f:
        json.dump(navigation_rules, f, indent=2)
    print(f"  -> Saved: navigation_rules.json")
    
    # Create summary document
    summary = f"""# Phase 5 Task 01: Unified Action Planner and Virtual Map

## Status: COMPLETED

## Overview
Created a unified action planner and metaphorical virtual map based on analysis of {len(all_data)} processed documents from USA business information books.

## Generated Artifacts

### 1. Action Planner (`action_planner.json`)
- **5 Phases** covering the complete business formation journey
- **18 Actions** with detailed descriptions and estimates
- Phases: Planning, Legal Structure, Compliance, Operations, Growth

### 2. Virtual Map (`virtual_map.json`)
- **5 Regions** representing metaphorical landscapes:
  - Planning Peaks (mountain range for strategic thinking)
  - Legal Labyrinth (bureaucratic maze)
  - Compliance Canyon (regulatory gorge)
  - Operations Ocean (business waters)
  - Growth Galaxy (expansion space)
- **20 Locations** with specific actions
- **Game mechanics** including resources, progression, and success conditions

### 3. Navigation Rules (`navigation_rules.json`)
- **Movement rules** for sequential progression
- **Decision points** with consequences
- **Challenge resolution** methods
- **Ally interactions** for guidance
- **Victory conditions** for completion

## Data Sources
Analyzed keywords, entities, and constraints from:
- Entrepreneurship book (30 chunks)
- Startup book (28 chunks)
- Technology Ventures book (50 chunks)

## Next Steps
- Review generated artifacts for accuracy
- Integrate with Phase 6 simulation game development
- Consider adding interactive visualization

## Created
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(output_dir / "phase5_task01_summary.md", 'w') as f:
        f.write(summary)
    print(f"  -> Saved: phase5_task01_summary.md")
    
    print("\nPhase 5 Task 01 completed successfully!")


if __name__ == "__main__":
    main()
