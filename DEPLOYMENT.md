# AI Job Tracker - Deployment Guide

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Azure Blob     │
│   (Port 3000)   │◄──►│  (Port 8000)     │◄──►│  Storage        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Azure Static    │    │ Azure App       │    │ - Resumes       │
│ Web Apps        │    │ Service         │    │ - Search Results│
└─────────────────┘    └─────────────────┘    │ - User Sessions │
                                              └─────────────────┘
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### 1. Clone and Setup Backend
```bash
cd src
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Setup Frontend
```bash
cd frontend
npm install
```

### 3. Environment Variables
Create `.env` file in project root:
```bash
# Required
RAPIDAPI_KEY=your_rapidapi_key_here
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Optional (for Azure)
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection_string
AZURE_STORAGE_CONTAINER=jobtracker
```

### 4. Run Development Servers
```bash
# Terminal 1 - Backend
cd src
uvicorn api.main:app --reload --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

Visit: http://localhost:3000

## 🐳 Docker Development

```bash
docker-compose up --build
```

## ☁️ Azure Deployment

### Step 1: Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-job-tracker --location eastus

# Create storage account
az storage account create \
  --name jobtrackerstorage$(date +%s) \
  --resource-group rg-job-tracker \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name jobtracker \
  --account-name jobtrackerstorage$(date +%s) \
  --auth-mode login

# Create App Service Plan
az appservice plan create \
  --name plan-job-tracker \
  --resource-group rg-job-tracker \
  --sku B1 \
  --is-linux

# Create Web App for Backend
az webapp create \
  --name job-tracker-api-$(date +%s) \
  --resource-group rg-job-tracker \
  --plan plan-job-tracker \
  --runtime "PYTHON|3.11"
```

### Step 2: Configure App Settings

```bash
az webapp config appsettings set \
  --name your-app-name \
  --resource-group rg-job-tracker \
  --settings \
  RAPIDAPI_KEY="your_key" \
  EMAIL_ADDRESS="your_email" \
  AZURE_STORAGE_CONNECTION_STRING="your_connection_string"
```

### Step 3: Deploy Backend

```bash
# From project root
cd src
zip -r ../deploy.zip .
az webapp deployment source config-zip \
  --name your-app-name \
  --resource-group rg-job-tracker \
  --src ../deploy.zip
```

### Step 4: Deploy Frontend (Static Web Apps)

```bash
# Build frontend
cd frontend
npm run build

# Create Static Web App
az staticwebapp create \
  --name job-tracker-frontend \
  --resource-group rg-job-tracker \
  --source . \
  --location eastus \
  --branch main \
  --app-location "frontend" \
  --output-location "dist"
```

## 🔧 GitHub Actions CI/CD

### Required Secrets
In GitHub repository settings, add these secrets:

```
AZURE_CREDENTIALS='{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret", 
  "subscriptionId": "your-subscription-id",
  "tenantId": "your-tenant-id"
}'

AZURE_STATIC_WEB_APPS_API_TOKEN=your_static_web_app_token
RAPIDAPI_KEY=your_rapidapi_key
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_password
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

### Create Service Principal
```bash
az ad sp create-for-rbac \
  --name "job-tracker-deploy" \
  --role contributor \
  --scopes /subscriptions/your-subscription-id \
  --sdk-auth
```

## 📊 Storage Organization

Azure Blob Storage structure:
```
jobtracker/
├── resumes/
│   └── {session-id}/
│       └── resume.pdf
├── profiles/
│   └── {session-id}/
│       └── profile.json
└── results/
    └── {session-id}/
        ├── latest.json
        └── search_20250117_143022.json
```

## 🔒 Security Best Practices

### Backend Security
- [ ] Use Azure Managed Identity instead of connection strings
- [ ] Implement rate limiting with Azure Front Door
- [ ] Add authentication (Azure AD B2C)
- [ ] Use Azure Key Vault for secrets

### Frontend Security
- [ ] Configure CORS properly for production
- [ ] Add CSP headers
- [ ] Implement HTTPS redirect
- [ ] Add request/response validation

## 📈 Monitoring & Scaling

### Application Insights
```bash
az extension add --name application-insights
az monitor app-insights component create \
  --app job-tracker-insights \
  --location eastus \
  --resource-group rg-job-tracker
```

### Auto-scaling
```bash
az monitor autoscale create \
  --resource-group rg-job-tracker \
  --resource your-app-service \
  --resource-type Microsoft.Web/serverfarms \
  --name job-tracker-autoscale \
  --min-count 1 \
  --max-count 5 \
  --count 2
```

## 🚨 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check logs
az webapp log tail --name your-app-name --resource-group rg-job-tracker

# Verify Python version
az webapp config show --name your-app-name --resource-group rg-job-tracker
```

**Frontend build fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Storage access denied:**
```bash
# Check connection string
az storage account show-connection-string \
  --name your-storage-account \
  --resource-group rg-job-tracker
```

## 💰 Cost Optimization

- Use B1 App Service Plan for development ($12/month)
- Standard_LRS storage for minimal costs
- Consider Azure Functions for serverless backend
- Use CDN for frontend static files

## 🔄 Development Workflow

1. **Feature Development:**
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

2. **Testing:**
   ```bash
   # Run backend tests
   cd src && python -m pytest
   
   # Run frontend tests  
   cd frontend && npm test
   ```

3. **Deployment:**
   - Create PR → triggers build
   - Merge to main → triggers deployment
   - Monitor Application Insights for issues

## 📚 Additional Resources

- [Azure App Service Python docs](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Azure Static Web Apps docs](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Azure Blob Storage Python SDK](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [React deployment guide](https://create-react-app.dev/docs/deployment/)
