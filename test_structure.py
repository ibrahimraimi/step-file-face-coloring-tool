#!/usr/bin/env python3
"""
Test script to verify project structure and basic functionality
"""

import os
import sys


def test_project_structure():
    """Test if all required files and directories exist"""
    print("Testing project structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "setup.sh",
        "run.sh",
        "install.py"
    ]
    
    required_dirs = [
        "gui",
        "core"
    ]
    
    required_gui_files = [
        "gui/__init__.py",
        "gui/main_window.py"
    ]
    
    required_core_files = [
        "core/__init__.py",
        "core/step_processor.py"
    ]
    
    all_good = True
    
    # Check main files
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False
    
    # Check directories
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"✓ {dir}/")
        else:
            print(f"✗ {dir}/ - MISSING")
            all_good = False
    
    # Check GUI files
    for file in required_gui_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False
    
    # Check core files
    for file in required_core_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False
    
    return all_good


def test_imports():
    """Test if modules can be imported"""
    print("\nTesting imports...")
    
    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    try:
        import core.step_processor
        print("✓ core.step_processor")
    except ImportError as e:
        print(f"✗ core.step_processor - {e}")
        return False
    
    try:
        import gui.main_window
        print("✓ gui.main_window")
    except ImportError as e:
        print(f"✗ gui.main_window - {e}")
        return False
    
    return True


def main():
    """Main test function"""
    print("STEP File Face Coloring Tool - Structure Test")
    print("=" * 50)
    
    structure_ok = test_project_structure()
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    if structure_ok and imports_ok:
        print("✓ All tests passed! Project structure is correct.")
        return True
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
