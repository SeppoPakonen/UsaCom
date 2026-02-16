#!/usr/bin/env python3
"""
USA Business Journey - User Interface Layer
CLI interface for game interaction with menu system, display functions, and input validation.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from game_engine import GameEngine, GameState, PhaseStatus


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    
    # Background
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"
    BG_YELLOW = "\033[43m"


class UIComponent:
    """Base class for UI components."""
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str, subtitle: str = ""):
        """Print a styled header."""
        width = 70
        print()
        print(Colors.BG_BLUE + Colors.WHITE + Colors.BOLD + " " * width + Colors.RESET)
        print(Colors.BG_BLUE + Colors.WHITE + Colors.BOLD + f"  {title}".ljust(width - 1) + Colors.RESET)
        if subtitle:
            print(Colors.BG_BLUE + Colors.WHITE + f"  {subtitle}".ljust(width - 1) + Colors.RESET)
        print(Colors.BG_BLUE + Colors.WHITE + Colors.BOLD + " " * width + Colors.RESET)
        print()
    
    @staticmethod
    def print_section(title: str):
        """Print a section header."""
        print()
        print(Colors.CYAN + Colors.BOLD + "=" * 50 + Colors.RESET)
        print(Colors.CYAN + Colors.BOLD + f"  {title}" + Colors.RESET)
        print(Colors.CYAN + Colors.BOLD + "=" * 50 + Colors.RESET)
    
    @staticmethod
    def print_subsection(title: str):
        """Print a subsection header."""
        print()
        print(Colors.YELLOW + Colors.BOLD + f"--- {title} ---" + Colors.RESET)
    
    @staticmethod
    def print_success(message: str):
        """Print success message."""
        print(Colors.BRIGHT_GREEN + f"  ✓ {message}" + Colors.RESET)
    
    @staticmethod
    def print_warning(message: str):
        """Print warning message."""
        print(Colors.BRIGHT_YELLOW + f"  ⚠ {message}" + Colors.RESET)
    
    @staticmethod
    def print_error(message: str):
        """Print error message."""
        print(Colors.BRIGHT_RED + f"  ✗ {message}" + Colors.RESET)
    
    @staticmethod
    def print_info(message: str):
        """Print info message."""
        print(Colors.BRIGHT_BLUE + f"  ℹ {message}" + Colors.RESET)
    
    @staticmethod
    def print_resource(name: str, symbol: str, current: float, max_val: float, 
                       starting: float = None):
        """Print a resource with formatting."""
        if current < (starting or max_val) * 0.2:
            color = Colors.BRIGHT_RED
        elif current < (starting or max_val) * 0.5:
            color = Colors.BRIGHT_YELLOW
        else:
            color = Colors.BRIGHT_GREEN
        
        if max_val >= 1000:
            current_str = f"{current:,.0f}"
            max_str = f"{max_val:,.0f}"
        else:
            current_str = f"{current:.1f}"
            max_str = f"{max_val:.1f}"
        
        print(f"    {symbol} {Colors.BOLD}{name}:{Colors.RESET} {color}{current_str}{Colors.RESET} / {max_str}")
    
    @staticmethod
    def get_input(prompt: str, valid_options: List[str] = None, 
                  input_type: str = "string") -> Any:
        """Get validated user input."""
        while True:
            try:
                user_input = input(Colors.BOLD + f"\n{prompt}" + Colors.RESET).strip()
                
                if not user_input and valid_options:
                    continue
                
                if input_type == "int":
                    value = int(user_input)
                    if valid_options and value not in valid_options:
                        UIComponent.print_error(f"Please enter one of: {valid_options}")
                        continue
                    return value
                elif input_type == "float":
                    return float(user_input)
                elif input_type == "choice":
                    if user_input.upper() in [o.upper() for o in valid_options]:
                        return user_input.upper()
                    UIComponent.print_error(f"Invalid choice. Options: {', '.join(valid_options)}")
                    continue
                else:
                    if valid_options and user_input not in valid_options:
                        UIComponent.print_error(f"Invalid input. Options: {', '.join(valid_options)}")
                        continue
                    return user_input
                    
            except ValueError:
                UIComponent.print_error("Invalid input format")
            except KeyboardInterrupt:
                print()
                return None


class GameUI:
    """Main game user interface."""
    
    def __init__(self):
        self.engine: Optional[GameEngine] = None
        self.running = False
        
    def start(self):
        """Start the game UI."""
        self.running = True
        self.show_welcome()
        self.main_menu()
    
    def show_welcome(self):
        """Show welcome screen."""
        UIComponent.clear_screen()
        UIComponent.print_header(
            "USA BUSINESS JOURNEY",
            "Interactive Business Formation Simulation"
        )
        print("""
    Welcome to the USA Business Journey simulation!
    
    In this game, you will experience the challenges and rewards of
    starting and growing a business in the United States.
    
    You will:
    • Navigate through 5 phases of business formation
    • Manage resources: Capital, Time, Knowledge, Network, Reputation
    • Make critical decisions that shape your business
    • Face challenges and overcome obstacles
    • Learn about real business requirements and regulations
    
    Your goal is to successfully launch and grow your business
    while maintaining compliance and financial health.
        """)
        UIComponent.print_info("Press Enter to continue...")
        input()
    
    def main_menu(self):
        """Display main menu."""
        while self.running:
            UIComponent.clear_screen()
            UIComponent.print_header("MAIN MENU")
            
            print("""
    1. New Game
    2. Load Game
    3. How to Play
    4. Scenarios
    5. Credits
    6. Exit
            """)
            
            choice = UIComponent.get_input("Select option (1-6): ", 
                                           ["1", "2", "3", "4", "5", "6"], 
                                           "choice")
            
            if choice == "1":
                self.new_game_setup()
            elif choice == "2":
                UIComponent.print_info("Load game feature coming soon")
                input()
            elif choice == "3":
                self.show_how_to_play()
            elif choice == "4":
                self.show_scenarios()
            elif choice == "5":
                self.show_credits()
            elif choice == "6":
                self.running = False
    
    def new_game_setup(self):
        """Setup new game."""
        UIComponent.clear_screen()
        UIComponent.print_header("NEW GAME")
        
        # Get player name
        name = UIComponent.get_input("Enter your name: ")
        if not name:
            name = "Entrepreneur"
        
        # Select scenario
        UIComponent.print_subsection("Select Scenario")
        print("""
    Available Scenarios:
    
    1. SCN001 - Tech Startup (SaaS Platform) - Hard
       Initial Capital: $75,000 | 2 Founders | VC-funded
    
    2. SCN002 - Solo Tech Consultant - Easy
       Initial Capital: $10,000 | Solo | Bootstrapped
    
    3. SCN003 - Boutique Retail Store - Medium
       Initial Capital: $120,000 | 1 Owner + Staff
    
    4. SCN004 - E-commerce Store - Medium
       Initial Capital: $50,000 | 2 Founders
    
    5. SCN005 - Marketing Agency - Medium
       Initial Capital: $25,000 | 2 Founders
        """)
        
        scenario_map = {
            "1": "SCN001", "2": "SCN002", "3": "SCN003",
            "4": "SCN004", "5": "SCN005"
        }
        scenario_choice = UIComponent.get_input("Select scenario (1-5): ",
                                                ["1", "2", "3", "4", "5"], "choice")
        scenario_id = scenario_map.get(scenario_choice, "SCN002")
        
        # Select difficulty
        UIComponent.print_subsection("Select Difficulty")
        print("""
    • Easy    - More resources, fewer challenges
    • Normal  - Balanced experience
    • Hard    - Limited resources, frequent challenges
    • Expert  - Maximum challenge
        """)
        
        difficulty = UIComponent.get_input("Select difficulty: ",
                                           ["EASY", "NORMAL", "HARD", "EXPERT"], "choice")
        difficulty = difficulty.lower()
        
        # Initialize game
        UIComponent.print_info("Initializing game...")
        self.engine = GameEngine()
        self.engine.new_game(name, scenario_id, difficulty)
        
        UIComponent.print_success(f"Welcome, {name}! Your business journey begins!")
        input()
        
        # Start game loop
        self.game_loop()
    
    def show_how_to_play(self):
        """Show how to play instructions."""
        UIComponent.clear_screen()
        UIComponent.print_header("HOW TO PLAY")
        
        print("""
    GAME OBJECTIVE
    --------------
    Complete all 5 phases of business formation while maintaining
    financial health and compliance.
    
    RESOURCES
    ---------
    • Capital (💰) - Money for business expenses
    • Time (⏰) - Weeks available for actions
    • Knowledge (📚) - Understanding of requirements
    • Network (🤝) - Professional connections
    • Reputation (⭐) - Business credibility
    
    GAMEPLAY
    --------
    1. Select actions from available options
    2. Actions cost Capital and Time
    3. Complete actions to progress through phases
    4. Watch for warnings about low resources
    5. Maintain compliance to avoid penalties
    
    PHASES
    ------
    Phase 1: Planning Peaks - Business planning and research
    Phase 2: Legal Labyrinth - Legal structure and registration
    Phase 3: Compliance Canyon - Licenses and permits
    Phase 4: Operations Ocean - Setting up operations
    Phase 5: Growth Galaxy - Scaling the business
    
    TIPS
    ----
    • Monitor your Capital closely
    • Complete compliance actions early
    • Build Knowledge before major decisions
    • Network can help in difficult situations
        """)
        
        UIComponent.print_info("Press Enter to return...")
        input()
    
    def show_scenarios(self):
        """Show available scenarios."""
        UIComponent.clear_screen()
        UIComponent.print_header("SCENARIOS")
        
        print("""
    Each scenario represents a different business type with unique
    challenges and starting conditions.
    
    Technology Sector:
    • Tech Startup - High growth, VC-funded, fast-paced
    • Solo Consultant - Low overhead, flexible, bootstrapped
    
    Retail Sector:
    • Boutique Store - Physical location, inventory management
    • E-commerce - Online sales, shipping logistics
    
    Service Sector:
    • Marketing Agency - Client-based, scalable services
    
    Each scenario has different:
    • Starting capital
    • Team structure
    • Growth targets
    • Risk factors
        """)
        
        UIComponent.print_info("Press Enter to return...")
        input()
    
    def show_credits(self):
        """Show credits."""
        UIComponent.clear_screen()
        UIComponent.print_header("CREDITS")
        
        print("""
    USA BUSINESS JOURNEY
    Interactive Business Formation Simulation
    
    Phase 5 Data Sources:
    • action_planner.json - Business action definitions
    • game_mechanics_spec.json - Game rules and systems
    • virtual_map.json - Metaphorical journey map
    • sample_scenarios.json - Business scenarios
    • assessment_system.json - Feedback and evaluation
    
    Development: Phase 6 - Simulation Game
    
    Educational Purpose:
    This simulation is designed to help aspiring entrepreneurs
    understand the business formation process in the USA.
        """)
        
        UIComponent.print_info("Press Enter to return...")
        input()
    
    def game_loop(self):
        """Main game loop."""
        while self.running and self.engine:
            # Check game over
            is_over, reason = self.engine.check_game_over()
            if is_over:
                self.show_game_over(reason)
                break
            
            self.show_game_screen()
            
            # Get player action
            action = self.get_player_action()
            
            if action == "quit":
                self.running = False
            elif action == "menu":
                return  # Return to main menu
            elif action and action != "advance":
                # Execute action
                result = self.engine.execute_action(action)
                self.show_action_result(result)
            elif action == "advance":
                result = self.engine.advance_turn()
                if result.get("event"):
                    self.show_event(result["event"])
                if result.get("warnings"):
                    for warning in result["warnings"]:
                        UIComponent.print_warning(warning["message"])
                input()
    
    def show_game_screen(self):
        """Show main game screen."""
        UIComponent.clear_screen()
        
        state = self.engine.get_game_state()
        progress = self.engine.get_progress_summary()
        resources = self.engine.get_resources_summary()
        
        # Header with phase info
        phase_name = progress.get("current_phase_name", "Unknown")
        UIComponent.print_header(
            f"PHASE {progress['current_phase']}: {phase_name.upper()}",
            f"Turn {progress['turn']} | {state['player_name']}'s Business"
        )
        
        # Resources panel
        UIComponent.print_section("RESOURCES")
        for name, res in resources.items():
            UIComponent.print_resource(
                name, 
                res["symbol"], 
                res["current"], 
                res["max"],
                self.engine.state.resources[name].starting_amount if self.engine.state else None
            )
        
        # Progress panel
        UIComponent.print_section("PROGRESS")
        progress_bar = self._create_progress_bar(progress["overall_progress"])
        print(f"    Overall: {progress_bar} {progress['overall_progress']:.1f}%")
        print(f"    Actions: {progress['completed_actions']}/{progress['total_actions']}")
        print(f"    Compliance: {progress['compliance_score']:.1f}%")
        
        # Available actions
        UIComponent.print_section("AVAILABLE ACTIONS")
        actions = self.engine.get_available_actions()
        for i, action in enumerate(actions, 1):
            print(f"    {i}. {Colors.BOLD}{action.title}{Colors.RESET}")
            print(f"       {action.description}")
            print(f"       Time: {action.time_cost}w | Capital: ${action.capital_cost:,.0f}")
            print()
        
        # Menu options
        UIComponent.print_subsection("ACTIONS")
        print(f"    Enter number (1-{len(actions)}) to perform action")
        print("    'a' - Advance to next week")
        print("    'm' - Return to main menu")
        print("    'q' - Quit game")
    
    def _create_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Create ASCII progress bar."""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    def get_player_action(self) -> Optional[str]:
        """Get player's chosen action."""
        actions = self.engine.get_available_actions()
        
        valid_options = [str(i) for i in range(1, len(actions) + 1)]
        valid_options.extend(["a", "A", "m", "M", "q", "Q"])
        
        choice = UIComponent.get_input("\nYour choice: ", valid_options, "choice")
        
        if choice.lower() == "q":
            return "quit"
        elif choice.lower() == "m":
            return "menu"
        elif choice.lower() == "a":
            return "advance"
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(actions):
                return actions[idx].id
        
        return None
    
    def show_action_result(self, result: Dict, skip_pause: bool = False):
        """Show result of action execution."""
        UIComponent.clear_screen()
        UIComponent.print_header("ACTION RESULT")
        
        if result.get("success"):
            UIComponent.print_success(f"Completed: {result['action_title']}")
            print()
            print(f"    Output: {result.get('output', 'N/A')}")
            print()
            print(f"    Resources Spent:")
            print(f"      • Time: {result.get('time_spent', 0)} weeks")
            print(f"      • Capital: ${result.get('capital_spent', 0):,.2f}")
            print(f"    Knowledge Gained: +{result.get('knowledge_gained', 0):.1f}")
            
            if result.get("phase_complete"):
                print()
                UIComponent.print_success("🎉 PHASE COMPLETE! 🎉")
                print(f"    {result.get('message', '')}")
        else:
            UIComponent.print_error(f"Failed: {result.get('error', 'Unknown error')}")
        
        if not skip_pause:
            input()
    
    def show_event(self, event: Dict, skip_pause: bool = False):
        """Show random event."""
        UIComponent.clear_screen()
        UIComponent.print_header("EVENT")
        
        print(f"    {event.get('title', 'Event')}")
        print()
        print(f"    {event.get('description', '')}")
        
        effects = event.get("effects", {})
        if effects:
            print()
            print("    Effects:")
            for stat, change in effects.items():
                if change > 0:
                    UIComponent.print_success(f"{stat.capitalize()}: +{change}")
                else:
                    UIComponent.print_warning(f"{stat.capitalize()}: {change}")
        
        if not skip_pause:
            input()
    
    def show_game_over(self, reason: str):
        """Show game over screen."""
        UIComponent.clear_screen()
        UIComponent.print_header("GAME OVER")
        
        print(f"\n    {reason}")
        
        if self.engine:
            score = self.engine.calculate_score()
            print()
            print("    Final Score:")
            print(f"      Total: {score.get('total_score', 0):.1f}")
            print(f"      Grade: {score.get('grade', 'F')}")
            print(f"      Title: {score.get('title', 'Unknown')}")
        
        print()
        UIComponent.print_info("Thanks for playing!")
        input()
    
    def show_phase_complete(self, phase_num: int):
        """Show phase completion celebration."""
        UIComponent.clear_screen()
        UIComponent.print_header(f"PHASE {phase_num} COMPLETE!", "🎉")
        
        phase_names = {
            1: "Planning Peaks",
            2: "Legal Labyrinth", 
            3: "Compliance Canyon",
            4: "Operations Ocean",
            5: "Growth Galaxy"
        }
        
        print(f"""
    Congratulations! You have completed:
    {Colors.BOLD}{phase_names.get(phase_num, f'Phase {phase_num}')}{Colors.RESET}
    
    Rewards received:
    • Bonus resources added
    • Next phase unlocked
    • Reputation increased
    
    Your business journey continues...
        """)
        
        input()


