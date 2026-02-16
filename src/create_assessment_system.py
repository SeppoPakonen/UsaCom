#!/usr/bin/env python3
"""
Phase 5 Task 09: Create Assessment and Feedback System
Design system for evaluating player progress and providing feedback.
"""

import json
from pathlib import Path
from datetime import datetime


def create_assessment_system() -> dict:
    """Create comprehensive assessment and feedback system."""

    system = {
        "title": "USA Business Journey - Assessment and Feedback System",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "System for evaluating player progress and providing contextual feedback",

        "1_progress_tracking_metrics": {
            "description": "Core metrics for tracking player progress through the simulation",

            "completion_metrics": {
                "overall_progress": {
                    "name": "Overall Journey Progress",
                    "type": "percentage",
                    "calculation": "(completed_actions / total_actions) * 100",
                    "phases": [
                        {"phase": 1, "weight": 0.15, "actions": 5},
                        {"phase": 2, "weight": 0.20, "actions": 5},
                        {"phase": 3, "weight": 0.25, "actions": 4},
                        {"phase": 4, "weight": 0.20, "actions": 5},
                        {"phase": 5, "weight": 0.20, "actions": 5}
                    ],
                    "thresholds": {
                        "just_starting": {"min": 0, "max": 10},
                        "getting_started": {"min": 11, "max": 30},
                        "making_progress": {"min": 31, "max": 60},
                        "nearing_completion": {"min": 61, "max": 90},
                        "journey_complete": {"min": 91, "max": 100}
                    }
                },
                "phase_completion": {
                    "name": "Phase Completion Status",
                    "type": "boolean_per_phase",
                    "phases": {
                        "phase_1": {"name": "Planning Peaks", "required_actions": ["action_1_1", "action_1_2", "action_1_3", "action_1_4", "action_1_5"]},
                        "phase_2": {"name": "Legal Labyrinth", "required_actions": ["action_2_1", "action_2_2", "action_2_3", "action_2_4", "action_2_5"]},
                        "phase_3": {"name": "Compliance Canyon", "required_actions": ["action_3_1", "action_3_2", "action_3_3", "action_3_4"]},
                        "phase_4": {"name": "Operations Ocean", "required_actions": ["action_4_1", "action_4_2", "action_4_3", "action_4_4", "action_4_5"]},
                        "phase_5": {"name": "Growth Galaxy", "required_actions": ["action_5_1", "action_5_2", "action_5_3", "action_5_4", "action_5_5"]}
                    }
                },
                "action_completion_rate": {
                    "name": "Action Completion Rate",
                    "type": "rate",
                    "calculation": "completed_actions / time_elapsed_weeks",
                    "benchmark": 0.5,
                    "interpretation": "Actions completed per week"
                }
            },

            "resource_metrics": {
                "capital_health": {
                    "name": "Capital Health",
                    "type": "percentage",
                    "calculation": "(current_capital / starting_capital) * 100",
                    "thresholds": {
                        "critical": {"min": 0, "max": 20, "alert": "Immediate action required"},
                        "warning": {"min": 21, "max": 50, "alert": "Consider fundraising"},
                        "stable": {"min": 51, "max": 80, "alert": "Monitor closely"},
                        "healthy": {"min": 81, "max": 100, "alert": "Good position"},
                        "thriving": {"min": 101, "max": 999, "alert": "Excellent - consider expansion"}
                    }
                },
                "time_efficiency": {
                    "name": "Time Efficiency",
                    "type": "percentage",
                    "calculation": "(estimated_time / actual_time) * 100",
                    "thresholds": {
                        "behind": {"min": 0, "max": 80},
                        "on_track": {"min": 81, "max": 120},
                        "ahead": {"min": 121, "max": 999}
                    }
                },
                "knowledge_level": {
                    "name": "Knowledge Level",
                    "type": "score",
                    "scale": {"min": 0, "max": 100},
                    "acquisition": "+5-10 per research action, +2-5 per completed action",
                    "thresholds": {
                        "novice": {"min": 0, "max": 25},
                        "learning": {"min": 26, "max": 50},
                        "knowledgeable": {"min": 51, "max": 75},
                        "expert": {"min": 76, "max": 100}
                    }
                },
                "network_strength": {
                    "name": "Network Strength",
                    "type": "score",
                    "scale": {"min": 0, "max": 100},
                    "thresholds": {
                        "isolated": {"min": 0, "max": 20},
                        "building": {"min": 21, "max": 50},
                        "connected": {"min": 51, "max": 80},
                        "well_connected": {"min": 81, "max": 100}
                    }
                },
                "reputation_score": {
                    "name": "Reputation Score",
                    "type": "score",
                    "scale": {"min": 0, "max": 100},
                    "thresholds": {
                        "unknown": {"min": 0, "max": 20},
                        "emerging": {"min": 21, "max": 50},
                        "respected": {"min": 51, "max": 80},
                        "prestigious": {"min": 81, "max": 100}
                    }
                }
            },

            "compliance_metrics": {
                "compliance_score": {
                    "name": "Compliance Score",
                    "type": "percentage",
                    "calculation": "(completed_compliance_actions / required_compliance_actions) * 100",
                    "thresholds": {
                        "non_compliant": {"min": 0, "max": 50, "consequence": "Penalties and legal risks"},
                        "at_risk": {"min": 51, "max": 70, "consequence": "Warning notices"},
                        "compliant": {"min": 71, "max": 90, "consequence": "Good standing"},
                        "exemplary": {"min": 91, "max": 100, "consequence": "Model business"}
                    }
                },
                "pending_deadlines": {
                    "name": "Pending Deadlines",
                    "type": "count",
                    "urgency_levels": {
                        "overdue": {"color": "red", "action": "Immediate attention required"},
                        "this_week": {"color": "orange", "action": "Priority task"},
                        "this_month": {"color": "yellow", "action": "Schedule soon"},
                        "future": {"color": "green", "action": "Track and plan"}
                    }
                },
                "filing_status": {
                    "name": "Filing Status",
                    "type": "categorical",
                    "categories": ["Not Started", "In Progress", "Submitted", "Approved", "Rejected"]
                }
            },

            "business_health_metrics": {
                "revenue_progress": {
                    "name": "Revenue Progress",
                    "type": "percentage",
                    "calculation": "(actual_revenue / target_revenue) * 100",
                    "thresholds": {
                        "below_expectations": {"min": 0, "max": 50},
                        "meeting_expectations": {"min": 51, "max": 90},
                        "exceeding_expectations": {"min": 91, "max": 999}
                    }
                },
                "customer_acquisition": {
                    "name": "Customer Acquisition Rate",
                    "type": "rate",
                    "calculation": "new_customers / time_period",
                    "comparison": "vs. scenario benchmark"
                },
                "team_growth": {
                    "name": "Team Growth",
                    "type": "count",
                    "comparison": "vs. scenario hiring plan"
                }
            }
        },

        "2_feedback_message_templates": {
            "description": "Contextual feedback messages for different game states",

            "progress_feedback": {
                "phase_entry": [
                    {
                        "trigger": "entering_phase_1",
                        "template": "Welcome to {phase_name}! This is where every great business begins. Take your time to {phase_focus}. You've got this!",
                        "tone": "encouraging"
                    },
                    {
                        "trigger": "entering_phase_2",
                        "template": "You're entering the {phase_name}. This is where many entrepreneurs feel overwhelmed, but remember: every successful business has navigated this path. Let's tackle it step by step.",
                        "tone": "supportive"
                    },
                    {
                        "trigger": "entering_phase_3",
                        "template": "Congratulations on reaching {phase_name}! Compliance might seem daunting, but it's your shield against future problems. Stay organized and you'll do great.",
                        "tone": "reassuring"
                    },
                    {
                        "trigger": "entering_phase_4",
                        "template": "Welcome to {phase_name}! Now the real work begins. Setting up solid operations today will save you countless headaches tomorrow.",
                        "tone": "motivational"
                    },
                    {
                        "trigger": "entering_phase_5",
                        "template": "You've made it to {phase_name}! This is where your business transforms from surviving to thriving. Time to scale!",
                        "tone": "celebratory"
                    }
                ],
                "action_completed": [
                    {
                        "trigger": "action_completed_easy",
                        "template": "Great job completing '{action_name}'! That's one step closer to your business goals.",
                        "tone": "positive"
                    },
                    {
                        "trigger": "action_completed_medium",
                        "template": "Excellent work on '{action_name}'! This was a significant step. You're building real momentum now.",
                        "tone": "encouraging"
                    },
                    {
                        "trigger": "action_completed_hard",
                        "template": "Outstanding! You've completed '{action_name}' - one of the tougher challenges. This demonstrates real commitment to your business.",
                        "tone": "celebratory"
                    }
                ],
                "milestone_reached": [
                    {
                        "trigger": "phase_completed",
                        "template": "🎉 Phase {phase_number} Complete! You've conquered the {phase_name}. Take a moment to appreciate how far you've come, then let's move forward!",
                        "tone": "celebratory"
                    },
                    {
                        "trigger": "halfway_point",
                        "template": "You're halfway through your journey! Look back at how much you've accomplished. The hardest parts are behind you - keep going!",
                        "tone": "motivational"
                    }
                ]
            },

            "resource_feedback": {
                "capital_warnings": [
                    {
                        "trigger": "capital_below_50_percent",
                        "template": "💰 Capital Alert: You're using more capital than expected. Consider reviewing your budget or exploring funding options.",
                        "tone": "advisory"
                    },
                    {
                        "trigger": "capital_below_30_percent",
                        "template": "⚠️ Capital Warning: Your funds are running low. It's time to take action - cut costs, accelerate revenue, or seek funding.",
                        "tone": "urgent"
                    },
                    {
                        "trigger": "capital_below_20_percent",
                        "template": "🚨 Capital Critical: You have less than 20% of your starting capital remaining. Immediate action is required to avoid business failure.",
                        "tone": "critical"
                    }
                ],
                "time_warnings": [
                    {
                        "trigger": "behind_schedule",
                        "template": "⏰ Time Check: You're falling behind schedule. Consider focusing on critical path activities and delegating or delaying non-essential tasks.",
                        "tone": "advisory"
                    },
                    {
                        "trigger": "deadline_approaching",
                        "template": "⏰ Deadline Alert: You have a filing deadline approaching in {days} days. Don't wait until the last minute!",
                        "tone": "urgent"
                    }
                ],
                "resource_positive": [
                    {
                        "trigger": "capital_above_target",
                        "template": "💰 Great financial management! You have more capital than expected. Consider accelerating your growth plans.",
                        "tone": "positive"
                    },
                    {
                        "trigger": "ahead_of_schedule",
                        "template": "⏰ Ahead of schedule! Your efficient progress gives you flexibility. Consider using extra time for strategic planning.",
                        "tone": "positive"
                    }
                ]
            },

            "compliance_feedback": {
                "compliance_warnings": [
                    {
                        "trigger": "compliance_score_dropping",
                        "template": "⚖️ Compliance Alert: Your compliance score has dropped to {score}%. Review your pending requirements and take action.",
                        "tone": "advisory"
                    },
                    {
                        "trigger": "deadline_missed",
                        "template": "⚖️ Deadline Missed: You've missed the deadline for {filing_name}. This may result in penalties. Take corrective action immediately.",
                        "tone": "urgent"
                    },
                    {
                        "trigger": "compliance_critical",
                        "template": "⚖️ Compliance Critical: Your compliance score is dangerously low. Multiple penalties and legal risks are imminent. Seek professional help immediately.",
                        "tone": "critical"
                    }
                ],
                "compliance_positive": [
                    {
                        "trigger": "compliance_milestone",
                        "template": "⚖️ Excellent compliance! You've maintained a {score}% compliance score. This discipline will pay dividends in avoiding problems.",
                        "tone": "positive"
                    },
                    {
                        "trigger": "filing_approved",
                        "template": "⚖️ Filing Approved: Your {filing_name} has been approved! Another compliance requirement checked off.",
                        "tone": "positive"
                    }
                ]
            },

            "decision_feedback": {
                "entity_selection": [
                    {
                        "trigger": "entity_selected_llc",
                        "template": "You've chosen an LLC - a flexible choice that provides liability protection with simpler taxation. Great for most small to medium businesses!",
                        "tone": "informative"
                    },
                    {
                        "trigger": "entity_selected_c_corp",
                        "template": "You've chosen a C-Corporation - the right choice if you're planning to raise venture capital or go public. Be prepared for more complex compliance.",
                        "tone": "informative"
                    },
                    {
                        "trigger": "entity_selected_s_corp",
                        "template": "You've chosen an S-Corporation - good for profitable businesses where owners want to take salaries. Remember the shareholder restrictions.",
                        "tone": "informative"
                    },
                    {
                        "trigger": "entity_selected_sole_prop",
                        "template": "You've chosen a Sole Proprietorship - the simplest option. Perfect for testing a business idea, but remember you have unlimited personal liability.",
                        "tone": "informative"
                    }
                ],
                "decision_consequence": [
                    {
                        "trigger": "good_decision",
                        "template": "Smart decision! Choosing {option} aligns well with your business goals. This should serve you well.",
                        "tone": "positive"
                    },
                    {
                        "trigger": "suboptimal_decision",
                        "template": "You've chosen {option}. This works, but be aware of {consequence}. You may want to revisit this decision as your business grows.",
                        "tone": "advisory"
                    }
                ]
            },

            "encouragement_messages": {
                "general_encouragement": [
                    "Every successful entrepreneur started exactly where you are now. Keep going!",
                    "Building a business is a marathon, not a sprint. You're making great progress!",
                    "The challenges you're facing today are building the resilience you'll need tomorrow.",
                    "Remember why you started this journey. You've got what it takes!",
                    "Progress, not perfection, is the goal. Celebrate every step forward!"
                ],
                "after_setback": [
                    "Setbacks are setups for comebacks. Learn from this and move forward stronger.",
                    "Every entrepreneur faces obstacles. What matters is how you respond. You've got this!",
                    "This is a temporary challenge, not a permanent failure. Adjust your approach and continue.",
                    "The businesses that succeed aren't those that never fail - they're those that never quit."
                ],
                "before_difficult_task": [
                    "This next step might feel challenging, but you're well-prepared. Take it one step at a time.",
                    "Many entrepreneurs find this step daunting. Break it down into smaller pieces and tackle them one by one.",
                    "You've handled tough challenges before. This is no different. Trust your abilities!"
                ]
            }
        },

        "3_milestone_celebrations": {
            "description": "Celebration events for achieving significant milestones",

            "milestones": [
                {
                    "milestone_id": "MS001",
                    "name": "First Steps",
                    "trigger": "complete_first_action",
                    "celebration": {
                        "type": "badge",
                        "badge_name": "First Steps",
                        "badge_icon": "👣",
                        "message": "Every journey begins with a single step. You've taken yours!",
                        "reward": {"knowledge": 5, "confidence": 10}
                    }
                },
                {
                    "milestone_id": "MS002",
                    "name": "Business Planner",
                    "trigger": "complete_phase_1",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Business Planner",
                        "badge_icon": "📋",
                        "message": "You've completed your business plan! A solid foundation is the key to success.",
                        "reward": {"knowledge": 15, "network": 5, "unlock": "investor_pitch_template"}
                    }
                },
                {
                    "milestone_id": "MS003",
                    "name": "Legally Born",
                    "trigger": "complete_phase_2",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Legally Born",
                        "badge_icon": "⚖️",
                        "message": "Your business is now a legal entity! You've navigated the bureaucracy like a pro.",
                        "reward": {"reputation": 10, "unlock": "legal_document_templates"}
                    }
                },
                {
                    "milestone_id": "MS004",
                    "name": "Compliance Champion",
                    "trigger": "complete_phase_3",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Compliance Champion",
                        "badge_icon": "🏆",
                        "message": "All licenses and permits secured! Your commitment to compliance will protect your business.",
                        "reward": {"compliance_bonus": 10, "reputation": 15}
                    }
                },
                {
                    "milestone_id": "MS005",
                    "name": "Operations Ready",
                    "trigger": "complete_phase_4",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Operations Ready",
                        "badge_icon": "🚀",
                        "message": "Your business infrastructure is complete! You're ready to focus on growth.",
                        "reward": {"efficiency_bonus": 15, "unlock": "growth_strategies"}
                    }
                },
                {
                    "milestone_id": "MS006",
                    "name": "Journey Complete",
                    "trigger": "complete_phase_5",
                    "celebration": {
                        "type": "grand_achievement",
                        "badge_name": "Journey Complete",
                        "badge_icon": "🌟",
                        "message": "Congratulations! You've completed the full business formation journey. Your business is launched and growing!",
                        "reward": {"reputation": 25, "unlock": "advanced_scaling_tools", "title": "Certified Entrepreneur"}
                    }
                },
                {
                    "milestone_id": "MS007",
                    "name": "First Customer",
                    "trigger": "acquire_first_customer",
                    "celebration": {
                        "type": "milestone",
                        "badge_name": "First Customer",
                        "badge_icon": "🎉",
                        "message": "You've acquired your first paying customer! This validates your business concept.",
                        "reward": {"reputation": 5, "confidence": 20}
                    }
                },
                {
                    "milestone_id": "MS008",
                    "name": "Revenue Milestone",
                    "trigger": "reach_revenue_target",
                    "celebration": {
                        "type": "milestone",
                        "badge_name": "Revenue Milestone",
                        "badge_icon": "💵",
                        "message": "You've hit your revenue target! Your business model is working.",
                        "reward": {"capital": "bonus", "reputation": 10}
                    }
                },
                {
                    "milestone_id": "MS009",
                    "name": "Team Builder",
                    "trigger": "hire_first_employee",
                    "celebration": {
                        "type": "milestone",
                        "badge_name": "Team Builder",
                        "badge_icon": "👥",
                        "message": "You've hired your first employee! Building a team is a major growth step.",
                        "reward": {"network": 10, "unlock": "hr_templates"}
                    }
                },
                {
                    "milestone_id": "MS010",
                    "name": "Funding Secured",
                    "trigger": "secure_funding",
                    "celebration": {
                        "type": "milestone",
                        "badge_name": "Funding Secured",
                        "badge_icon": "💰",
                        "message": "You've secured funding! This validation and capital will accelerate your growth.",
                        "reward": {"capital": "funding_amount", "reputation": 15}
                    }
                },
                {
                    "milestone_id": "MS011",
                    "name": "Compliance Perfection",
                    "trigger": "maintain_100_compliance_6_months",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Compliance Perfection",
                        "badge_icon": "✨",
                        "message": "Six months of perfect compliance! Your attention to detail is exemplary.",
                        "reward": {"compliance_bonus": 20, "reputation": 10}
                    }
                },
                {
                    "milestone_id": "MS012",
                    "name": "Speed Demon",
                    "trigger": "complete_journey_under_6_months",
                    "celebration": {
                        "type": "achievement",
                        "badge_name": "Speed Demon",
                        "badge_icon": "⚡",
                        "message": "Incredible! You completed the journey in under 6 months. Your execution is outstanding.",
                        "reward": {"time_bonus": 20, "reputation": 15}
                    }
                }
            ],

            "celebration_effects": {
                "badge": "Displayed in player profile, provides small stat boost",
                "achievement": "Unlocks new features or templates, moderate stat boost",
                "grand_achievement": "Major recognition, significant rewards, title unlock",
                "milestone": "Temporary morale boost, small rewards"
            }
        },

        "4_corrective_guidance_system": {
            "description": "System for providing help when players struggle or make mistakes",

            "struggle_detection": {
                "indicators": [
                    {
                        "indicator": "repeated_failures",
                        "trigger": "same_action_failed_3_times",
                        "severity": "medium"
                    },
                    {
                        "indicator": "time_stuck",
                        "trigger": "no_progress_2_weeks",
                        "severity": "medium"
                    },
                    {
                        "indicator": "resource_depletion",
                        "trigger": "capital_below_30_percent",
                        "severity": "high"
                    },
                    {
                        "indicator": "compliance_decline",
                        "trigger": "compliance_score_below_60",
                        "severity": "high"
                    },
                    {
                        "indicator": "avoidance_behavior",
                        "trigger": "skipping_difficult_actions",
                        "severity": "medium"
                    }
                ]
            },

            "guidance_interventions": [
                {
                    "intervention_id": "GI001",
                    "trigger": "repeated_failures",
                    "approach": "skill_building",
                    "message": "I notice you're having trouble with {action_name}. This is a common challenge. Would you like to:",
                    "options": [
                        "See a step-by-step guide",
                        "Watch a tutorial video",
                        "Connect with a mentor who's done this",
                        "Try a simplified version first"
                    ]
                },
                {
                    "intervention_id": "GI002",
                    "trigger": "time_stuck",
                    "approach": "motivation_and_clarity",
                    "message": "It looks like you've paused on {action_name}. This step can feel overwhelming. Let's break it down:",
                    "options": [
                        "Show me the next small step",
                        "Explain why this matters",
                        "Show me examples from similar businesses",
                        "I need encouragement"
                    ]
                },
                {
                    "intervention_id": "GI003",
                    "trigger": "resource_depletion",
                    "approach": "crisis_management",
                    "message": "Your capital is running low. Here are your immediate options:",
                    "options": [
                        "Review and cut non-essential expenses",
                        "Explore quick revenue opportunities",
                        "Consider bridge financing options",
                        "Connect with a financial advisor"
                    ],
                    "urgency": "high"
                },
                {
                    "intervention_id": "GI004",
                    "trigger": "compliance_decline",
                    "approach": "risk_mitigation",
                    "message": "Your compliance score is concerning. Missing requirements can lead to serious penalties. Let's prioritize:",
                    "options": [
                        "Show me the most critical pending items",
                        "Connect me with a compliance professional",
                        "Set up automatic reminders",
                        "Review penalty avoidance strategies"
                    ],
                    "urgency": "high"
                },
                {
                    "intervention_id": "GI005",
                    "trigger": "avoidance_behavior",
                    "approach": "reframing",
                    "message": "I notice you're focusing on easier tasks while {difficult_action} waits. This is natural, but let's address it:",
                    "options": [
                        "Help me understand why this matters",
                        "Break it into smaller steps",
                        "Show me the cost of delaying",
                        "Connect me with support"
                    ]
                }
            ],

            "hint_system": {
                "hint_levels": [
                    {
                        "level": 1,
                        "name": "Gentle Nudge",
                        "trigger": "first_sign_of_struggle",
                        "style": "Subtle suggestion",
                        "example": "Have you considered reviewing the requirements for this step?"
                    },
                    {
                        "level": 2,
                        "name": "Helpful Tip",
                        "trigger": "continued_struggle",
                        "style": "Specific guidance",
                        "example": "Many entrepreneurs find it helpful to start with the easiest sub-task first."
                    },
                    {
                        "level": 3,
                        "name": "Direct Help",
                        "trigger": "significant_struggle",
                        "style": "Step-by-step guidance",
                        "example": "Here's exactly what you need to do: 1) Gather documents A, B, C. 2) Fill out form X. 3) Submit to agency Y."
                    },
                    {
                        "level": 4,
                        "name": "Expert Intervention",
                        "trigger": "critical_situation",
                        "style": "Direct assistance offer",
                        "example": "This situation requires expert help. I can connect you with a professional who specializes in this area."
                    }
                ]
            },

            "recovery_paths": [
                {
                    "recovery_id": "RP001",
                    "situation": "capital_critical",
                    "recovery_plan": {
                        "immediate_actions": [
                            "Pause all non-essential spending",
                            "Accelerate accounts receivable collection",
                            "Negotiate payment terms with vendors",
                            "Consider emergency funding options"
                        ],
                        "short_term_actions": [
                            "Launch quick revenue campaign",
                            "Reduce burn rate by 30%",
                            "Explore bridge financing"
                        ],
                        "success_criteria": "Capital health above 40% within 4 weeks"
                    }
                },
                {
                    "recovery_id": "RP002",
                    "situation": "compliance_crisis",
                    "recovery_plan": {
                        "immediate_actions": [
                            "Identify all overdue filings",
                            "Calculate potential penalties",
                            "File emergency extensions where available",
                            "Consult with compliance professional"
                        ],
                        "short_term_actions": [
                            "Submit all overdue filings",
                            "Pay or negotiate penalties",
                            "Set up compliance tracking system"
                        ],
                        "success_criteria": "Compliance score above 80% within 6 weeks"
                    }
                },
                {
                    "recovery_id": "RP003",
                    "situation": "timeline_slippage",
                    "recovery_plan": {
                        "immediate_actions": [
                            "Reassess remaining timeline",
                            "Identify critical path activities",
                            "Consider scope adjustments"
                        ],
                        "short_term_actions": [
                            "Accelerate high-priority tasks",
                            "Delegate or outsource where possible",
                            "Adjust milestones if necessary"
                        ],
                        "success_criteria": "Back on track within 4 weeks or revised plan accepted"
                    }
                }
            ]
        },

        "5_assessment_reports": {
            "description": "Periodic assessment reports for player review",

            "report_types": [
                {
                    "report_id": "weekly_check_in",
                    "frequency": "weekly",
                    "sections": [
                        {
                            "section": "Progress Summary",
                            "metrics": ["actions_completed_this_week", "overall_progress_percentage", "phase_status"]
                        },
                        {
                            "section": "Resource Health",
                            "metrics": ["capital_remaining", "burn_rate", "runway_remaining"]
                        },
                        {
                            "section": "Compliance Status",
                            "metrics": ["compliance_score", "pending_deadlines", "upcoming_filings"]
                        },
                        {
                            "section": "This Week's Focus",
                            "content": "Recommended priorities based on current state"
                        }
                    ]
                },
                {
                    "report_id": "phase_completion_report",
                    "frequency": "per_phase",
                    "sections": [
                        {
                            "section": "Phase Summary",
                            "content": "Overview of completed phase"
                        },
                        {
                            "section": "Achievements",
                            "content": "Milestones and badges earned"
                        },
                        {
                            "section": "Lessons Learned",
                            "content": "Key takeaways from the phase"
                        },
                        {
                            "section": "Next Phase Preview",
                            "content": "What to expect in the upcoming phase"
                        },
                        {
                            "section": "Readiness Assessment",
                            "metrics": ["resource_readiness", "knowledge_readiness", "compliance_readiness"]
                        }
                    ]
                },
                {
                    "report_id": "journey_completion_report",
                    "frequency": "end_of_journey",
                    "sections": [
                        {
                            "section": "Journey Summary",
                            "content": "Complete overview of the entrepreneurial journey"
                        },
                        {
                            "section": "Final Metrics",
                            "metrics": ["total_time", "final_resources", "compliance_score", "revenue_achieved"]
                        },
                        {
                            "section": "Achievements Earned",
                            "content": "All badges and milestones"
                        },
                        {
                            "section": "Business Health Score",
                            "calculation": "Weighted average of all metrics"
                        },
                        {
                            "section": "Next Steps",
                            "content": "Recommendations for continued growth"
                        }
                    ]
                }
            ]
        }
    }

    return system


