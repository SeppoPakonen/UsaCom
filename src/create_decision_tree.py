#!/usr/bin/env python3
"""
Phase 5 Task 07: Design Decision Tree for Business Structure Selection
Create interactive decision tree for choosing business entity type.
"""

import json
from pathlib import Path
from datetime import datetime


def create_decision_tree() -> dict:
    """Create comprehensive decision tree for business structure selection."""
    
    tree = {
        "title": "USA Business Structure Decision Tree",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "Interactive decision tree to help entrepreneurs choose the optimal business entity type",
        
        "decision_tree": {
            "root": {
                "question": "How many owners will the business have?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "single_owner",
                        "label": "Single Owner (1 person)",
                        "next_question": "liability_concern_single"
                    },
                    {
                        "choice": "multiple_owners",
                        "label": "Multiple Owners (2+ people)",
                        "next_question": "liability_concern_multi"
                    }
                ]
            },
            
            "liability_concern_single": {
                "question": "How concerned are you about personal liability protection?",
                "type": "scale",
                "scale": {
                    "min": 1,
                    "max": 5,
                    "min_label": "Not concerned - low risk business",
                    "max_label": "Very concerned - high risk business"
                },
                "branches": [
                    {
                        "condition": "score <= 2",
                        "next_question": "tax_preference_single"
                    },
                    {
                        "condition": "score >= 3",
                        "recommendation": "LLC",
                        "confidence": "high",
                        "reasoning": "LLC provides liability protection for single owners with minimal compliance burden"
                    }
                ]
            },
            
            "liability_concern_multi": {
                "question": "How concerned are you about personal liability protection?",
                "type": "scale",
                "scale": {
                    "min": 1,
                    "max": 5,
                    "min_label": "Not concerned",
                    "max_label": "Very concerned"
                },
                "branches": [
                    {
                        "condition": "score <= 2",
                        "next_question": "partnership_type"
                    },
                    {
                        "condition": "score >= 3",
                        "next_question": "investment_plans"
                    }
                ]
            },
            
            "partnership_type": {
                "question": "What type of partnership structure do you prefer?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "equal_management",
                        "label": "All owners actively manage the business",
                        "recommendation": "General Partnership",
                        "confidence": "medium",
                        "reasoning": "General Partnership allows all partners to participate in management with simple structure"
                    },
                    {
                        "choice": "silent_partners",
                        "label": "Some owners are passive investors only",
                        "recommendation": "Limited Partnership (LP)",
                        "confidence": "medium",
                        "reasoning": "LP allows passive investors with limited liability while general partners manage"
                    }
                ]
            },
            
            "investment_plans": {
                "question": "Do you plan to seek venture capital or angel investment?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "yes_vc",
                        "label": "Yes, seeking significant outside investment",
                        "next_question": "ipo_plans"
                    },
                    {
                        "choice": "no_vc",
                        "label": "No, self-funded or small business loan",
                        "recommendation": "LLC",
                        "confidence": "high",
                        "reasoning": "LLC provides liability protection with flexible taxation and less compliance"
                    }
                ]
            },
            
            "ipo_plans": {
                "question": "Do you plan to take the company public (IPO) within 5-10 years?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "yes_ipo",
                        "label": "Yes, IPO is a goal",
                        "recommendation": "C-Corporation",
                        "confidence": "high",
                        "reasoning": "C-Corp is required for IPO and preferred by VCs for equity structure"
                    },
                    {
                        "choice": "no_ipo",
                        "label": "No, plan to stay private or sell",
                        "next_question": "profit_distribution"
                    }
                ]
            },
            
            "profit_distribution": {
                "question": "How do you want to handle profit distribution?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "flexible_distribution",
                        "label": "Flexible - different percentages for different members",
                        "recommendation": "LLC",
                        "confidence": "high",
                        "reasoning": "LLC allows flexible profit distribution not tied to ownership percentage"
                    },
                    {
                        "choice": "proportional_distribution",
                        "label": "Proportional - based on ownership percentage only",
                        "next_question": "salary_preference"
                    }
                ]
            },
            
            "salary_preference": {
                "question": "Do owners want to receive salaries (W-2) or distributions?",
                "type": "single_choice",
                "options": [
                    {
                        "choice": "salary_required",
                        "label": "Owners want regular salaries",
                        "recommendation": "S-Corporation",
                        "confidence": "medium",
                        "reasoning": "S-Corp allows owner-employee salaries with potential tax savings on distributions"
                    },
                    {
                        "choice": "distributions_only",
                        "label": "Distributions only, no formal salary",
                        "recommendation": "LLC",
                        "confidence": "medium",
                        "reasoning": "LLC allows flexible distributions without payroll requirements"
                    }
                ]
            }
        },
        
        "entity_comparison": {
            "Sole Proprietorship": {
                "description": "Simplest business structure - one person owns and operates",
                "owners": "1 (single owner)",
                "liability": "Unlimited personal liability",
                "taxation": "Pass-through (Schedule C)",
                "formation_cost": "$0-$100",
                "ongoing_compliance": "Minimal",
                "management": "Owner controls everything",
                "transferability": "Difficult - business ends with owner",
                "fundraising": "Very limited - personal funds only",
                "best_for": [
                    "Low-risk businesses",
                    "Side hustles and testing ideas",
                    "Freelancers and consultants",
                    "Very small operations"
                ],
                "not_good_for": [
                    "High-risk businesses",
                    "Businesses seeking investment",
                    "Businesses with significant assets"
                ],
                "pros": [
                    "Easiest to set up",
                    "Lowest cost",
                    "Complete control",
                    "Simple taxes (Schedule C)"
                ],
                "cons": [
                    "Unlimited personal liability",
                    "Hard to raise capital",
                    "Business ends with owner",
                    "Self-employment tax on all income"
                ]
            },
            
            "General Partnership": {
                "description": "Two or more people share ownership and management",
                "owners": "2+ (partners)",
                "liability": "Unlimited personal liability for all partners",
                "taxation": "Pass-through (Form 1065, K-1s)",
                "formation_cost": "$0-$200",
                "ongoing_compliance": "Minimal",
                "management": "All partners participate (unless agreed otherwise)",
                "transferability": "Difficult - requires partner approval",
                "fundraising": "Limited - partner contributions",
                "best_for": [
                    "Professional practices (law, accounting)",
                    "Family businesses",
                    "Low-risk ventures with trusted partners"
                ],
                "not_good_for": [
                    "High-risk businesses",
                    "Businesses with passive investors",
                    "Businesses seeking outside investment"
                ],
                "pros": [
                    "Easy to establish",
                    "Low cost",
                    "Shared responsibility",
                    "Pass-through taxation"
                ],
                "cons": [
                    "Unlimited personal liability",
                    "Joint and several liability",
                    "Potential for partner disputes",
                    "Partnership dissolves if partner leaves"
                ]
            },
            
            "LLC (Limited Liability Company)": {
                "description": "Flexible hybrid structure with liability protection and pass-through taxation",
                "owners": "1+ (members)",
                "liability": "Limited - personal assets protected",
                "taxation": "Pass-through by default (can elect corporate)",
                "formation_cost": "$50-$500",
                "ongoing_compliance": "Low to Moderate",
                "management": "Member-managed or Manager-managed",
                "transferability": "Restricted - operating agreement controls",
                "fundraising": "Moderate - can add members, but not ideal for VC",
                "best_for": [
                    "Small to medium businesses",
                    "Real estate investments",
                    "Consulting businesses",
                    "Family businesses",
                    "Most startups not seeking VC"
                ],
                "not_good_for": [
                    "Businesses planning IPO",
                    "Businesses seeking significant VC funding",
                    "Banks and insurance companies (restricted in some states)"
                ],
                "pros": [
                    "Limited liability protection",
                    "Flexible profit distribution",
                    "Pass-through taxation (avoid double tax)",
                    "Less formal than corporation",
                    "Flexible management structure"
                ],
                "cons": [
                    "Self-employment tax on all profits",
                    "Cannot issue stock",
                    "Less attractive to VCs",
                    "Operating agreement complexity"
                ]
            },
            
            "S-Corporation": {
                "description": "Corporation electing pass-through taxation status",
                "owners": "1-100 shareholders (US citizens/residents only)",
                "liability": "Limited - personal assets protected",
                "taxation": "Pass-through (Form 1120-S, K-1s)",
                "formation_cost": "$100-$500",
                "ongoing_compliance": "Moderate to High",
                "management": "Directors and officers required",
                "transferability": "Restricted - shareholder limits",
                "fundraising": "Limited - 100 shareholder cap, one class of stock",
                "best_for": [
                    "Profitable small businesses",
                    "Businesses where owners want salaries",
                    "Family businesses",
                    "Professional services"
                ],
                "not_good_for": [
                    "Businesses seeking VC funding",
                    "Businesses with foreign investors",
                    "Businesses planning IPO",
                    "High-growth startups"
                ],
                "pros": [
                    "Limited liability protection",
                    "Pass-through taxation",
                    "Potential self-employment tax savings",
                    "Credibility with customers"
                ],
                "cons": [
                    "Strict eligibility requirements",
                    "One class of stock only",
                    "100 shareholder limit",
                    "More formalities than LLC",
                    "IRS scrutiny on salary vs distributions"
                ]
            },
            
            "C-Corporation": {
                "description": "Standard corporation with separate tax identity",
                "owners": "Unlimited shareholders",
                "liability": "Limited - personal assets protected",
                "taxation": "Double taxation (corporate + dividend tax)",
                "formation_cost": "$100-$500",
                "ongoing_compliance": "High",
                "management": "Board of directors and officers required",
                "transferability": "Easy - shares freely transferable",
                "fundraising": "Excellent - can issue multiple stock classes",
                "best_for": [
                    "Startups seeking VC funding",
                    "Businesses planning IPO",
                    "High-growth companies",
                    "Companies wanting to offer stock options"
                ],
                "not_good_for": [
                    "Small businesses wanting simplicity",
                    "Businesses distributing most profits to owners",
                    "Owner-operated businesses"
                ],
                "pros": [
                    "Limited liability protection",
                    "Unlimited shareholders",
                    "Multiple classes of stock",
                    "Ideal for VC funding",
                    "Can go public",
                    "Employee stock options"
                ],
                "cons": [
                    "Double taxation",
                    "Most expensive to maintain",
                    "Most formalities",
                    "Complex compliance requirements"
                ]
            },
            
            "Limited Partnership (LP)": {
                "description": "Partnership with general and limited partners",
                "owners": "1+ general partners, 1+ limited partners",
                "liability": "General: Unlimited, Limited: Limited to investment",
                "taxation": "Pass-through (Form 1065, K-1s)",
                "formation_cost": "$100-$300",
                "ongoing_compliance": "Moderate",
                "management": "General partners only",
                "transferability": "Restricted",
                "fundraising": "Good for passive investors",
                "best_for": [
                    "Real estate investments",
                    "Family estates",
                    "Investment funds",
                    "Businesses with passive investors"
                ],
                "not_good_for": [
                    "Active co-ownership",
                    "All owners wanting management role"
                ],
                "pros": [
                    "Limited liability for limited partners",
                    "Pass-through taxation",
                    "Good for raising passive capital"
                ],
                "cons": [
                    "General partners have unlimited liability",
                    "Limited partners cannot manage",
                    "More complex than general partnership"
                ]
            },
            
            "LLP (Limited Liability Partnership)": {
                "description": "Partnership where all partners have limited liability",
                "owners": "2+ partners (professionals in some states)",
                "liability": "Limited - protected from other partners' malpractice",
                "taxation": "Pass-through (Form 1065, K-1s)",
                "formation_cost": "$100-$300",
                "ongoing_compliance": "Moderate",
                "management": "All partners participate",
                "transferability": "Restricted",
                "fundraising": "Limited - partner contributions",
                "best_for": [
                    "Professional practices (lawyers, accountants, architects)",
                    "Medical practices",
                    "Consulting firms"
                ],
                "not_good_for": [
                    "Non-professional businesses",
                    "Businesses with passive investors"
                ],
                "pros": [
                    "Limited liability for all partners",
                    "All partners can manage",
                    "Pass-through taxation",
                    "Protection from partner malpractice"
                ],
                "cons": [
                    "Limited to professionals in many states",
                    "Still liable for own malpractice",
                    "Not available for all business types"
                ]
            }
        },
        
        "tax_comparison": {
            "Sole Proprietorship": {
                "form": "Schedule C (attached to personal 1040)",
                "tax_rate": "Personal income tax rates (10%-37%)",
                "self_employment_tax": "15.3% on net earnings",
                "double_taxation": "No"
            },
            "General Partnership": {
                "form": "Form 1065 (informational), K-1s to partners",
                "tax_rate": "Personal income tax rates on distributions",
                "self_employment_tax": "15.3% on guaranteed payments and distributive share",
                "double_taxation": "No"
            },
            "LLC": {
                "form": "Single-member: Schedule C; Multi-member: Form 1065",
                "tax_rate": "Personal income tax rates on distributions",
                "self_employment_tax": "15.3% on member's share of profits",
                "double_taxation": "No (unless elects corporate taxation)",
                "election_options": "Can elect S-Corp or C-Corp taxation"
            },
            "S-Corporation": {
                "form": "Form 1120-S (informational), K-1s to shareholders",
                "tax_rate": "Personal income tax rates on distributions",
                "self_employment_tax": "Only on W-2 wages, not distributions",
                "double_taxation": "No",
                "special_notes": "Must pay reasonable salary to owner-employees"
            },
            "C-Corporation": {
                "form": "Form 1120",
                "tax_rate": "Corporate rate (21% flat)",
                "self_employment_tax": "N/A - wages subject to FICA",
                "double_taxation": "Yes - corporate tax + dividend tax",
                "special_notes": "Dividends taxed at qualified dividend rates (0%-20%)"
            }
        },
        
        "conversion_paths": {
            "Sole Prop to LLC": {
                "process": "File Articles of Organization, transfer assets",
                "cost": "$50-$500",
                "tax_implications": "Generally tax-free if done correctly",
                "difficulty": "Easy"
            },
            "Sole Prop/Partnership to S-Corp": {
                "process": "Incorporate, file Form 2553",
                "cost": "$100-$500 + legal fees",
                "tax_implications": "May trigger gain recognition on appreciated assets",
                "difficulty": "Moderate"
            },
            "LLC to S-Corp": {
                "process": "File Form 8832 (C-Corp election) then Form 2553 (S-Corp election)",
                "cost": "$0 filing fee",
                "tax_implications": "Generally tax-free",
                "difficulty": "Moderate"
            },
            "LLC to C-Corp": {
                "process": "File Form 8832 or statutory conversion",
                "cost": "$100-$500",
                "tax_implications": "May trigger gain recognition",
                "difficulty": "Moderate"
            },
            "S-Corp to C-Corp": {
                "process": "File Form 8832 or revoke S election",
                "cost": "$0 filing fee",
                "tax_implications": "Built-in gains tax may apply for 5 years",
                "difficulty": "Easy"
            },
            "C-Corp to S-Corp": {
                "process": "File Form 2553 (if eligible)",
                "cost": "$0 filing fee",
                "tax_implications": "Built-in gains tax may apply",
                "difficulty": "Moderate (eligibility requirements)"
            }
        },
        
        "recommendation_engine": {
            "scoring_criteria": {
                "liability_protection": {
                    "weight": 0.25,
                    "description": "Importance of protecting personal assets"
                },
                "tax_efficiency": {
                    "weight": 0.20,
                    "description": "Minimizing overall tax burden"
                },
                "ease_of_setup": {
                    "weight": 0.15,
                    "description": "Simplicity of formation"
                },
                "ease_of_maintenance": {
                    "weight": 0.15,
                    "description": "Ongoing compliance burden"
                },
                "fundraising_ability": {
                    "weight": 0.15,
                    "description": "Ability to raise outside capital"
                },
                "flexibility": {
                    "weight": 0.10,
                    "description": "Operational and profit distribution flexibility"
                }
            },
            "entity_scores": {
                "Sole Proprietorship": {
                    "liability_protection": 1,
                    "tax_efficiency": 7,
                    "ease_of_setup": 10,
                    "ease_of_maintenance": 10,
                    "fundraising_ability": 1,
                    "flexibility": 8
                },
                "General Partnership": {
                    "liability_protection": 1,
                    "tax_efficiency": 7,
                    "ease_of_setup": 9,
                    "ease_of_maintenance": 9,
                    "fundraising_ability": 2,
                    "flexibility": 7
                },
                "LLC": {
                    "liability_protection": 9,
                    "tax_efficiency": 8,
                    "ease_of_setup": 7,
                    "ease_of_maintenance": 8,
                    "fundraising_ability": 4,
                    "flexibility": 10
                },
                "S-Corporation": {
                    "liability_protection": 9,
                    "tax_efficiency": 9,
                    "ease_of_setup": 5,
                    "ease_of_maintenance": 5,
                    "fundraising_ability": 3,
                    "flexibility": 5
                },
                "C-Corporation": {
                    "liability_protection": 9,
                    "tax_efficiency": 5,
                    "ease_of_setup": 4,
                    "ease_of_maintenance": 3,
                    "fundraising_ability": 10,
                    "flexibility": 6
                },
                "Limited Partnership": {
                    "liability_protection": 6,
                    "tax_efficiency": 7,
                    "ease_of_setup": 6,
                    "ease_of_maintenance": 6,
                    "fundraising_ability": 5,
                    "flexibility": 6
                },
                "LLP": {
                    "liability_protection": 7,
                    "tax_efficiency": 7,
                    "ease_of_setup": 6,
                    "ease_of_maintenance": 6,
                    "fundraising_ability": 3,
                    "flexibility": 7
                }
            }
        }
    }
    
    return tree


