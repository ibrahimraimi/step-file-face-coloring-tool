#!/usr/bin/env python3
"""
STEP File Face Coloring Tool - Main Entry Point

A lightweight Python application for Windows that orients a solid body 
and colors faces of STEP files (.stp / .step) according to user-defined criteria.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from gui.main_window import main as gui_main
except ImportError as e:
    print(f"Error importing GUI components: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main application entry point"""
    print("STEP File Face Coloring Tool")
    print("=" * 40)
    
    try:
        # Launch GUI application
        gui_main()
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
