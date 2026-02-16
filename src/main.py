#!/usr/bin/env python3
"""
USA Business Journey - Main Entry Point
Integrates all game modules and provides the main game loop.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from game_engine import GameEngine, GameState
from game_ui import GameUI, UIComponent, Colors
from scenario_runner import ScenarioRunner, ScenarioStatus
from save_system import SaveSystem, SaveSlotStatus
from tutorial_system import TutorialSystem
from analytics_system import AnalyticsSystem
from decision_engine import DecisionEngine
from challenge_system import ChallengeSystem
from assessment_integration import AssessmentIntegration


class GameConfig:
    """Game configuration management."""

    DEFAULT_CONFIG = {
        "tutorial_enabled": True,
        "auto_save_enabled": True,
        "auto_save_interval": 5,
        "hint_frequency": "normal",
        "difficulty": "normal",
        "sound_enabled": False,
        "analytics_enabled": True,
        "default_scenario": "SCN002"
    }

    def __init__(self, config_path: str = None):
        """Initialize configuration."""
        self.base_path = Path(__file__).parent.parent
        self.config_path = Path(config_path) if config_path else self.base_path / "game_config.json"
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception:
                pass

    def save_config(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Set configuration value."""
        self.config[key] = value
        self.save_config()


class UsaComGame:
    """
    Main game class integrating all modules.
    """

    def __init__(self, config: GameConfig = None):
        """Initialize the game."""
        self.config = config or GameConfig()

        # Initialize all systems
        self.game_engine: Optional[GameEngine] = None
        self.scenario_runner: Optional[ScenarioRunner] = None
        self.save_system: Optional[SaveSystem] = None
        self.tutorial_system: Optional[TutorialSystem] = None
        self.analytics_system: Optional[AnalyticsSystem] = None
        self.decision_engine: Optional[DecisionEngine] = None
        self.challenge_system: Optional[ChallengeSystem] = None
        self.assessment_system: Optional[AssessmentIntegration] = None
        self.ui: Optional[GameUI] = None

        # Game state
        self.running = False
        self.player_name = ""
        self.current_scenario_id = ""

        self._initialize_systems()

    def _initialize_systems(self):
        """Initialize all game systems."""
        try:
            # Core systems
            self.game_engine = GameEngine()
            self.scenario_runner = ScenarioRunner()
            self.save_system = SaveSystem()
            self.tutorial_system = TutorialSystem()
            self.analytics_system = AnalyticsSystem()
            self.decision_engine = DecisionEngine()
            self.challenge_system = ChallengeSystem()
            self.assessment_system = AssessmentIntegration()
            self.ui = GameUI()

            # Apply configuration
            self.challenge_system.set_difficulty(self.config.get("difficulty", "normal"))
            self.save_system.set_auto_save_enabled(self.config.get("auto_save_enabled", True))
            self.tutorial_system.tutorial_enabled = self.config.get("tutorial_enabled", True)

        except Exception as e:
            print(f"{Colors.BRIGHT_RED}Error initializing game systems: {e}{Colors.RESET}")
            raise

    def start_new_game(self, player_name: str, scenario_id: str,
                       difficulty: str = "normal") -> bool:
        """
        Start a new game.

        Args:
            player_name: Name of the player
            scenario_id: Scenario ID to play
            difficulty: Game difficulty

        Returns:
            True if game started successfully
        """
        try:
            self.player_name = player_name
            self.current_scenario_id = scenario_id

            # Start scenario
            scenario_state = self.scenario_runner.start_scenario(scenario_id, player_name, difficulty)

            # Start game engine
            self.game_engine.new_game(player_name, scenario_id, difficulty)

            # Start tutorial
            self.tutorial_system.start_tutorial(player_name, self.config.get("tutorial_enabled", True))

            # Start analytics session
            self.analytics_system.start_session(player_name, scenario_id, 0, 0)

            # Initialize challenge system
            self.challenge_system.set_difficulty(difficulty)

            UIComponent.print_success(f"Welcome, {player_name}! Starting {scenario_state.scenario_name}...")
            return True

        except Exception as e:
            UIComponent.print_error(f"Failed to start game: {e}")
            return False

    def load_game(self, slot_id: int) -> bool:
        """
        Load a saved game.

        Args:
            slot_id: Save slot ID

        Returns:
            True if game loaded successfully
        """
        try:
            snapshot, message = self.save_system.load_game(slot_id)

            if not snapshot:
                UIComponent.print_error(f"Failed to load: {message}")
                return False

            self.player_name = snapshot.player_name
            self.current_scenario_id = snapshot.scenario_id

            # Restore game state
            # Note: Full restoration would require integrating with game_engine state

            UIComponent.print_success(f"Game loaded: {snapshot.player_name} - Turn {snapshot.current_turn}")
            return True

        except Exception as e:
            UIComponent.print_error(f"Load failed: {e}")
            return False

    def save_game(self, slot_id: int) -> bool:
        """
        Save current game.

        Args:
            slot_id: Save slot ID

        Returns:
            True if game saved successfully
        """
        try:
            if not self.game_engine or not self.game_engine.state:
                UIComponent.print_error("No game in progress")
                return False

            # Create snapshot from game state
            game_state = self.game_engine.get_game_state()
            scenario_name = self.scenario_runner.current_state.scenario_name if self.scenario_runner.current_state else ""

            snapshot = self.save_system.create_snapshot(game_state, scenario_name)
            success, message = self.save_system.save_game(slot_id, snapshot)

            if success:
                UIComponent.print_success(message)
            else:
                UIComponent.print_error(message)

            return success

        except Exception as e:
            UIComponent.print_error(f"Save failed: {e}")
            return False

    def execute_action(self, action_id: str) -> Dict:
        """
        Execute a game action.

        Args:
            action_id: ID of action to execute

        Returns:
            Action result dictionary
        """
        if not self.game_engine:
            return {"success": False, "error": "Game not initialized"}

        # Get resources before
        resources_before = {}
        if self.game_engine.state:
            for name, res in self.game_engine.state.resources.items():
                resources_before[name] = res.current

        # Execute action
        result = self.game_engine.execute_action(action_id)

        if result.get("success"):
            # Get resources after
            resources_after = {}
            if self.game_engine.state:
                for name, res in self.game_engine.state.resources.items():
                    resources_after[name] = res.current

            # Track in analytics
            action = next((a for p in self.game_engine.state.phases.values()
                          for a in p.actions if a.id == action_id), None)

            self.analytics_system.track_action(
                action_id=action_id,
                action_title=action.title if action else action_id,
                phase=self.game_engine.state.current_phase,
                current_turn=self.game_engine.state.current_turn,
                resources_before=resources_before,
                resources_after=resources_after
            )

            # Update tutorial
            if self.tutorial_system:
                self.tutorial_system.get_message_for_trigger("action_complete",
                                                             self.game_engine.state.current_phase)

            # Check for auto-save
            if self.config.get("auto_save_enabled", True):
                self.save_system.check_auto_save(
                    self.game_engine.state.current_turn,
                    self.game_engine.get_game_state()
                )

        return result

    def advance_turn(self) -> Dict:
        """Advance to the next turn."""
        if not self.game_engine:
            return {"success": False, "error": "Game not initialized"}

        result = self.game_engine.advance_turn()

        # Check for random challenges
        if self.challenge_system and self.game_engine.state:
            game_state = {
                "current_phase": self.game_engine.state.current_phase,
                "current_turn": self.game_engine.state.current_turn,
                "reputation": self.game_engine.state.resources.get("Reputation",
                    type('obj', (object,), {"current": 0})()).current if hasattr(
                    self.game_engine.state.resources.get("Reputation"), "current") else 0
            }
            challenge = self.challenge_system.generate_challenge(
                self.game_engine.state.current_phase,
                game_state
            )
            if challenge:
                result["challenge"] = challenge.to_dict()

        # Check for tutorial hints
        if self.tutorial_system and self.game_engine.state:
            hints = self.tutorial_system.get_contextual_hints(
                self.game_engine.get_game_state()
            )
            if hints:
                result["hints"] = [h.hint_text for h in hints]

        return result

    def get_game_status(self) -> Dict:
        """Get current game status."""
        status = {
            "game_active": self.game_engine is not None and self.game_engine.state is not None,
            "player_name": self.player_name,
            "scenario_id": self.current_scenario_id
        }

        if self.game_engine and self.game_engine.state:
            status["current_phase"] = self.game_engine.state.current_phase
            status["current_turn"] = self.game_engine.state.current_turn
            status["resources"] = self.game_engine.get_resources_summary()
            status["progress"] = self.game_engine.get_progress_summary()

        if self.scenario_runner and self.scenario_runner.current_state:
            status["scenario_objectives"] = self.scenario_runner.get_objectives_progress()

        if self.tutorial_system:
            status["tutorial"] = self.tutorial_system.get_tutorial_status()

        return status

    def end_game(self, outcome: str = "quit") -> Dict:
        """
        End the current game.

        Args:
            outcome: Game outcome (quit, win, loss)

        Returns:
            End game summary
        """
        summary = {
            "outcome": outcome,
            "player": self.player_name,
            "scenario": self.current_scenario_id,
            "timestamp": datetime.now().isoformat()
        }

        if self.game_engine and self.game_engine.state:
            summary["final_phase"] = self.game_engine.state.current_phase
            summary["final_turn"] = self.game_engine.state.current_turn
            summary["final_score"] = self.game_engine.calculate_score()

        if self.scenario_runner and self.scenario_runner.current_state:
            self.scenario_runner.end_scenario(
                "win" if outcome == "win" else "loss",
                f"Game {outcome}"
            )

        # End analytics session
        if self.analytics_system and self.game_engine and self.game_engine.state:
            progress = self.game_engine.get_progress_summary()
            self.analytics_system.end_session(
                self.game_engine.state.current_turn,
                progress.get("overall_progress", 0)
            )

        # Generate analytics report
        if self.analytics_system and self.config.get("analytics_enabled", True):
            report = self.analytics_system.generate_report("summary")
            self.analytics_system.save_report(report)

        return summary

    def get_scenario_list(self) -> list:
        """Get list of available scenarios."""
        if self.scenario_runner:
            return self.scenario_runner.get_scenario_list()
        return []

    def get_save_slots(self) -> list:
        """Get list of save slots."""
        if self.save_system:
            slots = self.save_system.get_all_slots()
            return [s.to_dict() for s in slots]
        return []

    def quit(self):
        """Quit the game."""
        if self.running:
            self.end_game("quit")
        self.running = False


