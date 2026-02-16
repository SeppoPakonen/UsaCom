#!/usr/bin/env python3
"""
Phase 5 Task 08: Generate Sample Business Scenarios
Create realistic business scenarios for testing the simulation.
"""

import json
from pathlib import Path
from datetime import datetime


def create_sample_scenarios() -> dict:
    """Create diverse business scenarios for simulation testing."""

    scenarios = {
        "title": "USA Business Journey - Sample Business Scenarios",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "Diverse business scenarios for testing the USA business formation simulation",
        "total_scenarios": 12,

        "scenario_categories": {
            "technology": {
                "description": "Technology-focused businesses with high growth potential",
                "characteristics": ["Scalable", "Innovation-driven", "VC-attractive"],
                "typical_challenges": ["Rapid scaling", "Talent acquisition", "Market timing"]
            },
            "retail": {
                "description": "Consumer-facing retail businesses",
                "characteristics": ["Location-dependent", "Inventory management", "Customer service"],
                "typical_challenges": ["Competition", "Cash flow", "Seasonal variations"]
            },
            "service": {
                "description": "Professional and personal service businesses",
                "characteristics": ["Skill-based", "Relationship-driven", "Low capital"],
                "typical_challenges": ["Client acquisition", "Time management", "Scaling services"]
            },
            "manufacturing": {
                "description": "Product manufacturing and distribution",
                "characteristics": ["Capital-intensive", "Supply chain", "Quality control"],
                "typical_challenges": ["Equipment costs", "Regulatory compliance", "Distribution"]
            },
            "food_beverage": {
                "description": "Restaurant, cafe, and food service businesses",
                "characteristics": ["High turnover", "Location critical", "Health regulations"],
                "typical_challenges": ["Staff turnover", "Food costs", "Health inspections"]
            },
            "healthcare": {
                "description": "Health and wellness service providers",
                "characteristics": ["Licensed professionals", "Insurance-based", "Trust-driven"],
                "typical_challenges": ["Licensing", "Insurance billing", "Liability"]
            }
        },

        "scenarios": [
            {
                "scenario_id": "SCN001",
                "name": "Tech Startup - SaaS Platform",
                "category": "technology",
                "description": "Two founders launching a B2B software-as-a-service platform for project management",
                "business_concept": {
                    "industry": "Software/Technology",
                    "product": "Cloud-based project management tool with AI features",
                    "target_market": "Small to medium businesses (10-500 employees)",
                    "revenue_model": "Monthly subscription ($29-299/user/month)",
                    "unique_value": "AI-powered task prioritization and automated reporting"
                },
                "funding_profile": {
                    "initial_capital": 75000,
                    "funding_source": "Personal savings + angel investor",
                    "burn_rate_monthly": 15000,
                    "runway_months": 5,
                    "future_funding_plans": "Seed round ($500K) at month 6"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 0,
                    "employees_year_1": 5,
                    "key_roles": ["CEO (technical)", "CTO (product)", "Developer", "Sales", "Support"],
                    "remote_first": True
                },
                "market_profile": {
                    "market_size": "$5.5B TAM",
                    "competition_level": "High",
                    "barriers_to_entry": "Medium",
                    "growth_potential": "High",
                    "geographic_scope": "Global (US launch first)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "C-Corporation",
                    "entity_reasoning": "Planning to raise VC funding and potentially IPO",
                    "phase_emphasis": {
                        "phase_1": "Heavy focus on market research and business plan for investors",
                        "phase_2": "C-Corp incorporation in Delaware",
                        "phase_3": "Standard compliance, IP protection critical",
                        "phase_4": "Tech infrastructure, minimal physical assets",
                        "phase_5": "Aggressive growth, multiple funding rounds"
                    },
                    "critical_actions": ["action_2_1", "action_2_4", "action_3_3", "action_5_2"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "6 months",
                    "customer_acquisition_target": "100 paying customers by month 12",
                    "revenue_target_year_1": "$250,000 ARR",
                    "funding_milestone": "Seed round closed by month 6",
                    "team_milestone": "5 full-time employees by month 12",
                    "compliance_score_required": 85
                },
                "risk_factors": [
                    {"risk": "Market competition", "severity": "High", "mitigation": "Focus on niche features"},
                    {"risk": "Running out of capital", "severity": "High", "mitigation": "Aggressive fundraising"},
                    {"risk": "Technical challenges", "severity": "Medium", "mitigation": "Experienced technical team"}
                ],
                "difficulty_level": "Hard"
            },
            {
                "scenario_id": "SCN002",
                "name": "Solo Tech Consultant",
                "category": "technology",
                "description": "Experienced software developer starting independent consulting practice",
                "business_concept": {
                    "industry": "Technology Consulting",
                    "product": "Custom software development and technical consulting",
                    "target_market": "Small businesses and startups needing technical expertise",
                    "revenue_model": "Hourly consulting ($150-250/hour) + project-based",
                    "unique_value": "Full-stack expertise with business acumen"
                },
                "funding_profile": {
                    "initial_capital": 10000,
                    "funding_source": "Personal savings",
                    "burn_rate_monthly": 3000,
                    "runway_months": 3,
                    "future_funding_plans": "Self-funded, reinvest profits"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 0,
                    "employees_year_1": 0,
                    "key_roles": ["Owner-operator (all functions)"],
                    "remote_first": True
                },
                "market_profile": {
                    "market_size": "$500B+ TAM",
                    "competition_level": "Medium",
                    "barriers_to_entry": "Low",
                    "growth_potential": "Medium",
                    "geographic_scope": "Remote (US-based clients)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection with simple taxation, no plans for outside investment",
                    "phase_emphasis": {
                        "phase_1": "Quick market validation, lean business plan",
                        "phase_2": "LLC formation in home state",
                        "phase_3": "Basic compliance, professional liability insurance",
                        "phase_4": "Minimal setup, home office",
                        "phase_5": "Organic growth, potential to add contractors"
                    },
                    "critical_actions": ["action_2_1", "action_2_3", "action_4_3", "action_4_2"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "1 month",
                    "customer_acquisition_target": "3 retainer clients by month 6",
                    "revenue_target_year_1": "$150,000",
                    "funding_milestone": "N/A - bootstrapped",
                    "team_milestone": "Remain solo or add 1 contractor",
                    "compliance_score_required": 90
                },
                "risk_factors": [
                    {"risk": "Income variability", "severity": "Medium", "mitigation": "Build 6-month emergency fund"},
                    {"risk": "Client concentration", "severity": "Medium", "mitigation": "Diversify client base"},
                    {"risk": "Burnout", "severity": "Medium", "mitigation": "Set boundaries, manage workload"}
                ],
                "difficulty_level": "Easy"
            },
            {
                "scenario_id": "SCN003",
                "name": "Boutique Retail Store",
                "category": "retail",
                "description": "Curated clothing and accessories boutique in urban location",
                "business_concept": {
                    "industry": "Retail Fashion",
                    "product": "Curated women's clothing, accessories, and gifts",
                    "target_market": "Women 25-45, middle to upper income",
                    "revenue_model": "In-store and online sales",
                    "unique_value": "Personalized styling services and unique brand selection"
                },
                "funding_profile": {
                    "initial_capital": 120000,
                    "funding_source": "Personal savings + SBA loan",
                    "burn_rate_monthly": 18000,
                    "runway_months": 6,
                    "future_funding_plans": "Reinvest profits, possible expansion loan year 3"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 2,
                    "employees_year_1": 4,
                    "key_roles": ["Owner/Manager", "Assistant Manager", "Sales Associates (2-3)"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$200M local market",
                    "competition_level": "High",
                    "barriers_to_entry": "Medium",
                    "growth_potential": "Medium",
                    "geographic_scope": "Local with online expansion"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection for retail risks, flexible management",
                    "phase_emphasis": {
                        "phase_1": "Location analysis, inventory planning",
                        "phase_2": "LLC formation, lease negotiations",
                        "phase_3": "Sales tax registration critical, local permits",
                        "phase_4": "POS system, inventory management, insurance",
                        "phase_5": "Local marketing, customer loyalty programs"
                    },
                    "critical_actions": ["action_2_1", "action_2_5", "action_3_2", "action_4_1", "action_4_3"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "4 months",
                    "customer_acquisition_target": "500 loyalty program members by month 12",
                    "revenue_target_year_1": "$400,000",
                    "funding_milestone": "SBA loan secured before opening",
                    "team_milestone": "4 employees trained by month 6",
                    "compliance_score_required": 95
                },
                "risk_factors": [
                    {"risk": "Location underperformance", "severity": "High", "mitigation": "Thorough site analysis"},
                    {"risk": "Inventory mismanagement", "severity": "High", "mitigation": "Inventory management system"},
                    {"risk": "E-commerce competition", "severity": "Medium", "mitigation": "Focus on experience and service"}
                ],
                "difficulty_level": "Medium"
            },
            {
                "scenario_id": "SCN004",
                "name": "E-commerce Store",
                "category": "retail",
                "description": "Online-only store selling specialty outdoor gear",
                "business_concept": {
                    "industry": "E-commerce Retail",
                    "product": "Camping, hiking, and outdoor adventure equipment",
                    "target_market": "Outdoor enthusiasts, ages 20-50",
                    "revenue_model": "Direct online sales, subscription box option",
                    "unique_value": "Curated gear bundles and expert content"
                },
                "funding_profile": {
                    "initial_capital": 50000,
                    "funding_source": "Personal savings + credit line",
                    "burn_rate_monthly": 8000,
                    "runway_months": 6,
                    "future_funding_plans": "Reinvest profits"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 0,
                    "employees_year_1": 2,
                    "key_roles": ["Co-founders", "Warehouse/packing (contractor)", "Customer service"],
                    "remote_first": True
                },
                "market_profile": {
                    "market_size": "$15B online outdoor gear market",
                    "competition_level": "Very High",
                    "barriers_to_entry": "Low",
                    "growth_potential": "High",
                    "geographic_scope": "National (US)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection, flexible for e-commerce operations",
                    "phase_emphasis": {
                        "phase_1": "Supplier relationships, platform selection",
                        "phase_2": "LLC formation, sales tax nexus analysis",
                        "phase_3": "Multi-state sales tax compliance critical",
                        "phase_4": "E-commerce platform, payment processing, fulfillment",
                        "phase_5": "Digital marketing, SEO, customer retention"
                    },
                    "critical_actions": ["action_2_1", "action_3_2", "action_4_2", "action_5_1"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "3 months",
                    "customer_acquisition_target": "1000 customers by month 12",
                    "revenue_target_year_1": "$300,000",
                    "funding_milestone": "Break even by month 10",
                    "team_milestone": "2 part-time helpers by month 8",
                    "compliance_score_required": 90
                },
                "risk_factors": [
                    {"risk": "Supplier reliability", "severity": "Medium", "mitigation": "Multiple suppliers"},
                    {"risk": "Shipping costs", "severity": "Medium", "mitigation": "Negotiated carrier rates"},
                    {"risk": "Customer acquisition costs", "severity": "High", "mitigation": "Focus on organic/SEO"}
                ],
                "difficulty_level": "Medium"
            },
            {
                "scenario_id": "SCN005",
                "name": "Marketing Agency",
                "category": "service",
                "description": "Digital marketing agency serving small businesses",
                "business_concept": {
                    "industry": "Marketing Services",
                    "product": "Social media management, SEO, PPC, content marketing",
                    "target_market": "Small businesses (5-50 employees)",
                    "revenue_model": "Monthly retainers ($2K-10K/month)",
                    "unique_value": "Full-service digital marketing with transparent reporting"
                },
                "funding_profile": {
                    "initial_capital": 25000,
                    "funding_source": "Personal savings",
                    "burn_rate_monthly": 5000,
                    "runway_months": 5,
                    "future_funding_plans": "Self-funded"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 0,
                    "employees_year_1": 4,
                    "key_roles": ["Co-founders (strategy/accounts)", "Content writer", "SEO specialist", "Ads manager"],
                    "remote_first": True
                },
                "market_profile": {
                    "market_size": "$200B+ digital marketing market",
                    "competition_level": "High",
                    "barriers_to_entry": "Low",
                    "growth_potential": "High",
                    "geographic_scope": "National (remote delivery)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection, flexible profit sharing among founders",
                    "phase_emphasis": {
                        "phase_1": "Service definition, pricing strategy",
                        "phase_2": "LLC formation, operating agreement critical",
                        "phase_3": "Business license, professional insurance",
                        "phase_4": "Project management tools, accounting system",
                        "phase_5": "Client acquisition, case studies, referrals"
                    },
                    "critical_actions": ["action_2_1", "action_2_4", "action_4_2", "action_4_4", "action_5_1"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "2 months",
                    "customer_acquisition_target": "10 retainer clients by month 12",
                    "revenue_target_year_1": "$360,000",
                    "funding_milestone": "N/A - bootstrapped",
                    "team_milestone": "4 team members by month 9",
                    "compliance_score_required": 85
                },
                "risk_factors": [
                    {"risk": "Client churn", "severity": "High", "mitigation": "Deliver results, regular communication"},
                    {"risk": "Cash flow gaps", "severity": "Medium", "mitigation": "Upfront payments, retainers"},
                    {"risk": "Talent retention", "severity": "Medium", "mitigation": "Culture, growth opportunities"}
                ],
                "difficulty_level": "Medium"
            },
            {
                "scenario_id": "SCN006",
                "name": "Home Cleaning Service",
                "category": "service",
                "description": "Residential cleaning service with subscription model",
                "business_concept": {
                    "industry": "Home Services",
                    "product": "Regular home cleaning, deep cleaning, move-in/out cleaning",
                    "target_market": "Dual-income families, busy professionals",
                    "revenue_model": "Per-visit pricing + subscription discounts",
                    "unique_value": "Background-checked staff, eco-friendly products, app booking"
                },
                "funding_profile": {
                    "initial_capital": 15000,
                    "funding_source": "Personal savings",
                    "burn_rate_monthly": 4000,
                    "runway_months": 3,
                    "future_funding_plans": "Reinvest profits"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 2,
                    "employees_year_1": 8,
                    "key_roles": ["Owner/Manager", "Cleaning Teams (2-4 people each)"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$50M local market",
                    "competition_level": "Medium",
                    "barriers_to_entry": "Low",
                    "growth_potential": "Medium",
                    "geographic_scope": "Local metro area"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection essential for service business with employees",
                    "phase_emphasis": {
                        "phase_1": "Service area analysis, pricing research",
                        "phase_2": "LLC formation, employment law compliance",
                        "phase_3": "Business license, bonding, insurance critical",
                        "phase_4": "Scheduling software, payroll system, vehicle setup",
                        "phase_5": "Local marketing, referral programs, reviews"
                    },
                    "critical_actions": ["action_2_1", "action_3_1", "action_4_2", "action_4_3", "action_5_2"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "2 months",
                    "customer_acquisition_target": "50 recurring clients by month 12",
                    "revenue_target_year_1": "$200,000",
                    "funding_milestone": "N/A - bootstrapped",
                    "team_milestone": "8 cleaners (2 teams) by month 10",
                    "compliance_score_required": 95
                },
                "risk_factors": [
                    {"risk": "Employee turnover", "severity": "High", "mitigation": "Competitive pay, culture"},
                    {"risk": "Liability claims", "severity": "Medium", "mitigation": "Thorough insurance, training"},
                    {"risk": "Scheduling inefficiency", "severity": "Medium", "mitigation": "Optimization software"}
                ],
                "difficulty_level": "Easy"
            },
            {
                "scenario_id": "SCN007",
                "name": "Specialty Food Manufacturing",
                "category": "manufacturing",
                "description": "Small-batch artisanal hot sauce production",
                "business_concept": {
                    "industry": "Food Manufacturing",
                    "product": "Premium artisanal hot sauces and condiments",
                    "target_market": "Food enthusiasts, specialty retailers, restaurants",
                    "revenue_model": "Wholesale to retailers + direct-to-consumer online",
                    "unique_value": "Unique flavor profiles, locally sourced ingredients"
                },
                "funding_profile": {
                    "initial_capital": 80000,
                    "funding_source": "Personal savings + equipment financing",
                    "burn_rate_monthly": 12000,
                    "runway_months": 6,
                    "future_funding_plans": "Revenue-based financing for expansion"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 2,
                    "employees_year_1": 5,
                    "key_roles": ["Co-founders", "Production Manager", "Sales Rep", "Warehouse"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$1.5B hot sauce market",
                    "competition_level": "Medium",
                    "barriers_to_entry": "Medium",
                    "growth_potential": "Medium",
                    "geographic_scope": "Regional expanding to national"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection for food products, flexible operations",
                    "phase_emphasis": {
                        "phase_1": "Recipe development, market testing, co-packer evaluation",
                        "phase_2": "LLC formation, FDA registration",
                        "phase_3": "Food facility registration, state health permits, labels",
                        "phase_4": "Production facility, liability insurance, distribution",
                        "phase_5": "Retail partnerships, trade shows, online growth"
                    },
                    "critical_actions": ["action_2_1", "action_3_1", "action_3_4", "action_4_3", "action_5_1"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "6 months",
                    "customer_acquisition_target": "25 retail accounts by month 12",
                    "revenue_target_year_1": "$350,000",
                    "funding_milestone": "Equipment financing secured",
                    "team_milestone": "5 employees by month 12",
                    "compliance_score_required": 98
                },
                "risk_factors": [
                    {"risk": "Food safety issues", "severity": "Critical", "mitigation": "HACCP plan, insurance"},
                    {"risk": "Retailer rejection", "severity": "High", "mitigation": "Start with local/specialty"},
                    {"risk": "Production scaling", "severity": "Medium", "mitigation": "Co-packer relationships"}
                ],
                "difficulty_level": "Hard"
            },
            {
                "scenario_id": "SCN008",
                "name": "Custom Furniture Workshop",
                "category": "manufacturing",
                "description": "Handcrafted custom furniture and cabinetry",
                "business_concept": {
                    "industry": "Custom Manufacturing",
                    "product": "Custom furniture, built-ins, and architectural millwork",
                    "target_market": "Homeowners, interior designers, contractors",
                    "revenue_model": "Project-based pricing",
                    "unique_value": "Heirloom quality, sustainable materials, custom designs"
                },
                "funding_profile": {
                    "initial_capital": 60000,
                    "funding_source": "Personal savings + equipment loan",
                    "burn_rate_monthly": 8000,
                    "runway_months": 7,
                    "future_funding_plans": "Reinvest profits"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 1,
                    "employees_year_1": 3,
                    "key_roles": ["Owner/Master Craftsman", "Apprentice", "Helper"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$15M local market",
                    "competition_level": "Low-Medium",
                    "barriers_to_entry": "Medium",
                    "growth_potential": "Medium",
                    "geographic_scope": "Regional (100-mile radius)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection, potential for growth",
                    "phase_emphasis": {
                        "phase_1": "Portfolio development, pricing strategy",
                        "phase_2": "LLC formation, workshop lease",
                        "phase_3": "Business license, sales tax, workers comp",
                        "phase_4": "Workshop setup, tool insurance, accounting",
                        "phase_5": "Portfolio marketing, designer relationships"
                    },
                    "critical_actions": ["action_2_1", "action_3_1", "action_3_2", "action_4_3", "action_5_1"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "3 months",
                    "customer_acquisition_target": "2 projects per month average",
                    "revenue_target_year_1": "$180,000",
                    "funding_milestone": "Equipment loan secured",
                    "team_milestone": "3 person team by month 10",
                    "compliance_score_required": 90
                },
                "risk_factors": [
                    {"risk": "Project delays", "severity": "Medium", "mitigation": "Buffer in timeline"},
                    {"risk": "Material cost volatility", "severity": "Medium", "mitigation": "Supplier relationships"},
                    {"risk": "Injury risk", "severity": "Medium", "mitigation": "Safety training, insurance"}
                ],
                "difficulty_level": "Medium"
            },
            {
                "scenario_id": "SCN009",
                "name": "Coffee Shop",
                "category": "food_beverage",
                "description": "Neighborhood coffee shop with light food menu",
                "business_concept": {
                    "industry": "Food Service",
                    "product": "Specialty coffee, espresso drinks, pastries, light lunch",
                    "target_market": "Local residents, remote workers, students",
                    "revenue_model": "In-store sales, catering, subscription",
                    "unique_value": "Community hub atmosphere, locally roasted beans"
                },
                "funding_profile": {
                    "initial_capital": 200000,
                    "funding_source": "Personal savings + SBA 7(a) loan",
                    "burn_rate_monthly": 25000,
                    "runway_months": 8,
                    "future_funding_plans": "Reinvest profits, possible second location"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 6,
                    "employees_year_1": 10,
                    "key_roles": ["Co-owners/Managers", "Head Barista", "Baristas (6-8)", "Kitchen staff"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$30M local market",
                    "competition_level": "High",
                    "barriers_to_entry": "Medium",
                    "growth_potential": "Medium",
                    "geographic_scope": "Local neighborhood"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection for food service, flexible management",
                    "phase_emphasis": {
                        "phase_1": "Location analysis, concept validation, financial projections",
                        "phase_2": "LLC formation, lease negotiation, buildout permits",
                        "phase_3": "Health department permits, food service license, liquor license",
                        "phase_4": "Equipment, POS, insurance, hiring",
                        "phase_5": "Grand opening, local marketing, loyalty program"
                    },
                    "critical_actions": ["action_2_1", "action_2_5", "action_3_1", "action_4_3", "action_5_1"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "8 months",
                    "customer_acquisition_target": "300 daily transactions by month 6",
                    "revenue_target_year_1": "$550,000",
                    "funding_milestone": "SBA loan closed before buildout",
                    "team_milestone": "10 staff trained by opening",
                    "compliance_score_required": 98
                },
                "risk_factors": [
                    {"risk": "Location underperformance", "severity": "Critical", "mitigation": "Thorough site analysis"},
                    {"risk": "Staff turnover", "severity": "High", "mitigation": "Good culture, competitive pay"},
                    {"risk": "Health violations", "severity": "Critical", "mitigation": "Strict protocols, training"}
                ],
                "difficulty_level": "Hard"
            },
            {
                "scenario_id": "SCN010",
                "name": "Food Truck",
                "category": "food_beverage",
                "description": "Gourmet taco food truck",
                "business_concept": {
                    "industry": "Food Service",
                    "product": "Gourmet tacos, burritos, Mexican street food",
                    "target_market": "Lunch crowds, events, late-night",
                    "revenue_model": "Direct sales, catering, events",
                    "unique_value": "Authentic recipes, premium ingredients, unique locations"
                },
                "funding_profile": {
                    "initial_capital": 80000,
                    "funding_source": "Personal savings + equipment financing",
                    "burn_rate_monthly": 12000,
                    "runway_months": 6,
                    "future_funding_plans": "Second truck or brick-and-mortar"
                },
                "team_profile": {
                    "founders": 2,
                    "employees_initial": 2,
                    "employees_year_1": 4,
                    "key_roles": ["Co-owners", "Cook", "Server/Cashier"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$10M local food truck market",
                    "competition_level": "Medium",
                    "barriers_to_entry": "Low-Medium",
                    "growth_potential": "Medium",
                    "geographic_scope": "Metro area"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC",
                    "entity_reasoning": "Liability protection for food service",
                    "phase_emphasis": {
                        "phase_1": "Menu development, location scouting",
                        "phase_2": "LLC formation, truck purchase/lease",
                        "phase_3": "Mobile food vendor permit, health permits, commissary",
                        "phase_4": "Truck outfitting, insurance, POS",
                        "phase_5": "Social media marketing, event bookings"
                    },
                    "critical_actions": ["action_2_1", "action_3_1", "action_4_3", "action_5_1"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "4 months",
                    "customer_acquisition_target": "200 daily transactions average",
                    "revenue_target_year_1": "$300,000",
                    "funding_milestone": "Truck financing secured",
                    "team_milestone": "4 person team by month 6",
                    "compliance_score_required": 95
                },
                "risk_factors": [
                    {"risk": "Weather dependency", "severity": "Medium", "mitigation": "Indoor events, catering"},
                    {"risk": "Truck breakdowns", "severity": "High", "mitigation": "Maintenance schedule, backup plan"},
                    {"risk": "Permit issues", "severity": "Medium", "mitigation": "Stay current on all permits"}
                ],
                "difficulty_level": "Medium"
            },
            {
                "scenario_id": "SCN011",
                "name": "Physical Therapy Clinic",
                "category": "healthcare",
                "description": "Outpatient physical therapy and sports rehabilitation",
                "business_concept": {
                    "industry": "Healthcare Services",
                    "product": "Physical therapy, sports rehab, injury prevention",
                    "target_market": "Athletes, injury recovery patients, seniors",
                    "revenue_model": "Insurance billing + cash-pay services",
                    "unique_value": "Specialized sports rehab, one-on-one sessions"
                },
                "funding_profile": {
                    "initial_capital": 150000,
                    "funding_source": "Personal savings + practice loan",
                    "burn_rate_monthly": 20000,
                    "runway_months": 7,
                    "future_funding_plans": "Reinvest profits"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 3,
                    "employees_year_1": 6,
                    "key_roles": ["Owner/PT", "Associate PTs (2)", "PTA", "Front desk", "Billing"],
                    "remote_first": False
                },
                "market_profile": {
                    "market_size": "$40M local market",
                    "competition_level": "Medium",
                    "barriers_to_entry": "High",
                    "growth_potential": "Medium",
                    "geographic_scope": "Local (15-mile radius)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "Professional LLC (PLLC) or PC",
                    "entity_reasoning": "Professional entity required for licensed healthcare in many states",
                    "phase_emphasis": {
                        "phase_1": "Market analysis, referral network development",
                        "phase_2": "PLLC/PC formation, professional licenses",
                        "phase_3": "Healthcare licenses, NPI, insurance credentialing",
                        "phase_4": "Clinic setup, EMR system, malpractice insurance",
                        "phase_5": "Physician referrals, community outreach"
                    },
                    "critical_actions": ["action_2_1", "action_3_1", "action_3_4", "action_4_3", "action_5_1"],
                    "accelerated_path": False
                },
                "success_metrics": {
                    "time_to_launch": "6 months",
                    "customer_acquisition_target": "40 patients/week by month 6",
                    "revenue_target_year_1": "$450,000",
                    "funding_milestone": "Practice loan secured",
                    "team_milestone": "6 staff by month 10",
                    "compliance_score_required": 98
                },
                "risk_factors": [
                    {"risk": "Insurance reimbursement delays", "severity": "High", "mitigation": "Cash reserve, billing service"},
                    {"risk": "Malpractice claims", "severity": "High", "mitigation": "Thorough documentation, insurance"},
                    {"risk": "Staff licensing", "severity": "Medium", "mitigation": "Track all licenses"}
                ],
                "difficulty_level": "Hard"
            },
            {
                "scenario_id": "SCN012",
                "name": "Wellness Coaching Practice",
                "category": "healthcare",
                "description": "Holistic health and wellness coaching",
                "business_concept": {
                    "industry": "Wellness Services",
                    "product": "Health coaching, nutrition guidance, wellness programs",
                    "target_market": "Health-conscious adults, corporate wellness",
                    "revenue_model": "Individual sessions, group programs, corporate contracts",
                    "unique_value": "Integrative approach, certified expertise"
                },
                "funding_profile": {
                    "initial_capital": 15000,
                    "funding_source": "Personal savings",
                    "burn_rate_monthly": 2500,
                    "runway_months": 6,
                    "future_funding_plans": "Self-funded"
                },
                "team_profile": {
                    "founders": 1,
                    "employees_initial": 0,
                    "employees_year_1": 1,
                    "key_roles": ["Owner/Coach", "Virtual Assistant (part-time)"],
                    "remote_first": True
                },
                "market_profile": {
                    "market_size": "$5B wellness coaching market",
                    "competition_level": "Medium",
                    "barriers_to_entry": "Low",
                    "growth_potential": "High",
                    "geographic_scope": "National (virtual delivery)"
                },
                "journey_path_mapping": {
                    "recommended_entity": "LLC or Sole Proprietorship",
                    "entity_reasoning": "Low risk, simple structure; LLC for liability protection",
                    "phase_emphasis": {
                        "phase_1": "Niche definition, program development",
                        "phase_2": "LLC formation (optional), certification verification",
                        "phase_3": "Business license, professional liability insurance",
                        "phase_4": "Website, scheduling system, payment processing",
                        "phase_5": "Content marketing, partnerships, corporate programs"
                    },
                    "critical_actions": ["action_2_1", "action_4_2", "action_4_3", "action_5_1"],
                    "accelerated_path": True
                },
                "success_metrics": {
                    "time_to_launch": "2 months",
                    "customer_acquisition_target": "20 ongoing clients by month 12",
                    "revenue_target_year_1": "$80,000",
                    "funding_milestone": "N/A - bootstrapped",
                    "team_milestone": "Part-time VA by month 8",
                    "compliance_score_required": 85
                },
                "risk_factors": [
                    {"risk": "Client acquisition", "severity": "Medium", "mitigation": "Content marketing, referrals"},
                    {"risk": "Scope of practice", "severity": "Medium", "mitigation": "Clear disclaimers, stay in lane"},
                    {"risk": "Income variability", "severity": "Medium", "mitigation": "Package programs, retainers"}
                ],
                "difficulty_level": "Easy"
            }
        ],

        "scenario_usage_guide": {
            "testing_purposes": [
                "Validate journey path recommendations",
                "Test entity selection decision tree",
                "Verify compliance requirements by industry",
                "Calibrate difficulty levels",
                "Test resource management mechanics"
            ],
            "difficulty_distribution": {
                "Easy": 3,
                "Medium": 5,
                "Hard": 4
            },
            "category_distribution": {
                "technology": 2,
                "retail": 2,
                "service": 2,
                "manufacturing": 2,
                "food_beverage": 2,
                "healthcare": 2
            }
        },

        "entity_recommendations_summary": {
            "LLC": {
                "count": 9,
                "scenarios": ["SCN002", "SCN003", "SCN004", "SCN005", "SCN006", "SCN007", "SCN008", "SCN009", "SCN010", "SCN012"],
                "reasoning": "Most versatile for small to medium businesses"
            },
            "C-Corporation": {
                "count": 1,
                "scenarios": ["SCN001"],
                "reasoning": "Required for VC-backed startups planning IPO"
            },
            "PLLC/PC": {
                "count": 1,
                "scenarios": ["SCN011"],
                "reasoning": "Required for licensed healthcare professionals"
            },
            "Sole Proprietorship": {
                "count": 1,
                "scenarios": ["SCN012"],
                "reasoning": "Optional for very low-risk solo practices"
            }
        }
    }

    return scenarios


def main():
    """Generate sample scenarios and save to processed directory."""
    processed_dir = Path("/home/sblo/Dev/UsaCom/processed")
    processed_dir.mkdir(exist_ok=True)

    # Create scenarios
    scenarios = create_sample_scenarios()

    # Save JSON
    output_file = processed_dir / "sample_scenarios.json"
    with open(output_file, 'w') as f:
        json.dump(scenarios, f, indent=2)

    print(f"Generated {scenarios['total_scenarios']} business scenarios")
    print(f"Output saved to: {output_file}")

    # Print summary
    print("\nScenario Distribution:")
    for category, count in scenarios['scenario_usage_guide']['category_distribution'].items():
        print(f"  - {category}: {count} scenarios")

    print("\nDifficulty Distribution:")
    for difficulty, count in scenarios['scenario_usage_guide']['difficulty_distribution'].items():
        print(f"  - {difficulty}: {count} scenarios")

    print("\nEntity Recommendations:")
    for entity, data in scenarios['entity_recommendations_summary'].items():
        print(f"  - {entity}: {data['count']} scenarios")


if __name__ == "__main__":
    main()
