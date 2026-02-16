# USA Business Journey - Simulation Game Mechanics Specification

## Overview
- **Title**: USA Business Journey - Simulation Game Mechanics
- **Version**: 1.0
- **Created**: 2026-02-16T18:05:48.535615
- **Description**: Detailed game mechanics for the USA business formation simulation game

---

## 1. Core Game Loop

The fundamental cycle of gameplay

**1. Select Action**: Player chooses an action from available options in current region

**2. Check Requirements**: Verify player has required resources and prerequisites

**3. Execute Action**: Player completes the action, spending resources and time

**4. Resolve Outcomes**: Apply effects, gain rewards, trigger events

**5. Update State**: Update progress, resources, and unlock new actions

---

## 2. Resource System

Resources that players manage throughout the game

### Resources

### 💰 Capital
- **Description**: Financial resources for business formation
- **Starting Amount**: {'min': 5000, 'max': 50000, 'default': 15000}
- **Max Capacity**: 1000000
- **Acquisition**: Personal savings (starting amount), Business loan (unlocks in Phase 2), Investor funding (unlocks in Phase 4)...
- **Spending**: Filing fees ($50-500 per action), Legal services ($500-5000), Insurance premiums ($100-1000/month)...
- **Depletion Penalty**: Game over if capital reaches $0 for 3 consecutive turns

### ⏰ Time
- **Description**: Available time for completing actions
- **Starting Amount**: 52
- **Max Capacity**: 104
- **Acquisition**: Weekly time allocation (1 week per turn), Hiring help (converts Capital to Time efficiency), Automation tools (reduces action time requirements)...
- **Spending**: Action completion (varies by action), Learning and research (optional), Networking (optional)...
- **Depletion Penalty**: Opportunity cost - competitors gain advantage

### 📚 Knowledge
- **Description**: Understanding of business formation requirements
- **Starting Amount**: 10
- **Max Capacity**: 100
- **Acquisition**: Research actions (+5-10 per action), Consulting experts (+10-20, costs Capital), Completing actions successfully (+2-5)...
- **Spending**: Unlock advanced actions (requires Knowledge threshold), Reduce action failure chance, Identify optimal paths...
- **Depletion Penalty**: None - Knowledge only grows

### 🤝 Network
- **Description**: Professional connections and relationships
- **Starting Amount**: 5
- **Max Capacity**: 100
- **Acquisition**: Networking events (+5-10), Mentor relationships (+10-20), Industry associations (+5-15)...
- **Spending**: Access to investors (requires Network threshold), Finding co-founders or partners, Getting referrals and recommendations...
- **Depletion Penalty**: Limited access to opportunities

### ⭐ Reputation
- **Description**: Business credibility and trustworthiness
- **Starting Amount**: 0
- **Max Capacity**: 100
- **Acquisition**: Completing compliance actions (+5-10), Successful business milestones (+10-20), Positive customer interactions (+5-15)...
- **Spending**: Attract investors (requires Reputation threshold), Secure partnerships, Premium pricing power...
- **Depletion Penalty**: Reduced opportunities, higher scrutiny

---

## 3. Progression System

How players advance through the game

**Type**: phase_gated_with_requirements

### Phase Requirements

| Phase | Name | Entry Requirements | Completion Requirements | Unlocks |
|-------|------|-------------------|------------------------|---------|
| 1 | Planning Peaks | {'capital': 5000, 'knowledge': 0} | ['action_1_1', 'action_1_2']... | Phase 2: Legal Labyrinth |
| 2 | Legal Labyrinth | {'capital': 3000, 'knowledge': 25} | ['action_2_1', 'action_2_2']... | Phase 3: Compliance Canyon |
| 3 | Compliance Canyon | {'capital': 2000, 'knowledge': 40} | ['action_3_1', 'action_3_2']... | Phase 4: Operations Ocean |
| 4 | Operations Ocean | {'capital': 5000, 'reputation': 10} | ['action_4_1', 'action_4_2']... | Phase 5: Growth Galaxy |
| 5 | Growth Galaxy | {'capital': 10000, 'reputation': 25} | ['action_5_1', 'action_5_2']... | Endgame: Sustainable Business |

---

## 4. Challenge System

Obstacles and difficulties players must overcome

### Environmental Challenges
Challenges from the business environment

- **Fog of Uncertainty**: Reduces visibility of optimal action paths
  - Mitigation: Research actions clear fog temporarily
  - Severity: low

- **Regulation Rapids**: Fast-changing rules require constant attention
  - Mitigation: Compliance system reduces impact
  - Severity: medium

### Enemy Challenges
Active threats that attack the player

- **Deadline Dragons**: Attack if filing deadlines are missed
  - Mitigation: Calendar reminders, automated filing
  - Severity: high

- **Liability Leviathan**: Emerges without proper insurance
  - Mitigation: Appropriate insurance coverage
  - Severity: critical

### Resource Challenges
Challenges requiring resource expenditure

- **Fee Toll Bridges**: Require payment to cross
  - Mitigation: Budget planning, fee waivers for qualifying businesses
  - Severity: low

