#!/bin/bash
# Run script for STEP File Face Coloring Tool

echo "Starting STEP File Face Coloring Tool..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
