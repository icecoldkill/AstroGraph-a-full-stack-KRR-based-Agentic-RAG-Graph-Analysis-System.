from fastapi import FastAPI, UploadFile, File, HTTPException
import os

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.query import Result
import hashlib
import os
import shutil
import json
import glob
from agent import SpaceAgent
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Space Explorer Reasoning Engine Online", "version": "3.1"}

# Configuration
RDF_PATH = "/Users/ahsansaleem/Desktop/krrfinalproject/data/space_data.rdf"
QUERIES_DIR = "/Users/ahsansaleem/Desktop/krrfinalproject/queries"
GROQ_KEY = os.getenv("GROQ_API_KEY", "your_key_here")

agent = SpaceAgent(api_key=GROQ_KEY, sparql_endpoint="http://localhost:7200/repositories/space-mission")
client = Groq(api_key=GROQ_KEY)

# Load RDF graph
def get_graph():
    g = Graph()
    if os.path.exists(RDF_PATH):
        g.parse(RDF_PATH, format="xml")
    return g

class ChatRequest(BaseModel):
    message: str

class SparqlRequest(BaseModel):
    query: str
    format: str = "json"  # json, xml, csv, tsv

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        reply = agent.run_query(request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_and_process")
async def upload_document(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Dynamic KRR: Extract Triples using Groq
        prompt = f"""
        Extract knowledge from the text below and return ONLY valid RDF/Turtle triples.
        Use namespace: @prefix : <http://krr.org/space_exploration.owl#> .
        Text: {content[:4000]}
        
        Format:
        :EntityName a :Class ;
            :hasProperty "Value" .
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        
        turtle_data = completion.choices[0].message.content
        if "```turtle" in turtle_data:
            turtle_data = turtle_data.split("```turtle")[1].split("```")[0]
        elif "```" in turtle_data:
            turtle_data = turtle_data.split("```")[1].split("```")[0]
            
        # Update Graph
        g = Graph()
        g.parse(RDF_PATH, format="xml")
        try:
            g.parse(data=turtle_data, format="turtle")
            g.serialize(destination=RDF_PATH, format="xml")
            result = {"status": "Success", "triples_added": len(turtle_data.split('\n'))}
        except Exception as parse_err:
             result = {"status": "Partial", "error": str(parse_err), "raw": turtle_data}

        os.remove(temp_path)
        return result
        
    except Exception as e:
        if os.path.exists(temp_path): os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/summary")
def get_graph_summary():
    if not os.path.exists(RDF_PATH):
        raise HTTPException(status_code=404, detail="RDF data not found")
        
    g = Graph()
    g.parse(RDF_PATH, format="xml")
    
    nodes = []
    edges = []
    seen_nodes = set()
    
    # Compress/Summarize for visual performance
    for s, p, o in g:
        if len(nodes) > 400: break # Increased limit for 3D
        
        s_id = str(s).split('/')[-1].split('#')[-1]
        o_id = str(o).split('/')[-1].split('#')[-1]
        p_label = str(p).split('#')[-1] or str(p).split('/')[-1]
        
        if s_id not in seen_nodes:
            seen_nodes.add(s_id)
            # Simple heuristic for group color
            group = 1 if "Mission" in s_id else 2
            nodes.append({"id": s_id, "label": s_id, "group": group})
            
        if o_id not in seen_nodes:
            seen_nodes.add(o_id)
            group = 1 if "Mission" in o_id else 2
            nodes.append({"id": o_id, "label": o_id, "group": group})
            
        edges.append({"source": s_id, "target": o_id, "label": p_label})
        
    content = g.serialize(format="nt")
    graph_hash = hashlib.sha256(content.encode()).hexdigest()
    
    return {
        "hash": graph_hash,
        "data": {"nodes": nodes, "edges": edges}
    }

# SPARQL Endpoint
@app.post("/sparql")
def execute_sparql(request: SparqlRequest):
    """
    Execute a SPARQL query against the knowledge graph.
    Supports SELECT, ASK, CONSTRUCT, and DESCRIBE queries.
    """
    try:
        g = get_graph()
        results = g.query(request.query)
        
        # Format results based on query type
        if isinstance(results, Result):
            if results.type == 'SELECT':
                bindings = []
                for row in results:
                    binding = {}
                    for var in results.vars:
                        value = row[var]
                        if value:
                            binding[str(var)] = {
                                "type": "uri" if isinstance(value, URIRef) else "literal",
                                "value": str(value)
                            }
                    bindings.append(binding)
                
                return {
                    "head": {"vars": [str(v) for v in results.vars]},
                    "results": {"bindings": bindings}
                }
            elif results.type == 'ASK':
                return {"boolean": bool(results)}
            else:
                # CONSTRUCT or DESCRIBE
                result_graph = Graph()
                for triple in results:
                    result_graph.add(triple)
                return {
                    "format": request.format,
                    "data": result_graph.serialize(format=request.format)
                }
        else:
            return {"error": "Unexpected result type"}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SPARQL query error: {str(e)}")

@app.get("/sparql/query/{query_id}")
def execute_predefined_query(query_id: str):
    """
    Execute a predefined SPARQL query by ID (filename without .sparql extension).
    Example: /sparql/query/query_01_all_missions
    """
    query_file = os.path.join(QUERIES_DIR, f"{query_id}.sparql")
    
    if not os.path.exists(query_file):
        raise HTTPException(status_code=404, detail=f"Query file not found: {query_id}")
    
    try:
        with open(query_file, 'r') as f:
            query_str = f.read()
        
        g = get_graph()
        results = g.query(query_str)
        
        # Format as JSON
        if isinstance(results, Result):
            if results.type == 'SELECT':
                bindings = []
                for row in results:
                    binding = {}
                    for var in results.vars:
                        value = row[var]
                        if value:
                            binding[str(var)] = {
                                "type": "uri" if isinstance(value, URIRef) else "literal",
                                "value": str(value)
                            }
                    bindings.append(binding)
                
                return {
                    "query_id": query_id,
                    "head": {"vars": [str(v) for v in results.vars]},
                    "results": {"bindings": bindings}
                }
            elif results.type == 'ASK':
                return {"query_id": query_id, "boolean": bool(results)}
            else:
                result_graph = Graph()
                for triple in results:
                    result_graph.add(triple)
                return {
                    "query_id": query_id,
                    "format": "turtle",
                    "data": result_graph.serialize(format="turtle")
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing query: {str(e)}")

@app.get("/sparql/queries")
def list_queries():
    """
    List all available SPARQL queries.
    """
    query_files = glob.glob(os.path.join(QUERIES_DIR, "query_*.sparql"))
    queries = []
    
    for query_file in sorted(query_files):
        query_id = os.path.basename(query_file).replace('.sparql', '')
        with open(query_file, 'r') as f:
            query_content = f.read()
            # Extract first comment or first line as description
            first_line = query_content.split('\n')[0].strip()
            description = first_line.replace('#', '').strip() if first_line.startswith('#') else "SPARQL Query"
        
        queries.append({
            "id": query_id,
            "file": os.path.basename(query_file),
            "description": description
        })
    
    return {"queries": queries, "count": len(queries)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
