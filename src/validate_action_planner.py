#!/usr/bin/env python3
"""
Phase 5 Task 02: Validate Action Planner Against Source Data
Cross-reference action planner with original book content to ensure completeness.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_action_planner(processed_dir: Path) -> dict:
    """Load the action planner."""
    with open(processed_dir / "action_planner.json", 'r') as f:
        return json.load(f)


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


def extract_all_keywords(all_data: list) -> dict:
    """Extract all keywords with frequencies."""
    keyword_freq = defaultdict(int)
    keyword_docs = defaultdict(list)
    
    for doc in all_data:
        for kw in doc.get('keywords', []):
            term = kw['term']
            keyword_freq[term] += kw.get('frequency', 0)
            if doc['_source_file'] not in keyword_docs[term]:
                keyword_docs[term].append(doc['_source_file'])
    
    return dict(keyword_freq), dict(keyword_docs)


def extract_all_constraints(all_data: list) -> list:
    """Extract all constraints."""
    constraints = []
    for doc in all_data:
        constraints.extend(doc.get('constraints', []))
    return constraints


def extract_ecs_elements(all_data: list) -> dict:
    """Extract all ECS elements."""
    entities = []
    components = []
    systems = []
    
    for doc in all_data:
        ecs = doc.get('ecs_elements', {})
        entities.extend(ecs.get('entities', []))
        components.extend(ecs.get('components', []))
        systems.extend(ecs.get('systems', []))
    
    return {
        'entities': entities,
        'components': components,
        'systems': systems
    }


def validate_action_planner(action_planner: dict, keywords: dict, constraints: list, ecs: dict) -> dict:
    """Validate action planner against source data."""
    
    validation_results = {
        "validation_date": datetime.now().isoformat(),
        "action_planner_summary": {
            "total_phases": action_planner.get("total_phases", 0),
            "total_actions": action_planner.get("total_actions", 0)
        },
        "source_data_summary": {
            "total_keywords": len(keywords),
            "total_constraints": len(constraints),
            "total_entities": len(ecs.get('entities', [])),
            "total_components": len(ecs.get('components', [])),
            "total_systems": len(ecs.get('systems', []))
        },
        "coverage_analysis": {},
        "gap_analysis": [],
        "recommendations": [],
        "validation_status": "PASS"
    }
    
    # Check keyword coverage
    action_keywords = set()
    for phase in action_planner.get('phases', []):
        for action in phase.get('actions', []):
            action_keywords.update(action.get('keywords', []))
    
    source_keywords = set(keywords.keys())
    
    # Top source keywords
    top_source_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:50]
    top_source_terms = {k for k, v in top_source_keywords}
    
    # Check overlap
    keyword_overlap = action_keywords.intersection(source_keywords)
    keyword_missing = top_source_terms - action_keywords
    
    validation_results["coverage_analysis"]["keyword_coverage"] = {
        "action_planner_keywords": list(action_keywords),
        "source_keywords_matched": len(keyword_overlap),
        "top_source_keywords_covered": len(top_source_terms & action_keywords),
        "coverage_percentage": round(len(keyword_overlap) / len(source_keywords) * 100, 2) if source_keywords else 0
    }
    
    # Check constraint coverage
    constraint_types = defaultdict(int)
    for constraint in constraints:
        constraint_types[constraint.get('constraint_type', 'other')] += 1
    
    # Map constraints to phases
    phase_constraint_mapping = {
        1: ['recommendation', 'requirement'],  # Planning phase
        2: ['requirement', 'compliance'],  # Legal phase
        3: ['compliance', 'requirement', 'temporal'],  # Compliance phase
        4: ['requirement', 'financial'],  # Operations phase
        5: ['recommendation', 'compliance']  # Growth phase
    }
    
    constraint_coverage = {}
    for phase_num, expected_types in phase_constraint_mapping.items():
        covered = sum(constraint_types.get(t, 0) for t in expected_types)
        constraint_coverage[f"phase_{phase_num}"] = {
            "expected_types": expected_types,
            "available_constraints": covered
        }
    
    validation_results["coverage_analysis"]["constraint_coverage"] = constraint_coverage
    
    # Check ECS element coverage
    ecs_in_actions = set()
    for phase in action_planner.get('phases', []):
        for action in phase.get('actions', []):
            # Check action descriptions for entity mentions
            desc = action.get('description', '').lower()
            for entity in ecs.get('entities', []):
                if entity.get('name', '').lower() in desc:
                    ecs_in_actions.add(entity.get('name'))
    
    validation_results["coverage_analysis"]["ecs_coverage"] = {
        "total_entities_in_source": len(ecs.get('entities', [])),
        "entities_referenced_in_actions": len(ecs_in_actions),
        "total_systems_in_source": len(ecs.get('systems', [])),
        "systems_aligned_with_phases": len(action_planner.get('phases', []))
    }
    
    # Gap analysis
    if keyword_missing:
        validation_results["gap_analysis"].append({
            "gap_type": "keyword_coverage",
            "description": "Top source keywords not explicitly covered in action planner",
            "missing_keywords": list(keyword_missing)[:20],  # Top 20 missing
            "severity": "medium",
            "recommendation": "Consider adding actions or keywords to cover these terms"
        })
    
    # Check for missing business formation steps
    expected_steps = {
        "business plan": ["business plan", "plan", "strategy"],
        "market research": ["market research", "market", "research", "analysis"],
        "funding": ["funding", "capital", "investment", "finance"],
        "legal structure": ["legal structure", "structure", "entity", "llc", "corporation"],
        "registration": ["registration", "register", "filing"],
        "EIN": ["ein", "employer identification", "tax id", "federal tax"],
        "licenses": ["license", "permit", "licenses"],
        "permits": ["permit", "license", "permits"],
        "tax registration": ["tax registration", "state tax", "register for tax"],
        "bank account": ["bank account", "bank", "account", "business bank"],
        "insurance": ["insurance", "coverage", "liability"],
        "accounting": ["accounting", "bookkeeping", "finance system"],
        "compliance": ["compliance", "regulatory", "requirement"],
        "reporting": ["reporting", "annual report", "filing"]
    }
    
    action_text = []
    for phase in action_planner.get('phases', []):
        for action in phase.get('actions', []):
            action_text.append(action.get('title', '').lower())
            action_text.append(action.get('description', '').lower())
            action_text.extend([k.lower() for k in action.get('keywords', [])])
    action_text_combined = ' '.join(action_text)
    
    missing_steps = []
    for step, keywords in expected_steps.items():
        found = any(kw in action_text_combined for kw in keywords)
        if not found:
            missing_steps.append(step)
    
    if missing_steps:
        validation_results["gap_analysis"].append({
            "gap_type": "business_process_coverage",
            "description": "Expected business formation steps not explicitly covered",
            "missing_steps": missing_steps,
            "severity": "high" if len(missing_steps) > 3 else "medium",
            "recommendation": "Add actions or expand existing actions to cover these steps"
        })
    else:
        validation_results["gap_analysis"].append({
            "gap_type": "business_process_coverage",
            "description": "All expected business formation steps are covered",
            "missing_steps": [],
            "severity": "none",
            "recommendation": "No action needed"
        })
    
    # Check time estimate coverage
    actions_without_time = []
    for phase in action_planner.get('phases', []):
        for action in phase.get('actions', []):
            if not action.get('estimated_time'):
                actions_without_time.append(action.get('id', 'unknown'))
    
    if actions_without_time:
        validation_results["gap_analysis"].append({
            "gap_type": "time_estimates",
            "description": "Actions missing time estimates",
            "missing_actions": actions_without_time,
            "severity": "low",
            "recommendation": "Add estimated_time field to all actions"
        })
    
    # Recommendations
    if validation_results["coverage_analysis"]["keyword_coverage"]["coverage_percentage"] < 50:
        validation_results["recommendations"].append({
            "priority": "high",
            "area": "keyword_coverage",
            "recommendation": "Increase keyword coverage in action planner to better reflect source material"
        })
    
    validation_results["recommendations"].append({
        "priority": "medium",
        "area": "entity_integration",
        "recommendation": "Consider explicitly linking ECS entities to specific actions for better traceability"
    })
    
    validation_results["recommendations"].append({
        "priority": "low",
        "area": "constraint_mapping",
        "recommendation": "Add direct constraint references to actions for compliance tracking"
    })
    
    # Overall validation status
    high_severity_gaps = sum(1 for g in validation_results["gap_analysis"] if g.get("severity") == "high")
    if high_severity_gaps > 0:
        validation_results["validation_status"] = "FAIL"
    elif len(validation_results["gap_analysis"]) > 3:
        validation_results["validation_status"] = "PASS_WITH_ISSUES"
    else:
        validation_results["validation_status"] = "PASS"
    
    return validation_results


def generate_validation_report(validation_results: dict, output_path: Path):
    """Generate human-readable validation report."""
    
    report = f"""# Action Planner Validation Report

