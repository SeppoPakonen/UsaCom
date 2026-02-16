#!/usr/bin/env python3
"""
USA Business Journey - Challenge System
Implements challenge generation, challenge types, difficulty scaling, and mitigation strategies.
Based on game_mechanics_spec.json challenge_system from Phase 5.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class ChallengeType(Enum):
    """Types of challenges in the game."""
    ENVIRONMENTAL = "environmental"
    ENEMY = "enemy"
    RESOURCE = "resource"


class Severity(Enum):
    """Challenge severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Challenge:
    """Represents a challenge in the game."""
    challenge_id: str
    name: str
    challenge_type: ChallengeType
    description: str
    severity: Severity
    effects: Dict[str, float]
    duration: int  # Turns
    mitigation_strategies: List[str]
    phase_min: int = 1
    phase_max: int = 5
    triggered: bool = False
    turn_triggered: int = 0
    turn_resolved: int = 0
    mitigated: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "challenge_id": self.challenge_id,
            "name": self.name,
            "challenge_type": self.challenge_type.value,
            "description": self.description,
            "severity": self.severity.value,
            "effects": self.effects,
            "duration": self.duration,
            "mitigation_strategies": self.mitigation_strategies,
            "phase_min": self.phase_min,
            "phase_max": self.phase_max,
            "triggered": self.triggered,
            "turn_triggered": self.turn_triggered,
            "turn_resolved": self.turn_resolved,
            "mitigated": self.mitigated
        }


