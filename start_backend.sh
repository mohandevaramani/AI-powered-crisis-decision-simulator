#!/bin/bash
# Linux/Mac startup script for backend

echo "Starting Crisis Simulator Backend API..."
echo

echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Starting Flask server on http://localhost:5000..."
echo "Press Ctrl+C to stop"
echo

cd crisis_simulator/backend
python app.py
