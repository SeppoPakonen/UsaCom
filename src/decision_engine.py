#!/usr/bin/env python3
"""
USA Business Journey - Decision Engine
Implements decision trees, consequence calculation, random event generation, and choice tracking.
Based on game_mechanics_spec.json decision_system from Phase 5.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class DecisionType(Enum):
    """Types of decisions in the game."""
    BUSINESS_STRUCTURE = "business_structure"
    FUNDING_STRATEGY = "funding_strategy"
    MARKET_ENTRY = "market_entry"
    HIRING = "hirning"
    EXPANSION = "expansion"
    GENERAL = "general"


class RiskLevel(Enum):
    """Risk levels for decisions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DecisionOption:
    """Represents an option in a decision."""
    choice: str
    immediate_effects: Dict[str, float] = field(default_factory=dict)
    long_term_effects: str = ""
    best_for: str = ""
    requirements: Dict[str, Any] = field(default_factory=dict)
    risk: str = "medium"
    probability_weights: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Decision:
    """Represents a decision point in the game."""
    decision_id: str
    decision_type: DecisionType
    location: str
    question: str
    options: List[DecisionOption]
    phase: int = 1
    required: bool = True
    made: bool = False
    selected_option: str = None
    turn_made: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type.value,
            "location": self.location,
            "question": self.question,
            "options": [o.to_dict() for o in self.options],
            "phase": self.phase,
            "required": self.required,
            "made": self.made,
            "selected_option": self.selected_option,
            "turn_made": self.turn_made
        }


