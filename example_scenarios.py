"""
Example Patient Scenarios for Testing
Demonstrates different patient profiles and recommended interventions
"""

# Patient profiles for testing different scenarios
PATIENT_PROFILES = {
    "high_risk_liver": {
        "name": "High Risk Liver Patient",
        "age": 42,
        "organ": "Liver",
        "risk_factors": [
            "Chronic alcohol consumption (3-4 drinks/day)",
            "Caffeine addiction (600mg/day)",
            "Sedentary lifestyle",
            "Poor sleep (5 hours/night)"
        ],
        "baseline_position": (2.5, 3.2, 2.8),
        "baseline_velocity": (0.35, 0.42, 0.38),
        "baseline_acceleration": (0.015, 0.018, 0.016),
        "description": "Patient with significant liver stress showing accelerated aging trajectory"
    },
    
    "moderate_cardiovascular": {
        "name": "Moderate Cardiovascular Risk",
        "age": 55,
        "organ": "Heart",
        "risk_factors": [
            "Mild hypertension",
            "Sedentary lifestyle",
            "Moderate stress",
            "Diet high in processed foods"
        ],
        "baseline_position": (1.5, 1.8, 1.6),
        "baseline_velocity": (0.18, 0.22, 0.19),
        "baseline_acceleration": (0.008, 0.010, 0.009),
        "description": "Middle-aged patient with moderate cardiovascular aging"
    },
    
    "young_healthy": {
        "name": "Young Healthy Individual",
        "age": 28,
        "organ": "Liver",
        "risk_factors": [
            "Occasional social drinking",
            "Active lifestyle",
            "Good sleep habits"
        ],
        "baseline_position": (0.3, 0.4, 0.35),
        "baseline_velocity": (0.06, 0.07, 0.06),
        "baseline_acceleration": (0.002, 0.002, 0.002),
        "description": "Young healthy individual with normal aging trajectory"
    },
    
    "elderly_declining": {
        "name": "Elderly Patient - Declining",
        "age": 72,
        "organ": "Brain",
        "risk_factors": [
            "Age-related cognitive decline",
            "Multiple comorbidities",
            "Polypharmacy",
            "Limited physical activity"
        ],
        "baseline_position": (3.8, 4.2, 3.9),
        "baseline_velocity": (0.45, 0.52, 0.48),
        "baseline_acceleration": (0.020, 0.025, 0.022),
        "description": "Elderly patient showing significant aging acceleration"
    }
}


# Recommended intervention scenarios
INTERVENTION_SCENARIOS = {
    "minimal_lifestyle": {
        "name": "Minimal Lifestyle Changes",
        "description": "Achievable changes for patients resistant to major interventions",
        "interventions": {
            "sleep_change": 1.0,
            "vo2max_change": 10.0,
            "alcohol_reduction": 30.0,
            "caffeine_reduction": 100.0,
            "nac_dose": 0,
            "metformin_dose": 0
        },
        "expected_improvement": "15-25% velocity reduction",
        "compliance_difficulty": "Low"
    },
    
    "moderate_comprehensive": {
        "name": "Moderate Comprehensive Plan",
        "description": "Balanced approach combining lifestyle and supplementation",
        "interventions": {
            "sleep_change": 2.0,
            "vo2max_change": 25.0,
            "alcohol_reduction": 70.0,
            "caffeine_reduction": 250.0,
            "nac_dose": 1200,
            "metformin_dose": 500
        },
        "expected_improvement": "40-55% velocity reduction",
        "compliance_difficulty": "Moderate"
    },
    
    "aggressive_reversal": {
        "name": "Aggressive Reversal Protocol",
        "description": "Maximum intervention for motivated patients with high risk",
        "interventions": {
            "sleep_change": 3.0,
            "vo2max_change": 45.0,
            "alcohol_reduction": 100.0,
            "caffeine_reduction": 400.0,
            "nac_dose": 1800,
            "metformin_dose": 1500
        },
        "expected_improvement": "60-75% velocity reduction",
        "compliance_difficulty": "High"
    },
    
    "alcohol_focused": {
        "name": "Alcohol Reduction Focus",
        "description": "Primarily targeting alcohol-related liver damage",
        "interventions": {
            "sleep_change": 1.5,
            "vo2max_change": 15.0,
            "alcohol_reduction": 90.0,
            "caffeine_reduction": 150.0,
            "nac_dose": 1600,
            "metformin_dose": 0
        },
        "expected_improvement": "50-60% velocity reduction (liver-specific)",
        "compliance_difficulty": "High (alcohol cessation)"
    },
    
    "metabolic_optimization": {
        "name": "Metabolic Optimization",
        "description": "Targeting metabolic dysfunction and insulin resistance",
        "interventions": {
            "sleep_change": 2.0,
            "vo2max_change": 35.0,
            "alcohol_reduction": 50.0,
            "caffeine_reduction": 200.0,
            "nac_dose": 600,
            "metformin_dose": 1500
        },
        "expected_improvement": "45-55% velocity reduction (metabolic axis)",
        "compliance_difficulty": "Moderate"
    },
    
    "antioxidant_boost": {
        "name": "Antioxidant & Recovery",
        "description": "Focusing on oxidative stress reduction and recovery",
        "interventions": {
            "sleep_change": 2.5,
            "vo2max_change": 20.0,
            "alcohol_reduction": 80.0,
            "caffeine_reduction": 300.0,
            "nac_dose": 2000,
            "metformin_dose": 500
        },
        "expected_improvement": "40-50% velocity reduction (oxidative axis)",
        "compliance_difficulty": "Moderate"
    }
}