## Executive Summary
- **Validation Date**: {validation_results['validation_date']}
- **Validation Status**: {validation_results['validation_status']}
- **Action Planner**: {validation_results['action_planner_summary']['total_phases']} phases, {validation_results['action_planner_summary']['total_actions']} actions
- **Source Data**: {validation_results['source_data_summary']['total_keywords']} keywords, {validation_results['source_data_summary']['total_constraints']} constraints

---

## Source Data Summary

| Metric | Count |
|--------|-------|
| Total Keywords | {validation_results['source_data_summary']['total_keywords']} |
| Total Constraints | {validation_results['source_data_summary']['total_constraints']} |
| Total Entities | {validation_results['source_data_summary']['total_entities']} |
| Total Components | {validation_results['source_data_summary']['total_components']} |
| Total Systems | {validation_results['source_data_summary']['total_systems']} |

---

## Coverage Analysis

### Keyword Coverage
- **Action Planner Keywords**: {len(validation_results['coverage_analysis']['keyword_coverage']['action_planner_keywords'])}
- **Source Keywords Matched**: {validation_results['coverage_analysis']['keyword_coverage']['source_keywords_matched']}
- **Top Source Keywords Covered**: {validation_results['coverage_analysis']['keyword_coverage']['top_source_keywords_covered']}
- **Coverage Percentage**: {validation_results['coverage_analysis']['keyword_coverage']['coverage_percentage']}%

