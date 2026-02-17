#!/usr/bin/env python3
"""
USA Business Journey - Tutorial System
Implements interactive tutorial flow, phase-specific messages,
hint system, and tutorial completion tracking.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path


class TutorialMessageType(Enum):
    """Types of tutorial messages."""
    INTRODUCTION = "introduction"
    PHASE_GUIDE = "phase_guide"
    ACTION_HINT = "action_hint"
    RESOURCE_TIP = "resource_tip"
    WARNING = "warning"
    MILESTONE = "milestone"
    COMPLETION = "completion"


class HintPriority(Enum):
    """Priority levels for hints."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OPTIONAL = "optional"


@dataclass
class TutorialMessage:
    """Represents a tutorial message."""
    message_id: str
    title: str
    content: str
    message_type: TutorialMessageType
    phase: int
    trigger: str
    priority: HintPriority
    shown: bool = False
    shown_count: int = 0
    last_shown: str = ""

    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "title": self.title,
            "content": self.content,
            "message_type": self.message_type.value,
            "phase": self.phase,
            "trigger": self.trigger,
            "priority": self.priority.value,
            "shown": self.shown,
            "shown_count": self.shown_count,
            "last_shown": self.last_shown
        }


@dataclass
class TutorialStep:
    """Represents a step in the tutorial flow."""
    step_id: str
    phase: int
    title: str
    description: str
    objectives: List[str]
    hints: List[str]
    completed: bool = False
    completion_time: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Hint:
    """Represents a contextual hint."""
    hint_id: str
    context: str
    hint_text: str
    priority: HintPriority
    phase_min: int
    phase_max: int
    prerequisites: List[str]
    shown: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TutorialProgress:
    """Tracks overall tutorial progress."""
    player_name: str
    tutorial_mode: bool
    current_phase: int
    completed_steps: List[str]
    total_steps: int
    hints_used: int
    hints_available: int
    completion_percentage: float
    started_at: str
    last_activity: str

    def to_dict(self) -> Dict:
        return asdict(self)


