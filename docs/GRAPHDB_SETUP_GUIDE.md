# GraphDB Setup Guide for KRR Project
## Fulfilling Rubric Requirements 8, 11, 12

This guide helps you set up GraphDB to meet the project requirements for:
- Graph Validation and Visualization using GraphDB
- Graph Published via GraphDB with SPARQL Endpoint
- SPARQL Queries via GraphDB

---

## Step 1: Start GraphDB

After Docker is installed, run:
```bash
./start_graphdb.sh
```

Or manually:
```bash
docker-compose up -d
```

Wait ~30 seconds for GraphDB to initialize.

---

## Step 2: Access GraphDB Workbench

Open your browser and go to: **http://localhost:7200**

---

## Step 3: Create a Repository

1. Click **"Setup"** in the left sidebar
2. Click **"Repositories"**
3. Click **"Create new repository"**
4. Fill in:
   - **Repository ID**: `space-missions`
   - **Repository title**: `Space Exploration Knowledge Graph`
5. Click **"Create"**

---

## Step 4: Import Your RDF Data

1. Click **"Import"** in the left sidebar
2. Click **"RDF"**
3. Click **"Upload RDF files"**
4. Navigate to: `/Users/ahsansaleem/Desktop/krrfinalproject/graphdb-import/`
5. Select both files:
   - `space_exploration.owl` (Ontology)
   - `space_data.rdf` (Data)
6. Click **"Import"**

---

## Step 5: Run SPARQL Queries (For Screenshots)

1. Click **"SPARQL"** in the left sidebar
2. Copy queries from the `queries/` folder:
   - `graphdb_q1_successful_missions.sparql`
   - `graphdb_q2_failed_missions.sparql`
   - `graphdb_q3_nasa_missions.sparql`
   - `graphdb_q4_high_budget.sparql`
   - `graphdb_q5_missions_by_agency.sparql`
   - `graphdb_q6_federated_dbpedia.sparql`
3. **Take screenshots** of each query and result!

---

## Step 6: Visualize the Graph

1. Click **"Explore"** → **"Visual Graph"**
2. Search for an entity like `Apollo 11` or `NASA`
3. Expand nodes to see relationships
4. **Take screenshots** of the visualization!

---

## Step 7: View SPARQL Endpoint

Your SPARQL endpoint is available at:
```
http://localhost:7200/repositories/space-missions
```

This can be used for programmatic queries!

---

## Screenshots to Take for Report

| Screenshot | Location in GraphDB |
|------------|---------------------|
| Repository created | Setup → Repositories |
| Data imported | Import → RDF |
| SPARQL query results (x5) | SPARQL tab |
| Visual graph exploration | Explore → Visual Graph |
| SPARQL endpoint info | Setup → Repositories → space-missions |

---

## Stopping GraphDB

```bash
docker-compose down
```

To restart: `docker-compose up -d`
