import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, OWL

# Load the dataset
df = pd.read_csv('data/space_missions.csv')

# Define Namespaces
EX = Namespace("http://krr.org/space/")
ONTO = Namespace("http://krr.org/space_exploration.owl#")
DBPEDIA = Namespace("http://dbpedia.org/resource/")

# Create a Graph
g = Graph()
g.bind("ex", EX)
g.bind("onto", ONTO)
g.bind("owl", OWL)

# Mapping CSV to RDF
for index, row in df.iterrows():
    mission_uri = EX[f"mission_{row['mission_id']}"]
    agency_uri = EX[f"agency_{row['agency'].replace(' ', '_')}"]
    rocket_uri = EX[f"rocket_{row['rocket'].replace(' ', '_')}"]
    launch_site_uri = EX[f"site_{row['launch_site'].replace(' ', '_')}"]
    
    # Mission triples
    g.add((mission_uri, RDF.type, ONTO.SpaceMission))
    g.add((mission_uri, ONTO.missionName, Literal(row['mission_name'], datatype=XSD.string)))
    g.add((mission_uri, ONTO.hasBudget, Literal(row['budget'], datatype=XSD.float)))
    g.add((mission_uri, ONTO.launchDate, Literal(row['launch_date'], datatype=XSD.date)))
    g.add((mission_uri, ONTO.environmentalImpact, Literal(row['environmental_impact'], datatype=XSD.integer)))
    
    # Success Status
    status_val = ONTO.Success if row['status'] == 'Success' else ONTO.Failure
    g.add((mission_uri, ONTO.isSuccess, status_val))
    
    # Special Mission Types
    if 'Moon' in row['mission_type']:
        g.add((mission_uri, RDF.type, ONTO.MoonMission))
    if 'Mars' in row['mission_type']:
        g.add((mission_uri, RDF.type, ONTO.MarsMission))
        
    # Agency triples
    agency_type = ONTO.PrivateCompany if row['agency_type'] == 'Private' else ONTO.GovernmentAgency
    g.add((agency_uri, RDF.type, agency_type))
    g.add((mission_uri, ONTO.launchedBy, agency_uri))
    
    # Link to DBpedia (Interlinking)
    # Simple heuristic: map Agency name to DBpedia
    if row['agency'] == 'NASA':
        g.add((agency_uri, OWL.sameAs, DBPEDIA.NASA))
    elif row['agency'] == 'SpaceX':
        g.add((agency_uri, OWL.sameAs, DBPEDIA.SpaceX))
    elif row['agency'] == 'ISRO':
        g.add((agency_uri, OWL.sameAs, DBPEDIA.Indian_Space_Research_Organisation))
    elif row['agency'] == 'Roscosmos':
        g.add((agency_uri, OWL.sameAs, DBPEDIA.Roscosmos))

    # Site and Rocket
    g.add((mission_uri, ONTO.launchedFrom, launch_site_uri))
    g.add((rocket_uri, RDF.type, ONTO.Rocket))
    g.add((rocket_uri, ONTO.hasAgency, agency_uri))

# Save the converted data
g.serialize(destination="/Users/ahsansaleem/Desktop/krrfinalproject/data/space_data.rdf", format="xml")
print(f"RDF data generated: {len(g)} triples.")
