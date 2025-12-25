#!/bin/bash

# Kill existing processes on ports 8000, 5001, 5173
kill -9 $(lsof -t -i:8000) 2>/dev/null
kill -9 $(lsof -t -i:5001) 2>/dev/null
kill -9 $(lsof -t -i:5173) 2>/dev/null

echo "🚀 Starting Space Explorer Full-Stack..."

# 1. Start Python KRR Bridge
cd backend_py
python3 main.py &
PYTHON_PID=$!
echo "✅ Python KRR Bridge starting (PID $PYTHON_PID)..."

# 2. Start Node.js Backend
cd ../backend_node
node server.js &
NODE_PID=$!
echo "✅ Node.js Backend starting (PID $NODE_PID)..."

# 3. Start React Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ React Frontend starting (PID $FRONTEND_PID)..."

echo "------------------------------------------------"
echo "KRR Bridge:  http://localhost:8000"
echo "Node API:    http://localhost:5001"
echo "Frontend UI: http://localhost:5173"
echo "------------------------------------------------"
echo "Press Ctrl+C to stop all services."

trap "kill $PYTHON_PID $NODE_PID $FRONTEND_PID; exit" INT
wait
