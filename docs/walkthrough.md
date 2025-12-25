# Walkthrough - Global Space Exploration Knowledge Graph

## Overview
This project successfully transformed a non-RDF space exploration dataset into a structured Knowledge Graph. The KG includes complex ontological axioms, reasoning capabilities, and interlinking with the Linked Open Data cloud (DBpedia).

## Accomplishments
- [x] **Ontology Design**: 20+ classes, 14+ properties, and complex axioms (Union, Intersection, Cardinality).
- [x] **Data Conversion**: Automated mapping of CSV data to RDF/OWL using Python and RDFLib.
- [x] **Interlinking**: Successfully linked local agency entities to DBpedia resources using `owl:sameAs`.
- [x] **Reasoning**: Used the HermiT reasoner to infer implicit classes, such as `HighBudgetMission` for missions exceeding $1B.
- [x] **Validation**: Verified the graph against 7 competency questions using SPARQL.

## Key Artifacts
- **Ontology File**: [space_exploration.owl](file:///Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration.owl)
- **Converted RDF**: [space_data.rdf](file:///Users/ahsansaleem/Desktop/krrfinalproject/data/space_data.rdf)
- **Validation Script**: [run_queries.py](file:///Users/ahsansaleem/Desktop/krrfinalproject/src/run_queries.py)

## Evidence of Work

### SPARQL Query Results
The following queries demonstrate the utility of the dataset:

| Query Type | Results Found | Description |
|---|---|---|
| Budget Analysis | 4 Missions | Identified missions with budget > $1B (Apollo 11, Artemis I, etc.) |
| Moon Missions | 3 Missions | Filtered successful missions targeting the Moon. |
| Interlinking | 4 Agencies | Verified links to DBpedia for NASA, SpaceX, ISRO, and Roscosmos. |

### Reasoning Inference
The reasoner successfully inferred:
- `Apollo_11_Manual` as a `HighBudgetMission`.
- `SuccessfulMoonMission` classification based on target and status.

## Visualizing the Knowledge Graph
> [!TIP]
> You can load the [space_data.rdf](file:///Users/ahsansaleem/Desktop/krrfinalproject/data/space_data.rdf) file into [GraphDB](https://graphdb.ontotext.com/) or [VOWL](http://vowl.visualdataweb.org/webvowl.html) for a rich graphical representation of the entities and their relationships.

## Extended Features: Agentic GraphRAG & UI
- **Agentic Reasoning**: Integrated **Groq (Llama 3)** to dynamically decide between querying the RDF Knowledge Graph and searching through unstructured documents.
- **Dynamic Enrichment**: Users can upload custom CSV/Txt files to add new context to the system without retraining.
- **Premium UI**: Built a Streamlit-based interface with dark mode, interactive chat, and graph visualization.

## How to Run
1. **Launch the UI**:
   ```bash
   streamlit run src/app.py
   ```
2. **Interact**: Enter your Groq API key in the sidebar and start chatting with the Space Explorer KG!

| Feature | Description |
|---|---|
| SPARQL Generator | Groq translates natural language into precise SPARQL queries. |
| Hybrid Retrieval | Combines KG facts with document-based semantic search. |
| Graph Visualization | View the relationships between agencies, missions, and sites. |

## Reflection
This extension demonstrates the power of combining traditional symbolic AI (Ontology + Reasoner) with modern LLMs. The result is a system that is both logically sound (KG) and highly flexible and user-friendly (LLM + UI).
