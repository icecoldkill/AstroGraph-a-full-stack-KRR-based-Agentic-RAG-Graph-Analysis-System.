# Full-Stack Space Exploration KG - Technical Report

## System Architecture
The space exploration knowledge graph has been migrated to a robust full-stack architecture to ensure scalability, performance, and a premium user experience.

### 1. Frontend (React + Vite)
- **UI Framework**: React 18 with Tailwind CSS.
- **Visuals**: `react-force-graph` for interactive Knowledge Graph exploration.
- **Communication**: Optimized Axios hooks to communicate with the Node.js API Gateway.

### 2. Backend Gateway (Node.js + Express)
- **Responsibility**: Handles user requests, proxies reasoning tasks to Python, and manages data persistence in PostgreSQL.
- **Persistence**: PostgreSQL stores mission metadata and graph versioning (hashes).

### 3. KRR Worker (Python + FastAPI)
- **Logic**: Executes RDFLib and Owlready2 operations.
- **Agentic reasoning**: Groq (Llama 3) translates natural language into SPARQL and synthesizes answers.
- **Efficiency**: Implements graph compression to reduce the payload sent to the frontend visualizer.

## Data Management
- **Hashing**: Every graph update generates a SHA-256 hash to track state changes.
- **Compression**: The RDF graph is serialized into a lightweight JSON adjacency list for fast WebGL rendering in the browser.

## Deployment
Use the provided `run_all.sh` to launch all services concurrently. Ensure Docker is running to host the PostgreSQL instance via `docker-compose.yml`.
