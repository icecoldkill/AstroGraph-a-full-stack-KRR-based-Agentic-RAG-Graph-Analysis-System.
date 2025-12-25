from owlready2 import *
import pandas as pd
import os

# Paths
CSV_PATH = "/Users/ahsansaleem/Desktop/krrfinalproject/data/space_missions.csv"
ONTO_PATH = "/Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration.owl"

class SpaceReasoner:
    def __init__(self, onto_path=ONTO_PATH, csv_path=CSV_PATH):
        self.onto_path = onto_path
        self.csv_path = csv_path
        
    def perform_reasoning(self):
        print("🚀 Loading Ontology...")
        self.world = World()
        # Use a temporary directory for owlready cache to avoid permissions issues
        self.onto = self.world.get_ontology(f"file://{self.onto_path}").load()
        
        print("📊 Loading CSV and Creating Individuals...")
        df = pd.read_csv(self.csv_path)
        
        with self.onto:
            for _, row in df.iterrows():
                # Get the appropriate class
                mission_class = self.onto.SpaceMission
                if "Moon" in row['mission_type']:
                    mission_class = self.onto.MoonMission
                elif "Mars" in row['mission_type']:
                    mission_class = self.onto.MarsMission
                
                # Create mission instance
                m_id = f"mission_{row['mission_id']}"
                mission = mission_class(m_id)
                mission.missionName = [str(row['mission_name'])]
                mission.hasBudget = float(row['budget']) # Functional
                mission.launchDate = [str(row['launch_date'])]
                
                # Map success
                if row['status'] == 'Success':
                    mission.isSuccess = self.onto.Success # Functional
                else:
                    mission.isSuccess = self.onto.Failure # Functional

                # Agency
                a_name = f"agency_{row['agency'].replace(' ', '_')}"
                a_class = self.onto.PrivateCompany if row['agency_type'] == 'Private' else self.onto.GovernmentAgency
                agency = a_class(a_name)
                mission.launchedBy = [agency]

        print(f"📊 World contains {len(list(self.world.individuals()))} individuals.")
        
        print("🧠 Running Reasoner (HermiT)...")
        try:
            with self.onto:
                sync_reasoner(self.world)
            print("✅ Reasoning complete.")
            return self.get_inferred_facts()
        except Exception as e:
            print(f"❌ Error during reasoning: {e}")
            return {"error": str(e), "Consistency": False}

    def get_inferred_facts(self):
        facts = {
            "SuccessfulMoonMissions": [],
            "HighBudgetMissions": [],
            "FailedMissions": [],
            "CommercialFlights": [],
            "Consistency": True
        }
        
        # Mapping of defined class names to result keys
        class_map = {
            "SuccessfulMoonMission": "SuccessfulMoonMissions",
            "HighBudgetMission": "HighBudgetMissions",
            "FailedMission": "FailedMissions",
            "CommercialSpaceFlight": "CommercialFlights"
        }
        
        for onto_class_name, fact_key in class_map.items():
            onto_class = self.onto[onto_class_name]
            if onto_class:
                instances = onto_class.instances()
                # names only
                facts[fact_key] = [i.name for i in instances if not i.name in ["Success", "Failure", "PartialFailure", "Scheduled"]]
                print(f"Found {len(facts[fact_key])} inferred instances for {onto_class_name}")
        
        return facts

if __name__ == "__main__":
    reasoner = SpaceReasoner()
    results = reasoner.perform_reasoning()
    print("\n--- Reasoning Results ---")
    import json
    print(json.dumps(results, indent=2))
