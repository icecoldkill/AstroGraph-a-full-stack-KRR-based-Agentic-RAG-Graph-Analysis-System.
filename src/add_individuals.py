from owlready2 import *

# Load the ontology
onto_path.append("/Users/ahsansaleem/Desktop/krrfinalproject/ontology/")
onto = get_ontology("space_exploration.owl").load()

# Add 10 individuals with annotations (as required by project)
with onto:
    # Individual 1: Neil Armstrong (Astronaut)
    neil = onto.Astronaut("Neil_Armstrong")
    neil.comment = ["The first human to walk on the moon."]
    
    # Individual 2: Saturn V
    saturn_v = onto.Rocket("Saturn_V")
    saturn_v.comment = ["The rocket used for the Apollo 11 mission."]
    
    # Individual 3: Apollo 11
    apollo11 = onto.SpaceMission("Apollo_11_Manual")
    apollo11.missionName = ["Apollo 11"]
    apollo11.isSuccess = onto.Success
    apollo11.hasBudget = 25400.0
    
    # ... previous individuals ...
    
    # Individual 9: Perseverance
    perseverance = onto.Payload("Perseverance_Rover")
    perseverance.payloadWeight = [1025.0]

    # Individual 10: Kennedy Space Center
    ksc = onto.SpacePort("Kennedy_Space_Center_Manual")
    ksc.comment = ["Primary launch site for NASA's human spaceflight."]

# Run reasoner
print("Running HermiT reasoner...")
with onto:
    sync_reasoner(infer_property_values=True)

# Save the ontology with individuals
onto.save(file="/Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration_with_individuals.owl", format="rdfxml")
print("Ontology with individuals saved.")
