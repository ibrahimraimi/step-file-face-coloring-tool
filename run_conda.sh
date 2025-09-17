#!/bin/bash
# Run script for STEP File Face Coloring Tool using conda

echo "Starting STEP File Face Coloring Tool (Conda)..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Please run setup_conda.sh first."
    exit 1
fi

# Activate conda environment
echo "Activating conda environment..."
conda activate step-face-coloring

# Check if environment exists
if [ $? -ne 0 ]; then
    echo "Environment 'step-face-coloring' not found. Please run setup_conda.sh first."
    exit 1
fi

# Run the application
echo "Running application..."
python main.py