class TutorialSystem:
    """
    Tutorial system for the USA Business Journey simulation.
    Implements interactive tutorial flow, hints, and progress tracking.
    """

    def __init__(self):
        """Initialize the tutorial system."""
        self.base_path = Path(__file__).parent.parent / "processed"

        # Tutorial messages organized by phase
        self.messages: Dict[str, TutorialMessage] = {}
        self.tutorial_steps: Dict[int, List[TutorialStep]] = {}
        self.hints: Dict[str, Hint] = {}

        # Player progress
        self.current_progress: Optional[TutorialProgress] = None
        self.message_history: List[Dict] = []

        # Settings
        self.tutorial_enabled = True
        self.hint_frequency = "normal"  # low, normal, high

        self._initialize_tutorial_content()

    def _initialize_tutorial_content(self):
        """Initialize all tutorial content."""
        self._create_phase_messages()
        self._create_tutorial_steps()
        self._create_hints()

    def _create_phase_messages(self):
        """Create tutorial messages for each phase."""
        msg_id = 0

        # Phase 1: Planning Peaks
        phase1_messages = [
            ("Welcome to your business journey! Every successful business starts with a solid plan.",
             "Planning Peaks - Introduction", "introduction", "phase_1_start"),
            ("Market research helps you understand your customers and competition.",
             "Market Research Tip", "action_hint", "action_1_1"),
            ("A well-written business plan is your roadmap to success.",
             "Business Plan Guide", "phase_guide", "action_1_2"),
            ("Understanding your target market is crucial for success.",
             "Target Market Tip", "resource_tip", "market_research"),
        ]

        for content, title, msg_type, trigger in phase1_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=1,
                trigger=trigger,
                priority=HintPriority.MEDIUM
            )

        # Phase 2: Legal Labyrinth
        phase2_messages = [
            ("Choosing the right business structure affects taxes, liability, and growth.",
             "Business Structure Guide", "phase_guide", "phase_2_start"),
            ("LLCs offer liability protection with simpler taxation than corporations.",
             "LLC Benefits", "action_hint", "entity_selection"),
            ("An EIN is like a Social Security number for your business.",
             "EIN Explanation", "resource_tip", "ein_registration"),
            ("Operating agreements define ownership and management structure.",
             "Operating Agreement Tip", "action_hint", "operating_agreement"),
        ]

        for content, title, msg_type, trigger in phase2_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=2,
                trigger=trigger,
                priority=HintPriority.HIGH
            )

        # Phase 3: Compliance Canyon
        phase3_messages = [
            ("Licenses and permits vary by industry and location.",
             "Compliance Overview", "phase_guide", "phase_3_start"),
            ("Sales tax permits are required for selling physical goods.",
             "Sales Tax Tip", "action_hint", "sales_tax_permit"),
            ("Health and safety regulations protect you and your customers.",
             "Safety Compliance", "warning", "health_permits"),
            ("Keep all compliance documents organized and accessible.",
             "Document Organization", "resource_tip", "compliance_docs"),
        ]

        for content, title, msg_type, trigger in phase3_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=3,
                trigger=trigger,
                priority=HintPriority.HIGH
            )

        # Phase 4: Operations Ocean
        phase4_messages = [
            ("Setting up efficient operations is key to scaling your business.",
             "Operations Overview", "phase_guide", "phase_4_start"),
            ("Good accounting software saves time and prevents errors.",
             "Accounting Systems", "action_hint", "accounting_setup"),
            ("Insurance protects your business from unexpected events.",
             "Insurance Guide", "warning", "insurance_setup"),
            ("Building reliable supplier relationships ensures smooth operations.",
             "Supplier Management", "resource_tip", "supplier_setup"),
        ]

        for content, title, msg_type, trigger in phase4_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=4,
                trigger=trigger,
                priority=HintPriority.MEDIUM
            )

        # Phase 5: Growth Galaxy
        phase5_messages = [
            ("Sustainable growth balances expansion with financial health.",
             "Growth Strategy", "phase_guide", "phase_5_start"),
            ("Marketing helps you reach new customers and grow revenue.",
             "Marketing Tips", "action_hint", "marketing_strategy"),
            ("Consider different funding options for expansion.",
             "Funding Options", "resource_tip", "funding_search"),
            ("Building a strong team is essential for scaling.",
             "Team Building", "action_hint", "hiring_plan"),
        ]

        for content, title, msg_type, trigger in phase5_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=5,
                trigger=trigger,
                priority=HintPriority.MEDIUM
            )

        # General messages
        general_messages = [
            ("Monitor your capital closely - running out of money is the #1 reason businesses fail.",
             "Capital Warning", "warning", "capital_low"),
            ("Great job completing that action! Keep up the momentum.",
             "Action Complete", "milestone", "action_complete"),
            ("You've completed a major milestone! Your business is growing!",
             "Milestone Achieved", "milestone", "milestone_reached"),
            ("Congratulations on completing your business journey!",
             "Journey Complete", "completion", "game_complete"),
        ]

        for content, title, msg_type, trigger in general_messages:
            msg_id += 1
            self.messages[f"tut_{msg_id:03d}"] = TutorialMessage(
                message_id=f"tut_{msg_id:03d}",
                title=title,
                content=content,
                message_type=TutorialMessageType(msg_type),
                phase=0,  # Applies to all phases
                trigger=trigger,
                priority=HintPriority.HIGH if "Warning" in title else HintPriority.MEDIUM
            )

    def _create_tutorial_steps(self):
        """Create tutorial steps for each phase."""
        # Phase 1 steps
        self.tutorial_steps[1] = [
            TutorialStep(
                step_id="p1_step1",
                phase=1,
                title="Understand Your Business Idea",
                description="Start by clearly defining what your business will do and who it will serve.",
                objectives=[
                    "Define your product or service",
                    "Identify your target customers",
                    "Research your competition"
                ],
                hints=[
                    "Think about problems you can solve for customers",
                    "Look at similar businesses in your area",
                    "Consider what makes your idea unique"
                ]
            ),
            TutorialStep(
                step_id="p1_step2",
                phase=1,
                title="Conduct Market Research",
                description="Gather information about your market, customers, and competitors.",
                objectives=[
                    "Analyze market size and trends",
                    "Survey potential customers",
                    "Study competitor offerings"
                ],
                hints=[
                    "Use online resources like Census data",
                    "Talk to people in your target market",
                    "Visit competitor businesses or websites"
                ]
            ),
            TutorialStep(
                step_id="p1_step3",
                phase=1,
                title="Create Your Business Plan",
                description="Document your business strategy, operations, and financial projections.",
                objectives=[
                    "Write executive summary",
                    "Define marketing strategy",
                    "Create financial projections"
                ],
                hints=[
                    "Keep it concise but comprehensive",
                    "Be realistic with financial projections",
                    "Update your plan as you learn more"
                ]
            )
        ]

        # Phase 2 steps
        self.tutorial_steps[2] = [
            TutorialStep(
                step_id="p2_step1",
                phase=2,
                title="Choose Business Structure",
                description="Select the legal structure that best fits your business needs.",
                objectives=[
                    "Compare LLC, Corporation, and Sole Proprietorship",
                    "Consider tax implications",
                    "Evaluate liability protection needs"
                ],
                hints=[
                    "LLCs are popular for small businesses",
                    "Corporations are better for raising investment",
                    "Consider consulting a lawyer or accountant"
                ]
            ),
            TutorialStep(
                step_id="p2_step2",
                phase=2,
                title="Register Your Business",
                description="File the necessary paperwork to legally establish your business.",
                objectives=[
                    "File formation documents",
                    "Obtain EIN from IRS",
                    "Create operating agreement or bylaws"
                ],
                hints=[
                    "Many states allow online filing",
                    "EIN application is free on IRS.gov",
                    "Operating agreements protect all owners"
                ]
            )
        ]

        # Phase 3 steps
        self.tutorial_steps[3] = [
            TutorialStep(
                step_id="p3_step1",
                phase=3,
                title="Obtain Required Licenses",
                description="Get the licenses and permits needed to operate legally.",
                objectives=[
                    "Identify required licenses for your industry",
                    "Apply for business license",
                    "Obtain industry-specific permits"
                ],
                hints=[
                    "Check city, county, and state requirements",
                    "Some industries need federal permits",
                    "Keep copies of all applications"
                ]
            ),
            TutorialStep(
                step_id="p3_step2",
                phase=3,
                title="Set Up Tax Accounts",
                description="Register for tax accounts and understand your obligations.",
                objectives=[
                    "Register for state taxes",
                    "Set up sales tax account if needed",
                    "Understand employment taxes"
                ],
                hints=[
                    "Sales tax is required for physical goods",
                    "Keep business and personal finances separate",
                    "Consider quarterly estimated taxes"
                ]
            )
        ]

        # Phase 4 steps
        self.tutorial_steps[4] = [
            TutorialStep(
                step_id="p4_step1",
                phase=4,
                title="Set Up Operations",
                description="Establish the systems and processes to run your business.",
                objectives=[
                    "Set up accounting system",
                    "Establish banking relationships",
                    "Create operational procedures"
                ],
                hints=[
                    "QuickBooks and Xero are popular options",
                    "Business banking keeps finances separate",
                    "Document processes for consistency"
                ]
            ),
            TutorialStep(
                step_id="p4_step2",
                phase=4,
                title="Get Insured",
                description="Protect your business with appropriate insurance coverage.",
                objectives=[
                    "Assess insurance needs",
                    "Get general liability insurance",
                    "Consider industry-specific coverage"
                ],
                hints=[
                    "General liability is essential for most businesses",
                    "Professional liability for service businesses",
                    "Workers comp required with employees"
                ]
            )
        ]

        # Phase 5 steps
        self.tutorial_steps[5] = [
            TutorialStep(
                step_id="p5_step1",
                phase=5,
                title="Develop Growth Strategy",
                description="Plan how you will expand your business sustainably.",
                objectives=[
                    "Set growth targets",
                    "Identify expansion opportunities",
                    "Plan resource requirements"
                ],
                hints=[
                    "Grow at a pace you can manage",
                    "Consider new markets or products",
                    "Build capacity before you need it"
                ]
            ),
            TutorialStep(
                step_id="p5_step2",
                phase=5,
                title="Scale Your Business",
                description="Execute your growth plan and expand operations.",
                objectives=[
                    "Implement marketing campaigns",
                    "Hire and train team members",
                    "Optimize operations for scale"
                ],
                hints=[
                    "Hire for culture fit and skills",
                    "Automate repetitive tasks",
                    "Monitor cash flow carefully during growth"
                ]
            )
        ]

    def _create_hints(self):
        """Create contextual hints."""
        hint_id = 0

        # Resource hints
        resource_hints = [
            ("capital_low", "Your capital is running low. Consider cutting costs or seeking funding.",
             HintPriority.CRITICAL, 1, 5, []),
            ("time_pressure", "Time is limited. Focus on high-priority actions.",
             HintPriority.HIGH, 1, 5, []),
            ("knowledge_needed", "Build more knowledge before making major decisions.",
             HintPriority.MEDIUM, 1, 5, []),
        ]

        for context, text, priority, pmin, pmax, prereqs in resource_hints:
            hint_id += 1
            self.hints[f"hint_{hint_id:03d}"] = Hint(
                hint_id=f"hint_{hint_id:03d}",
                context=context,
                hint_text=text,
                priority=priority,
                phase_min=pmin,
                phase_max=pmax,
                prerequisites=prereqs
            )

        # Action hints
        action_hints = [
            ("first_action", "Click on an action to see more details and complete it.",
             HintPriority.HIGH, 1, 1, []),
            ("phase_complete", "All required actions complete! Advance to the next phase.",
             HintPriority.MEDIUM, 1, 5, ["first_action"]),
            ("compliance_drop", "Your compliance score dropped. Address pending requirements.",
             HintPriority.HIGH, 2, 5, []),
        ]

        for context, text, priority, pmin, pmax, prereqs in action_hints:
            hint_id += 1
            self.hints[f"hint_{hint_id:03d}"] = Hint(
                hint_id=f"hint_{hint_id:03d}",
                context=context,
                hint_text=text,
                priority=priority,
                phase_min=pmin,
                phase_max=pmax,
                prerequisites=prereqs
            )

    def start_tutorial(self, player_name: str, tutorial_mode: bool = True) -> TutorialProgress:
        """
        Start a new tutorial session.

        Args:
            player_name: Name of the player
            tutorial_mode: Whether tutorial mode is enabled

        Returns:
            TutorialProgress object
        """
        self.tutorial_enabled = tutorial_mode

        total_steps = sum(len(steps) for steps in self.tutorial_steps.values())

        now = datetime.now().isoformat()

        self.current_progress = TutorialProgress(
            player_name=player_name,
            tutorial_mode=tutorial_mode,
            current_phase=1,
            completed_steps=[],
            total_steps=total_steps,
            hints_used=0,
            hints_available=len(self.hints),
            completion_percentage=0.0,
            started_at=now,
            last_activity=now
        )

        return self.current_progress

    def get_message_for_trigger(self, trigger: str, current_phase: int) -> Optional[TutorialMessage]:
        """
        Get a tutorial message for a specific trigger.

        Args:
            trigger: The trigger event
            current_phase: Current game phase

        Returns:
            TutorialMessage or None
        """
        if not self.tutorial_enabled:
            return None

        for message in self.messages.values():
            if message.trigger == trigger:
                # Check phase applicability
                if message.phase > 0 and message.phase != current_phase:
                    continue

                # Update message state
                message.shown = True
                message.shown_count += 1
                message.last_shown = datetime.now().isoformat()

                # Record in history
                self.message_history.append({
                    "message_id": message.message_id,
                    "trigger": trigger,
                    "timestamp": message.last_shown
                })

                return message

        return None

    def get_phase_introduction(self, phase: int) -> Optional[TutorialMessage]:
        """Get introduction message for a phase."""
        trigger = f"phase_{phase}_start"
        return self.get_message_for_trigger(trigger, phase)

    def get_hint_for_context(self, context: str, current_phase: int) -> Optional[Hint]:
        """
        Get a hint for a specific context.

        Args:
            context: The context requiring a hint
            current_phase: Current game phase

        Returns:
            Hint or None
        """
        if not self.tutorial_enabled:
            return None

        for hint in self.hints.values():
            if hint.context == context:
                # Check phase range
                if not (hint.phase_min <= current_phase <= hint.phase_max):
                    continue

                # Check prerequisites
                prereqs_met = all(
                    any(h.context == p and h.shown for h in self.hints.values())
                    for p in hint.prerequisites
                ) if hint.prerequisites else True

                if prereqs_met:
                    hint.shown = True
                    if self.current_progress:
                        self.current_progress.hints_used += 1
                    return hint

        return None

    def get_contextual_hints(self, game_state: Dict[str, Any]) -> List[Hint]:
        """
        Get hints based on current game state.

        Args:
            game_state: Current game state

        Returns:
            List of relevant hints
        """
        if not self.tutorial_enabled:
            return []

        hints = []
        current_phase = game_state.get("current_phase", 1)

        # Check capital - resources are stored as dicts with 'current' key
        resources = game_state.get("resources", {})
        capital_data = resources.get("Capital", {})
        if isinstance(capital_data, dict):
            capital = capital_data.get("current", 10000)
        else:
            capital = capital_data  # Fallback if it's already a number
        
        starting_capital_data = game_state.get("starting_capital", 15000)
        if isinstance(starting_capital_data, dict):
            starting_capital = starting_capital_data.get("value", 15000)
        else:
            starting_capital = starting_capital_data

        if starting_capital > 0 and (capital / starting_capital) < 0.3:
            hint = self.get_hint_for_context("capital_low", current_phase)
            if hint:
                hints.append(hint)

        # Check compliance
        compliance = game_state.get("compliance_score", 100)
        if compliance < 70:
            hint = self.get_hint_for_context("compliance_drop", current_phase)
            if hint:
                hints.append(hint)

        # Check for first action
        completed_actions = game_state.get("completed_actions", [])
        if len(completed_actions) == 0:
            hint = self.get_hint_for_context("first_action", current_phase)
            if hint:
                hints.append(hint)

        return hints

    def get_tutorial_step(self, phase: int, step_id: str) -> Optional[TutorialStep]:
        """Get a specific tutorial step."""
        steps = self.tutorial_steps.get(phase, [])
        for step in steps:
            if step.step_id == step_id:
                return step
        return None

    def get_current_steps(self, phase: int) -> List[TutorialStep]:
        """Get all tutorial steps for a phase."""
        return self.tutorial_steps.get(phase, [])

    def complete_step(self, step_id: str) -> bool:
        """
        Mark a tutorial step as completed.

        Args:
            step_id: ID of the step to complete

        Returns:
            True if step was found and completed
        """
        if not self.current_progress:
            return False

        for phase, steps in self.tutorial_steps.items():
            for step in steps:
                if step.step_id == step_id:
                    step.completed = True
                    step.completion_time = datetime.now().isoformat()

                    if step_id not in self.current_progress.completed_steps:
                        self.current_progress.completed_steps.append(step_id)
                        self._update_completion_percentage()

                    self.current_progress.last_activity = datetime.now().isoformat()
                    return True

        return False

    def _update_completion_percentage(self):
        """Update tutorial completion percentage."""
        if not self.current_progress:
            return

        completed = len(self.current_progress.completed_steps)
        total = self.current_progress.total_steps
        self.current_progress.completion_percentage = (completed / total * 100) if total > 0 else 0

    def update_phase(self, new_phase: int):
        """Update current phase in tutorial progress."""
        if self.current_progress:
            self.current_progress.current_phase = new_phase
            self.current_progress.last_activity = datetime.now().isoformat()

    def get_progress(self) -> Optional[TutorialProgress]:
        """Get current tutorial progress."""
        return self.current_progress

    def get_tutorial_status(self) -> Dict:
        """Get comprehensive tutorial status."""
        if not self.current_progress:
            return {"enabled": self.tutorial_enabled}

        status = {
            "enabled": self.tutorial_enabled,
            "progress": self.current_progress.to_dict(),
            "current_phase_steps": [],
            "available_hints": 0,
            "unread_messages": 0
        }

        # Add current phase steps
        current_steps = self.get_current_steps(self.current_progress.current_phase)
        for step in current_steps:
            status["current_phase_steps"].append({
                "step_id": step.step_id,
                "title": step.title,
                "completed": step.completed
            })

        # Count available hints
        status["available_hints"] = sum(1 for h in self.hints.values() if not h.shown)

        # Count unread messages
        status["unread_messages"] = sum(1 for m in self.messages.values() if not m.shown)

        return status

    def get_help_topic(self, topic: str) -> Optional[Dict]:
        """
        Get help information for a specific topic.

        Args:
            topic: Help topic name

        Returns:
            Help information dictionary
        """
        help_topics = {
            "business_structures": {
                "title": "Business Structures",
                "content": """
                Choosing the right business structure is one of your first important decisions.

                • Sole Proprietorship: Simplest form, but no liability protection
                • LLC (Limited Liability Company): Liability protection with pass-through taxation
                • C-Corporation: Best for raising investment, but double taxation
                • S-Corporation: Pass-through taxation with corporate structure

                For most small businesses, an LLC provides the best balance of protection and simplicity.
                """,
                "related_actions": ["action_2_1", "action_2_2"]
            },
            "funding": {
                "title": "Funding Your Business",
                "content": """
                There are several ways to fund your business:

                • Bootstrapping: Using personal savings and revenue
                • Friends & Family: Early investment from personal network
                • Bank Loans: Traditional debt financing
                • SBA Loans: Government-backed loans with favorable terms
                • Angel Investors: High-net-worth individuals
                • Venture Capital: Institutional investment for high-growth companies

                Each option has trade-offs in terms of control, cost, and availability.
                """,
                "related_actions": ["action_5_1", "action_5_2"]
            },
            "compliance": {
                "title": "Staying Compliant",
                "content": """
                Compliance keeps your business legal and avoids penalties:

                • Annual Reports: Most states require yearly filings
                • Taxes: Federal, state, and local tax obligations
                • Licenses: Industry and location-specific permits
                • Employment Law: Requirements when hiring employees

                Set up reminders for all deadlines and keep good records.
                """,
                "related_actions": ["action_3_1", "action_3_2", "action_3_3"]
            },
            "resources": {
                "title": "Managing Resources",
                "content": """
                Your business has several key resources to manage:

                • Capital: Money for operations and growth
                • Time: Limited weeks to complete actions
                • Knowledge: Understanding of requirements grows with actions
                • Network: Professional connections that help your business
                • Reputation: Business credibility with customers and partners

                Balance spending on immediate needs with building long-term capacity.
                """,
                "related_actions": []
            }
        }

        return help_topics.get(topic)

    def get_all_help_topics(self) -> List[str]:
        """Get list of all available help topics."""
        return [
            "business_structures",
            "funding",
            "compliance",
            "resources"
        ]

    def reset(self):
        """Reset tutorial system state."""
        self.current_progress = None
        self.message_history.clear()

        # Reset message shown status
        for message in self.messages.values():
            message.shown = False
            message.shown_count = 0
            message.last_shown = ""

        # Reset hint shown status
        for hint in self.hints.values():
            hint.shown = False

        # Reset step completion
        for steps in self.tutorial_steps.values():
            for step in steps:
                step.completed = False
                step.completion_time = ""


