#!/usr/bin/env python3
"""
Script to validate all SPARQL competency questions against the knowledge graph.
This script executes all queries in the queries/ directory and reports results.
"""

import os
import glob
from rdflib import Graph
from rdflib.query import Result
import json

# Configuration
import sys
import os
# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RDF_PATH = os.path.join(PROJECT_ROOT, "data", "space_data.rdf")
QUERIES_DIR = os.path.join(PROJECT_ROOT, "queries")

def load_graph():
    """Load the RDF graph."""
    g = Graph()
    if os.path.exists(RDF_PATH):
        g.parse(RDF_PATH, format="xml")
        print(f"✓ Loaded graph with {len(g)} triples")
    else:
        print(f"✗ RDF file not found: {RDF_PATH}")
    return g

def execute_query(g, query_file):
    """Execute a SPARQL query and return results."""
    try:
        with open(query_file, 'r') as f:
            query_str = f.read()
        
        # Skip federated queries with SERVICE clause as RDFLib has limited support
        if "SERVICE" in query_str.upper():
            return None, "Federated queries (SERVICE) not fully supported by RDFLib. Use GraphDB/Virtuoso for full support."
        
        results = g.query(query_str)
        return results, None
    except Exception as e:
        return None, str(e)

def format_results(results):
    """Format query results for display."""
    if isinstance(results, Result):
        if results.type == 'SELECT':
            bindings = []
            for row in results:
                binding = {}
                for var in results.vars:
                    value = row[var]
                    if value:
                        binding[str(var)] = str(value)
                bindings.append(binding)
            return {
                "type": "SELECT",
                "vars": [str(v) for v in results.vars],
                "count": len(bindings),
                "sample": bindings[:5]  # Show first 5 results
            }
        elif results.type == 'ASK':
            return {
                "type": "ASK",
                "result": bool(results)
            }
        else:
            # CONSTRUCT or DESCRIBE
            triples = list(results)
            return {
                "type": results.type,
                "count": len(triples),
                "sample": [str(t) for t in triples[:5]]
            }
    return {"type": "unknown", "results": str(results)}

def main():
    """Main execution function."""
    print("=" * 80)
    print("SPARQL Competency Questions Validation")
    print("=" * 80)
    print()
    
    # Load graph
    g = load_graph()
    if len(g) == 0:
        print("Cannot proceed without a loaded graph.")
        return
    
    # Find all query files
    query_files = glob.glob(os.path.join(QUERIES_DIR, "query_*.sparql"))
    query_files.sort()
    
    if not query_files:
        print(f"No query files found in {QUERIES_DIR}")
        return
    
    print(f"Found {len(query_files)} query files\n")
    print("-" * 80)
    
    # Execute each query
    results_summary = {
        "total": len(query_files),
        "successful": 0,
        "failed": 0,
        "empty": 0,
        "details": []
    }
    
    for query_file in query_files:
        query_id = os.path.basename(query_file).replace('.sparql', '')
        print(f"\n[{query_id}]")
        print(f"File: {query_file}")
        
        results, error = execute_query(g, query_file)
        
        if error:
            print(f"✗ ERROR: {error}")
            results_summary["failed"] += 1
            results_summary["details"].append({
                "query_id": query_id,
                "status": "error",
                "error": error
            })
        else:
            formatted = format_results(results)
            
            if formatted["type"] == "SELECT":
                count = formatted["count"]
                if count == 0:
                    print(f"⚠ EMPTY: Query returned 0 results")
                    results_summary["empty"] += 1
                    status = "empty"
                else:
                    print(f"✓ SUCCESS: {count} result(s)")
                    results_summary["successful"] += 1
                    status = "success"
                    if count > 0:
                        print(f"  Variables: {', '.join(formatted['vars'])}")
                        print(f"  Sample results:")
                        for i, binding in enumerate(formatted["sample"], 1):
                            print(f"    {i}. {binding}")
                
                results_summary["details"].append({
                    "query_id": query_id,
                    "status": status,
                    "result_count": count,
                    "variables": formatted["vars"]
                })
            elif formatted["type"] == "ASK":
                result = formatted["result"]
                print(f"✓ ASK RESULT: {result}")
                results_summary["successful"] += 1
                results_summary["details"].append({
                    "query_id": query_id,
                    "status": "success",
                    "ask_result": result
                })
            else:
                print(f"✓ {formatted['type']}: {formatted['count']} triple(s)")
                results_summary["successful"] += 1
                results_summary["details"].append({
                    "query_id": query_id,
                    "status": "success",
                    "result_count": formatted["count"]
                })
        
        print("-" * 80)
    
    # Print summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Queries: {results_summary['total']}")
    print(f"✓ Successful: {results_summary['successful']}")
    print(f"⚠ Empty Results: {results_summary['empty']}")
    print(f"✗ Failed: {results_summary['failed']}")
    print()
    
    # Save detailed results to JSON
    output_file = "queries/validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results_summary, f, indent=2)
    print(f"Detailed results saved to: {output_file}")

if __name__ == "__main__":
    main()
