# GitHub Issues - Manual Creation Guide

Go to: https://github.com/hitchcock9000/carbon-ai-microservice/issues/new

---

## Issue 1: Phase 6 - GenAI Integration

**Title:**
```
Phase 6: GenAI Integration - FastAPI Microservice + RAG Chatbot
```

**Labels:** `phase-6`, `genai`, `in-progress`, `api`

**Body:**
```markdown
## Overview
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
`feat/phase6-genai-integration`

## Current Status
- FastAPI structure: DONE
- ML endpoints: DONE
- RAG chatbot: IN PROGRESS
- Dashboard integration: PENDING

## Commits
- f4656dd: feat: implement FastAPI microservice with ML prediction endpoints
- 6eff212: fix: correct feature engineering to match XGBoost model requirements
- ceb08ad: docs: add GitHub issues creation script and roadmap
```

---

## Issue 2: Phase 5 - Deep Learning (OPTIONAL)

**Title:**
```
Phase 5: Deep Learning Models (OPTIONAL - Low Priority)
```

**Labels:** `phase-5`, `deep-learning`, `optional`, `low-priority`

**Body:**
```markdown
## Overview
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
- Can revisit after core features complete
```

---

## Issue 3: Phase 7 - API Production Readiness

**Title:**
```
Phase 7: API Enhancements & Production Readiness
```

**Labels:** `phase-7`, `api`, `production`

**Body:**
```markdown
## Overview
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
Partially combined with Phase 6 for efficiency.
```

---

## Issue 4: Phase 8 - Deployment

**Title:**
```
Phase 8: Deployment & Final Integration
```

**Labels:** `phase-8`, `deployment`, `production`

**Body:**
```markdown
## Overview
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
- Monitoring dashboards
```

---

## To Close Completed Issues

If issues #1-4 exist for old phases, close them with these comments:

### Close Issue #1 (Phase 1)
```
Phase 1 completed:
- Git repository initialized
- Project structure created
- CI/CD pipeline established
- Requirements and dependencies configured
```

### Close Issue #2 (Phase 2)
```
Phase 2 completed:
- ASHRAE dataset collected and analyzed
- EDA notebook created with comprehensive analysis
- Data quality assessment completed
See notebook: notebooks/01_eda/exploratory_analysis.ipynb
```

### Close Issue #3 (Phase 3)
```
Phase 3 completed:
- Data cleaning and feature engineering implemented
- Train/val/test splits created (70/15/15)
- Data saved in Parquet format for efficiency
See notebook: notebooks/02_preprocessing/data_preprocessing.ipynb
```

### Close Issue #4 (Phase 4)
```
Phase 4 completed:
- Baseline models: Random Forest (R² = 0.44)
- Advanced models: XGBoost (R² = 0.7486), LightGBM (R² = 0.74)
- Hyperparameter tuning completed
- Model saved: models/best_model_xgboost.pkl
- 97.8% improvement over baseline achieved
See commits: 94b0f47, 193393f, 1f0c359
```
