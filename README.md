# Global Space Exploration Knowledge Graph (GSE-KG)

This project is a Knowledge Representation and Reasoning (KRR) implementation that transforms space exploration data into a rich Knowledge Graph, extended with Agentic GraphRAG capabilities using Groq LLMs.

## Features
- **RDF/OWL Ontology**: 20+ classes and complex axioms (Cardinality, Enumeration, Unions).
- **Automated Data Pipeline**: Converts CSV data to RDF with interlinking to DBpedia.
- **Ontological Reasoning**: Uses HermiT to infer high-budget missions and mission classifications.
- **Agentic GraphRAG**: A Llama 3 powered agent that decides between SPARQL queries and Semantic Document search.
- **Interactive UI**: Streamlit dashboard for chat, data visualization, and document management.

## Project Structure
- `ontology/`: Contains the OWL files (with and without individuals).
- `data/`: Raw CSVs and generated RDF/TTL files.
- `src/`: Core logic (Ontology design, conversion, GraphRAG engine).
- `docs/`: Project reports and milestones.
- `queries/`: SPARQL competency questions.

## Setup & Installation
1. **Python Dependencies**:
   ```bash
   pip install streamlit groq langchain-huggingface rdflib owlready2 pandas networkx matplotlib chromadb
   ```
2. **Run the Application**:
   ```bash
   streamlit run src/app.py
   ```

## Usage
- **Chat**: Ask questions like "What is the budget of the Apollo 11 mission?" or "Which space agencies are linked to DBpedia?".
- **Documents**: Upload additional space-related documents to the sidebar to expand the knowledge base dynamically.
- **Graph**: Visualize the network of space missions and sites in the Graph tab.

## Groq API Key
The application is pre-configured with the provided Groq API key in the sidebar for immediate use.
