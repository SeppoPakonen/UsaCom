#!/usr/bin/env python3
"""
USA Business Journey - Scenario Runner
Integrates sample scenarios, manages scenario-specific conditions,
implements win/loss conditions, and tracks scenario progress.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class ScenarioStatus(Enum):
    """Status of a scenario run."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    WON = "won"
    LOST = "lost"


class WinConditionType(Enum):
    """Types of win conditions."""
    REVENUE_TARGET = "revenue_target"
    CUSTOMER_TARGET = "customer_target"
    FUNDING_MILESTONE = "funding_milestone"
    TEAM_MILESTONE = "team_milestone"
    COMPLETION_TARGET = "completion_target"
    TIME_TARGET = "time_target"
    COMBINED = "combined"


class LossConditionType(Enum):
    """Types of loss conditions."""
    BANKRUPTCY = "bankruptcy"
    COMPLIANCE_FAILURE = "compliance_failure"
    TIME_EXCEEDED = "time_exceeded"
    RUNWAY_EXHAUSTED = "runway_exhausted"


@dataclass
class ScenarioObjective:
    """Represents a scenario objective."""
    objective_id: str
    name: str
    description: str
    condition_type: str
    target_value: float
    current_value: float
    unit: str
    completed: bool = False
    is_primary: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ScenarioState:
    """Represents the state of a scenario run."""
    scenario_id: str
    scenario_name: str
    player_name: str
    status: ScenarioStatus
    start_time: str
    last_update: str
    current_turn: int
    current_phase: int
    objectives: List[ScenarioObjective]
    starting_conditions: Dict[str, Any]
    current_resources: Dict[str, float]
    milestones_achieved: List[str]
    critical_actions_completed: List[str]
    compliance_score: float
    risk_events_triggered: int
    difficulty: str

    def to_dict(self) -> Dict:
        return {
            "scenario_id": self.scenario_id,
            "scenario_name": self.scenario_name,
            "player_name": self.player_name,
            "status": self.status.value,
            "start_time": self.start_time,
            "last_update": self.last_update,
            "current_turn": self.current_turn,
            "current_phase": self.current_phase,
            "objectives": [o.to_dict() for o in self.objectives],
            "starting_conditions": self.starting_conditions,
            "current_resources": self.current_resources,
            "milestones_achieved": self.milestones_achieved,
            "critical_actions_completed": self.critical_actions_completed,
            "compliance_score": self.compliance_score,
            "risk_events_triggered": self.risk_events_triggered,
            "difficulty": self.difficulty
        }


@dataclass
class ScenarioResult:
    """Represents the result of a completed scenario."""
    scenario_id: str
    player_name: str
    outcome: str  # "win" or "loss"
    reason: str
    turns_taken: int
    final_score: float
    objectives_completed: int
    total_objectives: int
    milestones_achieved: List[str]
    completion_time: str
    statistics: Dict[str, Any]

    def to_dict(self) -> Dict:
        return asdict(self)