def run_tutorial_tests() -> Dict:
    """Run tutorial system tests."""
    print("Running Tutorial System Tests...")
    print("=" * 60)

    results = {
        "test_timestamp": datetime.now().isoformat(),
        "system_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "flow_tested": []
    }

    try:
        # Test 1: Initialize tutorial system
        print("\nTest 1: Initialize Tutorial System")
        try:
            tutorial = TutorialSystem()
            results["tests_run"] += 1
            results["tests_passed"] += 1
            results["test_results"].append({
                "test_name": "Initialize Tutorial System",
                "status": "PASSED",
                "details": f"Loaded {len(tutorial.messages)} messages, {len(tutorial.hints)} hints"
            })
            print(f"  PASSED: Loaded {len(tutorial.messages)} messages, {len(tutorial.hints)} hints")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Initialize Tutorial System",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")
            return results

        # Test 2: Start tutorial
        print("\nTest 2: Start Tutorial")
        try:
            progress = tutorial.start_tutorial("TestPlayer", True)
            results["tests_run"] += 1
            if progress and progress.player_name == "TestPlayer":
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Start Tutorial",
                    "status": "PASSED",
                    "details": f"Tutorial started for {progress.player_name}"
                })
                print(f"  PASSED: Tutorial started")
                results["flow_tested"].append("start")
            else:
                raise ValueError("Tutorial start failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Start Tutorial",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 3: Get phase introduction
        print("\nTest 3: Get Phase Introduction")
        try:
            intro = tutorial.get_phase_introduction(1)
            results["tests_run"] += 1
            if intro and "Planning" in intro.title:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Phase Introduction",
                    "status": "PASSED",
                    "details": f"Got intro: {intro.title}"
                })
                print(f"  PASSED: Got intro: {intro.title}")
            else:
                raise ValueError("Phase introduction not found")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Phase Introduction",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 4: Get tutorial steps for phase
        print("\nTest 4: Get Tutorial Steps")
        try:
            steps = tutorial.get_current_steps(1)
            results["tests_run"] += 1
            if len(steps) >= 2:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Tutorial Steps",
                    "status": "PASSED",
                    "details": f"Found {len(steps)} steps for phase 1"
                })
                print(f"  PASSED: Found {len(steps)} steps for phase 1")
            else:
                raise ValueError("Not enough tutorial steps")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Tutorial Steps",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 5: Complete tutorial step
        print("\nTest 5: Complete Tutorial Step")
        try:
            success = tutorial.complete_step("p1_step1")
            results["tests_run"] += 1
            if success:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Complete Tutorial Step",
                    "status": "PASSED",
                    "details": "Step completed successfully"
                })
                print(f"  PASSED: Step completed")
                results["flow_tested"].append("step_complete")
            else:
                raise ValueError("Step completion failed")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Complete Tutorial Step",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 6: Get contextual hints
        print("\nTest 6: Get Contextual Hints")
        try:
            game_state = {
                "current_phase": 1,
                "resources": {"Capital": 2000},
                "starting_capital": 15000,
                "compliance_score": 95,
                "completed_actions": []
            }
            hints = tutorial.get_contextual_hints(game_state)
            results["tests_run"] += 1
            if len(hints) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Contextual Hints",
                    "status": "PASSED",
                    "details": f"Got {len(hints)} contextual hints"
                })
                print(f"  PASSED: Got {len(hints)} contextual hints")
            else:
                raise ValueError("No hints returned")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Contextual Hints",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 7: Get message for trigger
        print("\nTest 7: Get Message for Trigger")
        try:
            msg = tutorial.get_message_for_trigger("capital_low", 1)
            results["tests_run"] += 1
            if msg and "capital" in msg.content.lower():
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Message for Trigger",
                    "status": "PASSED",
                    "details": f"Got message: {msg.title}"
                })
                print(f"  PASSED: Got message: {msg.title}")
            else:
                raise ValueError("Message not found")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Message for Trigger",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 8: Update phase
        print("\nTest 8: Update Phase")
        try:
            tutorial.update_phase(2)
            results["tests_run"] += 1
            if tutorial.current_progress.current_phase == 2:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Update Phase",
                    "status": "PASSED",
                    "details": "Phase updated to 2"
                })
                print(f"  PASSED: Phase updated")
                results["flow_tested"].append("phase_change")
            else:
                raise ValueError("Phase not updated")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Update Phase",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 9: Get tutorial status
        print("\nTest 9: Get Tutorial Status")
        try:
            status = tutorial.get_tutorial_status()
            results["tests_run"] += 1
            if "enabled" in status and "progress" in status:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Tutorial Status",
                    "status": "PASSED",
                    "details": f"Completion: {status['progress']['completion_percentage']:.1f}%"
                })
                print(f"  PASSED: Completion: {status['progress']['completion_percentage']:.1f}%")
            else:
                raise ValueError("Status incomplete")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Tutorial Status",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 10: Get help topic
        print("\nTest 10: Get Help Topic")
        try:
            help_info = tutorial.get_help_topic("business_structures")
            results["tests_run"] += 1
            if help_info and "LLC" in help_info["content"]:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Get Help Topic",
                    "status": "PASSED",
                    "details": f"Got help: {help_info['title']}"
                })
                print(f"  PASSED: Got help: {help_info['title']}")
            else:
                raise ValueError("Help topic not found")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Get Help Topic",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 11: Tutorial disabled
        print("\nTest 11: Tutorial Disabled Mode")
        try:
            tutorial.tutorial_enabled = False
            msg = tutorial.get_message_for_trigger("phase_1_start", 1)
            results["tests_run"] += 1
            if msg is None:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Tutorial Disabled Mode",
                    "status": "PASSED",
                    "details": "Messages suppressed when disabled"
                })
                print(f"  PASSED: Messages suppressed when disabled")
            else:
                raise ValueError("Messages shown when disabled")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Tutorial Disabled Mode",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 12: Reset tutorial
        print("\nTest 12: Reset Tutorial")
        try:
            tutorial.reset()
            results["tests_run"] += 1
            if tutorial.current_progress is None:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Reset Tutorial",
                    "status": "PASSED",
                    "details": "Tutorial reset successfully"
                })
                print(f"  PASSED: Tutorial reset")
            else:
                raise ValueError("Tutorial not reset")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Reset Tutorial",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 13: Complete flow test
        print("\nTest 13: Complete Tutorial Flow")
        try:
            tutorial.start_tutorial("FlowTest", True)

            # Complete all phase 1 steps
            for step in tutorial.get_current_steps(1):
                tutorial.complete_step(step.step_id)

            # Move to phase 2
            tutorial.update_phase(2)
            for step in tutorial.get_current_steps(2):
                tutorial.complete_step(step.step_id)

            status = tutorial.get_tutorial_status()
            results["tests_run"] += 1
            if status["progress"]["completion_percentage"] > 30:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Complete Tutorial Flow",
                    "status": "PASSED",
                    "details": f"Flow completed: {status['progress']['completion_percentage']:.1f}%"
                })
                print(f"  PASSED: Flow completed: {status['progress']['completion_percentage']:.1f}%")
                results["flow_tested"].append("full_flow")
            else:
                raise ValueError("Flow completion incorrect")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Complete Tutorial Flow",
                "status": "FAILED",
                "error": str(e)
            })
            print(f"  FAILED: {e}")

        # Test 14: Message history
        print("\nTest 14: Message History Tracking")
        try:
            history = tutorial.message_history
            results["tests_run"] += 1
            if len(history) >= 1:
                results["tests_passed"] += 1
                results["test_results"].append({
                    "test_name": "Message History Tracking",
                    "status": "PASSED",
                    "details": f"History has {len(history)} entries"
                })
                print(f"  PASSED: History has {len(history)} entries")
            else:
                raise ValueError("No history recorded")
        except Exception as e:
            results["tests_run"] += 1
            results["tests_failed"] += 1
            results["test_results"].append({
                "test_name": "Message History Tracking",
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
    test_results = run_tutorial_tests()

    # Save test results
    output_path = Path(__file__).parent.parent / "processed" / "tutorial_flow_test.json"
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)

    print(f"\nTest results saved to: {output_path}")