- **Paperwork Golems**: Slow progress with documentation requirements
  - Mitigation: Templates, professional services, automation
  - Severity: medium

---

## 5. Reward System

Rewards and achievements for player accomplishments

### Milestone Rewards
Rewards for completing major milestones

- **First Phase Complete**: {'capital': 1000, 'knowledge': 10, 'achievement': 'Planner'}
- **Business Registered**: {'capital': 500, 'reputation': 5, 'achievement': 'Founder'}
- **All Compliance Met**: {'knowledge': 20, 'reputation': 15, 'achievement': 'Compliant'}

### Achievement Rewards
Special accomplishments with badges

- **Bootstrapper**: Complete game without external funding
- **Speed Runner**: Complete game in under 26 weeks
- **Perfectionist**: Complete all actions with 100% compliance

### Unlock Rewards
New options and capabilities

- **Investor Meetings**: Reach Phase 4 with Reputation 30+
- **Media Coverage**: Reach Reputation 50+
- **Acquisition Offers**: Reach revenue milestone

---

## 6. Scoring System

How player performance is evaluated

### Score Categories

| Category | Weight | Metrics |
|----------|--------|---------|
| Financial Performance | 30% | Final Capital, Revenue Generated... |
| Speed | 20% | Time to Complete, Actions per Week... |
| Compliance | 25% | Compliance Score, Deadlines Met... |
| Growth | 15% | Network Size, Reputation... |
| Achievements | 10% | Achievements Unlocked... |

### Grade Scale

| Grade | Min Score | Title |
|-------|-----------|-------|
| S | 90+ | Visionary Entrepreneur |
| A | 80+ | Successful Founder |
| B | 70+ | Solid Business Owner |
| C | 60+ | Struggling Entrepreneur |
| D | 50+ | At-Risk Business |
| F | 0+ | Business Failure |

---

## 7. Decision System

Meaningful choices players must make

### Business Structure
**Location**: loc_2_1
**Question**: What business structure will you choose?

- **LLC**: {'capital': -200, 'time': -2}
  - Pass-through taxation, flexible management, moderate liability protection

- **C-Corporation**: {'capital': -500, 'time': -4}
  - Double taxation, investor-friendly, unlimited shareholders

- **S-Corporation**: {'capital': -400, 'time': -4}
  - Pass-through taxation, limited to 100 shareholders

### Funding Strategy
**Location**: loc_1_4
**Question**: How will you fund your business?

- **Bootstrapping**: Full ownership, slower growth, no debt
  - N/A

- **Bank Loan**: Debt obligation, retain ownership, interest payments
  - N/A

- **Angel Investor**: Equity dilution (10-25%), mentorship, faster growth
  - N/A

### Market Entry
**Location**: loc_5_1
**Question**: What is your market entry strategy?

- **MVP Launch**: {'time': -4, 'capital': -2000}
  - Fast feedback, iterate based on customer input

- **Soft Launch**: {'time': -8, 'capital': -5000}
  - Limited market testing, refine before full launch

- **Big Bang Launch**: {'time': -12, 'capital': -20000}
  - Maximum impact, high risk if not ready

---

## 8. Endgame System

How the game concludes

### Ending Types

#### Sustainable Success
- **Conditions**: {'all_phases_complete': True, 'capital': {'min': 50000}, 'reputation': {'min': 50}, 'compliance_score': {'min': 90}}
- **Narrative**: Your business is thriving with strong fundamentals and growth trajectory.

#### Acquisition Target
- **Conditions**: {'all_phases_complete': True, 'revenue': {'min': 500000}, 'reputation': {'min': 60}}
- **Narrative**: Your successful business attracts acquisition offers from larger companies.

#### Lifestyle Business
- **Conditions**: {'phases_complete': {'min': 4}, 'capital': {'min': 30000}, 'work_life_balance': {'min': 70}}
- **Narrative**: You've built a comfortable business that supports your desired lifestyle.

#### Pivot Success
- **Conditions**: {'phases_complete': {'min': 3}, 'pivots': {'min': 1}, 'final_revenue': {'min': 100000}}
- **Narrative**: Your willingness to pivot led to unexpected success in a new direction.

#### Gradual Decline
- **Conditions**: {'capital': {'max': 5000}, 'reputation': {'max': 20}, 'turns_without_revenue': {'min': 10}}
- **Narrative**: Despite your efforts, the business struggles to gain traction.

#### Bankruptcy
- **Conditions**: {'capital': {'max': 0}, 'debt': {'min': 10000}}
- **Narrative**: The business has failed due to insolvency. Time to learn and try again.

---

## Implementation Notes for Phase 6

1. **Resource Management**: Implement resource tracking with visual indicators
2. **Phase Gating**: Enforce progression requirements before unlocking new areas
3. **Challenge Timing**: Scale challenge frequency based on difficulty setting
4. **Save System**: Allow players to save progress at any point
5. **Tutorial**: Include guided tutorial for first-time players
6. **Accessibility**: Ensure UI is accessible to all players

---

*Specification generated: 2026-02-16 18:05:48*
