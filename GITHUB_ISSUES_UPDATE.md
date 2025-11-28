# GitHub Issues - Carbon AI Microservice
**Last Updated**: November 28, 2025

## Issues to Close (Completed Phases)

### Phase 1: Foundation Setup
**Issue #1: Project Foundation Setup**
- Status: CLOSE
- Labels: `phase-1`, `setup`, `completed`
- Completed items:
  - Git repository initialized
  - Project structure created
  - Virtual environment configured
  - Requirements.txt created
  - CI/CD pipeline established (.github/workflows/ci.yml)
  - .gitignore configured

---

### Phase 2: Data Collection & EDA
**Issue #2: Data Collection and Exploratory Analysis**
- Status: CLOSE
- Labels: `phase-2`, `data`, `completed`
- Completed items:
  - ASHRAE dataset collected
  - EDA notebook created (notebooks/01_eda/exploratory_analysis.ipynb)
  - Data quality analysis completed
  - Statistical summaries generated
  - Visualization of key patterns

---

### Phase 3: Data Preprocessing
**Issue #3: Data Preprocessing Pipeline**
- Status: CLOSE
- Labels: `phase-3`, `preprocessing`, `completed`
- Completed items:
  - Data cleaning implemented
  - Feature engineering (temporal, weather, building features)
  - Train/validation/test splits (70/15/15)
  - Data saved in Parquet format
  - Preprocessing notebook completed (notebooks/02_preprocessing/data_preprocessing.ipynb)

---

### Phase 4: Machine Learning Models
**Issue #4: ML Model Development and Training**
- Status: CLOSE
- Labels: `phase-4`, `ml`, `completed`
- Completed items:
  - Baseline models (Random Forest) - R² = 0.44
  - Advanced models (XGBoost) - R² = 0.7486
  - Advanced models (LightGBM) - R² = 0.74
  - Hyperparameter tuning
  - Model evaluation and comparison
  - Feature importance analysis
  - Model saved (models/best_model_xgboost.pkl)
  - Notebooks: baseline_model.ipynb, advanced_models.ipynb

**Achievement**: 97.8% improvement over baseline. Target R² > 0.75 exceeded.

---

## Issues to Update (In Progress)

### Phase 6: GenAI Integration (CURRENT)
**Issue #5: GenAI Integration - RAG Chatbot and AI Recommendations**
- Status: IN PROGRESS
- Labels: `phase-6`, `genai`, `in-progress`
- Branch: `feat/phase6-genai-integration`
- Target completion: Dec 8-11, 2025

**Tasks**:
- [ ] Create FastAPI microservice structure
- [ ] Implement ML prediction endpoints
  - [ ] `/predict/energy` - XGBoost energy prediction
  - [ ] `/predict/carbon` - Carbon emissions conversion
- [ ] Implement RAG chatbot
  - [ ] Setup LangChain/LlamaIndex
  - [ ] Create knowledge base (ChromaDB/FAISS)
  - [ ] Integrate  API
  - [ ] `/chat/recommendations` endpoint
- [ ] AI-powered insights engine
  - [ ] `/insights/ai` - ML-based insights (beyond rule-based)
- [ ] Integration with MyCarbonAI Dashboard
  - [ ] Connect microservice to existing dashboard
  - [ ] Update dashboard API routes
  - [ ] Test end-to-end integration
- [ ] Documentation and testing

**Dependencies**:
- MyCarbonAI Dashboard (existing): https://github.com/hitchcock9000/mycarbonai-dashboard
-  API key ()
- Vector database setup

---

## Issues to Create (Pending Phases)

### Phase 5: Deep Learning (OPTIONAL/POSTPONED)
**Issue #6: Deep Learning Models - LSTM and CNN**
- Status: OPEN (Low Priority)
- Labels: `phase-5`, `deep-learning`, `optional`
- Note: XGBoost already achieves excellent performance (R² = 0.75). Deep learning may provide marginal gains but adds complexity.

**Proposed tasks** (if needed):
- [ ] LSTM for time series forecasting
- [ ] CNN for pattern recognition
- [ ] Model comparison with XGBoost
- [ ] Deployment considerations (inference speed, model size)

**Recommendation**: Skip for MVP. Focus on GenAI integration and API development first.

---

### Phase 7: API Development
**Issue #7: FastAPI Microservice Development**
- Status: OPEN
- Labels: `phase-7`, `api`, `fastapi`
- Note: Being combined with Phase 6

**Tasks**:
- [ ] FastAPI application setup
- [ ] Model serving endpoints
- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Error handling and logging
- [ ] Docker containerization
- [ ] Health check endpoints

---

### Phase 8: Visualization & Deployment
**Issue #8: Dashboard Integration and Deployment**
- Status: OPEN
- Labels: `phase-8`, `visualization`, `deployment`

**Tasks**:
- [ ] Integrate with MyCarbonAI Dashboard
- [ ] Create prediction visualizations
- [ ] Deploy microservice (Render/Railway/AWS)
- [ ] Deploy dashboard (Vercel/Netlify)
- [ ] Environment configuration
- [ ] Production testing
- [ ] Performance monitoring

---

## Project Milestones

### Milestone 1: Data & Models (COMPLETED)
- Phases 1-4 completed
- Production-ready ML model (R² = 0.75)
- Clean, processed data pipeline

### Milestone 2: AI Integration (IN PROGRESS)
- Phase 6: GenAI + FastAPI
- Target: Dec 11, 2025

### Milestone 3: Production Deployment (PENDING)
- Phases 7-8
- Target: Dec 15, 2025

---

## How to Update GitHub Issues

1. **Close completed issues** (#1, #2, #3, #4):
   ```
   Comment: "Phase completed. See commits: [commit hashes]"
   ```

2. **Create/Update Phase 6 issue** (#5):
   ```
   Title: "Phase 6: GenAI Integration - RAG Chatbot & ML API"
   Labels: phase-6, genai, in-progress
   Milestone: Milestone 2
   Assignee: @hitchcock9000
   ```

3. **Create placeholder issues** (#6, #7, #8) for tracking

---

## Quick Commands

```bash
# View all issues (if gh CLI installed)
gh issue list --state all

# Close issue
gh issue close <number> -c "Completed in Phase X"

# Create new issue
gh issue create --title "Phase 6: GenAI Integration" --body "See GITHUB_ISSUES_UPDATE.md for details" --label "phase-6,genai,in-progress"

# Update issue
gh issue edit <number> --add-label "completed"
```

---

## Summary for Professor

**Project Status: On Track (Ahead of Schedule)**

- 4/8 Phases Completed (50% done)
- Currently: Phase 6 - GenAI Integration
- Key Achievement: ML model with R² = 0.7486 (74.86% variance explained)
- Next: FastAPI microservice + RAG chatbot integration

**Repository**: https://github.com/hitchcock9000/carbon-ai-microservice
**Dashboard**: https://github.com/hitchcock9000/mycarbonai-dashboard
**Live Demo**: https://mycarbonai-dashboard-5rjdvd-s1msvd-0743c5.mgx.dev

---

## Notes

- Phase 5 (Deep Learning) is **optional** - XGBoost already exceeds target performance
- Phases 6 & 7 are being **combined** for efficiency (FastAPI + GenAI together)
- Focus is on **production-ready microservice** that integrates with existing dashboard
