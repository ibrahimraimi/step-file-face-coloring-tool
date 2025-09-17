#!/usr/bin/env python3
"""
Installation script for STEP File Face Coloring Tool
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def check_dependencies():
    """Check if all dependencies are available"""
    print("Checking dependencies...")
    
    required_modules = [
        ("PyQt5", "PyQt5"),
        ("OCC", "pythonocc-core"),
        ("numpy", "numpy")
    ]
    
    missing = []
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✓ {package_name} is available")
        except ImportError:
            print(f"✗ {package_name} is missing")
            missing.append(package_name)
    
    return len(missing) == 0


def main():
    """Main installation function"""
    print("STEP File Face Coloring Tool - Installation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt not found. Please run this script from the project root.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("✗ Some dependencies are missing. Please check the installation.")
        return False
    
    print("\n✓ Installation completed successfully!")
    print("You can now run the application with: python main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
