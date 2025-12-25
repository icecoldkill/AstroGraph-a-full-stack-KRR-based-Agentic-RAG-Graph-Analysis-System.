from rdflib import Graph, Namespace
import os

# Define Paths
BASE_DIR = "/Users/ahsansaleem/Desktop/krrfinalproject"
ONTO_PATH = os.path.join(BASE_DIR, "ontology/space_exploration.owl")
DATA_PATH = os.path.join(BASE_DIR, "data/space_data.rdf")
OUTPUT_PATH = os.path.join(BASE_DIR, "ontology/protege_ready_space.owl")

def merge_krr_files():
    print("🚀 Starting Merge for Protégé...")
    
    # 1. Create a new graph
    full_graph = Graph()
    
    # 2. Load the Ontology (T-Box)
    print(f"📖 Loading Ontology: {ONTO_PATH}")
    full_graph.parse(ONTO_PATH, format="xml")
    
    # 3. Load the Data (A-Box)
    print(f"📖 Loading Data: {DATA_PATH}")
    full_graph.parse(DATA_PATH, format="xml")
    
    # 4. Serialize to a single file
    print(f"💾 Saving Merged File: {OUTPUT_PATH}")
    full_graph.serialize(destination=OUTPUT_PATH, format="xml")
    
    print("\n✅ Success! You can now open 'protege_ready_space.owl' in Protégé.")
    print("1. File -> Open -> ontology/protege_ready_space.owl")
    print("2. Reasoner -> Start Reasoner (HermiT)")
    print("3. File -> Export Inferred Axioms as Ontology...")

if __name__ == "__main__":
    merge_krr_files()
