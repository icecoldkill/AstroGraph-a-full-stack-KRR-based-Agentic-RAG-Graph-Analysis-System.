# SPARQL Endpoint Documentation

## Overview

The Space Exploration Knowledge Graph provides a RESTful SPARQL endpoint for querying the RDF data. The endpoint is accessible through both the Python FastAPI backend and the Node.js proxy.

## Endpoints

### 1. Execute Custom SPARQL Query

**POST** `/api/sparql` (via Node.js) or `/sparql` (direct Python)

**Request Body:**
```json
{
  "query": "PREFIX onto: <http://krr.org/space_exploration.owl#>\nSELECT ?mission WHERE { ?mission a onto:SpaceMission . }",
  "format": "json"
}
```

**Response:**
```json
{
  "head": {
    "vars": ["mission"]
  },
  "results": {
    "bindings": [
      {
        "mission": {
          "type": "uri",
          "value": "http://krr.org/space/mission_1"
        }
      }
    ]
  }
}
```

### 2. List Available Queries

**GET** `/api/sparql/queries`

**Response:**
```json
{
  "queries": [
    {
      "id": "query_01_all_missions",
      "file": "query_01_all_missions.sparql",
      "description": "Query to retrieve all space missions"
    }
  ],
  "count": 28
}
```

### 3. Execute Predefined Query

**GET** `/api/sparql/query/{query_id}`

**Example:** `/api/sparql/query/query_01_all_missions`

**Response:**
```json
{
  "query_id": "query_01_all_missions",
  "head": {
    "vars": ["mission", "missionName"]
  },
  "results": {
    "bindings": [...]
  }
}
```

## Usage Examples

### Using cURL

```bash
# Execute a custom query
curl -X POST http://localhost:5001/api/sparql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "PREFIX onto: <http://krr.org/space_exploration.owl#>\nSELECT ?mission WHERE { ?mission a onto:SpaceMission . } LIMIT 5"
  }'

# List all queries
curl http://localhost:5001/api/sparql/queries

# Execute a predefined query
curl http://localhost:5001/api/sparql/query/query_01_all_missions
```

### Using Python

```python
import requests

# Execute custom query
response = requests.post('http://localhost:5001/api/sparql', json={
    'query': '''
        PREFIX onto: <http://krr.org/space_exploration.owl#>
        SELECT ?mission ?missionName WHERE {
            ?mission a onto:SpaceMission .
            ?mission onto:missionName ?missionName .
        } LIMIT 10
    '''
})
results = response.json()
print(results)
```

### Using JavaScript/Node.js

```javascript
const axios = require('axios');

// Execute custom query
const response = await axios.post('http://localhost:5001/api/sparql', {
    query: `
        PREFIX onto: <http://krr.org/space_exploration.owl#>
        SELECT ?mission ?missionName WHERE {
            ?mission a onto:SpaceMission .
            ?mission onto:missionName ?missionName .
        } LIMIT 10
    `
});
console.log(response.data);
```

## Query Validation

Run the validation script to test all competency questions:

```bash
cd /Users/ahsansaleem/Desktop/krrfinalproject
python src/run_queries.py
```

This will:
- Execute all queries in the `queries/` directory
- Report success/failure for each query
- Generate a validation report in `queries/validation_results.json`

## Supported Query Types

1. **SELECT**: Returns variable bindings (most common)
2. **ASK**: Returns boolean true/false
3. **CONSTRUCT**: Returns an RDF graph
4. **DESCRIBE**: Returns RDF description of resources

## Namespaces

Common namespaces used in queries:

- `onto:` - `http://krr.org/space_exploration.owl#`
- `ex:` - `http://krr.org/space/`
- `rdf:` - `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
- `rdfs:` - `http://www.w3.org/2000/01/rdf-schema#`
- `owl:` - `http://www.w3.org/2002/07/owl#`
- `xsd:` - `http://www.w3.org/2001/XMLSchema#`

## Federated Queries

For federated queries with DBpedia or Wikidata, you can use the SERVICE clause:

```sparql
PREFIX onto: <http://krr.org/space_exploration.owl#>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?mission ?dbpediaInfo WHERE {
    ?mission a onto:SpaceMission .
    ?mission onto:launchedBy ?agency .
    ?agency owl:sameAs dbr:NASA .
    
    SERVICE <http://dbpedia.org/sparql> {
        dbr:NASA <http://dbpedia.org/ontology/abstract> ?dbpediaInfo .
        FILTER (lang(?dbpediaInfo) = "en")
    }
}
```

**Note:** Federated queries require the SPARQL endpoint to support SERVICE clauses. The current implementation uses RDFLib which has limited federated query support. For full federated query support, consider using GraphDB or Virtuoso.

## Error Handling

The endpoint returns appropriate HTTP status codes:

- `200 OK`: Query executed successfully
- `400 Bad Request`: Invalid SPARQL query syntax
- `404 Not Found`: Query file not found (for predefined queries)
- `500 Internal Server Error`: Server error during query execution

Error responses include a detail message:

```json
{
  "detail": "SPARQL query error: ..."
}
```