def show_main_menu(game: UsaComGame) -> str:
    """Show main menu and get user choice."""
    UIComponent.clear_screen()
    UIComponent.print_header("USA BUSINESS JOURNEY", "Main Menu")

    print("""
    1. New Game
    2. Load Game
    3. Scenarios
    4. Settings
    5. Credits
    6. Quit
    """)

    choice = UIComponent.get_input("Select option (1-6): ",
                                   ["1", "2", "3", "4", "5", "6"], "choice")
    return choice


def show_scenario_selection(game: UsaComGame) -> Optional[str]:
    """Show scenario selection and return chosen scenario ID."""
    UIComponent.clear_screen()
    UIComponent.print_header("SELECT SCENARIO")

    scenarios = game.get_scenario_list()

    for i, scenario in enumerate(scenarios[:6], 1):
        difficulty_colors = {
            "Easy": Colors.BRIGHT_GREEN,
            "Medium": Colors.BRIGHT_YELLOW,
            "Hard": Colors.BRIGHT_RED
        }
        color = difficulty_colors.get(scenario["difficulty_level"], Colors.WHITE)

        print(f"    {i}. {Colors.BOLD}{scenario['name']}{Colors.RESET}")
        print(f"       {scenario['description'][:60]}...")
        print(f"       Capital: ${scenario['initial_capital']:,} | ", end="")
        print(f"{color}{scenario['difficulty_level']}{Colors.RESET}")
        print()

    choice = UIComponent.get_input("Select scenario (1-6): ",
                                   ["1", "2", "3", "4", "5", "6"], "choice")

    if choice and choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(scenarios):
            return scenarios[idx]["scenario_id"]

    return None


