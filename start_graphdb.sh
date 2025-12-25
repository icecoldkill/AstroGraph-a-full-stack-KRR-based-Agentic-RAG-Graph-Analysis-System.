#!/bin/bash
# GraphDB Setup Script for KRR Project
# Run this after Docker is installed

echo "🚀 Starting GraphDB for Space Exploration Knowledge Graph..."

# Create directories
mkdir -p graphdb-data graphdb-import

# Copy RDF files to import directory
cp data/space_data.rdf graphdb-import/
cp ontology/space_exploration.owl graphdb-import/

# Start GraphDB
docker-compose up -d

echo ""
echo "✅ GraphDB is starting..."
echo ""
echo "📍 Access GraphDB Workbench at: http://localhost:7200"
echo ""
echo "📋 NEXT STEPS:"
echo "1. Wait ~30 seconds for GraphDB to fully start"
echo "2. Open http://localhost:7200 in your browser"
echo "3. Click 'Setup' → 'Repositories' → 'Create new repository'"
echo "4. Name it: space-missions"
echo "5. Click 'Import' → 'RDF' → 'Upload RDF files'"
echo "6. Upload files from: $(pwd)/graphdb-import/"
echo "7. Run SPARQL queries from 'SPARQL' tab"
echo ""
echo "🔧 To stop GraphDB: docker-compose down"
