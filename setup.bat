@echo off
REM AI Job Tracker - Quick Setup Script for Windows
REM This script automates the initial setup process

echo 🚀 Setting up AI Job Tracker...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install backend dependencies
echo 📥 Installing backend dependencies...
cd src
pip install -r requirements.txt

REM Download spaCy model
echo 🧠 Downloading spaCy English model...
python -m spacy download en_core_web_sm

REM Go back to root directory
cd ..

REM Check if Node.js is available for frontend setup
where npm >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found. Frontend setup skipped.
    echo    Install Node.js 18+ to enable the web interface.
) else (
    echo 📦 Setting up frontend...
    cd frontend
    npm install
    cd ..
    echo ✅ Frontend setup complete
)

REM Create sample .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating sample .env file...
    (
        echo # AI Job Tracker Configuration
        echo # Copy this file and add your actual API keys
        echo.
        echo # Required for job searching ^(get from RapidAPI^)
        echo RAPIDAPI_KEY=your_rapidapi_key_here
        echo.
        echo # Required for email notifications
        echo EMAIL_ADDRESS=your_email@example.com
        echo EMAIL_PASSWORD=your_app_password
        echo.
        echo # Optional: Azure Storage ^(uses local storage if not provided^)
        echo # AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
        echo # AZURE_STORAGE_CONTAINER=jobtracker
        echo.
        echo # Application Settings
        echo MATCH_SCORE_THRESHOLD=50.0
        echo USE_LLM_FILTERING=false
        echo MAX_JOBS_IN_EMAIL=10
    ) > .env
    echo ✅ Sample .env file created
) else (
    echo ✅ .env file already exists
)

echo.
echo 🎉 Setup complete! Next steps:
echo.
echo 1. Configure your API keys in the .env file
echo 2. Test the system:
echo    cd src ^&^& python test_complete_system.py
echo.
echo 3. Start the backend:
echo    cd src ^&^& python -m uvicorn api.main:app --reload --port 8001
echo.

where npm >nul 2>&1
if not errorlevel 1 (
    echo 4. Start the frontend ^(optional^):
    echo    cd frontend ^&^& npm run dev
    echo.
)

echo 5. Visit http://localhost:8001/docs for API documentation
echo.
echo 🔗 For detailed instructions, see README.md
echo.
pause