class ScenarioRunner:
    """
    Scenario runner for the USA Business Journey simulation.
    Manages scenario execution, win/loss conditions, and progress tracking.
    """

    def __init__(self, scenarios_path: str = None):
        """Initialize the scenario runner."""
        self.base_path = Path(__file__).parent.parent / "processed"

        # Load scenarios
        scenarios_file = scenarios_path or self.base_path / "sample_scenarios.json"
        with open(scenarios_file, 'r') as f:
            self.scenarios_data = json.load(f)

        # Index scenarios by ID
        self.scenarios: Dict[str, Dict] = {}
        for scenario in self.scenarios_data.get("scenarios", []):
            self.scenarios[scenario["scenario_id"]] = scenario

        # Current scenario state
        self.current_state: Optional[ScenarioState] = None
        self.scenario_history: List[ScenarioResult] = []

    def get_scenario_list(self) -> List[Dict]:
        """Get list of all available scenarios."""
        scenario_list = []
        for scenario in self.scenarios.values():
            scenario_list.append({
                "scenario_id": scenario["scenario_id"],
                "name": scenario["name"],
                "category": scenario["category"],
                "description": scenario["description"],
                "difficulty_level": scenario.get("difficulty_level", "Medium"),
                "initial_capital": scenario.get("funding_profile", {}).get("initial_capital", 0),
                "time_to_launch": scenario.get("success_metrics", {}).get("time_to_launch", "N/A")
            })
        return scenario_list

    def get_scenario_details(self, scenario_id: str) -> Optional[Dict]:
        """Get detailed information about a specific scenario."""
        scenario = self.scenarios.get(scenario_id)
        if not scenario:
            return None

        return {
            "scenario_id": scenario["scenario_id"],
            "name": scenario["name"],
            "category": scenario["category"],
            "description": scenario["description"],
            "business_concept": scenario.get("business_concept", {}),
            "funding_profile": scenario.get("funding_profile", {}),
            "team_profile": scenario.get("team_profile", {}),
            "market_profile": scenario.get("market_profile", {}),
            "journey_path_mapping": scenario.get("journey_path_mapping", {}),
            "success_metrics": scenario.get("success_metrics", {}),
            "risk_factors": scenario.get("risk_factors", []),
            "difficulty_level": scenario.get("difficulty_level", "Medium")
        }

    def start_scenario(self, scenario_id: str, player_name: str,
                       difficulty: str = "normal") -> ScenarioState:
        """
        Start a new scenario run.

        Args:
            scenario_id: ID of the scenario to start
            player_name: Name of the player
            difficulty: Difficulty level

        Returns:
            Initial scenario state
        """
        scenario = self.scenarios.get(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")

        # Create starting conditions from scenario
        starting_conditions = self._create_starting_conditions(scenario, difficulty)

        # Create objectives from success metrics
        objectives = self._create_objectives(scenario)

        now = datetime.now().isoformat()

        self.current_state = ScenarioState(
            scenario_id=scenario_id,
            scenario_name=scenario["name"],
            player_name=player_name,
            status=ScenarioStatus.IN_PROGRESS,
            start_time=now,
            last_update=now,
            current_turn=0,
            current_phase=1,
            objectives=objectives,
            starting_conditions=starting_conditions,
            current_resources=starting_conditions["resources"].copy(),
            milestones_achieved=[],
            critical_actions_completed=[],
            compliance_score=100.0,
            risk_events_triggered=0,
            difficulty=difficulty
        )

        return self.current_state

    def _create_starting_conditions(self, scenario: Dict,
                                    difficulty: str) -> Dict[str, Any]:
        """Create starting conditions based on scenario and difficulty."""
        funding = scenario.get("funding_profile", {})
        team = scenario.get("team_profile", {})

        # Apply difficulty modifiers
        difficulty_modifiers = {
            "easy": {"capital": 1.5, "time": 1.2, "knowledge": 1.3},
            "normal": {"capital": 1.0, "time": 1.0, "knowledge": 1.0},
            "hard": {"capital": 0.7, "time": 0.8, "knowledge": 0.8},
            "expert": {"capital": 0.5, "time": 0.6, "knowledge": 0.6}
        }

        mods = difficulty_modifiers.get(difficulty, difficulty_modifiers["normal"])

        initial_capital = funding.get("initial_capital", 15000) * mods["capital"]

        return {
            "resources": {
                "capital": initial_capital,
                "time": 52 * mods["time"],  # Weeks in a year
                "knowledge": 20 * mods["knowledge"],
                "network": 10,
                "reputation": 5
            },
            "team_size": team.get("employees_initial", 0),
            "founders": team.get("founders", 1),
            "burn_rate": funding.get("burn_rate_monthly", 0),
            "runway_months": funding.get("runway_months", 6),
            "recommended_entity": scenario.get("journey_path_mapping", {}).get("recommended_entity", "LLC"),
            "critical_actions": scenario.get("journey_path_mapping", {}).get("critical_actions", []),
            "accelerated_path": scenario.get("journey_path_mapping", {}).get("accelerated_path", False)
        }

    def _create_objectives(self, scenario: Dict) -> List[ScenarioObjective]:
        """Create objectives from scenario success metrics."""
        objectives = []
        metrics = scenario.get("success_metrics", {})
        obj_id = 0

        # Revenue target
        if "revenue_target_year_1" in metrics:
            obj_id += 1
            revenue_str = metrics["revenue_target_year_1"]
            revenue_value = float(revenue_str.replace("$", "").replace(",", ""))
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Revenue Target",
                description=f"Achieve ${revenue_value:,.0f} in annual revenue",
                condition_type=WinConditionType.REVENUE_TARGET.value,
                target_value=revenue_value,
                current_value=0,
                unit="USD",
                is_primary=True
            ))

        # Customer acquisition target
        if "customer_acquisition_target" in metrics:
            obj_id += 1
            cust_str = metrics["customer_acquisition_target"]
            # Parse "100 paying customers by month 12"
            cust_value = float(cust_str.split()[0])
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Customer Acquisition",
                description=f"Acquire {cust_value:.0f} customers",
                condition_type=WinConditionType.CUSTOMER_TARGET.value,
                target_value=cust_value,
                current_value=0,
                unit="customers",
                is_primary=True
            ))

        # Funding milestone
        if "funding_milestone" in metrics and "N/A" not in metrics["funding_milestone"]:
            obj_id += 1
            funding_desc = metrics["funding_milestone"]
            # Extract amount if present
            funding_value = 0
            if "$" in funding_desc:
                funding_str = funding_desc.split("$")[1].split()[0].replace("K", "000").replace("M", "000000")
                funding_value = float(funding_str.replace(",", ""))
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Funding Milestone",
                description=funding_desc,
                condition_type=WinConditionType.FUNDING_MILESTONE.value,
                target_value=funding_value,
                current_value=0,
                unit="USD",
                is_primary=False
            ))

        # Team milestone
        if "team_milestone" in metrics:
            obj_id += 1
            team_desc = metrics["team_milestone"]
            # Parse employee count
            team_value = 0
            for word in team_desc.split():
                if word.isdigit():
                    team_value = int(word)
                    break
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Team Building",
                description=team_desc,
                condition_type=WinConditionType.TEAM_MILESTONE.value,
                target_value=team_value,
                current_value=0,
                unit="employees",
                is_primary=False
            ))

        # Time to launch
        if "time_to_launch" in metrics:
            obj_id += 1
            time_str = metrics["time_to_launch"]
            # Parse "6 months"
            time_value = float(time_str.split()[0])
            time_unit = time_str.split()[1].lower()
            if time_unit.startswith("month"):
                time_value *= 4  # Convert to weeks
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Launch Timeline",
                description=f"Launch within {time_str}",
                condition_type=WinConditionType.TIME_TARGET.value,
                target_value=time_value,
                current_value=0,
                unit="weeks",
                is_primary=True
            ))

        # Compliance score requirement
        if "compliance_score_required" in metrics:
            obj_id += 1
            comp_value = metrics["compliance_score_required"]
            objectives.append(ScenarioObjective(
                objective_id=f"obj_{obj_id:03d}",
                name="Compliance Excellence",
                description=f"Maintain {comp_value}% compliance score",
                condition_type="compliance_target",
                target_value=comp_value,
                current_value=100,
                unit="percent",
                is_primary=True
            ))

        return objectives

    def update_resource(self, resource_name: str, value: float) -> bool:
        """Update a resource value."""
        if not self.current_state:
            return False

        if resource_name in self.current_state.current_resources:
            self.current_state.current_resources[resource_name] = value
            self.current_state.last_update = datetime.now().isoformat()
            return True
        return False

    def modify_resource(self, resource_name: str, delta: float) -> bool:
        """Modify a resource by a delta value."""
        if not self.current_state:
            return False

        if resource_name in self.current_state.current_resources:
            self.current_state.current_resources[resource_name] += delta
            self.current_state.last_update = datetime.now().isoformat()
            return True
        return False

    def update_objective_progress(self, objective_id: str, current_value: float) -> bool:
        """Update progress on an objective."""
        if not self.current_state:
            return False

        for obj in self.current_state.objectives:
            if obj.objective_id == objective_id:
                obj.current_value = current_value
                obj.completed = current_value >= obj.target_value
                self.current_state.last_update = datetime.now().isoformat()
                return True
        return False

    def advance_turn(self) -> Dict:
        """
        Advance to the next turn and check conditions.

        Returns:
            Dict with turn results and any triggered events
        """
        if not self.current_state:
            return {"error": "No scenario in progress"}

        self.current_state.current_turn += 1
        self.current_state.last_update = datetime.now().isoformat()

        # Apply burn rate (monthly / 4 for weekly)
        burn_rate = self.current_state.starting_conditions.get("burn_rate", 0)
        if burn_rate > 0:
            weekly_burn = burn_rate / 4
            self.current_state.current_resources["capital"] -= weekly_burn

        # Check objectives
        self._check_objectives()

        # Check win/loss conditions
        win_result = self.check_win_condition()
        loss_result = self.check_loss_condition()

        return {
            "turn": self.current_state.current_turn,
            "resources": self.current_state.current_resources.copy(),
            "objectives_progress": self.get_objectives_progress(),
            "win_achieved": win_result[0] if win_result else False,
            "loss_triggered": loss_result[0] if loss_result else False,
            "win_reason": win_result[1] if win_result else None,
            "loss_reason": loss_result[1] if loss_result else None
        }

    def _check_objectives(self):
        """Check and update objective completion status."""
        if not self.current_state:
            return

        for obj in self.current_state.objectives:
            if not obj.completed:
                if obj.current_value >= obj.target_value:
                    obj.completed = True

    def check_win_condition(self) -> Tuple[bool, str]:
        """
        Check if win conditions are met.

        Returns:
            Tuple of (is_won, reason)
        """
        if not self.current_state:
            return False, ""

        # Check primary objectives
        primary_objectives = [o for o in self.current_state.objectives if o.is_primary]
        completed_primary = sum(1 for o in primary_objectives if o.completed)

        # Win if all primary objectives are complete
        if completed_primary == len(primary_objectives) and len(primary_objectives) > 0:
            self.current_state.status = ScenarioStatus.WON
            return True, "All primary objectives completed!"

        # Alternative: Check phase completion
        if self.current_state.current_phase >= 5:
            # Check if most objectives are complete
            total_obj = len(self.current_state.objectives)
            completed_obj = sum(1 for o in self.current_state.objectives if o.completed)
            if completed_obj >= total_obj * 0.8:
                self.current_state.status = ScenarioStatus.WON
                return True, f"Completed {completed_obj}/{total_obj} objectives and reached Phase 5!"

        return False, ""

    def check_loss_condition(self) -> Tuple[bool, str]:
        """
        Check if loss conditions are met.

        Returns:
            Tuple of (is_lost, reason)
        """
        if not self.current_state:
            return False, ""

        # Check bankruptcy
        if self.current_state.current_resources.get("capital", 0) <= 0:
            self.current_state.status = ScenarioStatus.LOST
            return True, "Bankruptcy - Capital depleted!"

        # Check compliance failure
        if self.current_state.compliance_score < 30:
            self.current_state.status = ScenarioStatus.LOST
            return True, "Compliance Failure - Too many violations!"

        # Check runway exhaustion
        starting = self.current_state.starting_conditions
        runway = starting.get("runway_months", 6)
        current_capital = self.current_state.current_resources.get("capital", 0)
        burn_rate = starting.get("burn_rate", 0)

        if burn_rate > 0:
            remaining_months = current_capital / burn_rate
            if remaining_months < 1 and self.current_state.current_turn > runway * 4:
                self.current_state.status = ScenarioStatus.LOST
                return True, "Runway Exhausted - No funds to continue operations!"

        # Check time exceeded (2 years max)
        if self.current_state.current_turn > 104:  # 104 weeks = 2 years
            # Check if meaningful progress was made
            completed = sum(1 for o in self.current_state.objectives if o.completed)
            if completed < len(self.current_state.objectives) * 0.5:
                self.current_state.status = ScenarioStatus.LOST
                return True, "Time Exceeded - Business failed to gain traction!"

        return False, ""

    def get_objectives_progress(self) -> Dict:
        """Get current objectives progress."""
        if not self.current_state:
            return {}

        total = len(self.current_state.objectives)
        completed = sum(1 for o in self.current_state.objectives if o.completed)

        objectives_detail = []
        for obj in self.current_state.objectives:
            pct = (obj.current_value / obj.target_value * 100) if obj.target_value > 0 else 0
            objectives_detail.append({
                "name": obj.name,
                "description": obj.description,
                "current": obj.current_value,
                "target": obj.target_value,
                "unit": obj.unit,
                "progress_pct": min(100, pct),
                "completed": obj.completed,
                "is_primary": obj.is_primary
            })

        return {
            "total_objectives": total,
            "completed_objectives": completed,
            "progress_pct": (completed / total * 100) if total > 0 else 0,
            "objectives": objectives_detail
        }

    def get_scenario_status(self) -> Dict:
        """Get current scenario status."""
        if not self.current_state:
            return {}
        return self.current_state.to_dict()

    def complete_critical_action(self, action_id: str) -> bool:
        """Mark a critical action as completed."""
        if not self.current_state:
            return False

        critical_actions = self.current_state.starting_conditions.get("critical_actions", [])
        if action_id in critical_actions:
            if action_id not in self.current_state.critical_actions_completed:
                self.current_state.critical_actions_completed.append(action_id)
                self.current_state.last_update = datetime.now().isoformat()
                return True
        return False

    def achieve_milestone(self, milestone_name: str) -> bool:
        """Record a milestone achievement."""
        if not self.current_state:
            return False

        if milestone_name not in self.current_state.milestones_achieved:
            self.current_state.milestones_achieved.append(milestone_name)
            self.current_state.last_update = datetime.now().isoformat()
            return True
        return False

    def modify_compliance(self, delta: float) -> float:
        """Modify compliance score."""
        if not self.current_state:
            return 0

        self.current_state.compliance_score = max(0, min(100,
            self.current_state.compliance_score + delta))
        return self.current_state.compliance_score

    def end_scenario(self, outcome: str, reason: str) -> ScenarioResult:
        """
        End the current scenario and create a result record.

        Args:
            outcome: "win" or "loss"
            reason: Reason for the outcome

        Returns:
            ScenarioResult with statistics
        """
        if not self.current_state:
            raise ValueError("No scenario in progress")

        # Calculate final score
        final_score = self._calculate_final_score()

        # Create result
        result = ScenarioResult(
            scenario_id=self.current_state.scenario_id,
            player_name=self.current_state.player_name,
            outcome=outcome,
            reason=reason,
            turns_taken=self.current_state.current_turn,
            final_score=final_score,
            objectives_completed=sum(1 for o in self.current_state.objectives if o.completed),
            total_objectives=len(self.current_state.objectives),
            milestones_achieved=self.current_state.milestones_achieved.copy(),
            completion_time=datetime.now().isoformat(),
            statistics={
                "final_resources": self.current_state.current_resources.copy(),
                "critical_actions_completed": len(self.current_state.critical_actions_completed),
                "total_critical_actions": len(self.current_state.starting_conditions.get("critical_actions", [])),
                "final_compliance": self.current_state.compliance_score,
                "risk_events": self.current_state.risk_events_triggered,
                "difficulty": self.current_state.difficulty
            }
        )

        self.scenario_history.append(result)
        self.current_state.status = ScenarioStatus.WON if outcome == "win" else ScenarioStatus.LOST

        return result

    def _calculate_final_score(self) -> float:
        """Calculate final scenario score."""
        if not self.current_state:
            return 0

        score = 0

        # Objective completion (40%)
        obj_score = sum(1 for o in self.current_state.objectives if o.completed)
        obj_total = len(self.current_state.objectives)
        score += (obj_score / obj_total * 40) if obj_total > 0 else 0

        # Resource efficiency (20%)
        starting_cap = self.current_state.starting_conditions["resources"]["capital"]
        current_cap = self.current_state.current_resources.get("capital", 0)
        cap_ratio = current_cap / starting_cap if starting_cap > 0 else 0
        score += min(20, cap_ratio * 20)

        # Compliance (20%)
        score += self.current_state.compliance_score * 0.2

        # Speed bonus (10%)
        # Faster completion = higher bonus
        if self.current_state.current_turn < 52:
            score += 10
        elif self.current_state.current_turn < 78:
            score += 5

        # Critical actions (10%)
        critical = self.current_state.critical_actions_completed
        total_critical = len(self.current_state.starting_conditions.get("critical_actions", []))
        score += (len(critical) / total_critical * 10) if total_critical > 0 else 0

        return round(score, 2)

    def get_scenario_history(self) -> List[Dict]:
        """Get history of all completed scenarios."""
        return [r.to_dict() for r in self.scenario_history]

    def get_best_score(self, scenario_id: str = None) -> Optional[Dict]:
        """Get best score for a scenario or overall."""
        if scenario_id:
            results = [r for r in self.scenario_history if r.scenario_id == scenario_id]
        else:
            results = self.scenario_history

        if not results:
            return None

        best = max(results, key=lambda r: r.final_score)
        return best.to_dict()

    def reset(self):
        """Reset current scenario state."""
        self.current_state = None