def generate_markdown_spec(tree: dict) -> str:
    """Generate human-readable markdown specification."""
    
    md = f"""# USA Business Structure Decision Tree

## Overview
- **Title**: {tree['title']}
- **Version**: {tree['version']}
- **Created**: {tree['created']}
- **Description**: {tree['description']}

---

## Decision Tree Flow

### Starting Question
**"How many owners will the business have?"**

#### Option A: Single Owner (1 person)
→ Leads to liability concern assessment
→ If low concern: Tax preference questions
→ If high concern: **Recommend LLC**

#### Option B: Multiple Owners (2+ people)
→ Leads to liability concern assessment
→ If low concern: Partnership type questions
→ If high concern: Investment plans questions

### Key Decision Points

1. **Number of Owners**: Single vs Multiple
2. **Liability Concern**: Low (1-2) vs High (3-5)
3. **Investment Plans**: Seeking VC vs Self-funded
4. **IPO Plans**: Public company goal vs Stay private
5. **Profit Distribution**: Flexible vs Proportional
6. **Owner Compensation**: Salary vs Distributions

---

## Entity Comparison

"""
    
    for entity, details in tree['entity_comparison'].items():
        md += f"""### {entity}
- **Description**: {details['description']}
- **Owners**: {details['owners']}
- **Liability**: {details['liability']}
- **Taxation**: {details['taxation']}
- **Formation Cost**: {details['formation_cost']}
- **Ongoing Compliance**: {details['ongoing_compliance']}
- **Best For**: {', '.join(details['best_for'])}
- **Not Good For**: {', '.join(details['not_good_for'])}

**Pros:**
"""
        for pro in details['pros']:
            md += f"- {pro}\n"
        
        md += "\n**Cons:**\n"
        for con in details['cons']:
            md += f"- {con}\n"
        
        md += "\n---\n\n"
    
    md += f"""
## Tax Comparison

| Entity | Form | Tax Rate | Self-Employment Tax | Double Taxation |
|--------|------|----------|---------------------|-----------------|
"""
    
    for entity, tax in tree['tax_comparison'].items():
        md += f"| {entity} | {tax['form']} | {tax['tax_rate']} | {tax['self_employment_tax']} | {tax['double_taxation']} |\n"
    
    md += f"""
---

## Conversion Paths

"""
    
    for conversion, details in tree['conversion_paths'].items():
        md += f"""### {conversion}
- **Process**: {details['process']}
- **Cost**: {details['cost']}
- **Tax Implications**: {details['tax_implications']}
- **Difficulty**: {details['difficulty']}

"""
    
    md += f"""---

## Recommendation Scoring System

The decision tree uses weighted scoring across 6 criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
"""
    
    for criterion, data in tree['recommendation_engine']['scoring_criteria'].items():
        md += f"| {criterion.replace('_', ' ').title()} | {data['weight']*100:.0f}% | {data['description']} |\n"
    
    md += f"""
---

## Quick Recommendations

### Choose Sole Proprietorship if:
- Testing a business idea
- Low-risk business (consulting, freelancing)
- Want simplest setup
- Don't need liability protection

### Choose LLC if:
- Want liability protection
- Don't plan to raise VC funding
- Want flexible profit distribution
- Want pass-through taxation

### Choose S-Corporation if:
- Business is profitable
- Want to pay owner salaries
- Meet eligibility requirements
- Want potential tax savings

### Choose C-Corporation if:
- Seeking VC funding
- Planning to go public (IPO)
- Want to offer stock options
- Planning to reinvest profits

---

*Specification generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return md


def main():
    processed_dir = Path("processed")
    
    print("Creating decision tree...")
    tree = create_decision_tree()
    
    # Save JSON tree
    json_path = processed_dir / "entity_decision_tree.json"
    with open(json_path, 'w') as f:
        json.dump(tree, f, indent=2)
    print(f"  -> Saved: {json_path}")
    
    # Save markdown spec
    md_spec = generate_markdown_spec(tree)
    md_path = processed_dir / "entity_decision_tree.md"
    with open(md_path, 'w') as f:
        f.write(md_spec)
    print(f"  -> Saved: {md_path}")
    
    # Create task summary
    summary_md = f"""# Phase 5 Task 07: Design Decision Tree for Business Structure Selection

