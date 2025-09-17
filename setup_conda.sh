#!/bin/bash
# Conda setup script for STEP File Face Coloring Tool

echo "STEP File Face Coloring Tool - Conda Setup"
echo "=========================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Installing Miniforge..."
    
    # Download and install Miniforge
    wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/miniforge.sh
    bash /tmp/miniforge.sh -b -p $HOME/miniforge3
    
    # Initialize conda for current shell
    $HOME/miniforge3/bin/conda init zsh
    source ~/.zshrc
    
    echo "Miniforge installed. Please restart your terminal or run: source ~/.zshrc"
    echo "Then run this script again."
    exit 0
fi

# Create environment from environment.yml
echo "Creating conda environment from environment.yml..."
conda env create -f environment.yml

# Activate the environment
echo "Activating environment..."
conda activate step-face-coloring

# Verify installation
echo "Verifying installation..."
python -c "import OCC; print('✓ OCC (conda) installed')" 2>/dev/null || echo "✗ OCC not found"
python -c "import PyQt5; print('✓ PyQt5 (conda) installed')" 2>/dev/null || echo "✗ PyQt5 not found"
python -c "import numpy; print('✓ numpy (conda) installed')" 2>/dev/null || echo "✗ numpy not found"
python -c "import OCC.Core.STEPControl_Reader; print('✓ pythonocc-core (pip) installed')" 2>/dev/null || echo "✗ pythonocc-core not found"

echo ""
echo "Setup completed!"
echo "To activate the environment: conda activate step-face-coloring"
echo "To run the application: conda activate step-face-coloring && python main.py"
echo ""
echo "Or use the run_conda.sh script for convenience."
