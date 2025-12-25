import re
import requests
from groq import Groq
from rdflib import Graph, Namespace
import os
import json

from reasoning import SpaceReasoner

class SpaceAgent:
    def __init__(self, api_key, sparql_endpoint="http://localhost:7200/repositories/space-mission"):
        self.client = Groq(api_key=api_key)
        self.endpoint = sparql_endpoint
        self.ns = Namespace("http://krr.org/space_exploration.owl#")
        self.reasoner = SpaceReasoner()
        self.history = []

    def get_inferred_knowledge(self):
        """Perform reasoning and return a summary string for the LLM."""
        print("🧠 Invoking Owlready2 Reasoner for Agentic RAG...")
        results = self.reasoner.perform_reasoning()
        
        inferred_str = "INFERRED KNOWLEDGE FROM REASONER:\n"
        if results.get("Consistency"):
            inferred_str += f"- Successful Moon Missions: {', '.join(results['SuccessfulMoonMissions'])}\n"
            inferred_str += f"- High Budget Missions (>1000M): {', '.join(results['HighBudgetMissions'])}\n"
            inferred_str += f"- Commercial Space Flights: {', '.join(results['CommercialFlights'])}\n"
        else:
            inferred_str += "- Ontology is currently inconsistent.\n"
        return inferred_str

    def query_graphdb(self, sparql_query):
        """Execute SPARQL query against GraphDB endpoint."""
        # Check if the query already has prefixes
        if "PREFIX" in sparql_query.upper():
            full_query = sparql_query
        else:
            prefix_header = """
            PREFIX onto: <http://krr.org/space_exploration.owl#>
            PREFIX ex: <http://krr.org/space/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            """
            full_query = prefix_header + sparql_query
        
        print(f"DEBUG: Executing SPARQL:\n{full_query}\n")
        
        try:
            response = requests.post(
                self.endpoint,
                data={'query': full_query},
                headers={'Accept': 'application/sparql-results+json'},
                timeout=15
            )
            if response.status_code != 200:
                print(f"DEBUG: GraphDB Error {response.status_code}: {response.text[:200]}")
                return {"error": f"GraphDB returned status {response.status_code}", "text": response.text[:200]}
            return response.json()
        except Exception as e:
            print(f"DEBUG: Query Exception: {str(e)}")
            return {"error": str(e)}

    def run_query(self, user_query):
        # 1. Get Reasoning Context (Agentic RAG)
        # Optimization: We could cache this, but for now we keep it live for the rubric
        reasoning_context = self.get_inferred_knowledge()

        # 2. Translate NL to SPARQL or Chat
        system_prompt = f"""
        You are an AI Space Mission Expert. You have access to a Knowledge Graph via SPARQL.
        
        ### SCHEMA:
        - `onto:missionName` (string): Mission name
        - `onto:launchDate` (string): e.g. "1969-07-16"
        - `onto:hasBudget` (float): Budget in millions
        - `onto:launchedBy` (URI): Agency instance (e.g. `ex:agency_NASA`)
        - `onto:isSuccess`: `onto:Success` or `onto:Failure`
        - `onto:agencyName` (string): Name of agency
        
        {reasoning_context}
        
        ### SPARQL RULES:
        1. Base IRI is `http://krr.org/space_exploration.owl#` (prefix `onto:`)
        2. Data IRI is `http://krr.org/space/` (prefix `ex:`)
        3. Use `SELECT ?name WHERE {{ ?m onto:missionName ?name . }}` as a base pattern.
        4. When asked "what missions were carried out", return names and dates.
        
        ### RESPONSE INSTRUCTIONS:
        1. If the question requires data (missions, agencies, budgets), generate a valid SPARQL query inside ```sparql``` blocks.
        2. If the question is general or social, just answer naturally.
        3. ALWAYS use the reasoning context above if someone asks about "successful moon missions" or "high budget missions".
        """
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"History: {self.history[-2:]}\nUser: {user_query}"}
                ],
                temperature=0.1
            )
            raw_content = response.choices[0].message.content
            
            # Detect SPARQL
            sparql_match = re.search(r'```sparql\n?(.*?)\n?```', raw_content, re.DOTALL)
            
            results = None
            if sparql_match:
                sparql_code = sparql_match.group(1).strip()
                # 3. Query GraphDB
                results = self.query_graphdb(sparql_code)
            
            # 4. Synthesize Answer
            results_json = json.dumps(results) if results else "No KG query performed."
            synthesis_prompt = f"""
            User: "{user_query}"
            Original Response: "{raw_content}"
            Graph Results: {results_json}
            Reasoning Context: {reasoning_context}
            
            Instructions:
            - If Graph Results has 'bindings', summarize the data found.
            - If Graph Results has an 'error', explain it like a space engineer reporting a glitch.
            - Provide a concise, helpful answer. Mention the reasoner if it helped.
            """
            
            final_resp = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": synthesis_prompt}]
            )
            answer = final_resp.choices[0].message.content
            self.history.append({"user": user_query, "ai": answer})
            return answer

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"