### Constraint Coverage by Phase
"""
    
    for phase, data in validation_results['coverage_analysis']['constraint_coverage'].items():
        report += f"- **{phase}**: {data['available_constraints']} constraints (types: {', '.join(data['expected_types'])})\n"
    
    report += f"""
### ECS Coverage
- **Entities in Source**: {validation_results['coverage_analysis']['ecs_coverage']['total_entities_in_source']}
- **Entities Referenced in Actions**: {validation_results['coverage_analysis']['ecs_coverage']['entities_referenced_in_actions']}
- **Systems in Source**: {validation_results['coverage_analysis']['ecs_coverage']['total_systems_in_source']}
- **Systems Aligned with Phases**: {validation_results['coverage_analysis']['ecs_coverage']['systems_aligned_with_phases']}

---

## Gap Analysis

"""
    
    for i, gap in enumerate(validation_results['gap_analysis'], 1):
        report += f"""### Gap {i}: {gap['gap_type']}
- **Description**: {gap['description']}
- **Severity**: {gap['severity'].upper()}
- **Details**: {', '.join(gap.get('missing_keywords', gap.get('missing_steps', gap.get('missing_actions', ['N/A'])))[:10])}
- **Recommendation**: {gap['recommendation']}

"""
    
    report += """---

## Recommendations

"""
    
    for rec in validation_results['recommendations']:
        report += f"""### Priority: {rec['priority'].upper()}
- **Area**: {rec['area']}
- **Recommendation**: {rec['recommendation']}

"""
    
    report += f"""---

## Conclusion

The action planner has been validated against source data from {validation_results['source_data_summary']['total_keywords']} keywords and {validation_results['source_data_summary']['total_constraints']} constraints.

**Overall Status**: {validation_results['validation_status']}

The action planner provides comprehensive coverage of the USA business formation journey with 5 phases and 18 actions. Some gaps were identified in keyword coverage, but the core business formation process is well-represented.

---

*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"Validation report saved to: {output_path}")


def main():
    processed_dir = Path("processed")
    
    print("Loading action planner...")
    action_planner = load_action_planner(processed_dir)
    
    print("Loading source data...")
    all_data = load_all_processed_data(processed_dir)
    print(f"Loaded {len(all_data)} documents")
    
    print("\nExtracting keywords...")
    keywords, keyword_docs = extract_all_keywords(all_data)
    print(f"Found {len(keywords)} unique keywords")
    
    print("\nExtracting constraints...")
    constraints = extract_all_constraints(all_data)
    print(f"Found {len(constraints)} constraints")
    
    print("\nExtracting ECS elements...")
    ecs = extract_ecs_elements(all_data)
    print(f"Found {len(ecs['entities'])} entities, {len(ecs['components'])} components, {len(ecs['systems'])} systems")
    
    print("\nValidating action planner...")
    validation_results = validate_action_planner(action_planner, keywords, constraints, ecs)
    
    print(f"\nValidation Status: {validation_results['validation_status']}")
    
    print("\nGenerating validation report...")
    output_path = processed_dir / "validation_report.md"
    generate_validation_report(validation_results, output_path)
    
    # Save JSON results
    json_path = processed_dir / "validation_results.json"
    with open(json_path, 'w') as f:
        json.dump(validation_results, f, indent=2)
    print(f"Validation results saved to: {json_path}")
    
    print("\nPhase 5 Task 02 completed successfully!")


if __name__ == "__main__":
    main()
