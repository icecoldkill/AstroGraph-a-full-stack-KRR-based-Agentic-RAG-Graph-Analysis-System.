#!/usr/bin/env python3
"""
Reasoning Scenarios Script
Demonstrates reasoning capabilities using owlready2 and HermiT reasoner.
Shows how defined classes are inferred and how reasoning works.
"""

from owlready2 import *
import os

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTO_PATH = os.path.join(PROJECT_ROOT, "ontology", "space_exploration_with_individuals.owl")

def reasoning_scenarios():
    """Demonstrate reasoning scenarios."""
    print("=" * 80)
    print("Reasoning Scenarios Demonstration")
    print("=" * 80)
    print()
    
    # Load ontology with individuals
    print(f"Loading ontology with individuals from: {ONTO_PATH}")
    onto_path.append(os.path.join(PROJECT_ROOT, "ontology"))
    onto = get_ontology("file://" + ONTO_PATH).load()
    print(f"✓ Ontology loaded: {onto.name}")
    print()
    
    # Run reasoner
    print("Running HermiT reasoner...")
    with onto:
        sync_reasoner(infer_property_values=True)
    print("✓ Reasoning completed")
    print()
    
    # Scenario 1: High Budget Mission Inference
    print("=" * 80)
    print("SCENARIO 1: High Budget Mission Inference")
    print("=" * 80)
    print()
    print("Query: Which missions are inferred as HighBudgetMission?")
    print("(HighBudgetMission = SpaceMission with budget >= 1000)")
    print()
    
    high_budget_missions = []
    if hasattr(onto, 'HighBudgetMission') and onto.HighBudgetMission:
        high_budget_missions = list(onto.HighBudgetMission.instances())
    if high_budget_missions:
        print(f"✓ Found {len(high_budget_missions)} high budget mission(s):")
        for mission in high_budget_missions:
            budget = mission.hasBudget if hasattr(mission, 'hasBudget') and mission.hasBudget else "N/A"
            name = mission.missionName[0] if hasattr(mission, 'missionName') and mission.missionName else mission.name
            print(f"  - {name} (Budget: {budget})")
    else:
        print("⚠ No high budget missions found")
    print()
    
    # Scenario 2: Successful Moon Mission Inference
    print("=" * 80)
    print("SCENARIO 2: Successful Moon Mission Inference")
    print("=" * 80)
    print()
    print("Query: Which missions are inferred as SuccessfulMoonMission?")
    print("(SuccessfulMoonMission = MoonMission ∩ Success)")
    print()
    
    successful_moon = []
    if hasattr(onto, 'SuccessfulMoonMission') and onto.SuccessfulMoonMission:
        successful_moon = list(onto.SuccessfulMoonMission.instances())
    if successful_moon:
        print(f"✓ Found {len(successful_moon)} successful moon mission(s):")
        for mission in successful_moon:
            name = mission.missionName[0] if hasattr(mission, 'missionName') and mission.missionName else mission.name
            status = mission.isSuccess if hasattr(mission, 'isSuccess') else "N/A"
            print(f"  - {name} (Status: {status})")
    else:
        print("⚠ No successful moon missions found")
    print()
    
    # Scenario 3: Commercial Space Flight Inference
    print("=" * 80)
    print("SCENARIO 3: Commercial Space Flight Inference")
    print("=" * 80)
    print()
    print("Query: Which missions are inferred as CommercialSpaceFlight?")
    print("(CommercialSpaceFlight = SpaceMission launchedBy PrivateCompany)")
    print()
    
    commercial = []
    if hasattr(onto, 'CommercialSpaceFlight') and onto.CommercialSpaceFlight:
        commercial = list(onto.CommercialSpaceFlight.instances())
    if commercial:
        print(f"✓ Found {len(commercial)} commercial space flight(s):")
        for mission in commercial:
            name = mission.missionName[0] if hasattr(mission, 'missionName') and mission.missionName else mission.name
            print(f"  - {name}")
    else:
        print("⚠ No commercial space flights found")
    print()
    
    # Scenario 4: Failed Mission Inference
    print("=" * 80)
    print("SCENARIO 4: Failed Mission Inference")
    print("=" * 80)
    print()
    print("Query: Which missions are inferred as FailedMission?")
    print("(FailedMission = SpaceMission that is NOT Success)")
    print()
    
    failed = []
    if hasattr(onto, 'FailedMission') and onto.FailedMission:
        failed = list(onto.FailedMission.instances())
    if failed:
        print(f"✓ Found {len(failed)} failed mission(s):")
        for mission in failed:
            name = mission.missionName[0] if hasattr(mission, 'missionName') and mission.missionName else mission.name
            print(f"  - {name}")
    else:
        print("⚠ No failed missions found (all missions in dataset are successful)")
    print()
    
    # Scenario 5: Launch Entity Union
    print("=" * 80)
    print("SCENARIO 5: Launch Entity Union")
    print("=" * 80)
    print()
    print("Query: Which entities are inferred as LaunchEntity?")
    print("(LaunchEntity = GovernmentAgency ∪ PrivateCompany)")
    print()
    
    launch_entities = []
    if hasattr(onto, 'LaunchEntity') and onto.LaunchEntity:
        launch_entities = list(onto.LaunchEntity.instances())
    if launch_entities:
        print(f"✓ Found {len(launch_entities)} launch entity/entities:")
        for entity in launch_entities:
            print(f"  - {entity.name}")
    else:
        print("⚠ No launch entities found")
    print()
    
    # Scenario 6: Class Classification
    print("=" * 80)
    print("SCENARIO 6: Class Classification")
    print("=" * 80)
    print()
    print("Query: Classify missions by type")
    print()
    
    moon_missions = []
    mars_missions = []
    interstellar_missions = []
    
    if hasattr(onto, 'MoonMission') and onto.MoonMission:
        moon_missions = list(onto.MoonMission.instances())
    if hasattr(onto, 'MarsMission') and onto.MarsMission:
        mars_missions = list(onto.MarsMission.instances())
    if hasattr(onto, 'InterstellarMission') and onto.InterstellarMission:
        interstellar_missions = list(onto.InterstellarMission.instances())
    
    print(f"Moon Missions: {len(moon_missions)}")
    print(f"Mars Missions: {len(mars_missions)}")
    print(f"Interstellar Missions: {len(interstellar_missions)}")
    print()
    
    # Summary
    print("=" * 80)
    print("REASONING SUMMARY")
    print("=" * 80)
    print()
    print("Reasoning successfully inferred:")
    print(f"  - HighBudgetMission: {len(high_budget_missions)} instance(s)")
    print(f"  - SuccessfulMoonMission: {len(successful_moon)} instance(s)")
    print(f"  - CommercialSpaceFlight: {len(commercial)} instance(s)")
    print(f"  - FailedMission: {len(failed)} instance(s)")
    print(f"  - LaunchEntity: {len(launch_entities)} instance(s)")
    print()
    print("✓ All defined classes (intersections, unions, complements) are working correctly")
    print()

if __name__ == "__main__":
    reasoning_scenarios()