def run_game_loop(game: UsaComGame):
    """Run the main game loop."""
    game.running = True

    while game.running and game.game_engine and game.game_engine.state:
        # Check game over
        is_over, reason = game.game_engine.check_game_over()
        if is_over:
            UIComponent.clear_screen()
            UIComponent.print_header("GAME OVER")
            print(f"\n    {reason}")

            if game.game_engine.state:
                score = game.game_engine.calculate_score()
                print(f"\n    Final Score: {score.get('total_score', 0):.1f}")
                print(f"    Grade: {score.get('grade', 'F')}")

            game.end_game("loss" if "Bankruptcy" in reason else "win")
            input("\n    Press Enter to continue...")
            break

        # Show game screen
        UIComponent.clear_screen()

        status = game.get_game_status()
        progress = status.get("progress", {})
        resources = status.get("resources", {})

        # Header
        phase_name = progress.get("current_phase_name", "Unknown")
        UIComponent.print_header(
            f"PHASE {progress.get('current_phase', 1)}: {phase_name.upper()}",
            f"Turn {progress.get('turn', 0)} | {game.player_name}'s Business"
        )

        # Resources
        UIComponent.print_section("RESOURCES")
        for name, res in resources.items():
            UIComponent.print_resource(
                name,
                res.get("symbol", ""),
                res.get("current", 0),
                res.get("max", 100),
                res.get("current", 0)
            )

        # Progress
        UIComponent.print_section("PROGRESS")
        print(f"    Overall: {progress.get('overall_progress', 0):.1f}%")
        print(f"    Actions: {progress.get('completed_actions', 0)}/{progress.get('total_actions', 0)}")
        print(f"    Compliance: {progress.get('compliance_score', 100):.1f}%")

        # Available actions
        UIComponent.print_section("AVAILABLE ACTIONS")
        actions = game.game_engine.get_available_actions()
        for i, action in enumerate(actions, 1):
            print(f"    {i}. {Colors.BOLD}{action.title}{Colors.RESET}")
            print(f"       {action.description[:50]}...")
            print(f"       Time: {action.time_cost}w | Capital: ${action.capital_cost:,.0f}")
            print()

        # Tutorial hints
        if status.get("tutorial", {}).get("enabled"):
            hints = game.tutorial_system.get_contextual_hints(game.game_engine.get_game_state())
            if hints:
                UIComponent.print_section("HINTS")
                for hint in hints[:2]:
                    print(f"    {Colors.BRIGHT_CYAN}💡 {hint.hint_text}{Colors.RESET}")
                print()

        # Menu
        UIComponent.print_subsection("ACTIONS")
        print(f"    Enter number (1-{len(actions)}) to perform action")
        print("    'a' - Advance to next week")
        print("    's' - Save game")
        print("    'm' - Main menu")
        print("    'q' - Quit game")

        # Get player input
        valid_options = [str(i) for i in range(1, len(actions) + 1)]
        valid_options.extend(["a", "A", "s", "S", "m", "M", "q", "Q"])

        choice = UIComponent.get_input("\nYour choice: ", valid_options, "choice")

        if choice.lower() == "q":
            game.quit()
        elif choice.lower() == "m":
            return  # Return to main menu
        elif choice.lower() == "s":
            game.save_game(1)  # Quick save to slot 1
            input()
        elif choice.lower() == "a":
            result = game.advance_turn()
            if result.get("challenge"):
                UIComponent.print_warning(f"Challenge: {result['challenge'].get('name', 'Unknown')}")
            if result.get("hints"):
                for hint in result["hints"]:
                    UIComponent.print_info(f"Hint: {hint}")
            input()
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(actions):
                action_id = actions[idx].id
                result = game.execute_action(action_id)
                if result.get("success"):
                    UIComponent.print_success(f"Completed: {result.get('action_title', action_id)}")
                else:
                    UIComponent.print_error(result.get("error", "Action failed"))
                input()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="USA Business Journey Simulation")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--player", type=str, help="Player name")
    parser.add_argument("--scenario", type=str, help="Scenario ID")
    parser.add_argument("--difficulty", type=str, default="normal",
                        choices=["easy", "normal", "hard", "expert"],
                        help="Game difficulty")
    parser.add_argument("--no-tutorial", action="store_true", help="Disable tutorial")
    parser.add_argument("--no-analytics", action="store_true", help="Disable analytics")
    args = parser.parse_args()

    # Initialize configuration
    config = GameConfig(args.config)

    # Apply command line overrides
    if args.no_tutorial:
        config.set("tutorial_enabled", False)
    if args.no_analytics:
        config.set("analytics_enabled", False)
    if args.difficulty:
        config.set("difficulty", args.difficulty)

    # Initialize game
    try:
        game = UsaComGame(config)
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}Failed to initialize game: {e}{Colors.RESET}")
        sys.exit(1)

    # Handle command line game start
    if args.player and args.scenario:
        if game.start_new_game(args.player, args.scenario, args.difficulty):
            run_game_loop(game)
        sys.exit(0)

    # Main menu loop
    while True:
        choice = show_main_menu(game)

        if choice == "1":  # New Game
            # Get player name
            name = UIComponent.get_input("Enter your name: ")
            if not name:
                name = "Entrepreneur"

            # Select scenario
            scenario_id = show_scenario_selection(game)
            if not scenario_id:
                scenario_id = config.get("default_scenario", "SCN002")

            # Select difficulty
            UIComponent.print_subsection("Select Difficulty")
            difficulty = UIComponent.get_input("Difficulty (easy/normal/hard/expert): ",
                                               ["EASY", "NORMAL", "HARD", "EXPERT"], "choice")
            difficulty = difficulty.lower()

            # Start game
            if game.start_new_game(name, scenario_id, difficulty):
                run_game_loop(game)

        elif choice == "2":  # Load Game
            UIComponent.clear_screen()
            UIComponent.print_header("LOAD GAME")

            slots = game.get_save_slots()
            for slot in slots:
                status_icon = "✓" if slot["status"] == "valid" else "✗" if slot["status"] == "corrupted" else " "
                if slot["metadata"]:
                    print(f"    {slot['slot_id']}. [{status_icon}] {slot['metadata']['player_name']} - "
                          f"{slot['metadata']['scenario_name']} (Turn {slot['metadata']['current_turn']})")
                else:
                    print(f"    {slot['slot_id']}. [{status_icon}] Empty")

            slot_choice = UIComponent.get_input("\nSelect slot (1-10): ",
                                                [str(i) for i in range(1, 11)], "choice")
            if slot_choice:
                if game.load_game(int(slot_choice)):
                    run_game_loop(game)
                else:
                    input()

        elif choice == "3":  # Scenarios
            UIComponent.clear_screen()
            UIComponent.print_header("SCENARIOS")

            scenarios = game.get_scenario_list()
            for scenario in scenarios:
                print(f"    {Colors.BOLD}{scenario['scenario_id']}: {scenario['name']}{Colors.RESET}")
                print(f"    Category: {scenario['category']}")
                print(f"    Difficulty: {scenario['difficulty_level']}")
                print(f"    Starting Capital: ${scenario['initial_capital']:,}")
                print(f"    {scenario['description'][:80]}...")
                print()

            input("    Press Enter to return...")

        elif choice == "4":  # Settings
            UIComponent.clear_screen()
            UIComponent.print_header("SETTINGS")

            print(f"""
    Current Settings:
    • Tutorial: {'Enabled' if config.get('tutorial_enabled') else 'Disabled'}
    • Auto-Save: {'Enabled' if config.get('auto_save_enabled') else 'Disabled'}
    • Analytics: {'Enabled' if config.get('analytics_enabled') else 'Disabled'}
    • Difficulty: {config.get('difficulty', 'normal').capitalize()}
    • Hint Frequency: {config.get('hint_frequency', 'normal').capitalize()}
            """)

            setting = UIComponent.get_input("Change setting (tutorial/auto/analytics/difficulty) or Enter to return: ")

            if setting:
                if setting.lower() == "tutorial":
                    config.set("tutorial_enabled", not config.get("tutorial_enabled", True))
                    UIComponent.print_success("Tutorial setting updated")
                elif setting.lower() == "auto":
                    config.set("auto_save_enabled", not config.get("auto_save_enabled", True))
                    UIComponent.print_success("Auto-save setting updated")
                elif setting.lower() == "analytics":
                    config.set("analytics_enabled", not config.get("analytics_enabled", True))
                    UIComponent.print_success("Analytics setting updated")
                elif setting.lower() == "difficulty":
                    diff = UIComponent.get_input("New difficulty: ",
                                                 ["EASY", "NORMAL", "HARD", "EXPERT"], "choice")
                    config.set("difficulty", diff.lower())
                    UIComponent.print_success("Difficulty updated")

            input()

        elif choice == "5":  # Credits
            UIComponent.clear_screen()
            UIComponent.print_header("CREDITS")

            print("""
    USA BUSINESS JOURNEY
    Interactive Business Formation Simulation

    Phase 6 - Simulation Game Development

    Core Modules:
    • game_engine.py - Core game mechanics and state management
    • game_ui.py - User interface and display
    • scenario_runner.py - Scenario management and win/loss conditions
    • save_system.py - Save/load functionality
    • tutorial_system.py - Interactive tutorials and hints
    • analytics_system.py - Player behavior tracking and reports
    • decision_engine.py - Decision trees and consequences
    • challenge_system.py - Challenge generation and resolution
    • assessment_integration.py - Feedback and evaluation

    Educational Purpose:
    This simulation helps aspiring entrepreneurs understand
    the business formation process in the USA.

    Data Sources (Phase 5):
    • action_planner.json
    • game_mechanics_spec.json
    • virtual_map.json
    • sample_scenarios.json
    • assessment_system.json
            """)

            input("    Press Enter to return...")

        elif choice == "6":  # Quit
            UIComponent.clear_screen()
            UIComponent.print_header("GOODBYE!")
            print("\n    Thanks for playing USA Business Journey!")
            print("    Your entrepreneurial journey continues...\n")
            break


if __name__ == "__main__":
    main()
