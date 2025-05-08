import sys
import os
import subprocess

def check_python_version():
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

def check_packages():
    print("\nChecking installed packages:")
    try:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]
        installed_packages = sorted(installed_packages, key=lambda x: x.key.lower())
        for package in installed_packages:
            print(f"{package.key}=={package.version}")
    except Exception as e:
        print(f"Error checking packages: {e}")

def check_flask():
    print("\nChecking Flask installation:")
    try:
        import flask
        print(f"Flask version: {flask.__version__}")
        return True
    except ImportError:
        print("Flask is not installed or not accessible")
        return False

def check_flask_imports():
    print("\nTrying to import Flask components:")
    try:
        from flask import Flask, request, jsonify, render_template
        print("Successfully imported Flask components")
        return True
    except Exception as e:
        print(f"Error importing Flask components: {e}")
        return False

def main():
    print("=== Environment Check ===")
    check_python_version()
    check_packages()
    
    if check_flask():
        check_flask_imports()
    
    print("\n=== Environment Check Complete ===")

if __name__ == "__main__":
    main()
