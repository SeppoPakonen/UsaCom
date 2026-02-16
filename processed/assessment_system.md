# USA Business Journey - Assessment and Feedback System

## Overview

This document describes the comprehensive assessment and feedback system designed for the USA Business Journey simulation game. The system tracks player progress, provides contextual feedback, celebrates milestones, and offers corrective guidance when needed.

**Version:** 1.0
**Created:** 2026-02-16

---

## Table of Contents

1. [Progress Tracking Metrics](#1-progress-tracking-metrics)
2. [Feedback Message Templates](#2-feedback-message-templates)
3. [Milestone Celebrations](#3-milestone-celebrations)
4. [Corrective Guidance System](#4-corrective-guidance-system)
5. [Assessment Reports](#5-assessment-reports)

---

## 1. Progress Tracking Metrics

### 1.1 Completion Metrics

#### Overall Journey Progress
- **Type:** Percentage (0-100%)
- **Calculation:** (completed_actions / total_actions) × 100
- **Phase Weights:**
  - Phase 1 (Planning): 15%
  - Phase 2 (Legal): 20%
  - Phase 3 (Compliance): 25%
  - Phase 4 (Operations): 20%
  - Phase 5 (Growth): 20%

#### Progress Thresholds
| Status | Range | Description |
|--------|-------|-------------|
| Just Starting | 0-10% | Beginning the journey |
| Getting Started | 11-30% | Initial momentum building |
| Making Progress | 31-60% | Solid advancement |
| Nearing Completion | 61-90% | Final stretch |
| Journey Complete | 91-100% | Mission accomplished |

### 1.2 Resource Metrics

#### Capital Health
| Level | Range | Alert |
|-------|-------|-------|
| Critical | 0-20% | Immediate action required |
| Warning | 21-50% | Consider fundraising |
| Stable | 51-80% | Monitor closely |
| Healthy | 81-100% | Good position |
| Thriving | 100%+ | Consider expansion |

#### Knowledge Level
| Level | Score | Description |
|-------|-------|-------------|
| Novice | 0-25 | Learning basics |
| Learning | 26-50 | Building understanding |
| Knowledgeable | 51-75 | Solid grasp |
| Expert | 76-100 | Mastery level |

### 1.3 Compliance Metrics

#### Compliance Score
| Status | Range | Consequence |
|--------|-------|-------------|
| Non-Compliant | 0-50% | Penalties and legal risks |
| At Risk | 51-70% | Warning notices |
| Compliant | 71-90% | Good standing |
| Exemplary | 91-100% | Model business |

---

## 2. Feedback Message Templates

### 2.1 Progress Feedback

#### Phase Entry Messages
Each phase has a customized welcome message that:
- Acknowledges the achievement of reaching the phase
- Sets expectations for what's ahead
- Provides encouragement

#### Action Completion Messages
Messages vary based on action difficulty:
- **Easy:** Quick positive reinforcement
- **Medium:** Acknowledgment of significant progress
- **Hard:** Celebration of overcoming challenges

### 2.2 Resource Feedback

#### Capital Alerts
Three-tier warning system:
1. **Below 50%:** Advisory - review budget
2. **Below 30%:** Urgent - take action
3. **Below 20%:** Critical - immediate action required

#### Time Warnings
- **Behind Schedule:** Advisory to refocus
- **Deadline Approaching:** Urgent notification with days remaining

### 2.3 Decision Feedback

#### Entity Selection
Contextual information provided after entity selection explaining:
- Why the choice makes sense for their scenario
- Key considerations to remember
- Potential future implications

---

## 3. Milestone Celebrations

### 3.1 Achievement Badges

| Badge | Icon | Trigger | Reward |
|-------|------|---------|--------|
| First Steps | 👣 | Complete first action | +5 Knowledge, +10 Confidence |
| Business Planner | 📋 | Complete Phase 1 | +15 Knowledge, +5 Network |
| Legally Born | ⚖️ | Complete Phase 2 | +10 Reputation |
| Compliance Champion | 🏆 | Complete Phase 3 | +10 Compliance Bonus |
| Operations Ready | 🚀 | Complete Phase 4 | +15 Efficiency Bonus |
| Journey Complete | 🌟 | Complete Phase 5 | +25 Reputation, Title |

### 3.2 Special Milestones

- **First Customer** (🎉): Validates business concept
- **Revenue Milestone** (💵): Business model working
- **Team Builder** (👥): First employee hired
- **Funding Secured** (💰): External validation
- **Compliance Perfection** (✨): 6 months perfect compliance
- **Speed Demon** (⚡): Complete journey under 6 months

---

## 4. Corrective Guidance System

### 4.1 Struggle Detection

The system monitors for:
- **Repeated Failures:** Same action failed 3+ times
- **Time Stuck:** No progress for 2 weeks
- **Resource Depletion:** Capital below 30%
- **Compliance Decline:** Score below 60%
- **Avoidance Behavior:** Skipping difficult actions

### 4.2 Intervention Types

| Intervention | Trigger | Approach |
|--------------|---------|----------|
| Skill Building | Repeated failures | Offer tutorials and guides |
| Motivation | Time stuck | Break down tasks, explain importance |
| Crisis Management | Resource depletion | Immediate action options |
| Risk Mitigation | Compliance decline | Prioritize critical items |
| Reframing | Avoidance | Address psychological barriers |

### 4.3 Hint System Levels

1. **Gentle Nudge:** Subtle suggestion
2. **Helpful Tip:** Specific guidance
3. **Direct Help:** Step-by-step instructions
4. **Expert Intervention:** Professional assistance offer

### 4.4 Recovery Paths

Pre-defined recovery plans for critical situations:
- **Capital Crisis:** Spending freeze, revenue acceleration
- **Compliance Crisis:** Emergency filings, professional consultation
- **Timeline Slippage:** Reprioritization, scope adjustment

---

## 5. Assessment Reports

### 5.1 Weekly Check-In

**Frequency:** Every 7 days

**Sections:**
- Progress Summary (actions completed, overall %)
- Resource Health (capital, burn rate, runway)
- Compliance Status (score, deadlines, upcoming filings)
- This Week's Focus (recommended priorities)

### 5.2 Phase Completion Report

**Frequency:** End of each phase

**Sections:**
- Phase Summary
- Achievements Earned
- Lessons Learned
- Next Phase Preview
- Readiness Assessment

### 5.3 Journey Completion Report

**Frequency:** End of simulation

**Sections:**
- Complete Journey Summary
- Final Metrics
- All Achievements
- Business Health Score
- Next Steps Recommendations

---

## Implementation Guidelines

### Integration Points

1. **Action Completion Hook:** Trigger feedback and progress updates
2. **Resource Change Hook:** Monitor and alert on resource thresholds
3. **Time Tick Hook:** Weekly check-ins, deadline monitoring
4. **Phase Transition Hook:** Phase entry/exit celebrations
5. **Milestone Check Hook:** Evaluate achievement triggers

### Data Requirements

- Player state (progress, resources, compliance)
- Action history (completed, failed, in-progress)
- Timeline tracking (start date, current week)
- Scenario benchmarks (for comparison)

### Customization Options

- Message tone (formal, casual, motivational)
- Alert thresholds (adjustable per scenario difficulty)
- Celebration frequency (to avoid notification fatigue)
- Hint system aggressiveness (player preference)

---

## Conclusion

This assessment and feedback system provides comprehensive support for players throughout their entrepreneurial journey simulation. By combining quantitative metrics with qualitative guidance, the system helps players learn from their decisions, recover from setbacks, and celebrate their achievements.

The modular design allows for easy customization based on scenario type, difficulty level, and player preferences, making it adaptable for a wide range of simulation experiences.
