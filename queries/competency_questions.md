# Competency Questions for Space Exploration Knowledge Graph

## Domain: Space Exploration Missions and Agencies

### Motivation
These competency questions validate the ontology design and ensure the knowledge graph can answer meaningful queries about space missions, agencies, budgets, launch sites, and their relationships.

---

## CQ1: Mission Information Queries

### CQ1.1: What are all the space missions in the knowledge base?
**Purpose**: Validate basic class instantiation and retrieval
**SPARQL**: `query_01_all_missions.sparql`

### CQ1.2: What is the budget of a specific mission (e.g., Apollo 11)?
**Purpose**: Validate datatype property queries
**SPARQL**: `query_02_mission_budget.sparql`

### CQ1.3: Which missions were launched by NASA?
**Purpose**: Validate object property relationships
**SPARQL**: `query_03_missions_by_agency.sparql`

### CQ1.4: What are the launch dates of all Moon missions?
**Purpose**: Validate subclass queries and date filtering
**SPARQL**: `query_04_moon_missions_dates.sparql`

---

## CQ2: Agency and Organization Queries

### CQ2.1: Which agencies are government agencies?
**Purpose**: Validate subclass classification
**SPARQL**: `query_05_government_agencies.sparql`

### CQ2.2: Which missions were launched by private companies?
**Purpose**: Validate union classes and property restrictions
**SPARQL**: `query_06_private_company_missions.sparql`

### CQ2.3: What countries do the agencies belong to?
**Purpose**: Validate transitive relationships
**SPARQL**: `query_07_agency_countries.sparql`

---

## CQ3: Budget and Cost Analysis

### CQ3.1: Which missions have a budget greater than $1000 million?
**Purpose**: Validate defined classes (HighBudgetMission) and reasoning
**SPARQL**: `query_08_high_budget_missions.sparql`

### CQ3.2: What is the total budget of all successful missions?
**Purpose**: Validate aggregation and filtering
**SPARQL**: `query_09_total_budget_successful.sparql`

### CQ3.3: Which agency has the highest total mission budget?
**Purpose**: Validate grouping and aggregation
**SPARQL**: `query_10_agency_highest_budget.sparql`

---

## CQ4: Mission Success and Status

### CQ4.1: Which missions were successful?
**Purpose**: Validate enumeration class (LaunchStatus)
**SPARQL**: `query_11_successful_missions.sparql`

### CQ4.2: Which Moon missions were successful?
**Purpose**: Validate intersection classes (SuccessfulMoonMission)
**SPARQL**: `query_12_successful_moon_missions.sparql`

### CQ4.3: Which missions failed?
**Purpose**: Validate complement classes (FailedMission)
**SPARQL**: `query_13_failed_missions.sparql`

---

## CQ5: Launch Site and Location Queries

### CQ5.1: Which missions were launched from Kennedy Space Center?
**Purpose**: Validate launch site relationships
**SPARQL**: `query_14_missions_from_site.sparql`

### CQ5.2: How many missions were launched from each site?
**Purpose**: Validate counting and grouping
**SPARQL**: `query_15_launch_site_counts.sparql`

---

## CQ6: Mission Type Classification

### CQ6.1: Which missions are crewed missions?
**Purpose**: Validate subclass classification
**SPARQL**: `query_16_crewed_missions.sparql`

### CQ6.2: Which missions are Mars missions?
**Purpose**: Validate target-specific mission types
**SPARQL**: `query_17_mars_missions.sparql`

### CQ6.3: Which missions are interstellar missions?
**Purpose**: Validate mission type classification
**SPARQL**: `query_18_interstellar_missions.sparql`

---

## CQ7: Environmental Impact

### CQ7.1: Which missions have the highest environmental impact?
**Purpose**: Validate ordering and filtering
**SPARQL**: `query_19_high_environmental_impact.sparql`

### CQ7.2: What is the average environmental impact by agency?
**Purpose**: Validate aggregation and grouping
**SPARQL**: `query_20_avg_environmental_impact.sparql`

---

## CQ8: Rocket and Payload Queries

### CQ8.1: Which rockets are reusable?
**Purpose**: Validate subclass classification
**SPARQL**: `query_21_reusable_rockets.sparql`

### CQ8.2: What is the payload weight of missions?
**Purpose**: Validate payload relationships
**SPARQL**: `query_22_payload_weights.sparql`

---

## CQ9: Temporal Queries

### CQ9.1: Which missions were launched in 2023?
**Purpose**: Validate date filtering
**SPARQL**: `query_23_missions_2023.sparql`

### CQ9.2: What is the chronological order of Moon missions?
**Purpose**: Validate date ordering
**SPARQL**: `query_24_moon_missions_chronological.sparql`

---

## CQ10: Federated Queries (Linked Data)

### CQ10.1: Which agencies are linked to DBpedia?
**Purpose**: Validate interlinking with external datasets
**SPARQL**: `query_25_federated_dbpedia_agencies.sparql`

### CQ10.2: Get additional information about NASA from DBpedia
**Purpose**: Validate federated SPARQL queries
**SPARQL**: `query_26_federated_nasa_info.sparql`

---

## CQ11: Complex Reasoning Queries

### CQ11.1: Find commercial space flights (missions by private companies)
**Purpose**: Validate defined classes (CommercialSpaceFlight)
**SPARQL**: `query_27_commercial_space_flights.sparql`

### CQ11.2: Find non-government missions
**Purpose**: Validate complement classes
**SPARQL**: `query_28_non_government_missions.sparql`

---

## Validation Notes

- All queries should return results when executed against the populated knowledge graph
- Queries involving reasoning (HighBudgetMission, SuccessfulMoonMission, etc.) should leverage the reasoner
- Federated queries require access to external SPARQL endpoints (DBpedia, Wikidata)
- Some queries may return empty results if the data doesn't contain matching instances