# Timeline-based intervention strategies
INTERVENTION_TIMELINES = {
    "3_month_intensive": {
        "name": "3-Month Intensive Start",
        "description": "Rapid intervention to demonstrate results and build momentum",
        "phase_1": {
            "duration": "Weeks 1-4",
            "focus": "Alcohol reduction, sleep improvement, NAC supplementation",
            "interventions": {
                "sleep_change": 2.0,
                "vo2max_change": 10.0,
                "alcohol_reduction": 80.0,
                "caffeine_reduction": 200.0,
                "nac_dose": 1600,
                "metformin_dose": 0
            }
        },
        "phase_2": {
            "duration": "Weeks 5-12",
            "focus": "Add exercise, optimize supplements, maintain alcohol reduction",
            "interventions": {
                "sleep_change": 2.5,
                "vo2max_change": 30.0,
                "alcohol_reduction": 90.0,
                "caffeine_reduction": 250.0,
                "nac_dose": 1600,
                "metformin_dose": 1000
            }
        }
    },
    
    "6_month_sustainable": {
        "name": "6-Month Sustainable Build",
        "description": "Gradual escalation for long-term adherence",
        "phase_1": {
            "duration": "Months 1-2",
            "focus": "Sleep and basic lifestyle",
            "interventions": {
                "sleep_change": 1.5,
                "vo2max_change": 15.0,
                "alcohol_reduction": 50.0,
                "caffeine_reduction": 150.0,
                "nac_dose": 600,
                "metformin_dose": 0
            }
        },
        "phase_2": {
            "duration": "Months 3-4",
            "focus": "Increase exercise, reduce substances",
            "interventions": {
                "sleep_change": 2.0,
                "vo2max_change": 25.0,
                "alcohol_reduction": 75.0,
                "caffeine_reduction": 250.0,
                "nac_dose": 1200,
                "metformin_dose": 500
            }
        },
        "phase_3": {
            "duration": "Months 5-6",
            "focus": "Optimize all parameters",
            "interventions": {
                "sleep_change": 2.5,
                "vo2max_change": 35.0,
                "alcohol_reduction": 90.0,
                "caffeine_reduction": 300.0,
                "nac_dose": 1600,
                "metformin_dose": 1000
            }
        }
    },
    
    "12_month_transformation": {
        "name": "12-Month Complete Transformation",
        "description": "Comprehensive year-long protocol for complete trajectory reversal",
        "phase_1": {
            "duration": "Months 1-3",
            "focus": "Foundation building",
            "interventions": {
                "sleep_change": 1.5,
                "vo2max_change": 15.0,
                "alcohol_reduction": 60.0,
                "caffeine_reduction": 200.0,
                "nac_dose": 800,
                "metformin_dose": 0
            }
        },
        "phase_2": {
            "duration": "Months 4-6",
            "focus": "Intensification",
            "interventions": {
                "sleep_change": 2.0,
                "vo2max_change": 30.0,
                "alcohol_reduction": 80.0,
                "caffeine_reduction": 300.0,
                "nac_dose": 1400,
                "metformin_dose": 1000
            }
        },
        "phase_3": {
            "duration": "Months 7-9",
            "focus": "Optimization",
            "interventions": {
                "sleep_change": 2.5,
                "vo2max_change": 40.0,
                "alcohol_reduction": 95.0,
                "caffeine_reduction": 350.0,
                "nac_dose": 1800,
                "metformin_dose": 1500
            }
        },
        "phase_4": {
            "duration": "Months 10-12",
            "focus": "Maintenance and fine-tuning",
            "interventions": {
                "sleep_change": 2.5,
                "vo2max_change": 45.0,
                "alcohol_reduction": 100.0,
                "caffeine_reduction": 400.0,
                "nac_dose": 1600,
                "metformin_dose": 1500
            }
        }
    }
}


