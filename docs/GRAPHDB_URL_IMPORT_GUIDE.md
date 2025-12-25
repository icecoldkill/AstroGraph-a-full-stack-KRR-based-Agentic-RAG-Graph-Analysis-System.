# GraphDB URL Import Guide
## Following Professor's Instructions: Google Drive → GraphDB

This guide shows how to publish your RDF data as Linked Data via Google Drive and import it into GraphDB using URL.

---

## Step 1: Files Ready for Upload

Two N-Triples files have been created:
- `data/space_data.nt` (113 triples - your mission data)
- `ontology/space_exploration.nt` (225 triples - your ontology)

---

## Step 2: Upload to Google Drive

1. Go to [Google Drive](https://drive.google.com)
2. Upload both `.nt` files
3. Right-click each file → **Share**
4. Click **"Anyone with the link"** → **Viewer**
5. Click **Copy link**

---

## Step 3: Create Direct Download URL

Google Drive share links look like:
```
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

Convert to direct download link:
```
https://drive.google.com/uc?export=download&id=FILE_ID
```

**Example:**
- Share link: `https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing`
- Direct link: `https://drive.google.com/uc?export=download&id=1ABC123xyz`

---

## Step 4: Import into GraphDB via URL

1. Open [GraphDB Workbench](http://localhost:7200)
2. **Create Repository** (if not done):
   - Setup → Repositories → Create new repository
   - Repository ID: `space-missions`
3. **Import from URL**:
   - Click **Import** → **RDF**
   - Click **"Get RDF data from a URL"**
   - Paste your direct download URL
   - Click **Import**
4. Repeat for both files (ontology + data)

---

## Step 5: Visualize the Graph

1. Click **Explore** → **Visual Graph**
2. Search for:
   - `Apollo 11`
   - `NASA`
   - `SpaceX`
3. Expand nodes to see relationships
4. **Take screenshots** for your report!

---

## Step 6: Run SPARQL Queries

1. Click **SPARQL** tab
2. Use these queries:

### Query 1: All Successful Missions
```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>

SELECT ?missionName ?launchDate WHERE {
    ?m onto:missionName ?missionName .
    ?m onto:launchDate ?launchDate .
    ?m onto:isSuccess onto:Success .
}
```

### Query 2: All Failed Missions
```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>

SELECT ?missionName WHERE {
    ?m onto:missionName ?missionName .
    ?m onto:isSuccess onto:Failure .
}
```

### Query 3: Missions by NASA
```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>

SELECT ?missionName ?budget WHERE {
    ?m onto:missionName ?missionName .
    ?m onto:launchedBy ?a .
    FILTER(CONTAINS(LCASE(str(?a)), "nasa"))
    OPTIONAL { ?m onto:hasBudget ?budget }
}
```

### Query 4: High Budget Missions (>1000M)
```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>

SELECT ?missionName ?budget WHERE {
    ?m onto:missionName ?missionName .
    ?m onto:hasBudget ?budget .
    FILTER(?budget > 1000)
}
ORDER BY DESC(?budget)
```

### Query 5: Count by Agency
```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>

SELECT ?agency (COUNT(?m) AS ?count) WHERE {
    ?m onto:launchedBy ?agency .
}
GROUP BY ?agency
ORDER BY DESC(?count)
```

---

## Screenshots Checklist for Report

| Screenshot | Location |
|------------|----------|
| Repository Created | Setup → Repositories |
| Import from URL | Import → RDF → URL |
| Import Success | After import completes |
| Visual Graph - Apollo 11 | Explore → Visual Graph |
| Visual Graph - NASA | Explore → Visual Graph |
| SPARQL Query 1 Result | SPARQL tab |
| SPARQL Query 2 Result | SPARQL tab |
| SPARQL Query 3 Result | SPARQL tab |
| SPARQL Query 4 Result | SPARQL tab |
| SPARQL Query 5 Result | SPARQL tab |

---

## SPARQL Endpoint URL

After importing, your SPARQL endpoint is:
```
http://localhost:7200/repositories/space-missions
```

This can be used for federated queries from other applications!