@dataclass
class ChallengeOutcome:
    """Represents the outcome of a challenge."""
    outcome_id: str
    challenge_id: str
    player_actions: List[str]
    resources_lost: Dict[str, float]
    resources_saved: Dict[str, float]
    success: bool
    narrative: str
    turn_resolved: int
    lessons_learned: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ChallengeSystem:
    """
    Challenge system for the USA Business Journey simulation.
    Implements challenge generation, difficulty scaling, and mitigation.
    """
    
    def __init__(self, game_mechanics_path: str = None):
        """Initialize the challenge system."""
        self.base_path = Path(__file__).parent.parent / "processed"
        
        # Load game mechanics
        mechanics_path = game_mechanics_path or self.base_path / "game_mechanics_spec.json"
        with open(mechanics_path, 'r') as f:
            self.game_mechanics = json.load(f)
        
        # Initialize challenges
        self.challenges: Dict[str, Challenge] = {}
        self.active_challenges: List[Challenge] = []
        self.challenge_outcomes: List[ChallengeOutcome] = []
        self.difficulty = "normal"
        
        self._load_challenges()
    
    def _load_challenges(self):
        """Load challenges from game mechanics."""
        challenge_system = self.game_mechanics.get("4_challenge_system", {})
        
        # Environmental challenges
        env_challenges = [
            Challenge(
                challenge_id="fog_of_uncertainty",
                name="Fog of Uncertainty",
                challenge_type=ChallengeType.ENVIRONMENTAL,
                description="Market uncertainty makes it hard to identify optimal business paths.",
                severity=Severity.LOW,
                effects={"knowledge": -5},
                duration=3,
                mitigation_strategies=["Conduct market research", "Consult industry experts", "Analyze competitors"],
                phase_min=1,
                phase_max=2
            ),
            Challenge(
                challenge_id="regulation_rapids",
                name="Regulation Rapids",
                challenge_type=ChallengeType.ENVIRONMENTAL,
                description="Fast-changing regulations require constant attention and adaptation.",
                severity=Severity.MEDIUM,
                effects={"time": -2, "capital": -300},
                duration=4,
                mitigation_strategies=["Hire compliance consultant", "Subscribe to regulatory updates", "Join industry association"],
                phase_min=3,
                phase_max=5
            ),
            Challenge(
                challenge_id="cash_flow_currents",
                name="Cash Flow Currents",
                challenge_type=ChallengeType.ENVIRONMENTAL,
                description="Strong cash flow pressures affect business movement and decisions.",
                severity=Severity.HIGH,
                effects={"capital": -1000, "stress": 20},
                duration=5,
                mitigation_strategies=["Maintain 3-month operating reserve", "Negotiate payment terms", "Secure line of credit"],
                phase_min=2,
                phase_max=5
            ),
            Challenge(
                challenge_id="burnout_black_hole",
                name="Burnout Black Hole",
                challenge_type=ChallengeType.ENVIRONMENTAL,
                description="Excessive work pulls resources without proper work-life balance.",
                severity=Severity.HIGH,
                effects={"time": -5, "knowledge": -10},
                duration=6,
                mitigation_strategies=["Set work boundaries", "Delegate tasks", "Take regular breaks"],
                phase_min=3,
                phase_max=5
            )
        ]
        
        # Enemy challenges
        enemy_challenges = [
            Challenge(
                challenge_id="deadline_dragons",
                name="Deadline Dragons",
                challenge_type=ChallengeType.ENEMY,
                description="Missed filing deadlines attack with penalties and interest.",
                severity=Severity.HIGH,
                effects={"capital": -500, "reputation": -10},
                duration=1,
                mitigation_strategies=["Calendar reminders", "Automated filing system", "Hire accountant"],
                phase_min=2,
                phase_max=5
            ),
            Challenge(
                challenge_id="liability_leviathan",
                name="Liability Leviathan",
                challenge_type=ChallengeType.ENEMY,
                description="Emerges without proper insurance, causing massive damage.",
                severity=Severity.CRITICAL,
                effects={"capital": -10000, "reputation": -20},
                duration=1,
                mitigation_strategies=["General liability insurance", "Professional liability insurance", "Proper business structure"],
                phase_min=2,
                phase_max=5
            ),
            Challenge(
                challenge_id="competition_comets",
                name="Competition Comets",
                challenge_type=ChallengeType.ENEMY,
                description="Rival businesses crossing your path, taking market share.",
                severity=Severity.MEDIUM,
                effects={"capital": -2000, "reputation": -5},
                duration=4,
                mitigation_strategies=["Differentiate offerings", "Speed to market", "Build customer loyalty"],
                phase_min=4,
                phase_max=5
            ),
            Challenge(
                challenge_id="paperwork_golems",
                name="Paperwork Golems",
                challenge_type=ChallengeType.ENEMY,
                description="Documentation requirements slow progress significantly.",
                severity=Severity.MEDIUM,
                effects={"time": -4, "knowledge": -5},
                duration=3,
                mitigation_strategies=["Use templates", "Hire professional services", "Automation tools"],
                phase_min=2,
                phase_max=4
            )
        ]
        
        # Resource challenges
        resource_challenges = [
            Challenge(
                challenge_id="fee_toll_bridges",
                name="Fee Toll Bridges",
                challenge_type=ChallengeType.RESOURCE,
                description="Required payments to cross various business thresholds.",
                severity=Severity.LOW,
                effects={"capital": -500},
                duration=1,
                mitigation_strategies=["Budget planning", "Fee waivers for qualifying businesses", "Payment plans"],
                phase_min=1,
                phase_max=3
            ),
            Challenge(
                challenge_id="talent_shortage",
                name="Talent Shortage",
                challenge_type=ChallengeType.RESOURCE,
                description="Difficulty finding qualified team members.",
                severity=Severity.MEDIUM,
                effects={"time": -3, "capital": -1500},
                duration=4,
                mitigation_strategies=["Competitive compensation", "Remote hiring", "Training programs"],
                phase_min=3,
                phase_max=5
            ),
            Challenge(
                challenge_id="supply_chain_disruption",
                name="Supply Chain Disruption",
                challenge_type=ChallengeType.RESOURCE,
                description="Suppliers fail to deliver on time or at expected quality.",
                severity=Severity.HIGH,
                effects={"capital": -3000, "time": -5},
                duration=5,
                mitigation_strategies=["Multiple suppliers", "Inventory buffer", "Local sourcing"],
                phase_min=4,
                phase_max=5
            ),
            Challenge(
                challenge_id="funding_gap",
                name="Funding Gap",
                challenge_type=ChallengeType.RESOURCE,
                description="Expected funding doesn't materialize when needed.",
                severity=Severity.HIGH,
                effects={"capital": -5000},
                duration=6,
                mitigation_strategies=["Multiple funding sources", "Bootstrapping plan", "Cost reduction"],
                phase_min=2,
                phase_max=5
            )
        ]
        
        # Add all challenges
        for challenge in env_challenges + enemy_challenges + resource_challenges:
            self.challenges[challenge.challenge_id] = challenge
    
    def set_difficulty(self, difficulty: str):
        """Set game difficulty level."""
        valid_difficulties = ["easy", "normal", "hard", "expert"]
        if difficulty.lower() in valid_difficulties:
            self.difficulty = difficulty.lower()
    
    def get_difficulty_settings(self) -> Dict:
        """Get difficulty scaling settings."""
        difficulty_settings = self.game_mechanics.get("4_challenge_system", {}).get("difficulty_scaling", {})
        return difficulty_settings.get(self.difficulty, {
            "challenge_frequency": 0.25,
            "severity_modifier": 1.0
        })
    
    def generate_challenge(self, current_phase: int, 
                          game_state: Dict[str, Any]) -> Optional[Challenge]:
        """
        Generate a challenge based on current game state.
        
        Args:
            current_phase: Current game phase
            game_state: Current game state for context
        
        Returns:
            Generated challenge or None
        """
        settings = self.get_difficulty_settings()
        frequency = settings.get("challenge_frequency", 0.25)
        
        # Check if challenge should occur
        if random.random() > frequency:
            return None
        
        # Get eligible challenges
        eligible = []
        for challenge in self.challenges.values():
            if challenge.triggered:
                continue
            if challenge.phase_min <= current_phase <= challenge.phase_max:
                # Check additional conditions
                if self._check_challenge_conditions(challenge, game_state):
                    eligible.append(challenge)
        
        if not eligible:
            return None
        
        # Weight by severity (lower severity more common early)
        weights = self._calculate_challenge_weights(eligible, current_phase)
        
        selected = random.choices(eligible, weights=weights)[0]
        selected.triggered = True
        selected.turn_triggered = game_state.get("current_turn", 0)
        
        self.active_challenges.append(selected)
        
        return selected
    
    def _check_challenge_conditions(self, challenge: Challenge,
                                    game_state: Dict[str, Any]) -> bool:
        """Check if challenge conditions are met."""
        # Enemy challenges require certain reputation to attract
        if challenge.challenge_type == ChallengeType.ENEMY:
            if game_state.get("reputation", 0) < 5:
                return False
        
        # Resource challenges require certain activity level
        if challenge.challenge_type == ChallengeType.RESOURCE:
            if game_state.get("current_phase", 1) < 2:
                return False
        
        return True
    
    def _calculate_challenge_weights(self, challenges: List[Challenge],
                                     current_phase: int) -> List[float]:
        """Calculate selection weights for challenges."""
        weights = []
        severity_base = {"low": 4, "medium": 3, "high": 2, "critical": 1}
        
        for challenge in challenges:
            weight = severity_base.get(challenge.severity.value, 2)
            
            # Adjust based on phase appropriateness
            phase_center = (challenge.phase_min + challenge.phase_max) / 2
            phase_diff = abs(phase_center - current_phase)
            weight *= (1.0 / (phase_diff + 1))
            
            weights.append(weight)
        
        return weights
    
    def apply_challenge_effects(self, challenge: Challenge,
                                game_state: Dict[str, float],
                                mitigation_level: float = 0.0) -> Dict[str, float]:
        """
        Apply challenge effects to game state.
        
        Args:
            challenge: The challenge to apply
            game_state: Current game state
            mitigation_level: 0.0 to 1.0 mitigation effectiveness
        
        Returns:
            Actual effects applied
        """
        settings = self.get_difficulty_settings()
        severity_modifier = settings.get("severity_modifier", 1.0)
        
        actual_effects = {}
        for resource, effect in challenge.effects.items():
            # Apply severity modifier
            modified_effect = effect * severity_modifier
            
            # Apply mitigation
            mitigated_effect = modified_effect * (1 - mitigation_level)
            
            actual_effects[resource] = mitigated_effect
            
            # Apply to game state
            if resource in game_state:
                game_state[resource] += mitigated_effect
        
        return actual_effects
    
    def resolve_challenge(self, challenge: Challenge, 
                         player_actions: List[str],
                         game_state: Dict[str, Any]) -> ChallengeOutcome:
        """
        Resolve a challenge based on player actions.
        
        Args:
            challenge: The challenge to resolve
            player_actions: Actions taken to address challenge
            game_state: Current game state
        
        Returns:
            ChallengeOutcome with results
        """
        # Calculate mitigation effectiveness
        mitigation_level = self._calculate_mitigation(challenge, player_actions, game_state)
        
        # Apply effects
        actual_effects = self.apply_challenge_effects(challenge, game_state, mitigation_level)
        
        # Determine success
        success = mitigation_level > 0.5
        
        # Calculate resources lost/saved
        resources_lost = {k: abs(v) for k, v in actual_effects.items() if v < 0}
        resources_saved = {}
        for resource, original in challenge.effects.items():
            if original < 0:
                saved = abs(original) - resources_lost.get(resource, 0)
                if saved > 0:
                    resources_saved[resource] = saved
        
        # Generate narrative
        narrative = self._generate_challenge_narrative(challenge, success, mitigation_level)
        
        # Generate lessons learned
        lessons = self._generate_lessons(challenge, success)
        
        # Create outcome
        outcome = ChallengeOutcome(
            outcome_id=f"outcome_{challenge.challenge_id}_{game_state.get('current_turn', 0)}",
            challenge_id=challenge.challenge_id,
            player_actions=player_actions,
            resources_lost=resources_lost,
            resources_saved=resources_saved,
            success=success,
            narrative=narrative,
            turn_resolved=game_state.get("current_turn", 0),
            lessons_learned=lessons
        )
        
        self.challenge_outcomes.append(outcome)
        challenge.mitigated = success
        challenge.turn_resolved = game_state.get("current_turn", 0)
        
        # Remove from active challenges
        if challenge in self.active_challenges:
            self.active_challenges.remove(challenge)
        
        return outcome
    
    def _calculate_mitigation(self, challenge: Challenge,
                             player_actions: List[str],
                             game_state: Dict[str, Any]) -> float:
        """Calculate mitigation effectiveness based on player actions."""
        mitigation = 0.0
        
        # Check if player has implemented mitigation strategies
        for action in player_actions:
            action_lower = action.lower()
            for strategy in challenge.mitigation_strategies:
                if any(word in action_lower for word in strategy.lower().split()[:2]):
                    mitigation += 0.3
        
        # Check relevant resources
        if challenge.challenge_type == ChallengeType.ENVIRONMENTAL:
            if game_state.get("knowledge", 0) > 50:
                mitigation += 0.2
        elif challenge.challenge_type == ChallengeType.ENEMY:
            if game_state.get("reputation", 0) > 30:
                mitigation += 0.2
        elif challenge.challenge_type == ChallengeType.RESOURCE:
            if game_state.get("capital", 0) > 50000:
                mitigation += 0.2
        
        # Cap at 90% mitigation
        return min(0.9, mitigation)
    
    def _generate_challenge_narrative(self, challenge: Challenge,
                                      success: bool,
                                      mitigation_level: float) -> str:
        """Generate narrative for challenge resolution."""
        if success:
            templates = [
                f"You successfully navigated the {challenge.name}! Your preparation paid off.",
                f"The {challenge.name} was tough, but you managed it well.",
                f"Thanks to your proactive approach, the {challenge.name} had minimal impact.",
            ]
        else:
            templates = [
                f"The {challenge.name} hit hard. You'll need to recover from the setbacks.",
                f"You struggled with the {challenge.name}. Consider different strategies next time.",
                f"The {challenge.name} caused significant damage. Time to regroup.",
            ]
        
        return random.choice(templates)
    
    def _generate_lessons(self, challenge: Challenge, success: bool) -> List[str]:
        """Generate lessons learned from challenge."""
        lessons = []
        
        if success:
            lessons.append(f"Preparation is key to handling {challenge.challenge_type.value} challenges.")
            lessons.append(f"Implementing mitigation strategies reduces impact significantly.")
        else:
            lessons.append(f"Consider implementing mitigation strategies earlier.")
            lessons.append(f"Build reserves before challenges arise.")
        
        # Specific lessons by type
        if challenge.challenge_type == ChallengeType.ENEMY:
            lessons.append("Stay vigilant about compliance deadlines.")
        elif challenge.challenge_type == ChallengeType.RESOURCE:
            lessons.append("Maintain diverse resource options.")
        elif challenge.challenge_type == ChallengeType.ENVIRONMENTAL:
            lessons.append("Adapt quickly to changing conditions.")
        
        return lessons
    
    def get_active_challenges(self) -> List[Challenge]:
        """Get list of currently active challenges."""
        return self.active_challenges
    
    def get_mitigation_strategies(self, challenge_id: str) -> List[str]:
        """Get mitigation strategies for a challenge."""
        challenge = self.challenges.get(challenge_id)
        if challenge:
            return challenge.mitigation_strategies
        return []
    
    def get_challenge_outcomes_summary(self) -> Dict:
        """Get summary of all challenge outcomes."""
        total_outcomes = len(self.challenge_outcomes)
        successful = sum(1 for o in self.challenge_outcomes if o.success)
        
        total_lost = {}
        total_saved = {}
        
        for outcome in self.challenge_outcomes:
            for resource, amount in outcome.resources_lost.items():
                total_lost[resource] = total_lost.get(resource, 0) + amount
            for resource, amount in outcome.resources_saved.items():
                total_saved[resource] = total_saved.get(resource, 0) + amount
        
        return {
            "total_challenges": total_outcomes,
            "successful_resolutions": successful,
            "failed_resolutions": total_outcomes - successful,
            "success_rate": (successful / total_outcomes * 100) if total_outcomes > 0 else 0,
            "total_resources_lost": total_lost,
            "total_resources_saved": total_saved,
            "outcomes": [o.to_dict() for o in self.challenge_outcomes]
        }
    
    def reset(self):
        """Reset challenge system state."""
        for challenge in self.challenges.values():
            challenge.triggered = False
            challenge.turn_triggered = 0
            challenge.turn_resolved = 0
            challenge.mitigated = False
        
        self.active_challenges.clear()
        self.challenge_outcomes.clear()


