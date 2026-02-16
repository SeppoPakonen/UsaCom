#!/usr/bin/env python3
"""
USA Business Journey - Analytics System
Implements player behavior tracking, decision analytics,
challenge tracking, and analytics report generation.
"""

import json
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from collections import defaultdict


class ActionType(Enum):
    """Types of player actions."""
    ACTION_COMPLETE = "action_complete"
    DECISION_MADE = "decision_made"
    RESOURCE_SPENT = "resource_spent"
    MILESTONE_REACHED = "milestone_reached"
    CHALLENGE_FACED = "challenge_faced"
    CHALLENGE_RESOLVED = "challenge_resolved"
    PHASE_COMPLETE = "phase_complete"


class DecisionOutcome(Enum):
    """Outcomes of decisions."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class ActionRecord:
    """Record of a player action."""
    record_id: str
    action_type: ActionType
    timestamp: str
    turn: int
    phase: int
    details: Dict[str, Any]
    resources_before: Dict[str, float]
    resources_after: Dict[str, float]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DecisionRecord:
    """Record of a player decision."""
    record_id: str
    decision_id: str
    decision_type: str
    timestamp: str
    turn: int
    phase: int
    option_chosen: str
    outcome: DecisionOutcome
    effects: Dict[str, float]
    time_to_decide: int  # Seconds spent on decision

    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "outcome": self.outcome.value
        }


@dataclass
class ChallengeRecord:
    """Record of a challenge encounter."""
    record_id: str
    challenge_id: str
    challenge_type: str
    timestamp: str
    turn: int
    phase: int
    severity: str
    success: bool
    resources_lost: Dict[str, float]
    resources_saved: Dict[str, float]
    mitigation_used: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SessionRecord:
    """Record of a gameplay session."""
    session_id: str
    player_name: str
    scenario_id: str
    start_time: str
    end_time: str
    turns_played: int
    actions_taken: int
    decisions_made: int
    challenges_faced: int
    challenges_won: int
    progress_start: float
    progress_end: float

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PlayerProfile:
    """Analytics profile for a player."""
    player_name: str
    total_sessions: int
    total_play_time_minutes: int
    scenarios_played: List[str]
    scenarios_completed: int
    average_score: float
    best_score: float
    preferred_difficulty: str
    play_style: str  # cautious, aggressive, balanced
    strength_areas: List[str]
    improvement_areas: List[str]
    last_played: str

    def to_dict(self) -> Dict:
        return asdict(self)


class AnalyticsSystem:
    """
    Analytics system for the USA Business Journey simulation.
    Tracks player behavior, decisions, challenges, and generates reports.
    """

    def __init__(self, analytics_dir: str = None):
        """Initialize the analytics system."""
        self.base_path = Path(__file__).parent.parent
        self.analytics_dir = Path(analytics_dir) if analytics_dir else self.base_path / "analytics"

        # Create analytics directory
        self.analytics_dir.mkdir(parents=True, exist_ok=True)

        # Data stores
        self.action_history: List[ActionRecord] = []
        self.decision_history: List[DecisionRecord] = []
        self.challenge_history: List[ChallengeRecord] = []
        self.session_history: List[SessionRecord] = []
        self.player_profiles: Dict[str, PlayerProfile] = {}

        # Current session tracking
        self.current_session: Optional[SessionRecord] = None
        self.current_player: str = ""
        self.current_scenario: str = ""
        self.session_start_turn: int = 0
        self.session_start_progress: float = 0

        # Timing tracking
        self.decision_start_times: Dict[str, datetime] = {}
        self.record_counter: int = 0

    def _generate_record_id(self, prefix: str) -> str:
        """Generate a unique record ID."""
        self.record_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}_{self.record_counter:04d}"

    def start_session(self, player_name: str, scenario_id: str,
                      starting_turn: int = 0, starting_progress: float = 0):
        """
        Start a new analytics session.

        Args:
            player_name: Name of the player
            scenario_id: Current scenario ID
            starting_turn: Starting turn number
            starting_progress: Starting progress percentage
        """
        self.current_player = player_name
        self.current_scenario = scenario_id
        self.session_start_turn = starting_turn
        self.session_start_progress = starting_progress

        self.current_session = SessionRecord(
            session_id=self._generate_record_id("sess"),
            player_name=player_name,
            scenario_id=scenario_id,
            start_time=datetime.now().isoformat(),
            end_time="",
            turns_played=0,
            actions_taken=0,
            decisions_made=0,
            challenges_faced=0,
            challenges_won=0,
            progress_start=starting_progress,
            progress_end=starting_progress
        )

    def end_session(self, final_turn: int, final_progress: float):
        """
        End the current analytics session.

        Args:
            final_turn: Final turn number
            final_progress: Final progress percentage
        """
        if self.current_session:
            self.current_session.end_time = datetime.now().isoformat()
            self.current_session.turns_played = final_turn - self.session_start_turn
            self.current_session.progress_end = final_progress

            self.session_history.append(self.current_session)

            # Update player profile
            self._update_player_profile()

            self.current_session = None

    def track_action(self, action_id: str, action_title: str, phase: int,
                     current_turn: int, resources_before: Dict[str, float],
                     resources_after: Dict[str, float],
                     additional_details: Dict[str, Any] = None):
        """
        Track a player action.

        Args:
            action_id: ID of the action
            action_title: Title of the action
            phase: Current phase
            current_turn: Current turn number
            resources_before: Resources before action
            resources_after: Resources after action
            additional_details: Additional action details
        """
        record = ActionRecord(
            record_id=self._generate_record_id("act"),
            action_type=ActionType.ACTION_COMPLETE,
            timestamp=datetime.now().isoformat(),
            turn=current_turn,
            phase=phase,
            details={
                "action_id": action_id,
                "action_title": action_title,
                **(additional_details or {})
            },
            resources_before=resources_before.copy(),
            resources_after=resources_after.copy()
        )

        self.action_history.append(record)

        if self.current_session:
            self.current_session.actions_taken += 1

    def start_decision_timer(self, decision_id: str):
        """Start timing a decision."""
        self.decision_start_times[decision_id] = datetime.now()

    def track_decision(self, decision_id: str, decision_type: str, phase: int,
                       current_turn: int, option_chosen: str,
                       effects: Dict[str, float], outcome: str = "neutral"):
        """
        Track a player decision.

        Args:
            decision_id: ID of the decision
            decision_type: Type of decision
            phase: Current phase
            current_turn: Current turn number
            option_chosen: Option selected
            effects: Effects of the decision
            outcome: Outcome type (positive, neutral, negative)
        """
        # Calculate time to decide
        time_to_decide = 0
        if decision_id in self.decision_start_times:
            start_time = self.decision_start_times.pop(decision_id)
            time_to_decide = int((datetime.now() - start_time).total_seconds())

        record = DecisionRecord(
            record_id=self._generate_record_id("dec"),
            decision_id=decision_id,
            decision_type=decision_type,
            timestamp=datetime.now().isoformat(),
            turn=current_turn,
            phase=phase,
            option_chosen=option_chosen,
            outcome=DecisionOutcome(outcome),
            effects=effects.copy(),
            time_to_decide=time_to_decide
        )

        self.decision_history.append(record)

        if self.current_session:
            self.current_session.decisions_made += 1

    def track_challenge(self, challenge_id: str, challenge_type: str, phase: int,
                        current_turn: int, severity: str, success: bool,
                        resources_lost: Dict[str, float],
                        resources_saved: Dict[str, float],
                        mitigation_used: List[str]):
        """
        Track a challenge encounter.

        Args:
            challenge_id: ID of the challenge
            challenge_type: Type of challenge
            phase: Current phase
            current_turn: Current turn number
            severity: Challenge severity
            success: Whether challenge was overcome
            resources_lost: Resources lost in challenge
            resources_saved: Resources saved through mitigation
            mitigation_used: Mitigation strategies used
        """
        record = ChallengeRecord(
            record_id=self._generate_record_id("chl"),
            challenge_id=challenge_id,
            challenge_type=challenge_type,
            timestamp=datetime.now().isoformat(),
            turn=current_turn,
            phase=phase,
            severity=severity,
            success=success,
            resources_lost=resources_lost.copy(),
            resources_saved=resources_saved.copy(),
            mitigation_used=mitigation_used.copy()
        )

        self.challenge_history.append(record)

        if self.current_session:
            self.current_session.challenges_faced += 1
            if success:
                self.current_session.challenges_won += 1

    def track_milestone(self, milestone_name: str, phase: int, current_turn: int,
                        reward: Dict[str, Any]):
        """Track a milestone achievement."""
        self.track_action(
            action_id="milestone",
            action_title=milestone_name,
            phase=phase,
            current_turn=current_turn,
            resources_before={},
            resources_after={},
            additional_details={
                "milestone": milestone_name,
                "reward": reward,
                "event_type": "milestone"
            }
        )

    def track_phase_complete(self, phase: int, current_turn: int,
                             actions_in_phase: int, time_in_phase: int):
        """Track phase completion."""
        self.track_action(
            action_id=f"phase_{phase}_complete",
            action_title=f"Phase {phase} Complete",
            phase=phase,
            current_turn=current_turn,
            resources_before={},
            resources_after={},
            additional_details={
                "actions_completed": actions_in_phase,
                "turns_spent": time_in_phase,
                "event_type": "phase_complete"
            }
        )

    def _update_player_profile(self):
        """Update player profile based on session history."""
        if not self.current_player:
            return

        player_sessions = [s for s in self.session_history
                          if s.player_name == self.current_player]

        if not player_sessions:
            return

        # Calculate statistics
        total_time = 0
        scenarios = set()
        completed = 0
        scores = []

        for session in player_sessions:
            scenarios.add(session.scenario_id)
            # Estimate play time (1 min per turn average)
            total_time += session.turns_played
            if session.progress_end >= 100:
                completed += 1

        # Get existing profile or create new
        if self.current_player in self.player_profiles:
            profile = self.player_profiles[self.current_player]
            profile.total_sessions += len(player_sessions)
            profile.total_play_time_minutes += total_time
            profile.scenarios_played = list(scenarios)
            profile.scenarios_completed = completed
            profile.last_played = datetime.now().isoformat()
        else:
            profile = PlayerProfile(
                player_name=self.current_player,
                total_sessions=len(player_sessions),
                total_play_time_minutes=total_time,
                scenarios_played=list(scenarios),
                scenarios_completed=completed,
                average_score=0,
                best_score=0,
                preferred_difficulty="normal",
                play_style=self._determine_play_style(),
                strength_areas=self._identify_strengths(),
                improvement_areas=self._identify_improvements(),
                last_played=datetime.now().isoformat()
            )

        self.player_profiles[self.current_player] = profile

    def _determine_play_style(self) -> str:
        """Determine player's play style based on history."""
        if not self.action_history:
            return "balanced"

        # Analyze action patterns
        fast_actions = sum(1 for a in self.action_history
                         if a.details.get("time_cost", 1) <= 1)
        total_actions = len(self.action_history)

        if total_actions == 0:
            return "balanced"

        fast_ratio = fast_actions / total_actions

        if fast_ratio > 0.7:
            return "aggressive"
        elif fast_ratio < 0.3:
            return "cautious"
        return "balanced"

    def _identify_strengths(self) -> List[str]:
        """Identify player's strength areas."""
        strengths = []

        # Check challenge success rate
        if self.challenge_history:
            success_rate = sum(1 for c in self.challenge_history if c.success) / len(self.challenge_history)
            if success_rate > 0.7:
                strengths.append("Challenge Management")

        # Check resource management
        capital_changes = []
        for action in self.action_history:
            if "Capital" in action.resources_before and "Capital" in action.resources_after:
                change = action.resources_after["Capital"] - action.resources_before["Capital"]
                capital_changes.append(change)

        if capital_changes:
            avg_change = statistics.mean(capital_changes)
            if avg_change > -100:  # Not losing much capital
                strengths.append("Resource Management")

        # Check decision outcomes
        if self.decision_history:
            positive = sum(1 for d in self.decision_history if d.outcome == DecisionOutcome.POSITIVE)
            if positive / len(self.decision_history) > 0.5:
                strengths.append("Decision Making")

        return strengths if strengths else ["Learning"]

    def _identify_improvements(self) -> List[str]:
        """Identify areas for improvement."""
        improvements = []

        # Check challenge failures
        if self.challenge_history:
            failures = sum(1 for c in self.challenge_history if not c.success)
            if failures > 3:
                improvements.append("Challenge Preparation")

        # Check rapid capital depletion
        for action in self.action_history:
            if "Capital" in action.resources_before and "Capital" in action.resources_after:
                loss = action.resources_before["Capital"] - action.resources_after["Capital"]
                if loss > 1000:
                    improvements.append("Large Expense Planning")
                    break

        return improvements if improvements else ["Continue Learning"]

    def get_action_analytics(self) -> Dict:
        """Get analytics on player actions."""
        if not self.action_history:
            return {"total_actions": 0}

        # Actions by phase
        by_phase = defaultdict(int)
        for action in self.action_history:
            by_phase[action.phase] += 1

        # Actions by type
        by_type = defaultdict(int)
        for action in self.action_history:
            action_type = action.details.get("action_title", "Unknown")
            by_type[action_type] += 1

        # Resource spending patterns
        capital_spent = 0
        for action in self.action_history:
            if "Capital" in action.resources_before and "Capital" in action.resources_after:
                spent = action.resources_before["Capital"] - action.resources_after["Capital"]
                if spent > 0:
                    capital_spent += spent

        return {
            "total_actions": len(self.action_history),
            "actions_by_phase": dict(by_phase),
            "actions_by_type": dict(by_type),
            "total_capital_spent": capital_spent,
            "average_actions_per_turn": len(self.action_history) / max(1, self.action_history[-1].turn if self.action_history else 1)
        }

    def get_decision_analytics(self) -> Dict:
        """Get analytics on player decisions."""
        if not self.decision_history:
            return {"total_decisions": 0}

        # Outcomes distribution
        outcomes = defaultdict(int)
        for decision in self.decision_history:
            outcomes[decision.outcome.value] += 1

        # Decision types
        by_type = defaultdict(int)
        for decision in self.decision_history:
            by_type[decision.decision_type] += 1

        # Average decision time
        times = [d.time_to_decide for d in self.decision_history if d.time_to_decide > 0]
        avg_time = statistics.mean(times) if times else 0

        return {
            "total_decisions": len(self.decision_history),
            "outcomes": dict(outcomes),
            "decisions_by_type": dict(by_type),
            "average_decision_time_seconds": round(avg_time, 1),
            "positive_outcome_rate": outcomes.get("positive", 0) / len(self.decision_history) * 100
        }

    def get_challenge_analytics(self) -> Dict:
        """Get analytics on challenge encounters."""
        if not self.challenge_history:
            return {"total_challenges": 0}

        # Success rate
        successes = sum(1 for c in self.challenge_history if c.success)
        success_rate = successes / len(self.challenge_history) * 100

        # By type
        by_type = defaultdict(lambda: {"total": 0, "successes": 0})
        for challenge in self.challenge_history:
            by_type[challenge.challenge_type]["total"] += 1
            if challenge.success:
                by_type[challenge.challenge_type]["successes"] += 1

        # By severity
        by_severity = defaultdict(lambda: {"total": 0, "successes": 0})
        for challenge in self.challenge_history:
            by_severity[challenge.severity]["total"] += 1
            if challenge.success:
                by_severity[challenge.severity]["successes"] += 1

        # Resources lost
        total_lost = defaultdict(float)
        total_saved = defaultdict(float)
        for challenge in self.challenge_history:
            for resource, amount in challenge.resources_lost.items():
                total_lost[resource] += amount
            for resource, amount in challenge.resources_saved.items():
                total_saved[resource] += amount

        return {
            "total_challenges": len(self.challenge_history),
            "successes": successes,
            "failures": len(self.challenge_history) - successes,
            "success_rate": round(success_rate, 1),
            "by_type": {k: dict(v) for k, v in by_type.items()},
            "by_severity": {k: dict(v) for k, v in by_severity.items()},
            "total_resources_lost": dict(total_lost),
            "total_resources_saved": dict(total_saved)
        }

    def get_session_analytics(self) -> Dict:
        """Get analytics on gameplay sessions."""
        if not self.session_history:
            return {"total_sessions": 0}

        # Session statistics
        total_turns = sum(s.turns_played for s in self.session_history)
        total_actions = sum(s.actions_taken for s in self.session_history)

        # Average progress per session
        progress_gains = [s.progress_end - s.progress_start for s in self.session_history]
        avg_progress = statistics.mean(progress_gains) if progress_gains else 0

        # Challenge success rate across sessions
        total_challenges = sum(s.challenges_faced for s in self.session_history)
        total_won = sum(s.challenges_won for s in self.session_history)

        return {
            "total_sessions": len(self.session_history),
            "total_turns_played": total_turns,
            "total_actions_taken": total_actions,
            "average_turns_per_session": round(total_turns / len(self.session_history), 1),
            "average_actions_per_session": round(total_actions / len(self.session_history), 1),
            "average_progress_per_session": round(avg_progress, 1),
            "overall_challenge_success_rate": round(total_won / total_challenges * 100, 1) if total_challenges > 0 else 0
        }

    def get_player_profile(self, player_name: str = None) -> Optional[Dict]:
        """Get player profile."""
        name = player_name or self.current_player
        if name in self.player_profiles:
            return self.player_profiles[name].to_dict()
        return None

    def generate_report(self, report_type: str = "summary") -> Dict:
        """
        Generate an analytics report.

        Args:
            report_type: Type of report (summary, detailed, session, player)

        Returns:
            Report dictionary
        """
        report = {
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "player": self.current_player,
            "scenario": self.current_scenario
        }

        if report_type == "summary":
            report["action_summary"] = self.get_action_analytics()
            report["decision_summary"] = self.get_decision_analytics()
            report["challenge_summary"] = self.get_challenge_analytics()
            report["session_summary"] = self.get_session_analytics()

        elif report_type == "detailed":
            report["action_summary"] = self.get_action_analytics()
            report["decision_summary"] = self.get_decision_analytics()
            report["challenge_summary"] = self.get_challenge_analytics()
            report["session_summary"] = self.get_session_analytics()
            report["player_profile"] = self.get_player_profile()

            # Add recent history
            report["recent_actions"] = [a.to_dict() for a in self.action_history[-10:]]
            report["recent_decisions"] = [d.to_dict() for d in self.decision_history[-10:]]
            report["recent_challenges"] = [c.to_dict() for c in self.challenge_history[-10:]]

        elif report_type == "session":
            if self.current_session:
                report["current_session"] = self.current_session.to_dict()
            report["session_history"] = [s.to_dict() for s in self.session_history[-5:]]

        elif report_type == "player":
            report["profile"] = self.get_player_profile()
            report["all_sessions"] = [s.to_dict() for s in self.session_history
                                      if s.player_name == self.current_player]

        return report

    def save_report(self, report: Dict, filename: str = None) -> str:
        """
        Save a report to file.

        Args:
            report: Report dictionary
            filename: Output filename (auto-generated if None)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analytics_report_{timestamp}.json"

        file_path = self.analytics_dir / filename

        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2)

        return str(file_path)

    def export_sample_report(self) -> str:
        """Export a sample analytics report for demonstration."""
        # Create sample data
        sample_report = {
            "report_type": "sample_analytics_report",
            "generated_at": datetime.now().isoformat(),
            "game_version": "1.0.0",
            "sample_data": True,
            "player_analytics": {
                "player_name": "Sample Player",
                "total_sessions": 5,
                "total_play_time_minutes": 180,
                "scenarios_completed": 2,
                "average_score": 78.5,
                "play_style": "balanced",
                "strengths": ["Resource Management", "Decision Making"],
                "improvements": ["Challenge Preparation"]
            },
            "action_analytics": {
                "total_actions": 45,
                "actions_by_phase": {
                    "1": 12,
                    "2": 10,
                    "3": 9,
                    "4": 8,
                    "5": 6
                },
                "most_common_actions": [
                    "Market Research",
                    "Business Registration",
                    "License Application"
                ],
                "average_actions_per_turn": 0.85
            },
            "decision_analytics": {
                "total_decisions": 15,
                "outcomes": {
                    "positive": 8,
                    "neutral": 5,
                    "negative": 2
                },
                "positive_outcome_rate": 53.3,
                "average_decision_time_seconds": 45.2,
                "decisions_by_type": {
                    "business_structure": 3,
                    "funding_strategy": 4,
                    "market_entry": 5,
                    "hiring": 3
                }
            },
            "challenge_analytics": {
                "total_challenges": 12,
                "success_rate": 66.7,
                "by_type": {
                    "environmental": {"total": 4, "successes": 3},
                    "enemy": {"total": 5, "successes": 3},
                    "resource": {"total": 3, "successes": 2}
                },
                "by_severity": {
                    "low": {"total": 4, "successes": 4},
                    "medium": {"total": 5, "successes": 3},
                    "high": {"total": 3, "successes": 1}
                },
                "total_resources_lost": {
                    "capital": 4500,
                    "time": 8,
                    "reputation": 15
                }
            },
            "session_analytics": {
                "total_sessions": 5,
                "average_turns_per_session": 25.4,
                "average_actions_per_session": 21.6,
                "average_progress_per_session": 18.5,
                "best_session_score": 92.0,
                "completion_rate": 40.0
            },
            "recommendations": [
                "Focus on building capital reserves before major expansions",
                "Consider more thorough preparation before facing high-severity challenges",
                "Your decision-making is strong - continue researching before major choices",
                "Try different scenarios to develop diverse business skills"
            ]
        }

        file_path = self.analytics_dir / "sample_analytics_report.json"
        with open(file_path, 'w') as f:
            json.dump(sample_report, f, indent=2)

        return str(file_path)

    def reset(self):
        """Reset analytics system."""
        self.action_history.clear()
        self.decision_history.clear()
        self.challenge_history.clear()
        self.session_history.clear()
        self.current_session = None
        self.current_player = ""
        self.current_scenario = ""
        self.decision_start_times.clear()
        self.record_counter = 0


def run_analytics_tests() -> Dict:
    """Run analytics system tests."""
    print("Running Analytics System Tests...")
    print("=" * 60)

    results = {
        "test_timestamp": datetime.now().isoformat(),
        "system_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "analytics_tested": []
    }

    try:
        # Test 1: Initialize analytics system
        print("\nTest 1: Initialize Analytics System")
        try:
            analytics = AnalyticsSystem()
            results["tests_run"] += 1
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Initialize Analytics System",
                "status": "PASSED",
                "details": "Analytics system initialized"
            })
            print(f"  PASSED: Analytics system initialized")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Initialize Analytics System",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")
            return results

        # Test 2: Start session
        print("\nTest 2: Start Session")
        try:
            analytics.start_session("TestPlayer", "SCN002", 0, 0)
            results["tests_run"] += 1
            if analytics.current_session and analytics.current_player == "TestPlayer":
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Start Session",
                    "status": "PASSED",
                    "details": "Session started for TestPlayer"
                })
                print(f"  PASSED: Session started")
                results["analytics_tested"].append("session")
            else:
                raise ValueError("Session not started")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Start Session",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 3: Track action
        print("\nTest 3: Track Action")
        try:
            analytics.track_action(
                action_id="action_1_1",
                action_title="Market Research",
                phase=1,
                current_turn=1,
                resources_before={"Capital": 10000},
                resources_after={"Capital": 9850},
                additional_details={"time_cost": 1}
            )
            results["tests_run"] += 1
            if len(analytics.action_history) == 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Track Action",
                    "status": "PASSED",
                    "details": "Action tracked"
                })
                print(f"  PASSED: Action tracked")
                results["analytics_tested"].append("action")
            else:
                raise ValueError("Action not tracked")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Track Action",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 4: Track decision
        print("\nTest 4: Track Decision")
        try:
            analytics.start_decision_timer("business_structure")
            import time
            time.sleep(0.1)  # Small delay
            analytics.track_decision(
                decision_id="business_structure",
                decision_type="business_structure",
                phase=2,
                current_turn=5,
                option_chosen="LLC",
                effects={"capital": -500},
                outcome="positive"
            )
            results["tests_run"] += 1
            if len(analytics.decision_history) == 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Track Decision",
                    "status": "PASSED",
                    "details": "Decision tracked"
                })
                print(f"  PASSED: Decision tracked")
                results["analytics_tested"].append("decision")
            else:
                raise ValueError("Decision not tracked")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Track Decision",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 5: Track challenge
        print("\nTest 5: Track Challenge")
        try:
            analytics.track_challenge(
                challenge_id="cash_flow_currents",
                challenge_type="environmental",
                phase=2,
                current_turn=8,
                severity="high",
                success=True,
                resources_lost={"capital": 500},
                resources_saved={"capital": 500},
                mitigation_used=["Maintain reserve"]
            )
            results["tests_run"] += 1
            if len(analytics.challenge_history) == 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Track Challenge",
                    "status": "PASSED",
                    "details": "Challenge tracked"
                })
                print(f"  PASSED: Challenge tracked")
                results["analytics_tested"].append("challenge")
            else:
                raise ValueError("Challenge not tracked")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Track Challenge",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 6: Get action analytics
        print("\nTest 6: Get Action Analytics")
        try:
            action_analytics = analytics.get_action_analytics()
            results["tests_run"] += 1
            if action_analytics.get("total_actions", 0) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Action Analytics",
                    "status": "PASSED",
                    "details": f"Total actions: {action_analytics['total_actions']}"
                })
                print(f"  PASSED: Total actions: {action_analytics['total_actions']}")
            else:
                raise ValueError("Action analytics failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Action Analytics",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 7: Get decision analytics
        print("\nTest 7: Get Decision Analytics")
        try:
            decision_analytics = analytics.get_decision_analytics()
            results["tests_run"] += 1
            if decision_analytics.get("total_decisions", 0) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Decision Analytics",
                    "status": "PASSED",
                    "details": f"Total decisions: {decision_analytics['total_decisions']}"
                })
                print(f"  PASSED: Total decisions: {decision_analytics['total_decisions']}")
            else:
                raise ValueError("Decision analytics failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Decision Analytics",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 8: Get challenge analytics
        print("\nTest 8: Get Challenge Analytics")
        try:
            challenge_analytics = analytics.get_challenge_analytics()
            results["tests_run"] += 1
            if challenge_analytics.get("total_challenges", 0) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Challenge Analytics",
                    "status": "PASSED",
                    "details": f"Success rate: {challenge_analytics.get('success_rate', 0)}%"
                })
                print(f"  PASSED: Success rate: {challenge_analytics.get('success_rate', 0)}%")
            else:
                raise ValueError("Challenge analytics failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Challenge Analytics",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 9: Generate summary report
        print("\nTest 9: Generate Summary Report")
        try:
            report = analytics.generate_report("summary")
            results["tests_run"] += 1
            if "action_summary" in report and "decision_summary" in report:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Generate Summary Report",
                    "status": "PASSED",
                    "details": "Summary report generated"
                })
                print(f"  PASSED: Summary report generated")
                results["analytics_tested"].append("report")
            else:
                raise ValueError("Report generation failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Generate Summary Report",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 10: End session
        print("\nTest 10: End Session")
        try:
            analytics.end_session(20, 35.5)
            results["tests_run"] += 1
            if len(analytics.session_history) == 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "End Session",
                    "status": "PASSED",
                    "details": "Session ended and recorded"
                })
                print(f"  PASSED: Session ended")
            else:
                raise ValueError("Session not ended properly")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "End Session",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 11: Get session analytics
        print("\nTest 11: Get Session Analytics")
        try:
            session_analytics = analytics.get_session_analytics()
            results["tests_run"] += 1
            if session_analytics.get("total_sessions", 0) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Session Analytics",
                    "status": "PASSED",
                    "details": f"Total sessions: {session_analytics['total_sessions']}"
                })
                print(f"  PASSED: Total sessions: {session_analytics['total_sessions']}")
            else:
                raise ValueError("Session analytics failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Session Analytics",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 12: Export sample report
        print("\nTest 12: Export Sample Report")
        try:
            report_path = analytics.export_sample_report()
            results["tests_run"] += 1
            if Path(report_path).exists():
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Export Sample Report",
                    "status": "PASSED",
                    "details": f"Report saved to {report_path}"
                })
                print(f"  PASSED: Report saved")
            else:
                raise ValueError("Sample report not created")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Export Sample Report",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 13: Player profile
        print("\nTest 13: Player Profile")
        try:
            profile = analytics.get_player_profile("TestPlayer")
            results["tests_run"] += 1
            if profile and profile.get("player_name") == "TestPlayer":
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Player Profile",
                    "status": "PASSED",
                    "details": f"Profile created for {profile['player_name']}"
                })
                print(f"  PASSED: Profile created")
                results["analytics_tested"].append("profile")
            else:
                raise ValueError("Profile not created")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Player Profile",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 14: Reset analytics
        print("\nTest 14: Reset Analytics")
        try:
            analytics.reset()
            results["tests_run"] += 1
            if len(analytics.action_history) == 0 and analytics.current_session is None:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Reset Analytics",
                    "status": "PASSED",
                    "details": "Analytics reset"
                })
                print(f"  PASSED: Analytics reset")
            else:
                raise ValueError("Analytics not reset")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Reset Analytics",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Run: {results['tests_run']}")
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    pass_rate = (results['tests_passed'] / results['tests_run'] * 100) if results['tests_run'] > 0 else 0
    print(f"Pass Rate: {pass_rate:.1f}%")

    return results


if __name__ == "__main__":
    test_results = run_analytics_tests()

    # Save test results
    output_path = Path(__file__).parent.parent / "processed" / "analytics_sample_report.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\nTest results saved to: {output_path}")