# Success stories (fictional examples for demonstration)
SUCCESS_CASES = {
    "case_1": {
        "patient": "Male, 45, Liver",
        "initial_state": {
            "aging_velocity": 0.42,
            "deviation_from_healthy": 185,
            "trajectory": "Rapidly diverging"
        },
        "interventions": "Aggressive reversal protocol (12 months)",
        "final_state": {
            "aging_velocity": 0.14,
            "deviation_from_healthy": 45,
            "trajectory": "Converging toward healthy"
        },
        "key_factors": [
            "Complete alcohol cessation",
            "Consistent exercise program",
            "NAC supplementation"
        ],
        "time_to_healthy": "18 months projected"
    },
    
    "case_2": {
        "patient": "Female, 52, Heart",
        "initial_state": {
            "aging_velocity": 0.28,
            "deviation_from_healthy": 95,
            "trajectory": "Moderate divergence"
        },
        "interventions": "Moderate comprehensive plan (6 months)",
        "final_state": {
            "aging_velocity": 0.16,
            "deviation_from_healthy": 35,
            "trajectory": "Stabilized, near healthy"
        },
        "key_factors": [
            "VO2max improvement through walking program",
            "Sleep hygiene improvements",
            "Metformin addition"
        ],
        "time_to_healthy": "9 months projected"
    }
}


def get_profile(profile_name: str):
    """Get a patient profile by name"""
    return PATIENT_PROFILES.get(profile_name)


def get_scenario(scenario_name: str):
    """Get an intervention scenario by name"""
    return INTERVENTION_SCENARIOS.get(scenario_name)


def get_timeline(timeline_name: str):
    """Get an intervention timeline by name"""
    return INTERVENTION_TIMELINES.get(timeline_name)


def list_all_profiles():
    """List all available patient profiles"""
    return list(PATIENT_PROFILES.keys())


def list_all_scenarios():
    """List all available intervention scenarios"""
    return list(INTERVENTION_SCENARIOS.keys())


def list_all_timelines():
    """List all available intervention timelines"""
    return list(INTERVENTION_TIMELINES.keys())


if __name__ == "__main__":
    print("=== Available Patient Profiles ===")
    for name, profile in PATIENT_PROFILES.items():
        print(f"\n{name}:")
        print(f"  {profile['description']}")
    
    print("\n\n=== Available Intervention Scenarios ===")
    for name, scenario in INTERVENTION_SCENARIOS.items():
        print(f"\n{name}:")
        print(f"  {scenario['description']}")
        print(f"  Expected: {scenario['expected_improvement']}")
    
    print("\n\n=== Available Intervention Timelines ===")
    for name, timeline in INTERVENTION_TIMELINES.items():
        print(f"\n{name}:")
        print(f"  {timeline['description']}")

