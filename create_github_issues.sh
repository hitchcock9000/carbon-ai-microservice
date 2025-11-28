#!/bin/bash
# Script to create GitHub issues for Carbon AI Microservice
# Run this script to create all project tracking issues

REPO="hitchcock9000/carbon-ai-microservice"

echo "Creating GitHub Issues for Carbon AI Microservice"
echo "=================================================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) is not installed"
    echo "Install it with: brew install gh"
    echo "Then authenticate: gh auth login"
    exit 1
fi

# Close completed phases
echo "Step 1: Closing completed phase issues..."
echo ""

# Issue #1: Phase 1 - Foundation
gh issue close 1 -c "Phase 1 completed:
- Git repository initialized
- Project structure created
- CI/CD pipeline established
- Requirements and dependencies configured
See commits: 1f0c359, earlier commits" 2>/dev/null || echo "Issue #1 not found or already closed"

# Issue #2: Phase 2 - Data Collection & EDA
gh issue close 2 -c "Phase 2 completed:
- ASHRAE dataset collected and analyzed
- EDA notebook created with comprehensive analysis
- Data quality assessment completed
See notebook: notebooks/01_eda/exploratory_analysis.ipynb" 2>/dev/null || echo "Issue #2 not found or already closed"

# Issue #3: Phase 3 - Preprocessing
gh issue close 3 -c "Phase 3 completed:
- Data cleaning and feature engineering implemented
- Train/val/test splits created (70/15/15)
- Data saved in Parquet format for efficiency
See notebook: notebooks/02_preprocessing/data_preprocessing.ipynb" 2>/dev/null || echo "Issue #3 not found or already closed"

# Issue #4: Phase 4 - ML Models
gh issue close 4 -c "Phase 4 completed:
- Baseline models: Random Forest (R² = 0.44)
- Advanced models: XGBoost (R² = 0.7486), LightGBM (R² = 0.74)
- Hyperparameter tuning completed
- Model saved: models/best_model_xgboost.pkl
- 97.8% improvement over baseline achieved
See commits: 94b0f47, 193393f" 2>/dev/null || echo "Issue #4 not found or already closed"

echo ""
echo "Step 2: Creating new tracking issues..."
echo ""

# Create Phase 6 issue (current work)
echo "Creating Phase 6 issue..."
gh issue create \
  --title "Phase 6: GenAI Integration - FastAPI Microservice + RAG Chatbot" \
  --body "## Overview
Implement GenAI-powered features with FastAPI microservice for ML predictions and intelligent recommendations.

## Sprint Tasks

### 6.1 FastAPI Microservice Setup
- [x] Create FastAPI application structure
- [x] Implement CORS middleware
- [x] Setup Pydantic models for validation
- [x] Create health check endpoints

### 6.2 ML Prediction Endpoints
- [x] Load XGBoost model (R² = 0.7486)
- [x] Implement feature engineering service
- [x] Create /api/predict/energy endpoint
- [x] Create /api/predict/carbon endpoint
- [x] Create /api/predict/full pipeline endpoint
- [x] Test predictions locally (54.35 kWh, 20.92 kg CO2e)

### 6.3 RAG Chatbot Implementation
- [ ] Setup LangChain with  API
- [ ] Create energy efficiency knowledge base
- [ ] Implement vector database (ChromaDB/FAISS)
- [ ] Create /api/chat/recommendations endpoint
- [ ] Add conversation history management

### 6.4 AI Insights Engine
- [ ] Implement ML-based insights (beyond rule-based)
- [ ] Create /api/insights/ai endpoint
- [ ] Add anomaly detection
- [ ] Generate actionable recommendations

### 6.5 Dashboard Integration
- [ ] Connect microservice to MyCarbonAI Dashboard
- [ ] Update dashboard to call ML endpoints
- [ ] Add prediction visualizations
- [ ] Test end-to-end integration

### 6.6 Documentation & Testing
- [ ] Write API documentation (Swagger/OpenAPI)
- [ ] Create integration tests
- [ ] Add error handling and logging
- [ ] Document deployment process