def create_assessment_documentation(system: dict) -> str:
    """Create human-readable markdown documentation for the assessment system."""

    doc = """# USA Business Journey - Assessment and Feedback System

## Overview

This document describes the comprehensive assessment and feedback system designed for the USA Business Journey simulation game. The system tracks player progress, provides contextual feedback, celebrates milestones, and offers corrective guidance when needed.

**Version:** 1.0
**Created:** """ + datetime.now().strftime("%Y-%m-%d") + """

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
"""

    return doc


def main():
    """Generate assessment system and save to processed directory."""
    processed_dir = Path("/home/sblo/Dev/UsaCom/processed")
    processed_dir.mkdir(exist_ok=True)

    # Create assessment system
    system = create_assessment_system()

    # Save JSON
    json_file = processed_dir / "assessment_system.json"
    with open(json_file, 'w') as f:
        json.dump(system, f, indent=2)

    # Create and save documentation
    doc = create_assessment_documentation(system)
    md_file = processed_dir / "assessment_system.md"
    with open(md_file, 'w') as f:
        f.write(doc)

    print("Assessment and Feedback System Generated")
    print(f"JSON output: {json_file}")
    print(f"Documentation: {md_file}")

    # Print summary
    print("\nSystem Components:")
    print(f"  - Progress Tracking Metrics: 5 categories")
    print(f"  - Feedback Templates: {sum(len(v) for v in system['2_feedback_message_templates'].values())} template groups")
    print(f"  - Milestone Celebrations: {len(system['3_milestone_celebrations']['milestones'])} milestones")
    print(f"  - Corrective Guidance: {len(system['4_corrective_guidance_system']['guidance_interventions'])} interventions")
    print(f"  - Assessment Reports: {len(system['5_assessment_reports']['report_types'])} report types")


if __name__ == "__main__":
    main()
