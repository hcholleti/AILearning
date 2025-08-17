# 🤖 AI Job Tracker

> **An intelligent job matching system powered by AI that analyzes your resume and finds the most relevant job opportunities with advanced filtering and scoring.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![Azure](https://img.shields.io/badge/Azure-Cloud_Ready-blue.svg)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

AI Job Tracker is a modern, full-stack application that revolutionizes job searching by using artificial intelligence to match your skills and experience with relevant job opportunities. The system parses your resume, understands your technical skills, and intelligently filters job postings to find the best matches.

## ✨ Key Features

- 🧠 **AI-Powered Resume Analysis** - Extracts skills, experience, and technologies from PDF/DOCX resumes
- 🎯 **Smart Job Matching** - Uses semantic similarity and machine learning for accurate job scoring (0-100%)
- 🔍 **Natural Language Filtering** - Filter jobs using prompts like "DevOps jobs requiring Terraform"
- 📊 **Advanced Scoring System** - Multi-factor scoring including semantic similarity, skill matching, and experience level
- 💾 **Cloud Storage Integration** - Azure Blob Storage for resume and results persistence
- 🌐 **Modern Web Interface** - React + Tailwind UI for intuitive user experience
- 📧 **Enhanced Email Reports** - Rich HTML emails with match insights and recommendations
- 🔄 **RESTful API** - Complete API for integration and automation
- 🚀 **Production Ready** - Docker, CI/CD, and Azure deployment configured

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Azure Blob     │
│   (Tailwind UI) │◄──►│  (AI Processing) │◄──►│  Storage        │
│   Port 3000      │    │  Port 8001       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ • Resume Upload │    │ • Job Fetching  │    │ • User Sessions │
│ • Job Search UI │    │ • AI Matching   │    │ • Resume Files  │
│ • Results View  │    │ • Email Reports │    │ • Search Results│
│ • Export Tools  │    │ • Session Mgmt  │    │ • Metadata      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
ai-job-tracker/
├── 📁 src/                           # Backend source code
│   ├── 📁 api/                       # FastAPI application
│   │   ├── main.py                   # API endpoints & server
│   │   └── storage.py                # Azure Blob Storage integration
│   ├── 📁 jobtracker/                # Core modules
│   │   ├── 📁 emailer/               # Email functionality
│   │   │   ├── email_sender.py       # SMTP email sending
│   │   │   └── send_email.py         # Email formatting & reports
│   │   ├── 📁 fetcher/               # Job data fetching
│   │   │   └── fetcher.py            # RapidAPI job search integration
│   │   ├── 📁 filter/                # Job filtering & processing
│   │   │   ├── filter.py             # Deduplication & basic filtering
│   │   │   └── llm_filter.py         # AI-powered semantic filtering
│   │   ├── 📁 matcher/               # AI job matching
│   │   │   └── matcher.py            # Sentence transformers matching
│   │   ├── 📁 resume/                # Resume processing
│   │   │   └── parser.py             # PDF/DOCX parsing & skill extraction
│   │   ├── config.py                 # Configuration management
│   │   └── utils.py                  # Utility functions
│   ├── main.py                       # CLI application entry point
│   ├── requirements.txt              # Python dependencies
│   └── test_*.py                     # Individual module tests
├── 📁 frontend/                      # React frontend
│   ├── 📁 src/
│   │   ├── 📁 components/            # React components
│   │   ├── 📁 pages/                 # Page components
│   │   ├── 📁 context/               # State management
│   │   └── App.jsx                   # Main application
│   ├── package.json                  # Node.js dependencies
│   ├── vite.config.js                # Build configuration
│   └── tailwind.config.js            # UI styling
├── 📁 .github/workflows/             # CI/CD automation
│   └── azure-deploy.yml              # GitHub Actions deployment
├── 📁 resumes/                       # Resume storage directory
├── 📁 outputs/                       # Generated reports & results
├── .env                              # Environment variables
├── Dockerfile                        # Container configuration
├── docker-compose.yml               # Local development setup
├── DEPLOYMENT.md                     # Azure deployment guide
└── README.md                         # This file
```

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.11+
- **Web Framework**: FastAPI (high-performance async API)
- **AI/ML Libraries**:
  - `sentence-transformers` - Semantic text matching
  - `scikit-learn` - Machine learning utilities
  - `spaCy` - Natural language processing
- **Document Processing**:
  - `pdfplumber` - PDF text extraction
  - `python-docx` - DOCX document parsing
- **Data Processing**:
  - `pandas` - Data manipulation
  - `numpy` - Numerical computations
- **Cloud Integration**:
  - `azure-storage-blob` - Azure Blob Storage
  - `azure-identity` - Azure authentication

### Frontend
- **Framework**: React 18+ with Vite
- **Styling**: Tailwind CSS + Headless UI
- **State Management**: React Context API
- **HTTP Client**: Axios
- **UI Components**: Lucide React (icons)
- **File Upload**: React Dropzone
- **Notifications**: React Hot Toast

### Infrastructure & DevOps
- **Containerization**: Docker + Docker Compose
- **Cloud Platform**: Microsoft Azure
  - App Service (Backend hosting)
  - Static Web Apps (Frontend hosting)
  - Blob Storage (File storage)
- **CI/CD**: GitHub Actions
- **Web Server**: Uvicorn (ASGI)
- **Reverse Proxy**: Nginx (production)

### Development Tools
- **API Documentation**: FastAPI automatic OpenAPI/Swagger
- **Code Quality**: ESLint, Prettier
- **Testing**: pytest (Python), Jest (JavaScript)
- **Environment Management**: python-dotenv

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/hcholleti/ai-job-tracker.git
cd ai-job-tracker

# For Linux/macOS:
./setup.sh

# For Windows:
setup.bat
```

### Option 2: Manual Setup

### Prerequisites
- **Python 3.11+** with pip
- **Node.js 18+** with npm (for frontend)
- **Git** for cloning the repository
- **Internet connection** for downloading models and dependencies

**Note**: The system will automatically download the required spaCy language model during setup.

### 1. Clone Repository
```bash
git clone https://github.com/hcholleti/ai-job-tracker.git
cd ai-job-tracker
```

### 2. Backend Setup
```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
cd src
pip install -r requirements.txt

# Install required spaCy model
python -m spacy download en_core_web_sm
```

### 3. Environment Configuration
Create `.env` file in project root:
```bash
# Required API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Optional Azure Configuration
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
AZURE_STORAGE_CONTAINER=jobtracker
```

### 4. Run Backend
```bash
cd src
python -m uvicorn api.main:app --reload --port 8001
```

### 5. Run Frontend (Optional)
```bash
cd frontend
npm install
npm run dev
```

### 6. Test the System
```bash
# Validate setup first
cd src && python validate_setup.py

# Quick smoke test (run this first to verify setup)
cd src && python test_complete_system.py

# CLI interface
cd src && python main.py

# API documentation
open http://localhost:8001/docs

# Web interface  
open http://localhost:3000
```

## 📊 Core Modules

### 🧠 Resume Parser (`resume/parser.py`)
- **Purpose**: Extract skills, experience, and metadata from resume files
- **Features**:
  - PDF and DOCX support
  - 71+ predefined technical skills recognition
  - Experience years detection using regex
  - Entity extraction (companies, technologies)
- **Input**: Resume file (PDF/DOCX)
- **Output**: Structured profile with skills, experience, and text content

### 🎯 Job Matcher (`matcher/matcher.py`)
- **Purpose**: AI-powered job compatibility scoring
- **Features**:
  - Semantic similarity using sentence-transformers
  - Multi-factor scoring (70% semantic + 30% skills)
  - Experience level bonus calculation
  - Skill highlighting and matching
- **Algorithm**: Cosine similarity with `all-MiniLM-L6-v2` model
- **Output**: Jobs ranked by compatibility score (0-100%)

### 🔍 Smart Filter (`filter/llm_filter.py`)
- **Purpose**: Natural language job filtering
- **Features**:
  - Semantic filtering using embeddings
  - Keyword extraction and matching
  - Configurable similarity thresholds
  - Ready for LLM integration (OpenAI/HuggingFace)
- **Input**: Natural language prompts
- **Output**: Filtered and scored job list

### 📡 Job Fetcher (`fetcher/fetcher.py`)
- **Purpose**: Retrieve job postings from external APIs
- **Features**:
  - RapidAPI JSearch integration
  - Configurable search parameters
  - Rate limiting and error handling
  - Multiple job board support
- **Data Sources**: JSearch API (Indeed, LinkedIn, etc.)

### 💾 Storage System (`api/storage.py`)
- **Purpose**: Persistent data storage and session management
- **Features**:
  - Azure Blob Storage integration
  - Local file system fallback
  - Session-based data organization
  - Export functionality (CSV/JSON)
- **Structure**: Organized by user sessions with metadata

### 📧 Email System (`emailer/`)
- **Purpose**: Intelligent job report generation
- **Features**:
  - Rich HTML email formatting
  - Match insights and recommendations
  - Skill analysis and trends
  - Excel attachment generation
- **Templates**: Customizable email layouts

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | Health check and system status |
| `/upload-resume` | POST | Upload and parse resume file |
| `/search-jobs` | POST | Search and match jobs with resume |
| `/search-results/{session_id}` | GET | Retrieve saved search results |
| `/export-results/{session_id}` | GET | Export results (CSV/JSON) |
| `/session/{session_id}` | DELETE | Delete session data |
| `/sessions` | GET | List all sessions (admin) |

## 🧪 Testing

### Quick Verification
```bash
# Run comprehensive smoke test
cd src
python test_complete_system.py
```
**Expected Output**: All 5 tests should pass (✅), confirming the system is ready.

### Run All Tests
```bash
cd src
python test_enhanced_features.py
```

### Individual Module Tests
```bash
# Resume parser
python test_resume_parser.py

# Job matcher  
python test_job_matcher.py

# LLM filter
python test_llm_filter.py

# Email system
python test_send_email.py
```

### API Testing
```bash
# Start backend first
python -m uvicorn api.main:app --port 8001

# Test endpoints
curl http://localhost:8001/health
curl http://localhost:8001/docs  # Interactive documentation
```

## 🔧 Troubleshooting

### Common Issues

#### ❌ **"Can't find model 'en_core_web_sm'"**
```bash
# Install the required spaCy model
python -m spacy download en_core_web_sm
```

#### ❌ **API Server Won't Start**
```bash
# Check if port 8001 is in use
lsof -i :8001

# Kill existing process if needed
pkill -f "uvicorn"

# Restart server
cd src && python -m uvicorn api.main:app --reload --port 8001
```

#### ❌ **Module Import Errors**
```bash
# Ensure you're in the correct directory and virtual environment
cd ai-job-tracker/src
pip install -r requirements.txt
```

#### ❌ **Frontend Won't Start**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### ⚠️ **Azure Storage Errors (Optional)**
The system works with local storage if Azure credentials are not provided. For Azure setup, ensure your `.env` file has:
```bash
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_STORAGE_CONTAINER=jobtracker
```

### Verification Steps
1. **Backend Health**: Visit `http://localhost:8001/health` (should return status: healthy)
2. **API Documentation**: Visit `http://localhost:8001/docs` (interactive API docs)
3. **Frontend**: Visit `http://localhost:3000` (React application)
4. **Smoke Test**: Run `python test_complete_system.py` (all 5 tests should pass)

## 🌐 Deployment

### Local Development (Docker)
```bash
docker-compose up --build
```

### Azure Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Azure deployment instructions.

**Quick Azure Setup:**
```bash
# Create resources
az group create --name rg-job-tracker --location eastus

# Deploy with GitHub Actions
git push origin main  # Triggers automatic deployment
```

## 📈 Usage Examples

### CLI Interface
```bash
# Basic job search
python main.py

# Custom configuration
RAPIDAPI_KEY="your_key" python main.py
```

### API Usage
```python
import requests

# Upload resume
with open("resume.pdf", "rb") as f:
    response = requests.post("http://localhost:8001/upload-resume", 
                           files={"file": f})
session_id = response.json()["session_id"]

# Search jobs
search_params = {
    "keywords": "Python Developer",
    "location": "San Francisco",
    "user_prompt": "remote Python jobs with FastAPI"
}
response = requests.post(f"http://localhost:8001/search-jobs?session_id={session_id}",
                        json=search_params)
jobs = response.json()["jobs"]
```

## 🔧 Configuration

### Environment Variables
```bash
# Job Search API
RAPIDAPI_KEY=your_rapidapi_key

# Email Configuration  
EMAIL_ADDRESS=your_email@domain.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Azure Storage (Optional)
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_STORAGE_CONTAINER=jobtracker

# Application Settings
MATCH_SCORE_THRESHOLD=50.0
USE_LLM_FILTERING=false
MAX_JOBS_IN_EMAIL=10
```

### Customization
- **Skill Categories**: Edit `TECH_SKILLS` in `config.py`
- **Scoring Weights**: Modify semantic/skill weights in `JobTrackerConfig`
- **Filter Prompts**: Customize default prompts and thresholds
- **Email Templates**: Update templates in `emailer/send_email.py`

## 📋 Current Status

### ✅ Completed Features
- [x] AI-powered resume parsing (PDF/DOCX)
- [x] Semantic job matching with scoring
- [x] Natural language job filtering  
- [x] RESTful API with FastAPI
- [x] React frontend with modern UI
- [x] Azure Blob Storage integration
- [x] Email report generation
- [x] Docker containerization
- [x] GitHub Actions CI/CD
- [x] Comprehensive testing suite
- [x] Production deployment guides

### 🚧 Work in Progress
- [ ] **Advanced LLM Integration**: OpenAI/Claude API for better filtering
- [ ] **Vector Database**: FAISS/Pinecone for scalable similarity search
- [ ] **User Authentication**: Azure AD B2C integration
- [ ] **Multi-Resume Support**: Handle different resumes for different job types
- [ ] **Analytics Dashboard**: Success rate tracking and insights
- [ ] **Real-time Notifications**: WebSocket updates for job alerts
- [ ] **Mobile App**: React Native mobile application
- [ ] **Browser Extension**: Chrome extension for job board integration

### 🎯 Planned Enhancements
- [ ] **Advanced Matching**: Deep learning models for better accuracy
- [ ] **Company Intelligence**: Glassdoor/LinkedIn company data integration
- [ ] **Salary Prediction**: ML models for salary estimation
- [ ] **Interview Prep**: AI-generated interview questions based on job requirements
- [ ] **Application Tracking**: Track application status and follow-ups
- [ ] **Social Features**: Share profiles and recommendations
- [ ] **API Marketplace**: Third-party integrations and plugins

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/AILearning.git

# Install development dependencies
pip install -r requirements-dev.txt
npm install --dev

# Run tests before submitting
python -m pytest tests/
npm test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Documentation**: [API Docs](http://localhost:8001/docs)
- **Issues**: [GitHub Issues](https://github.com/hcholleti/AILearning/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hcholleti/AILearning/discussions)

## 🎉 Acknowledgments

- **OpenAI** for inspiring AI-powered applications
- **HuggingFace** for sentence transformers models
- **FastAPI** community for excellent documentation
- **Azure** for cloud infrastructure support

---

**⭐ Star this repository if you find it useful!**

*Built with ❤️ by [Harish Cholleti](https://github.com/hcholleti)*
