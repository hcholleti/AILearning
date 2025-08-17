#!/usr/bin/env python3
"""
Quick validation script to verify AI Job Tracker setup
Run this after setup to ensure everything is working correctly
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (3.11+ required)")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"✅ {package_name}")
        return True
    else:
        print(f"❌ {package_name}")
        return False

def check_spacy_model():
    """Check if spaCy English model is installed"""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy en_core_web_sm model")
        return True
    except OSError:
        print("❌ spaCy en_core_web_sm model")
        return False
    except ImportError:
        print("❌ spaCy not installed")
        return False

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists("../.env"):
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found (create one with your API keys)")
        return False

def check_frontend():
    """Check if frontend is set up"""
    frontend_path = "../frontend"
    if os.path.exists(frontend_path):
        package_json = os.path.join(frontend_path, "package.json")
        node_modules = os.path.join(frontend_path, "node_modules")
        if os.path.exists(package_json) and os.path.exists(node_modules):
            print("✅ Frontend setup complete")
            return True
        elif os.path.exists(package_json):
            print("⚠️  Frontend dependencies not installed (run: cd frontend && npm install)")
            return False
    print("⚠️  Frontend not found")
    return False

def main():
    print("🔍 AI Job Tracker - Setup Validation")
    print("=" * 40)
    
    checks = []
    
    # Core requirements
    print("\n📋 Core Requirements:")
    checks.append(check_python_version())
    
    # Python packages
    print("\n📦 Python Packages:")
    required_packages = [
        "fastapi", "uvicorn", "requests", "pandas", 
        "spacy", "sentence_transformers", "scikit_learn"
    ]
    
    for package in required_packages:
        # Handle sklearn vs scikit-learn naming
        check_name = "sklearn" if package == "scikit_learn" else package
        checks.append(check_package(check_name))
    
    # spaCy model
    print("\n🧠 Language Models:")
    checks.append(check_spacy_model())
    
    # Configuration
    print("\n⚙️  Configuration:")
    checks.append(check_env_file())
    
    # Frontend
    print("\n🎨 Frontend:")
    check_frontend()  # Not critical for core functionality
    
    # Summary
    print("\n" + "=" * 40)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print("\n✨ Your setup is ready!")
        print("\n🚀 Next steps:")
        print("1. Configure API keys in .env file")
        print("2. Run: python test_complete_system.py")
        print("3. Start API: python -m uvicorn api.main:app --reload --port 8001")
        return True
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\n🔧 Fix the failed checks above and run this script again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