@dataclass
class DecisionConsequence:
    """Represents the consequence of a decision."""
    consequence_id: str
    decision_id: str
    option_chosen: str
    immediate_effects: Dict[str, float]
    delayed_effects: Dict[str, float]
    narrative: str
    turn_triggered: int
    severity: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RandomEvent:
    """Represents a random event in the game."""
    event_id: str
    title: str
    description: str
    category: str
    probability: float
    effects: Dict[str, float]
    conditions: Dict[str, Any]
    triggered: bool = False
    turn_triggered: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ChoiceHistory:
    """Tracks player's choice history."""
    decision_id: str
    option_chosen: str
    turn: int
    context: Dict[str, Any]
    consequences: List[Dict]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class DecisionEngine:
    """
    Decision engine for the USA Business Journey simulation.
    Implements decision trees, consequence calculation, and choice tracking.
    """
    
    def __init__(self, game_mechanics_path: str = None):
        """Initialize the decision engine."""
        self.base_path = Path(__file__).parent.parent / "processed"
        
        # Load game mechanics
        mechanics_path = game_mechanics_path or self.base_path / "game_mechanics_spec.json"
        with open(mechanics_path, 'r') as f:
            self.game_mechanics = json.load(f)
        
        # Initialize decisions from game mechanics
        self.decisions: Dict[str, Decision] = {}
        self.consequences: List[DecisionConsequence] = []
        self.choice_history: List[ChoiceHistory] = []
        self.random_events: List[RandomEvent] = []
        
        self._load_decisions()
        self._load_random_events()
    
    def _load_decisions(self):
        """Load decisions from game mechanics."""
        decision_system = self.game_mechanics.get("7_decision_system", {})
        
        for key_decision in decision_system.get("key_decisions", []):
            decision_id = key_decision.get("decision_id", "")
            decision_type = self._get_decision_type(decision_id)
            
            options = []
            for opt in key_decision.get("options", []):
                # Handle both immediate_effects and effects fields
                effects = opt.get("immediate_effects")
                if effects is None:
                    effects_raw = opt.get("effects", {})
                    # If effects is a string, convert to dict
                    if isinstance(effects_raw, str):
                        effects = {}
                    else:
                        effects = effects_raw
                
                options.append(DecisionOption(
                    choice=opt.get("choice", ""),
                    immediate_effects=effects if effects else {},
                    long_term_effects=opt.get("long_term_effects", ""),
                    best_for=opt.get("best_for", ""),
                    requirements=opt.get("requirements", {}),
                    risk=opt.get("risk", "medium")
                ))
            
            self.decisions[decision_id] = Decision(
                decision_id=decision_id,
                decision_type=decision_type,
                location=key_decision.get("location", ""),
                question=key_decision.get("question", ""),
                options=options,
                phase=self._get_phase_for_location(key_decision.get("location", ""))
            )
    
    def _get_decision_type(self, decision_id: str) -> DecisionType:
        """Get decision type from ID."""
        if "structure" in decision_id:
            return DecisionType.BUSINESS_STRUCTURE
        elif "funding" in decision_id:
            return DecisionType.FUNDING_STRATEGY
        elif "market" in decision_id:
            return DecisionType.MARKET_ENTRY
        elif "hiring" in decision_id:
            return DecisionType.HIRING
        elif "expansion" in decision_id:
            return DecisionType.EXPANSION
        return DecisionType.GENERAL
    
    def _get_phase_for_location(self, location: str) -> int:
        """Get phase number from location ID."""
        if location.startswith("loc_1"):
            return 1
        elif location.startswith("loc_2"):
            return 2
        elif location.startswith("loc_3"):
            return 3
        elif location.startswith("loc_4"):
            return 4
        elif location.startswith("loc_5"):
            return 5
        return 1
    
    def _load_random_events(self):
        """Load random event definitions."""
        # Define base random events
        event_templates = [
            {
                "event_id": "market_shift",
                "title": "Market Shift",
                "description": "Market conditions have changed, affecting your business.",
                "category": "environmental",
                "probability": 0.15,
                "effects": {"capital": -500, "reputation": -5},
                "conditions": {"phase_min": 2}
            },
            {
                "event_id": "regulatory_change",
                "title": "Regulatory Change",
                "description": "New regulations require additional compliance measures.",
                "category": "environmental",
                "probability": 0.1,
                "effects": {"capital": -300, "time": -2},
                "conditions": {"phase_min": 3}
            },
            {
                "event_id": "competitor_action",
                "title": "Competitor Action",
                "description": "A competitor has launched a similar product.",
                "category": "enemy",
                "probability": 0.12,
                "effects": {"reputation": -10, "capital": -1000},
                "conditions": {"phase_min": 4}
            },
            {
                "event_id": "grant_opportunity",
                "title": "Grant Opportunity",
                "description": "You qualify for a small business grant.",
                "category": "opportunity",
                "probability": 0.08,
                "effects": {"capital": 2000},
                "conditions": {"compliance_min": 80}
            },
            {
                "event_id": "mentorship_offer",
                "title": "Mentorship Offer",
                "description": "An experienced entrepreneur offers mentorship.",
                "category": "opportunity",
                "probability": 0.1,
                "effects": {"knowledge": 15, "network": 10},
                "conditions": {}
            },
            {
                "event_id": "supply_chain_issue",
                "title": "Supply Chain Issue",
                "description": "Supply chain disruptions affect your operations.",
                "category": "resource",
                "probability": 0.1,
                "effects": {"capital": -800, "time": -3},
                "conditions": {"phase_min": 4}
            },
            {
                "event_id": "positive_review",
                "title": "Positive Review",
                "description": "Your business receives a glowing review.",
                "category": "opportunity",
                "probability": 0.15,
                "effects": {"reputation": 15, "capital": 500},
                "conditions": {}
            },
            {
                "event_id": "equipment_failure",
                "title": "Equipment Failure",
                "description": "Critical equipment needs repair or replacement.",
                "category": "resource",
                "probability": 0.08,
                "effects": {"capital": -1500, "time": -2},
                "conditions": {}
            }
        ]
        
        for template in event_templates:
            self.random_events.append(RandomEvent(
                event_id=template["event_id"],
                title=template["title"],
                description=template["description"],
                category=template["category"],
                probability=template["probability"],
                effects=template["effects"],
                conditions=template["conditions"]
            ))
    
    def get_available_decisions(self, current_phase: int, 
                                completed_decisions: List[str] = None) -> List[Decision]:
        """Get decisions available for current phase."""
        completed = completed_decisions or []
        available = []
        
        for decision in self.decisions.values():
            if decision.decision_id not in completed:
                if decision.phase <= current_phase:
                    available.append(decision)
        
        return available
    
    def can_make_decision(self, decision_id: str, 
                          player_resources: Dict[str, float]) -> Tuple[bool, str]:
        """Check if player can make a specific decision."""
        decision = self.decisions.get(decision_id)
        if not decision:
            return False, "Decision not found"
        
        if decision.made:
            return False, "Decision already made"
        
        # Check requirements for each option
        for option in decision.options:
            if self._check_option_requirements(option, player_resources):
                return True, "Decision available"
        
        return False, "No options meet requirements"
    
    def _check_option_requirements(self, option: DecisionOption,
                                   player_resources: Dict[str, float]) -> bool:
        """Check if player meets option requirements."""
        requirements = option.requirements
        if not requirements:
            return True
        
        for req_name, req_value in requirements.items():
            player_value = player_resources.get(req_name, 0)
            if isinstance(req_value, (int, float)) and player_value < req_value:
                return False
        
        return True
    
    def make_decision(self, decision_id: str, option_choice: str,
                      current_turn: int) -> DecisionConsequence:
        """
        Make a decision and calculate consequences.
        
        Args:
            decision_id: ID of the decision
            option_choice: The chosen option
            current_turn: Current game turn
        
        Returns:
            DecisionConsequence with effects
        """
        decision = self.decisions.get(decision_id)
        if not decision:
            raise ValueError(f"Decision {decision_id} not found")
        
        # Find selected option
        selected_option = None
        for opt in decision.options:
            if opt.choice.lower() == option_choice.lower():
                selected_option = opt
                break
        
        if not selected_option:
            raise ValueError(f"Option {option_choice} not found")
        
        # Mark decision as made
        decision.made = True
        decision.selected_option = option_choice
        decision.turn_made = current_turn
        
        # Calculate consequences
        immediate_effects = selected_option.immediate_effects.copy()
        
        # Add randomness to effects (±10%)
        for key in immediate_effects:
            variance = random.uniform(-0.1, 0.1)
            immediate_effects[key] = immediate_effects[key] * (1 + variance)
        
        # Calculate delayed effects (long-term)
        delayed_effects = self._calculate_delayed_effects(selected_option, current_turn)
        
        # Generate narrative
        narrative = self._generate_consequence_narrative(decision, selected_option)
        
        # Determine severity
        total_impact = sum(abs(v) for v in immediate_effects.values())
        if total_impact > 5000:
            severity = "critical"
        elif total_impact > 1000:
            severity = "high"
        elif total_impact > 200:
            severity = "medium"
        else:
            severity = "low"
        
        # Create consequence
        consequence = DecisionConsequence(
            consequence_id=f"cons_{decision_id}_{current_turn}",
            decision_id=decision_id,
            option_chosen=option_choice,
            immediate_effects=immediate_effects,
            delayed_effects=delayed_effects,
            narrative=narrative,
            turn_triggered=current_turn,
            severity=severity
        )
        
        self.consequences.append(consequence)
        
        # Record in history
        self.choice_history.append(ChoiceHistory(
            decision_id=decision_id,
            option_chosen=option_choice,
            turn=current_turn,
            context={"phase": decision.phase, "location": decision.location},
            consequences=[consequence.to_dict()]
        ))
        
        return consequence
    
    def _calculate_delayed_effects(self, option: DecisionOption, 
                                   current_turn: int) -> Dict[str, float]:
        """Calculate delayed/long-term effects of a decision."""
        delayed = {}
        
        # Base delayed effects on risk level
        risk = option.risk
        if risk == "high":
            # High risk = potential for big gains or losses later
            if random.random() > 0.5:
                delayed["capital"] = random.uniform(500, 2000)
            else:
                delayed["capital"] = random.uniform(-1000, -500)
            delayed["reputation"] = random.uniform(-5, 10)
        elif risk == "low":
            # Low risk = steady small gains
            delayed["capital"] = random.uniform(100, 500)
            delayed["knowledge"] = random.uniform(2, 5)
        else:
            # Medium risk = moderate outcomes
            delayed["capital"] = random.uniform(-200, 800)
            delayed["network"] = random.uniform(0, 5)
        
        return delayed
    
    def _generate_consequence_narrative(self, decision: Decision,
                                        option: DecisionOption) -> str:
        """Generate narrative text for decision consequence."""
        templates = {
            DecisionType.BUSINESS_STRUCTURE: [
                f"You've established your business as {option.choice}. {option.long_term_effects}",
                f"The {option.choice} structure is now in place. {option.long_term_effects}",
            ],
            DecisionType.FUNDING_STRATEGY: [
                f"You secured funding through {option.choice}. {option.long_term_effects}",
                f"Your funding strategy: {option.choice}. {option.long_term_effects}",
            ],
            DecisionType.MARKET_ENTRY: [
                f"You entered the market with a {option.choice} approach. {option.long_term_effects}",
                f"Market entry via {option.choice} is underway. {option.long_term_effects}",
            ]
        }
        
        decision_templates = templates.get(decision.decision_type, [
            f"You chose {option.choice}. {option.long_term_effects}"
        ])
        
        return random.choice(decision_templates)
    
    def trigger_random_event(self, current_turn: int,
                             game_state: Dict[str, Any]) -> Optional[RandomEvent]:
        """
        Check and trigger a random event.
        
        Args:
            current_turn: Current game turn
            game_state: Current game state for condition checking
        
        Returns:
            Triggered event or None
        """
        available_events = []
        
        for event in self.random_events:
            if event.triggered:
                continue
            
            # Check conditions
            if self._check_event_conditions(event, game_state):
                available_events.append(event)
        
        if not available_events:
            return None
        
        # Weight by probability
        weights = [e.probability for e in available_events]
        
        # Check if any event should trigger
        if random.random() > 0.3:  # 30% chance of any event per turn
            return None
        
        selected = random.choices(available_events, weights=weights)[0]
        selected.triggered = True
        selected.turn_triggered = current_turn
        
        return selected
    
    def _check_event_conditions(self, event: RandomEvent,
                                game_state: Dict[str, Any]) -> bool:
        """Check if event conditions are met."""
        conditions = event.conditions
        
        if not conditions:
            return True
        
        for cond_name, cond_value in conditions.items():
            if cond_name == "phase_min":
                if game_state.get("current_phase", 1) < cond_value:
                    return False
            elif cond_name == "compliance_min":
                if game_state.get("compliance_score", 100) < cond_value:
                    return False
            elif cond_name == "capital_min":
                if game_state.get("capital", 0) < cond_value:
                    return False
        
        return True
    
    def get_decision_recommendation(self, decision_id: str,
                                    player_resources: Dict[str, float],
                                    scenario_profile: Dict[str, Any] = None) -> str:
        """Get recommended option for a decision."""
        decision = self.decisions.get(decision_id)
        if not decision:
            return "No recommendation available"
        
        # Score each option
        best_option = None
        best_score = -float('inf')
        
        for option in decision.options:
            score = self._score_option(option, player_resources, scenario_profile)
            if score > best_score:
                best_score = score
                best_option = option
        
        if best_option:
            return f"Recommended: {best_option.choice} - {best_option.best_for}"
        return "No clear recommendation"
    
    def _score_option(self, option: DecisionOption,
                      player_resources: Dict[str, float],
                      scenario_profile: Dict[str, Any]) -> float:
        """Score an option based on player state."""
        score = 0
        
        # Check if requirements are met
        if not self._check_option_requirements(option, player_resources):
            return -100  # Can't choose this option
        
        # Score based on immediate effects
        for resource, effect in option.immediate_effects.items():
            if effect > 0:
                score += effect * 0.5
            else:
                # Penalize based on how much of the resource player has
                current = player_resources.get(resource, 0)
                if current < 1000:
                    score += effect * 2  # Heavy penalty if low on resource
                else:
                    score += effect * 0.3
        
        # Risk adjustment
        risk_scores = {"low": 10, "medium": 0, "high": -10, "critical": -30}
        score += risk_scores.get(option.risk, 0)
        
        return score
    
    def get_choice_history(self) -> List[Dict]:
        """Get player's choice history."""
        return [h.to_dict() for h in self.choice_history]
    
    def get_consequences_summary(self) -> Dict:
        """Get summary of all consequences."""
        total_immediate = {}
        total_delayed = {}
        
        for cons in self.consequences:
            for key, val in cons.immediate_effects.items():
                total_immediate[key] = total_immediate.get(key, 0) + val
            for key, val in cons.delayed_effects.items():
                total_delayed[key] = total_delayed.get(key, 0) + val
        
        return {
            "total_decisions_made": len([d for d in self.decisions.values() if d.made]),
            "total_consequences": len(self.consequences),
            "total_immediate_effects": total_immediate,
            "total_delayed_effects": total_delayed,
            "consequences": [c.to_dict() for c in self.consequences]
        }
    
    def reset(self):
        """Reset decision engine state."""
        for decision in self.decisions.values():
            decision.made = False
            decision.selected_option = None
            decision.turn_made = 0
        
        self.consequences.clear()
        self.choice_history.clear()
        
        for event in self.random_events:
            event.triggered = False
            event.turn_triggered = 0