## Technical Details
- **Framework**: FastAPI + Uvicorn
- **ML Model**: XGBoost (R² = 0.7486)
- **GenAI**:   + LangChain
- **Vector DB**: ChromaDB or FAISS
- **Integration**: MyCarbonAI Dashboard (React + Express)

## Branch
\`feat/phase6-genai-integration\`

## Current Status
- FastAPI structure: DONE
- ML endpoints: DONE
- RAG chatbot: IN PROGRESS
- Dashboard integration: PENDING

## Dependencies
-  API key ()
- MyCarbonAI Dashboard running
- XGBoost model file

## Acceptance Criteria
- [ ] ML predictions working via API
- [ ] RAG chatbot provides relevant recommendations
- [ ] Dashboard successfully calls microservice
- [ ] All endpoints documented in Swagger
- [ ] Integration tests passing" \
  --label "phase-6,genai,in-progress,api" \
  --milestone "Milestone 2: AI Integration"

echo ""
echo "Creating Phase 5 issue (optional)..."
gh issue create \
  --title "Phase 5: Deep Learning Models (OPTIONAL)" \
  --body "## Overview
Experiment with deep learning models for time series prediction.

**Note**: This phase is OPTIONAL. XGBoost already achieves R² = 0.75, which exceeds target performance.

## Tasks (if pursued)
- [ ] Implement LSTM for time series forecasting
- [ ] Implement CNN for pattern recognition
- [ ] Compare with XGBoost performance
- [ ] Evaluate inference speed and model size
- [ ] Document trade-offs

## Recommendation
**SKIP for MVP**. Focus on GenAI integration (Phase 6) and API development instead.

## Reason
- XGBoost already meets performance targets
- Deep learning adds complexity with marginal gains
- Slower inference time
- Larger model size
- Can revisit after core features complete" \
  --label "phase-5,deep-learning,optional,low-priority"

echo ""
echo "Creating Phase 7 issue..."
gh issue create \
  --title "Phase 7: API Enhancements & Production Readiness" \
  --body "## Overview
Enhance API with production features (combined with Phase 6).

## Tasks
- [ ] Add authentication and authorization (JWT)
- [ ] Implement rate limiting
- [ ] Add request validation and error handling
- [ ] Setup logging and monitoring
- [ ] Create Docker containerization
- [ ] Add API versioning
- [ ] Implement caching for predictions
- [ ] Add batch prediction endpoint

## Production Requirements
- [ ] Environment configuration
- [ ] Security hardening
- [ ] Performance optimization
- [ ] Load testing
- [ ] Documentation updates

## Status
Partially combined with Phase 6 for efficiency." \
  --label "phase-7,api,production"

echo ""
echo "Creating Phase 8 issue..."
gh issue create \
  --title "Phase 8: Deployment & Final Integration" \
  --body "## Overview
Deploy microservice and dashboard to production.

## Deployment Tasks

### Microservice Deployment
- [ ] Deploy to Render/Railway/AWS
- [ ] Configure environment variables
- [ ] Setup domain and SSL
- [ ] Configure CORS for production
- [ ] Setup monitoring (Sentry/LogRocket)

### Dashboard Integration
- [ ] Update dashboard API endpoints
- [ ] Deploy dashboard (Vercel/Netlify)
- [ ] Test production integration
- [ ] Add loading states and error handling

### Testing & Monitoring
- [ ] End-to-end production testing
- [ ] Performance monitoring setup
- [ ] Error tracking configuration
- [ ] Usage analytics

### Documentation
- [ ] API documentation (public)
- [ ] Integration guide for dashboard
- [ ] Deployment runbook
- [ ] User documentation

## Deliverables
- Live microservice URL
- Live dashboard URL
- Complete documentation
- Monitoring dashboards" \
  --label "phase-8,deployment,production"

echo ""
echo "=================================================="
echo "GitHub Issues Created Successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. View issues: gh issue list"
echo "2. Assign yourself: gh issue edit <number> --add-assignee @me"
echo "3. Add to project board if available"
echo ""
