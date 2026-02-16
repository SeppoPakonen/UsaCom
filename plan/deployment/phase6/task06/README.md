# Task 06: Create Game Scenario Runner

**Status:** COMPLETE
**Completion Date:** 2026-02-16

## Overview
Implement the scenario runner module that integrates all 12 business scenarios, manages scenario-specific conditions, and handles win/loss evaluation.

## Deliverables

### Source Files
- `src/scenario_runner.py` - Main scenario runner module

### Output Files
- `processed/scenario_tests.json` - Test results

## Features Implemented

### Scenario Integration
- Loads all 12 scenarios from `processed/sample_scenarios.json`
- Provides scenario list with metadata (name, category, difficulty, capital)
- Detailed scenario information retrieval

### Starting Conditions
- Dynamic starting conditions based on scenario funding profiles
- Difficulty modifiers (easy: 1.5x, normal: 1.0x, hard: 0.7x, expert: 0.5x capital)
- Team size and burn rate initialization
- Critical actions identification per scenario

### Win/Loss Conditions
**Win Conditions:**
- All primary objectives completed
- 80%+ objectives completed by Phase 5

**Loss Conditions:**
- Bankruptcy (capital <= 0)
- Compliance failure (score < 30)
- Runway exhaustion
- Time exceeded (104 weeks) without traction

### Objective System
- Revenue targets
- Customer acquisition goals
- Funding milestones
- Team building objectives
- Launch timeline
- Compliance score requirements

### Progress Tracking
- Real-time objective progress updates
- Milestone achievement recording
- Critical action completion tracking
- Resource modification tracking

## Test Results
```
Tests Run: 14
Tests Passed: 14
Tests Failed: 0
Pass Rate: 100.0%
```

## Usage Example
```python
from scenario_runner import ScenarioRunner

runner = ScenarioRunner()

# Get scenario list
scenarios = runner.get_scenario_list()

# Start a scenario
state = runner.start_scenario("SCN002", "PlayerName", "normal")

# Update objective progress
runner.update_objective_progress("obj_001", 50000)

# Check win/loss
win, reason = runner.check_win_condition()
loss, reason = runner.check_loss_condition()

# End scenario
result = runner.end_scenario("win", "All objectives completed!")
```

## Integration Points
- Integrates with `sample_scenarios.json` for scenario data
- Works with `game_engine.py` for resource tracking
- Provides scenario context to `analytics_system.py`

## Notes
- All 12 scenarios fully supported
- Difficulty scaling affects starting resources
- Scenario history maintained for statistics