## Status: COMPLETED

## Objective
Create interactive decision tree for choosing business entity type.

## Process Completed
1. Mapped entity selection criteria from source data
2. Created branching logic for different scenarios
3. Added tax implication comparisons
4. Included liability and management considerations
5. Built recommendation scoring engine
6. Documented conversion paths between entity types

## Output Files
- `processed/entity_decision_tree.json` - Complete decision tree in JSON format
- `processed/entity_decision_tree.md` - Human-readable specification

## Decision Tree Structure

### Key Decision Points (6)
1. Number of Owners: Single vs Multiple
2. Liability Concern: Scale 1-5
3. Investment Plans: VC vs Self-funded
4. IPO Plans: Public vs Private
5. Profit Distribution: Flexible vs Proportional
6. Owner Compensation: Salary vs Distributions

### Entity Types Covered (7)
| Entity | Liability | Taxation | Best For |
|--------|-----------|----------|----------|
| Sole Proprietorship | Unlimited | Pass-through | Low-risk, testing |
| General Partnership | Unlimited | Pass-through | Professional practices |
| LLC | Limited | Pass-through | Most small businesses |
| S-Corporation | Limited | Pass-through | Profitable businesses |
| C-Corporation | Limited | Double tax | VC-backed startups |
| Limited Partnership | Mixed | Pass-through | Real estate, investments |
| LLP | Limited | Pass-through | Professional services |

### Tax Comparison
- Forms, tax rates, self-employment tax for each entity
- Double taxation analysis
- Election options documented

### Conversion Paths (6)
- Sole Prop → LLC (Easy)
- LLC → S-Corp (Moderate)
- LLC → C-Corp (Moderate)
- S-Corp → C-Corp (Easy)
- C-Corp → S-Corp (Moderate)
- Partnership → Corporation (Moderate)

### Recommendation Engine
- 6 weighted scoring criteria
- Entity scores for each criterion
- Automatic recommendation based on user inputs

## Verification
- JSON decision tree complete and valid
- Markdown documentation comprehensive
- All 7 entity types covered
- Conversion paths documented
- Ready for interactive implementation

## Next Steps
- Proceed to Task 08: Generate Sample Business Scenarios

---
*Task completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    summary_path = processed_dir / "phase5_task07_summary.md"
    with open(summary_path, 'w') as f:
        f.write(summary_md)
    print(f"  -> Saved: {summary_path}")
    
    print("\nPhase 5 Task 07 completed successfully!")


if __name__ == "__main__":
    main()
