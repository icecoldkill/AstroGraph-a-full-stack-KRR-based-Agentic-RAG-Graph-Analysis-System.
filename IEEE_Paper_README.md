# IEEE Paper: Global Space Exploration Knowledge Graph

## Overview

This directory contains the complete IEEE conference paper for the Global Space Exploration Knowledge Graph (GSE-KG) project, titled **"Global Space Exploration Knowledge Graph: An Agentic GraphRAG Approach to Semantic Space Mission Data Integration"**.

## Files

- **`GSE_KG_IEEE_Paper.tex`** - Main LaTeX source file for the IEEE paper
- **`compile_paper.sh`** - Bash script to compile the paper with proper formatting
- **`IEEE_Paper_README.md`** - This documentation file

## Paper Contents

The IEEE paper includes the following sections:

### 1. Abstract
Comprehensive overview of the GSE-KG system, its contributions, and evaluation results.

### 2. Introduction
Problem statement, challenges in space exploration data management, and main contributions.

### 3. Related Work
Review of existing knowledge graphs in space exploration, GraphRAG systems, and ontology engineering approaches.

### 4. System Architecture
Detailed description of the three-layer microservices architecture with diagrams:
- Frontend Layer (React + 3D Visualization)
- Backend Gateway (Node.js API Gateway)
- Knowledge Representation Layer (Python FastAPI)

### 5. Ontology Design
Comprehensive documentation of:
- 34+ class hierarchy with inheritance relationships
- Advanced OWL features (enumerations, cardinality, unions, intersections, complements)
- Property design and domain/range specifications

### 6. Data Integration Pipeline
Automated pipeline for:
- CSV to RDF conversion algorithm
- DBpedia interlinking strategy
- URI generation and namespace management

### 7. Agentic GraphRAG Engine
Novel two-stage query processing approach:
- LLM-based query planning and routing
- Parallel SPARQL and vector search execution
- Result synthesis and response generation

### 8. SPARQL Endpoint and Query Evaluation
- RESTful SPARQL endpoint implementation
- 28 competency questions across 11 categories
- Query examples and validation results

### 9. Evaluation and Results
Comprehensive evaluation including:
- Knowledge graph statistics (113 triples, 34 classes)
- Query validation results (18 successful, 9 empty, 1 failed)
- Performance metrics (45ms average SPARQL query time)
- Ontology feature validation

### 10. Discussion
Key insights, limitations, and challenges encountered during implementation.

### 11. Conclusion and Future Work
Summary of contributions and directions for future enhancement.

## Key Features of the Paper

### Technical Diagrams
- **Figure 1**: System Architecture Overview (TikZ diagram)
- **Figure 2**: Core Ontology Class Hierarchy
- **Figure 3**: Agentic Query Routing Flow
- **Figure 4**: Overall System Architecture

### Tables
- **Table 1**: Key Object Properties
- **Table 2**: Competency Question Categories
- **Table 3**: Knowledge Graph Statistics
- **Table 4**: System Performance Metrics

### Algorithms
- **Algorithm 1**: CSV to RDF Conversion process

### Code Examples
- SPARQL query examples for high-budget missions and successful moon missions
- Turtle syntax examples for ontology axioms

## Compilation Instructions

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- pdflatex command available in PATH

### Compilation Steps

1. **Make the compilation script executable** (if not already done):
   ```bash
   chmod +x compile_paper.sh
   ```

2. **Run the compilation script**:
   ```bash
   ./compile_paper.sh
   ```

3. **Alternative manual compilation**:
   ```bash
   pdflatex GSE_KG_IEEE_Paper.tex
   pdflatex GSE_KG_IEEE_Paper.tex  # Second pass for references
   pdflatex GSE_KG_IEEE_Paper.tex  # Third pass for final formatting
   ```

### Output
The compilation will generate:
- **`GSE_KG_IEEE_Paper.pdf`** - The final IEEE-formatted paper
- Cleaned auxiliary files (automatically removed)

## Paper Highlights

### Novel Contributions
1. **Comprehensive Space Ontology**: 34+ classes with advanced OWL features
2. **Agentic GraphRAG Architecture**: LLM-powered query routing between SPARQL and vector search
3. **Automated Data Pipeline**: CSV to RDF conversion with DBpedia interlinking
4. **Full-Stack Implementation**: Production-ready system with interactive visualization

### Technical Achievements
- **28 Competency Questions**: Validating all ontology features
- **Multi-Modal Query Processing**: Combining symbolic reasoning with vector similarity
- **Real-Time Performance**: Sub-second response times for most queries
- **Extensible Architecture**: Support for dynamic document enrichment

### Evaluation Results
- **Query Success Rate**: 64% (18/28 queries successful)
- **Ontology Coverage**: 100% of advanced OWL features validated
- **Performance**: 45ms average SPARQL query execution time
- **Scalability**: Handles 113+ triples with interactive visualization

## IEEE Compliance

The paper follows IEEE conference paper standards:
- **Format**: IEEEtran document class, 10pt, two-column layout
- **Citations**: IEEE citation style with numbered references
- **Figures**: TikZ-generated technical diagrams
- **Tables**: Professional formatting with booktabs
- **Abstract**: Structured abstract under 250 words
- **Keywords**: IEEE-compliant keyword section

## Related Project Files

The paper references several files from the main project:
- `src/design_ontology.py` - Ontology implementation
- `src/convert_to_rdf.py` - Data conversion pipeline
- `src/graph_rag_engine.py` - Agentic reasoning engine
- `backend_py/main.py` - SPARQL endpoint implementation
- `queries/` - SPARQL competency questions
- `ontology/space_exploration.owl` - Main ontology file

## Citation Information

If you reference this work, please cite as:

```
A. Saleem, "Global Space Exploration Knowledge Graph: An Agentic GraphRAG Approach to Semantic Space Mission Data Integration," in Proceedings of the IEEE International Conference on Semantic Computing, 2024.
```

## Contact

For questions about the paper or the GSE-KG project, please refer to the project documentation or create an issue in the project repository.