def run_challenge_tests() -> Dict:
    """Run challenge system tests."""
    print("Running Challenge System Tests...")
    print("=" * 60)
    
    results = {
        "test_timestamp": datetime.now().isoformat(),
        "system_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "outcomes_tested": []
    }
    
    # Test 1: Initialize system
    print("\nTest 1: Initialize Challenge System")
    try:
        system = ChallengeSystem()
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Challenge System",
            "status": "PASSED",
            "details": f"Loaded {len(system.challenges)} challenges"
        })
        print(f"  PASSED: Loaded {len(system.challenges)} challenges")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Challenge System",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
        return results
    
    # Test 2: Challenge types
    print("\nTest 2: Challenge Types Distribution")
    try:
        types = {}
        for challenge in system.challenges.values():
            type_name = challenge.challenge_type.value
            types[type_name] = types.get(type_name, 0) + 1
        
        results["tests_run"] += 1
        if len(types) == 3:  # environmental, enemy, resource
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Challenge Types Distribution",
                "status": "PASSED",
                "details": f"Types: {types}"
            })
            print(f"  PASSED: All 3 challenge types present: {types}")
        else:
            raise ValueError(f"Missing challenge types: {types}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Types Distribution",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 3: Difficulty settings
    print("\nTest 3: Difficulty Settings")
    try:
        for difficulty in ["easy", "normal", "hard", "expert"]:
            system.set_difficulty(difficulty)
            settings = system.get_difficulty_settings()
            assert "challenge_frequency" in settings
            assert "severity_modifier" in settings
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Difficulty Settings",
            "status": "PASSED",
            "details": "All difficulty levels configured"
        })
        print("  PASSED: All difficulty levels configured")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Difficulty Settings",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 4: Generate challenge
    print("\nTest 4: Challenge Generation")
    try:
        system.set_difficulty("normal")
        game_state = {"current_phase": 2, "current_turn": 5, "reputation": 10}
        challenge = system.generate_challenge(2, game_state)
        
        results["tests_run"] += 1
        if challenge:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Challenge Generation",
                "status": "PASSED",
                "details": f"Generated: {challenge.name} ({challenge.severity.value})"
            })
            print(f"  PASSED: Generated {challenge.name} ({challenge.severity.value})")
        else:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Challenge Generation",
                "status": "PASSED",
                "details": "No challenge generated (within probability)"
            })
            print("  PASSED: No challenge generated (within probability)")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Generation",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 5: Apply challenge effects
    print("\nTest 5: Apply Challenge Effects")
    try:
        system.reset()
        challenge = system.challenges["fee_toll_bridges"]
        challenge.triggered = True
        
        game_state = {"capital": 10000, "time": 50}
        effects = system.apply_challenge_effects(challenge, game_state, mitigation_level=0.0)
        
        results["tests_run"] += 1
        if "capital" in effects and effects["capital"] < 0:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Apply Challenge Effects",
                "status": "PASSED",
                "details": f"Effects applied: {effects}"
            })
            print(f"  PASSED: Effects applied: {effects}")
        else:
            raise ValueError("Effects not applied correctly")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Apply Challenge Effects",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 6: Mitigation effectiveness
    print("\nTest 6: Mitigation Effectiveness")
    try:
        system.reset()
        challenge = system.challenges["fee_toll_bridges"]
        
        game_state = {"capital": 10000, "time": 50}
        effects_no_mitigation = system.apply_challenge_effects(challenge, game_state.copy(), 0.0)
        effects_with_mitigation = system.apply_challenge_effects(challenge, game_state.copy(), 0.5)
        
        results["tests_run"] += 1
        if abs(effects_with_mitigation["capital"]) < abs(effects_no_mitigation["capital"]):
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Mitigation Effectiveness",
                "status": "PASSED",
                "details": f"Without mitigation: {effects_no_mitigation}, With 50%: {effects_with_mitigation}"
            })
            print(f"  PASSED: Mitigation reduces effects")
        else:
            raise ValueError("Mitigation not working")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Mitigation Effectiveness",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 7: Resolve challenge
    print("\nTest 7: Challenge Resolution")
    try:
        system.reset()
        challenge = system.challenges["deadline_dragons"]
        challenge.triggered = True
        system.active_challenges.append(challenge)
        
        game_state = {"current_turn": 10, "capital": 10000, "reputation": 20}
        player_actions = ["Set calendar reminders", "Hired accountant"]
        
        outcome = system.resolve_challenge(challenge, player_actions, game_state)
        results["outcomes_tested"].append(outcome.to_dict())
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Resolution",
            "status": "PASSED",
            "details": f"Success: {outcome.success}, Narrative: {outcome.narrative[:50]}..."
        })
        print(f"  PASSED: Challenge resolved - Success: {outcome.success}")
        print(f"    Narrative: {outcome.narrative[:60]}...")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Resolution",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 8: Get mitigation strategies
    print("\nTest 8: Get Mitigation Strategies")
    try:
        strategies = system.get_mitigation_strategies("liability_leviathan")
        results["tests_run"] += 1
        if len(strategies) >= 2:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Get Mitigation Strategies",
                "status": "PASSED",
                "details": f"Strategies: {strategies}"
            })
            print(f"  PASSED: Found {len(strategies)} strategies")
        else:
            raise ValueError("No strategies found")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Get Mitigation Strategies",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 9: Challenge outcomes summary
    print("\nTest 9: Challenge Outcomes Summary")
    try:
        summary = system.get_challenge_outcomes_summary()
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Outcomes Summary",
            "status": "PASSED",
            "details": f"Total: {summary['total_challenges']}, Success rate: {summary['success_rate']:.1f}%"
        })
        print(f"  PASSED: {summary['total_challenges']} outcomes, {summary['success_rate']:.1f}% success")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Challenge Outcomes Summary",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 10: Multiple challenge scenarios
    print("\nTest 10: Multiple Challenge Scenarios")
    try:
        scenarios = [
            {"phase": 1, "turn": 2, "name": "Early Phase"},
            {"phase": 3, "turn": 15, "name": "Mid Game"},
            {"phase": 5, "turn": 30, "name": "Late Game"}
        ]
        
        outcomes = []
        for scenario in scenarios:
            system.reset()
            game_state = {"current_phase": scenario["phase"], "current_turn": scenario["turn"], "reputation": 20, "capital": 20000}
            
            # Generate and resolve challenges
            for _ in range(3):
                challenge = system.generate_challenge(scenario["phase"], game_state)
                if challenge:
                    outcome = system.resolve_challenge(challenge, ["took action"], game_state)
                    outcomes.append(outcome.to_dict())
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Multiple Challenge Scenarios",
            "status": "PASSED",
            "details": f"Tested {len(scenarios)} scenarios"
        })
        print(f"  PASSED: Tested {len(scenarios)} scenarios")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Multiple Challenge Scenarios",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 11: Severity scaling
    print("\nTest 11: Severity Scaling")
    try:
        system.set_difficulty("easy")
        easy_settings = system.get_difficulty_settings()
        
        system.set_difficulty("expert")
        expert_settings = system.get_difficulty_settings()
        
        results["tests_run"] += 1
        if expert_settings["challenge_frequency"] > easy_settings["challenge_frequency"]:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Severity Scaling",
                "status": "PASSED",
                "details": f"Easy freq: {easy_settings['challenge_frequency']}, Expert freq: {expert_settings['challenge_frequency']}"
            })
            print(f"  PASSED: Difficulty scaling works correctly")
        else:
            raise ValueError("Scaling not working")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Severity Scaling",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 12: System reset
    print("\nTest 12: System Reset")
    try:
        system.reset()
        active = system.get_active_challenges()
        results["tests_run"] += 1
        if len(active) == 0:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "System Reset",
                "status": "PASSED",
                "details": "System reset successfully"
            })
            print("  PASSED: System reset successfully")
        else:
            raise ValueError("Reset failed")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "System Reset",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run:    {results['tests_run']}")
    print(f"Tests Passed: {results['tests_passed']}")
    print(f"Tests Failed: {results['tests_failed']}")
    print(f"Pass Rate:    {results['tests_passed']/results['tests_run']*100:.1f}%")
    print(f"Outcomes Tested: {len(results['outcomes_tested'])}")
    
    results["summary"] = {
        "pass_rate": results['tests_passed']/results['tests_run']*100 if results['tests_run'] > 0 else 0,
        "total_tests": results['tests_run'],
        "outcomes_tested_count": len(results['outcomes_tested'])
    }
    
    return results


if __name__ == "__main__":
    # Run tests and save results
    test_results = run_challenge_tests()
    
    # Save test results
    output_path = Path(__file__).parent.parent / "processed" / "challenge_outcomes_test.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nTest results saved to: {output_path}")