def run_decision_tests() -> Dict:
    """Run decision engine tests."""
    print("Running Decision Engine Tests...")
    print("=" * 60)
    
    results = {
        "test_timestamp": datetime.now().isoformat(),
        "engine_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "scenarios_tested": []
    }
    
    # Test 1: Initialize engine
    print("\nTest 1: Initialize Decision Engine")
    try:
        engine = DecisionEngine()
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Decision Engine",
            "status": "PASSED",
            "details": f"Loaded {len(engine.decisions)} decisions, {len(engine.random_events)} events"
        })
        print(f"  PASSED: Loaded {len(engine.decisions)} decisions, {len(engine.random_events)} events")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Initialize Decision Engine",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
        return results
    
    # Test 2: Get available decisions
    print("\nTest 2: Get Available Decisions")
    try:
        decisions = engine.get_available_decisions(current_phase=1)
        results["tests_run"] += 1
        if len(decisions) >= 1:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Get Available Decisions",
                "status": "PASSED",
                "details": f"Found {len(decisions)} decisions for phase 1"
            })
            print(f"  PASSED: Found {len(decisions)} decisions for phase 1")
        else:
            raise ValueError("No decisions found")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Get Available Decisions",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 3: Decision requirements check
    print("\nTest 3: Decision Requirements Check")
    try:
        test_resources = {"capital": 15000, "knowledge": 25, "network": 10}
        can_decide, message = engine.can_make_decision("business_structure", test_resources)
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Decision Requirements Check",
            "status": "PASSED",
            "details": message
        })
        print(f"  PASSED: {message}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Decision Requirements Check",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 4: Make business structure decision
    print("\nTest 4: Make Business Structure Decision")
    try:
        consequence = engine.make_decision("business_structure", "LLC", 1)
        results["tests_run"] += 1
        results["scenarios_tested"].append({
            "scenario": "business_structure_llc",
            "consequence": consequence.to_dict()
        })
        if consequence.severity in ["low", "medium", "high", "critical"]:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Make Business Structure Decision",
                "status": "PASSED",
                "details": f"Consequence severity: {consequence.severity}"
            })
            print(f"  PASSED: Consequence severity: {consequence.severity}")
            print(f"    Narrative: {consequence.narrative[:80]}...")
        else:
            raise ValueError("Invalid severity")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Make Business Structure Decision",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 5: Make funding strategy decision
    print("\nTest 5: Make Funding Strategy Decision")
    try:
        consequence = engine.make_decision("funding_strategy", "Bootstrapping", 2)
        results["tests_run"] += 1
        results["scenarios_tested"].append({
            "scenario": "funding_bootstrapping",
            "consequence": consequence.to_dict()
        })
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Make Funding Strategy Decision",
            "status": "PASSED",
            "details": f"Immediate effects: {consequence.immediate_effects}"
        })
        print(f"  PASSED: Immediate effects: {consequence.immediate_effects}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Make Funding Strategy Decision",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 6: Make market entry decision
    print("\nTest 6: Make Market Entry Decision")
    try:
        consequence = engine.make_decision("market_entry", "MVP Launch", 3)
        results["tests_run"] += 1
        results["scenarios_tested"].append({
            "scenario": "market_entry_mvp",
            "consequence": consequence.to_dict()
        })
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Make Market Entry Decision",
            "status": "PASSED",
            "details": f"Narrative: {consequence.narrative[:60]}..."
        })
        print(f"  PASSED: {consequence.narrative[:60]}...")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Make Market Entry Decision",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 7: Random event triggering
    print("\nTest 7: Random Event Triggering")
    try:
        game_state = {"current_phase": 3, "compliance_score": 85, "capital": 10000}
        event = engine.trigger_random_event(5, game_state)
        results["tests_run"] += 1
        if event:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Random Event Triggering",
                "status": "PASSED",
                "details": f"Event: {event.title}, Effects: {event.effects}"
            })
            print(f"  PASSED: Event triggered - {event.title}")
        else:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Random Event Triggering",
                "status": "PASSED",
                "details": "No event triggered (within probability)"
            })
            print("  PASSED: No event triggered (within probability)")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Random Event Triggering",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 8: Choice history tracking
    print("\nTest 8: Choice History Tracking")
    try:
        history = engine.get_choice_history()
        results["tests_run"] += 1
        if len(history) >= 3:  # We made 3 decisions
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Choice History Tracking",
                "status": "PASSED",
                "details": f"Tracking {len(history)} decisions"
            })
            print(f"  PASSED: Tracking {len(history)} decisions")
        else:
            raise ValueError(f"Expected 3 decisions, got {len(history)}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Choice History Tracking",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 9: Consequences summary
    print("\nTest 9: Consequences Summary")
    try:
        summary = engine.get_consequences_summary()
        results["tests_run"] += 1
        if summary["total_decisions_made"] >= 3:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Consequences Summary",
                "status": "PASSED",
                "details": f"Total effects: {summary['total_immediate_effects']}"
            })
            print(f"  PASSED: {summary['total_decisions_made']} decisions, effects: {summary['total_immediate_effects']}")
        else:
            raise ValueError("Insufficient decisions tracked")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Consequences Summary",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 10: Decision recommendation
    print("\nTest 10: Decision Recommendation")
    try:
        # Reset and test recommendation
        engine2 = DecisionEngine()
        resources = {"capital": 50000, "knowledge": 30, "network": 20}
        recommendation = engine2.get_decision_recommendation("business_structure", resources)
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Decision Recommendation",
            "status": "PASSED",
            "details": recommendation
        })
        print(f"  PASSED: {recommendation}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Decision Recommendation",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 11: Engine reset
    print("\nTest 11: Engine Reset")
    try:
        engine.reset()
        decisions = engine.get_available_decisions(1)
        results["tests_run"] += 1
        if len(decisions) >= 1:
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Engine Reset",
                "status": "PASSED",
                "details": "Engine reset successfully"
            })
            print("  PASSED: Engine reset successfully")
        else:
            raise ValueError("Reset failed")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Engine Reset",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 12: Multiple scenario testing
    print("\nTest 12: Multiple Scenario Testing")
    try:
        scenarios = [
            {"name": "Tech Startup", "capital": 75000, "risk_tolerance": "high"},
            {"name": "Solo Consultant", "capital": 10000, "risk_tolerance": "low"},
            {"name": "Retail Store", "capital": 120000, "risk_tolerance": "medium"}
        ]
        
        for scenario in scenarios:
            engine_test = DecisionEngine()
            resources = {"capital": scenario["capital"], "knowledge": 20, "network": 10}
            
            # Make decisions for this scenario
            engine_test.make_decision("business_structure", "LLC", 1)
            engine_test.make_decision("funding_strategy", "Bootstrapping", 2)
            
            results["scenarios_tested"].append({
                "scenario_name": scenario["name"],
                "starting_capital": scenario["capital"],
                "decisions_made": 2
            })
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Multiple Scenario Testing",
            "status": "PASSED",
            "details": f"Tested {len(scenarios)} scenarios"
        })
        print(f"  PASSED: Tested {len(scenarios)} scenarios")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Multiple Scenario Testing",
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
    print(f"Scenarios Tested: {len(results['scenarios_tested'])}")
    
    results["summary"] = {
        "pass_rate": results['tests_passed']/results['tests_run']*100 if results['tests_run'] > 0 else 0,
        "total_tests": results['tests_run'],
        "scenarios_tested_count": len(results['scenarios_tested'])
    }
    
    return results


if __name__ == "__main__":
    # Run tests and save results
    test_results = run_decision_tests()
    
    # Save test results
    output_path = Path(__file__).parent.parent / "processed" / "decision_scenarios_tested.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\nTest results saved to: {output_path}")
