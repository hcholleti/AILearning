#!/bin/bash

# AI Job Tracker - Quick Setup Script
# This script automates the initial setup process

set -e  # Exit on any error

echo "🚀 Setting up AI Job Tracker..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
if [[ $(echo "$python_version >= 3.11" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.11+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd src
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Go back to root directory
cd ..

# Check if Node.js is available for frontend setup
if command -v npm &> /dev/null; then
    echo "📦 Setting up frontend..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend setup complete"
else
    echo "⚠️  Node.js not found. Frontend setup skipped."
    echo "   Install Node.js 18+ to enable the web interface."
fi

# Create sample .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating sample .env file..."
    cat > .env << EOF
# AI Job Tracker Configuration
# Copy this file and add your actual API keys

# Required for job searching (get from RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key_here

# Required for email notifications
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Optional: Azure Storage (uses local storage if not provided)
# AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
# AZURE_STORAGE_CONTAINER=jobtracker

# Application Settings
MATCH_SCORE_THRESHOLD=50.0
USE_LLM_FILTERING=false
MAX_JOBS_IN_EMAIL=10
EOF
    echo "✅ Sample .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Configure your API keys in the .env file"
echo "2. Test the system:"
echo "   cd src && python test_complete_system.py"
echo ""
echo "3. Start the backend:"
echo "   cd src && python -m uvicorn api.main:app --reload --port 8001"
echo ""
if command -v npm &> /dev/null; then
    echo "4. Start the frontend (optional):"
    echo "   cd frontend && npm run dev"
    echo ""
fi
echo "5. Visit http://localhost:8001/docs for API documentation"
echo ""
echo "🔗 For detailed instructions, see README.md"
