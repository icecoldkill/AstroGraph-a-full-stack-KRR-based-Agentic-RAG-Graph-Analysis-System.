import os
from rdflib import Graph, Namespace
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

class GraphRAGEngine:
    def __init__(self, groq_api_key, rdf_path, vector_db_path="./chroma_db"):
        self.client = Groq(api_key=groq_api_key)
        self.g = Graph()
        self.g.parse(rdf_path, format="xml")
        self.onto_ns = Namespace("http://krr.org/space_exploration.owl#")
        self.ex_ns = Namespace("http://krr.org/space/")
        
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db_path = vector_db_path
        self.vector_db = None
        
        if os.path.exists(vector_db_path):
            self.vector_db = Chroma(persist_directory=vector_db_path, embedding_function=self.embeddings)
            
    def add_documents(self, file_paths):
        docs = []
        for path in file_paths:
            with open(path, 'r') as f:
                text = f.read()
                splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                chunks = splitter.split_text(text)
                for i, chunk in enumerate(chunks):
                    docs.append(Document(page_content=chunk, metadata={"source": path, "chunk": i}))
        
        if not self.vector_db:
            self.vector_db = Chroma.from_documents(docs, self.embeddings, persist_directory=self.vector_db_path)
        else:
            self.vector_db.add_documents(docs)
            
    def query_graph(self, sparql_query):
        try:
            results = self.g.query(sparql_query)
            return [str(row) for row in results]
        except Exception as e:
            return [f"Error in SPARQL: {e}"]

    def get_agent_response(self, user_query):
        # 1. Groq decides if it needs KG (SPARQL), Vector Search, or both.
        prompt = f"""
        You are an AI assistant for a Space Exploration Knowledge Graph.
        User Query: {user_query}
        
        Namespaces:
        - onto: <http://krr.org/space_exploration.owl#>
        - ex: <http://krr.org/space/>
        
        Available Tools:
        1. SPARQL: Query the Knowledge Graph (Missions, Agencies, Budgets, etc.)
        2. Vector Search: Search unstructured documents (Bios, Technical specs, etc.)
        
        Explain your plan and provide a SPARQL query if needed. Wrap the SPARQL query in ```sparql ... ```.
        If you need Vector Search, mention 'VECTOR_SEARCH_NEEDED'.
        """
        
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        plan = completion.choices[0].message.content
        
        kg_results = []
        if "```sparql" in plan:
            sparql = plan.split("```sparql")[1].split("```")[0].strip()
            kg_results = self.query_graph(sparql)
            
        vector_results = []
        if "VECTOR_SEARCH_NEEDED" in plan and self.vector_db:
            vector_results = self.vector_db.similarity_search(user_query, k=3)
            vector_results = [doc.page_content for doc in vector_results]
            
        # 2. Synthesize final answer
        final_prompt = f"""
        User Query: {user_query}
        KG Results: {kg_results}
        Document Results: {vector_results}
        
        Provide a comprehensive answer based on the above context.
        """
        
        final_completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": final_prompt}]
        )
        return final_completion.choices[0].message.content
