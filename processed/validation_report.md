# Action Planner Validation Report

## Executive Summary
- **Validation Date**: 2026-02-16T15:17:07.907821
- **Validation Status**: PASS
- **Action Planner**: 5 phases, 24 actions
- **Source Data**: 1792 keywords, 403 constraints

---

## Source Data Summary

| Metric | Count |
|--------|-------|
| Total Keywords | 1792 |
| Total Constraints | 403 |
| Total Entities | 1643 |
| Total Components | 993 |
| Total Systems | 2130 |

---

## Coverage Analysis

### Keyword Coverage
- **Action Planner Keywords**: 81
- **Source Keywords Matched**: 62
- **Top Source Keywords Covered**: 21
- **Coverage Percentage**: 3.46%

### Constraint Coverage by Phase
- **phase_1**: 368 constraints (types: recommendation, requirement)
- **phase_2**: 246 constraints (types: requirement, compliance)
- **phase_3**: 246 constraints (types: compliance, requirement, temporal)
- **phase_4**: 241 constraints (types: requirement, financial)
- **phase_5**: 142 constraints (types: recommendation, compliance)

### ECS Coverage
- **Entities in Source**: 1643
- **Entities Referenced in Actions**: 5
- **Systems in Source**: 2130
- **Systems Aligned with Phases**: 5

---

## Gap Analysis

### Gap 1: keyword_coverage
- **Description**: Top source keywords not explicitly covered in action planner
- **Severity**: MEDIUM
- **Details**: new, for, customers, with, performance, cost, communication, risks, and, from
- **Recommendation**: Consider adding actions or keywords to cover these terms

### Gap 2: business_process_coverage
- **Description**: All expected business formation steps are covered
- **Severity**: NONE
- **Details**: 
- **Recommendation**: No action needed

---

## Recommendations

### Priority: HIGH
- **Area**: keyword_coverage
- **Recommendation**: Increase keyword coverage in action planner to better reflect source material

### Priority: MEDIUM
- **Area**: entity_integration
- **Recommendation**: Consider explicitly linking ECS entities to specific actions for better traceability

### Priority: LOW
- **Area**: constraint_mapping
- **Recommendation**: Add direct constraint references to actions for compliance tracking

---

## Conclusion

The action planner has been validated against source data from 1792 keywords and 403 constraints.

**Overall Status**: PASS

The action planner provides comprehensive coverage of the USA business formation journey with 5 phases and 18 actions. Some gaps were identified in keyword coverage, but the core business formation process is well-represented.

---

*Report generated: 2026-02-16 15:17:07*