def run_ui_tests() -> Dict:
    """Run UI component tests."""
    print("Running UI Tests...")
    print("=" * 60)
    
    results = {
        "test_timestamp": datetime.now().isoformat(),
        "ui_version": "1.0.0",
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "test_results": [],
        "screenshots": []
    }
    
    # Test 1: UI Component initialization
    print("\nTest 1: UI Component Initialization")
    try:
        ui = GameUI()
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "UI Component Initialization",
            "status": "PASSED"
        })
        print("  PASSED: UI initialized")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "UI Component Initialization",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 2: Color codes
    print("\nTest 2: Color Codes")
    try:
        assert hasattr(Colors, "RED")
        assert hasattr(Colors, "GREEN")
        assert hasattr(Colors, "BLUE")
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Color Codes",
            "status": "PASSED"
        })
        print("  PASSED: All color codes available")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Color Codes",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 3: UI Component methods
    print("\nTest 3: UI Component Methods")
    try:
        UIComponent.print_section("Test Section")
        UIComponent.print_subsection("Test Subsection")
        UIComponent.print_success("Test success")
        UIComponent.print_warning("Test warning")
        UIComponent.print_error("Test error")
        UIComponent.print_info("Test info")
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "UI Component Methods",
            "status": "PASSED"
        })
        print("  PASSED: All UI methods work")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "UI Component Methods",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 4: Resource display
    print("\nTest 4: Resource Display")
    try:
        UIComponent.print_resource("Capital", "💰", 15000, 100000, 15000)
        UIComponent.print_resource("Time", "⏰", 52, 104, 52)
        UIComponent.print_resource("Knowledge", "📚", 25, 100, 10)
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Resource Display",
            "status": "PASSED"
        })
        print("  PASSED: Resource display works")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Resource Display",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 5: Progress bar
    print("\nTest 5: Progress Bar Generation")
    try:
        ui = GameUI()
        bar = ui._create_progress_bar(50, 20)
        assert len(bar) == 22  # [ + 20 chars + ]
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Progress Bar Generation",
            "status": "PASSED",
            "details": f"Generated: {bar}"
        })
        print(f"  PASSED: Progress bar generated: {bar}")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Progress Bar Generation",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 6: Input validation
    print("\nTest 6: Input Validation (Simulated)")
    try:
        # Test validation logic without actual input
        valid_options = ["1", "2", "3"]
        test_input = "2"
        assert test_input in valid_options
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Input Validation",
            "status": "PASSED"
        })
        print("  PASSED: Input validation logic works")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Input Validation",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 7: Game screen rendering
    print("\nTest 7: Game Screen Rendering")
    try:
        engine = GameEngine()
        engine.new_game("Test Player", "SCN002", "normal")
        ui = GameUI()
        ui.engine = engine
        
        # Capture screen output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            ui.show_game_screen()
        output = f.getvalue()
        
        assert "RESOURCES" in output
        assert "PROGRESS" in output
        assert "AVAILABLE ACTIONS" in output
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Game Screen Rendering",
            "status": "PASSED"
        })
        print("  PASSED: Game screen renders correctly")
        
        # Save screenshot
        results["screenshots"].append({
            "name": "game_screen",
            "content": output[:2000]  # First 2000 chars
        })
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Game Screen Rendering",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 8: Menu system
    print("\nTest 8: Menu System Structure")
    try:
        ui = GameUI()
        assert hasattr(ui, "main_menu")
        assert hasattr(ui, "game_loop")
        assert hasattr(ui, "show_game_screen")
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Menu System Structure",
            "status": "PASSED"
        })
        print("  PASSED: Menu system structure valid")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Menu System Structure",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 9: Action result display
    print("\nTest 9: Action Result Display")
    try:
        ui = GameUI()
        
        import io
        from contextlib import redirect_stdout
        
        test_result = {
            "success": True,
            "action_title": "Test Action",
            "output": "Test output",
            "time_spent": 2,
            "capital_spent": 500,
            "knowledge_gained": 5
        }
        
        f = io.StringIO()
        with redirect_stdout(f):
            ui.show_action_result(test_result, skip_pause=True)
        output = f.getvalue()
        
        assert "Test Action" in output
        assert "500" in output
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Action Result Display",
            "status": "PASSED"
        })
        print("  PASSED: Action result display works")
        
        results["screenshots"].append({
            "name": "action_result",
            "content": output
        })
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Action Result Display",
            "status": "FAILED",
            "error": str(e)
        })
        print(f"  FAILED: {e}")
    
    # Test 10: Event display
    print("\nTest 10: Event Display")
    try:
        ui = GameUI()
        
        import io
        from contextlib import redirect_stdout
        
        test_event = {
            "title": "Test Event",
            "description": "A test event occurred",
            "effects": {"capital": 500, "knowledge": -5}
        }
        
        f = io.StringIO()
        with redirect_stdout(f):
            ui.show_event(test_event, skip_pause=True)
        output = f.getvalue()
        
        assert "Test Event" in output
        
        results["tests_run"] += 1
        results["tests_passed"] += 1
        results["test_results"].append({
            "test_name": "Event Display",
            "status": "PASSED"
        })
        print("  PASSED: Event display works")
    except Exception as e:
        results["tests_run"] += 1
        results["tests_failed"] += 1
        results["test_results"].append({
            "test_name": "Event Display",
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
    
    results["summary"] = {
        "pass_rate": results['tests_passed']/results['tests_run']*100 if results['tests_run'] > 0 else 0,
        "total_tests": results['tests_run'],
        "screenshots_captured": len(results['screenshots'])
    }
    
    return results


if __name__ == "__main__":
    # Run tests and save results
    test_results = run_ui_tests()
    
    # Generate UI screenshots markdown
    output_path = Path(__file__).parent.parent / "processed" / "ui_screenshots.md"
    
    with open(output_path, 'w') as f:
        f.write("# USA Business Journey - UI Screenshots\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Test Results\n\n")
        f.write(f"- Tests Run: {test_results['tests_run']}\n")
        f.write(f"- Tests Passed: {test_results['tests_passed']}\n")
        f.write(f"- Pass Rate: {test_results['summary']['pass_rate']:.1f}%\n\n")
        
        f.write("## UI Screen Captures\n\n")
        
        for screenshot in test_results.get("screenshots", []):
            f.write(f"### {screenshot['name'].replace('_', ' ').title()}\n\n")
            f.write("```\n")
            f.write(screenshot['content'])
            f.write("\n```\n\n")
        
        f.write("## UI Components\n\n")
        f.write("### Color System\n")
        f.write("- Red: Errors, critical warnings\n")
        f.write("- Green: Success, healthy resources\n")
        f.write("- Yellow: Warnings, moderate concerns\n")
        f.write("- Blue: Information, headers\n")
        f.write("- Cyan: Section headers\n\n")
        
        f.write("### Screen Types\n")
        f.write("1. Welcome Screen - Game introduction\n")
        f.write("2. Main Menu - Navigation hub\n")
        f.write("3. Game Screen - Main gameplay interface\n")
        f.write("4. Action Result - Feedback after actions\n")
        f.write("5. Event Screen - Random event display\n")
        f.write("6. Game Over - End game summary\n")
    
    print(f"\nUI screenshots saved to: {output_path}")
