#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug script for Python 2.7 compatibility checker

This script helps diagnose issues when trying to run the SystemAIR-API with Python 2.7.
The SystemAIR-API library requires Python 3.7+ and won't work with Python 2.
This diagnostic tool:

1. Checks your Python version
2. Examines your environment setup
3. Verifies project structure and dependencies
4. Provides guidance on how to set up a Python 3 environment

Usage:
    python debug_api_py2.py
"""

from __future__ import print_function
import os
import sys
import json
import traceback
import platform

def main():
    """Main diagnostic function."""
    log_file = open("debug_py2.log", "w")
    
    def log(msg):
        """Log to both stdout and file."""
        print(msg)
        log_file.write(msg + "\n")
        log_file.flush()
    
    log("SystemAIR API Compatibility Check")
    log("=" * 50)
    
    # Check Python version
    python_version = ".".join(map(str, sys.version_info[:3]))
    log("Python version: " + python_version)
    log("Python executable: " + sys.executable)
    log("Platform: " + platform.platform())
    
    is_python3 = sys.version_info[0] >= 3
    if is_python3:
        log("\nYou are using Python 3, which is compatible with SystemAIR-API.")
        if sys.version_info[1] < 7:
            log("However, Python 3.7+ is recommended. You're using " + python_version)
    else:
        log("\nWARNING: You are using Python 2, which is NOT compatible with SystemAIR-API.")
        log("SystemAIR-API requires Python 3.7 or higher.")
    
    # Check if we have Python 3 available
    log("\nChecking for Python 3 availability...")
    python3_paths = [
        "/usr/bin/python3",
        "/usr/local/bin/python3",
        "C:\\Python39\\python.exe",
        "C:\\Python38\\python.exe",
        "C:\\Python37\\python.exe"
    ]
    
    python3_found = False
    for path in python3_paths:
        if os.path.exists(path):
            log("+ Found Python 3 at: " + path)
            python3_found = True
            break
    
    if not python3_found:
        log("x No common Python 3 installation found")
        log("  You'll need to install Python 3.7 or later")
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    log("\nChecking for .env file: " + env_file)
    if os.path.exists(env_file):
        log("+ .env file exists")
        with open(env_file, "r") as f:
            log("  First few lines (without passwords):")
            for line in f.readlines()[:5]:
                if "PASSWORD" not in line.upper():
                    log("  " + line.strip())
    else:
        log("x .env file does NOT exist")
        log("  You should create one with your Systemair credentials:")
        log("  EMAIL=your.email@example.com")
        log("  PASSWORD=your_password")
    
    # Check Python packages availability
    log("\nChecking for required packages:")
    required_packages = [
        ("requests", "For API communication"),
        ("websocket-client", "For real-time updates"),
        ("bs4", "For authentication form parsing"),
        ("dotenv", "For loading environment variables"),
        ("textual", "For the TUI interface")
    ]
    
    for package, purpose in required_packages:
        try:
            # Try to import the package
            __import__(package)
            log("+ " + package + " package is installed - " + purpose)
        except ImportError:
            log("x " + package + " package is NOT installed - " + purpose)
    
    # Check project structure
    log("\nChecking project structure:")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    log("Project directory: " + project_dir)
    
    # Check key files
    key_files = [
        "systemair_api/auth/authenticator.py",
        "systemair_api/api/systemair_api.py",
        "systemair_api/models/ventilation_unit.py",
        "systemair_api/api/websocket_client.py",
        "examples/systemair_tui.py"
    ]
    
    all_files_exist = True
    for file_path in key_files:
        full_path = os.path.join(project_dir, file_path)
        if os.path.exists(full_path):
            log("+ " + file_path + " exists")
            # Try to detect Python 3 features
            with open(full_path, "r") as f:
                try:
                    content = f.read()
                    # Check for type annotations (Python 3 feature)
                    if ": " in content and "->" in content:
                        log("  Contains Python 3 type annotations")
                except:
                    log("  Error reading file")
        else:
            log("x " + file_path + " does NOT exist")
            all_files_exist = False
    
    # Check for textual CSS file
    tui_css_path = os.path.join(project_dir, "examples", "systemair_tui.css")
    if os.path.exists(tui_css_path):
        log("+ TUI CSS file exists")
    else:
        log("x TUI CSS file does NOT exist - it will be created on first run")
    
    # Recommendations section
    log("\n" + "=" * 50)
    log("DIAGNOSIS:")
    
    if not is_python3:
        log("The SystemAIR-API library requires Python 3.7+")
        log("You are currently using Python " + python_version + " which is not compatible.")
    
    if not all_files_exist:
        log("Some essential project files are missing. Ensure you have downloaded the complete project.")
    
    log("\nRECOMMENDATIONS:")
    if not is_python3:
        log("1. Install Python 3.7 or later from https://www.python.org/downloads/")
        log("2. Create a Python 3 virtual environment:")
        log("   python3 -m venv .venv")
        log("3. Activate the virtual environment:")
        if platform.system() == "Windows":
            log("   .venv\\Scripts\\activate")
        else:
            log("   source .venv/bin/activate")
        log("4. Install required packages:")
        log("   pip install -r requirements.txt")
        log("   pip install -r examples/requirements-tui.txt  # For TUI")
    else:
        # Python 3 is already being used
        log("1. Create a virtual environment if you haven't already:")
        log("   python -m venv .venv")
        log("2. Activate the virtual environment:")
        if platform.system() == "Windows":
            log("   .venv\\Scripts\\activate")
        else:
            log("   source .venv/bin/activate")
        log("3. Install required packages:")
        log("   pip install -r requirements.txt")
        log("   pip install -r examples/requirements-tui.txt  # For TUI")
    
    log("\nTroubleshooting the TUI:")
    log("1. Ensure textual is installed: pip install 'textual>=0.27.0'")
    log("2. Run the diagnostic script for API connectivity: python debug_api.py")
    log("3. Check the log files: systemair_tui_debug.log and debug_api.log")
    log("4. If units don't appear, verify API connectivity and credentials")
    
    log_file.close()
    log("\nDebug information written to debug_py2.log")
    
    # Return code: 0 for Python 3, 1 for Python 2
    return 0 if is_python3 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)