def run_scenario_tests() -> Dict:
    """Run scenario runner tests."""
    print("Running Scenario Runner Tests...")
    print("=" * 60)

    results = {
        "test_timestamp": datetime.now().isoformat(),
        "runner_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "scenarios_tested": []
    }

    # Test 1: Initialize runner
    print("\nTest 1: Initialize Scenario Runner")
    try:
        runner = ScenarioRunner()
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Scenario Runner",
            "status": "PASSED",
            "details": f"Loaded {len(runner.scenarios)} scenarios"
        })
        print(f"  PASSED: Loaded {len(runner.scenarios)} scenarios")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Scenario Runner",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
        return results

    # Test 2: Get scenario list
    print("\nTest 2: Get Scenario List")
    try:
        scenario_list = runner.get_scenario_list()
        results["tests_run"] += 1
        if len(scenario_list) >= 10:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Get Scenario List",
                "status": "PASSED",
                "details": f"Found {len(scenario_list)} scenarios"
            })
            print(f"  PASSED: Found {len(scenario_list)} scenarios")
            results["scenarios_tested"] = [s["scenario_id"] for s in scenario_list[:5]]
        else:
            raise ValueError(f"Expected 10+ scenarios, found {len(scenario_list)}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Get Scenario List",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 3: Get scenario details
    print("\nTest 3: Get Scenario Details")
    try:
        details = runner.get_scenario_details("SCN001")
        results["tests_run"] += 1
        if details and details["name"]:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Get Scenario Details",
                "status": "PASSED",
                "details": f"Retrieved details for {details['name']}"
            })
            print(f"  PASSED: Retrieved details for {details['name']}")
        else:
            raise ValueError("Could not retrieve scenario details")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Get Scenario Details",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 4: Start scenario
    print("\nTest 4: Start Scenario")
    try:
        state = runner.start_scenario("SCN002", "TestPlayer", "normal")
        results["tests_run"] += 1
        if state.status == ScenarioStatus.IN_PROGRESS:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Start Scenario",
                "status": "PASSED",
                "details": f"Started {state.scenario_name}"
            })
            print(f"  PASSED: Started {state.scenario_name}")
        else:
            raise ValueError("Scenario did not start properly")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Start Scenario",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 5: Starting conditions
    print("\nTest 5: Starting Conditions")
    try:
        starting = runner.current_state.starting_conditions
        assert "resources" in starting
        assert "capital" in starting["resources"]
        assert starting["resources"]["capital"] > 0
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Starting Conditions",
            "status": "PASSED",
            "details": f"Capital: ${starting['resources']['capital']:,.0f}"
        })
        print(f"  PASSED: Starting capital: ${starting['resources']['capital']:,.0f}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Starting Conditions",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 6: Objectives created
    print("\nTest 6: Objectives Creation")
    try:
        objectives = runner.current_state.objectives
        results["tests_run"] += 1
        if len(objectives) >= 3:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Objectives Creation",
                "status": "PASSED",
                "details": f"Created {len(objectives)} objectives"
            })
            print(f"  PASSED: Created {len(objectives)} objectives")
        else:
            raise ValueError(f"Expected 3+ objectives, found {len(objectives)}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Objectives Creation",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 7: Resource modification
    print("\nTest 7: Resource Modification")
    try:
        initial_capital = runner.current_state.current_resources["capital"]
        runner.modify_resource("capital", -1000)
        new_capital = runner.current_state.current_resources["capital"]
        assert abs(new_capital - (initial_capital - 1000)) < 0.01
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Resource Modification",
            "status": "PASSED",
            "details": f"Capital changed from ${initial_capital:,.0f} to ${new_capital:,.0f}"
        })
        print(f"  PASSED: Capital modified correctly")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Resource Modification",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 8: Advance turn
    print("\nTest 8: Advance Turn")
    try:
        result = runner.advance_turn()
        results["tests_run"] += 1
        if result["turn"] == 1:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Advance Turn",
                "status": "PASSED",
                "details": f"Turn advanced to {result['turn']}"
            })
            print(f"  PASSED: Turn advanced to {result['turn']}")
        else:
            raise ValueError("Turn did not advance")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Advance Turn",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 9: Objectives progress
    print("\nTest 9: Objectives Progress Tracking")
    try:
        progress = runner.get_objectives_progress()
        results["tests_run"] += 1
        if "total_objectives" in progress and "objectives" in progress:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Objectives Progress Tracking",
                "status": "PASSED",
                "details": f"Tracking {progress['total_objectives']} objectives"
            })
            print(f"  PASSED: Tracking {progress['total_objectives']} objectives")
        else:
            raise ValueError("Progress tracking failed")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Objectives Progress Tracking",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 10: Win/Loss conditions
    print("\nTest 10: Win/Loss Condition Checks")
    try:
        win_check = runner.check_win_condition()
        loss_check = runner.check_loss_condition()
        results["tests_run"] += 1
        # Early game should not have win/loss
        if not win_check[0] and not loss_check[0]:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Win/Loss Condition Checks",
                "status": "PASSED",
                "details": "Conditions checked correctly for early game"
            })
            print(f"  PASSED: Win/Loss conditions working")
        else:
            raise ValueError("Unexpected win/loss state")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Win/Loss Condition Checks",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 11: Bankruptcy loss condition
    print("\nTest 11: Bankruptcy Loss Condition")
    try:
        runner.update_resource("capital", -100)
        loss_check = runner.check_loss_condition()
        results["tests_run"] += 1
        if loss_check[0] and "Bankruptcy" in loss_check[1]:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Bankruptcy Loss Condition",
                "status": "PASSED",
                "details": "Bankruptcy detected correctly"
            })
            print(f"  PASSED: Bankruptcy detected")
        else:
            raise ValueError("Bankruptcy not detected")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Bankruptcy Loss Condition",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 12: Scenario completion
    print("\nTest 12: Scenario End and Result")
    try:
        # Reset and create fresh scenario for this test
        runner.reset()
        runner.start_scenario("SCN002", "TestPlayer", "easy")
        # Simulate winning by completing objectives
        for obj in runner.current_state.objectives:
            obj.current_value = obj.target_value * 2
            obj.completed = True
        result = runner.end_scenario("win", "All objectives completed!")
        results["tests_run"] += 1
        if result.outcome == "win" and result.final_score > 0:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Scenario End and Result",
                "status": "PASSED",
                "details": f"Scenario ended with score {result.final_score}"
            })
            print(f"  PASSED: Scenario completed with score {result.final_score}")
        else:
            raise ValueError("Scenario completion failed")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Scenario End and Result",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 13: Difficulty modifiers
    print("\nTest 13: Difficulty Modifiers")
    try:
        runner.reset()
        easy_state = runner.start_scenario("SCN002", "Player1", "easy")
        easy_capital = easy_state.current_resources["capital"]

        runner.reset()
        hard_state = runner.start_scenario("SCN002", "Player2", "hard")
        hard_capital = hard_state.current_resources["capital"]

        results["tests_run"] += 1
        if easy_capital > hard_capital:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Difficulty Modifiers",
                "status": "PASSED",
                "details": f"Easy: ${easy_capital:,.0f}, Hard: ${hard_capital:,.0f}"
            })
            print(f"  PASSED: Difficulty modifiers working (Easy: ${easy_capital:,.0f} > Hard: ${hard_capital:,.0f})")
        else:
            raise ValueError("Difficulty modifiers not working")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Difficulty Modifiers",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Test 14: Scenario history
    print("\nTest 14: Scenario History")
    try:
        history = runner.get_scenario_history()
        results["tests_run"] += 1
        if len(history) >= 1:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Scenario History",
                "status": "PASSED",
                "details": f"History contains {len(history)} scenarios"
            })
            print(f"  PASSED: History contains {len(history)} scenarios")
        else:
            raise ValueError("History not recorded")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Scenario History",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")

    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Run: {results['tests_run']}")
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    pass_rate = (results['tests_passed'] / results['tests_run'] * 100) if results['tests_run'] > 0 else 0
    print(f"Pass Rate: {pass_rate:.1f}%")

    return results


if __name__ == "__main__":
    test_results = run_scenario_tests()

    # Save test results
    output_path = Path(__file__).parent.parent / "processed" / "scenario_tests.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\nTest results saved to: {output_path}")
