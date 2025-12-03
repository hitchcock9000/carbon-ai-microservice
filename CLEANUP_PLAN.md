# Project Cleanup Plan

**Date:** 2025-12-03
**Purpose:** Remove unnecessary, duplicate, and test files from the project

---

## Files to DELETE

### 1. Test Scripts in Root (Move to tests/ or delete)
- [ ] `test_api.py` - Move to tests/ directory
- [ ] `test_chatbot.py` - Move to tests/ directory
- [ ] `test_forecast_endpoint.py` - Move to tests/ directory
- [ ] `test_lstm_model.py` - Move to tests/ directory
- [ ] `test_api.sh` - Delete (redundant)
- [ ] `test_api_live.sh` - Delete (redundant)
- [ ] `test_integration.sh` - Move to tests/
- [ ] `test_full_integration.sh` - Move to tests/

### 2. Utility Scripts (Low value)
- [ ] `check_security.py` - Delete (one-time use)
- [ ] `convert_md_to_pdf.py` - Delete (not needed)
- [ ] `debug_env.py` - Delete (debugging only)
- [ ] `setup_security.sh` - Delete (one-time setup)
- [ ] `create_github_issues.sh` - Delete (one-time use)

### 3. Duplicate/Backup Notebooks
- [ ] `notebooks/03_modeling/baseline_model_backup.ipynb` - DELETE (backup of baseline_model.ipynb)
- [ ] `notebooks/03_modeling/lstm_forecasting_v2.ipynb` - DELETE (replaced by lstm_forecasting.ipynb and lstm_forecasting_colab.ipynb)
- [ ] `notebooks/03_modeling/test_model_loading.py` - Move to examples/ or delete

### 4. Redundant Planning Docs
- [ ] `LSTM_INTEGRATION_GUIDE.md` - Keep (useful reference)
- [ ] `PRODUCT_REQUIREMENTS.md` - Move to docs/
- [ ] `PROJECT_PLAN.md` - Move to docs/
- [ ] `QUICK_START.md` - Keep (useful)

### 5. Cache Files
- [ ] `tests/__pycache__/` - Delete entire directory
- [ ] Any `.pyc` files

---

## Files to KEEP

### Root Directory
- [x] `README.md` - Main documentation
- [x] `requirements.txt` - Dependencies
- [x] `run_api.sh` - Production script
- [x] `start_server.sh` - Production script
- [x] `.env` - Configuration
- [x] `.gitignore` - Git configuration

### Notebooks (Keep)
- [x] `notebooks/01_data_collection/data_download.ipynb`
- [x] `notebooks/02_preprocessing/data_preprocessing.ipynb`
- [x] `notebooks/02_preprocessing/feature_engineering.ipynb`
- [x] `notebooks/03_modeling/baseline_model.ipynb`
- [x] `notebooks/03_modeling/lstm_forecasting.ipynb`
- [x] `notebooks/03_modeling/lstm_forecasting_colab.ipynb`
- [x] `notebooks/04_evaluation/model_evaluation.ipynb`

### Documentation (Keep)
- [x] `docs/PROJECT_STATUS.md`
- [x] `docs/model_analysis.md`
- [x] `docs/API_DOCUMENTATION.md`
- [x] `notebooks/03_modeling/COLAB_SETUP.md`
- [x] `notebooks/03_modeling/GPU_TROUBLESHOOTING.md`

### Source Code (Keep all)
- [x] `src/api/`
- [x] `src/core/`
- [x] `src/models/`
- [x] `examples/`

---

## Execution Plan

### Phase 1: Safe Deletions (No Git History Impact)
```bash
# Delete backup and duplicate notebooks
rm notebooks/03_modeling/baseline_model_backup.ipynb
rm notebooks/03_modeling/lstm_forecasting_v2.ipynb

# Delete utility scripts
rm check_security.py
rm convert_md_to_pdf.py
rm debug_env.py
rm setup_security.sh
rm create_github_issues.sh

# Delete cache
rm -rf tests/__pycache__/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
```

### Phase 2: Reorganize Tests
```bash
# Move test scripts to tests/
mv test_api.py tests/
mv test_chatbot.py tests/
mv test_forecast_endpoint.py tests/
mv test_lstm_model.py tests/
mv test_integration.sh tests/
mv test_full_integration.sh tests/

# Delete redundant test scripts
rm test_api.sh
rm test_api_live.sh
```

### Phase 3: Reorganize Documentation
```bash
# Move planning docs to docs/
mv PRODUCT_REQUIREMENTS.md docs/
mv PROJECT_PLAN.md docs/
```

### Phase 4: Git Cleanup
```bash
# Add deletions to git
git add -A

# Commit cleanup
git commit -m "chore: remove duplicate, backup, and unnecessary files

- Delete backup notebooks (baseline_model_backup.ipynb, lstm_forecasting_v2.ipynb)
- Remove one-time utility scripts
- Reorganize test files into tests/ directory
- Move planning docs to docs/
- Clean up cache files

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to remote
git push origin feat/phase6-genai-integration
```

---

## Summary

**Files to Delete:** 15
**Files to Move:** 6
**Files to Keep:** All production code + documentation

**Estimated Space Saved:** ~5-10 MB (mostly cache and duplicates)

**Risk Level:** LOW (all deletions are backups, test files, or utilities)

---

## Before Execution Checklist

- [ ] Review this plan
- [ ] Backup important files (optional)
- [ ] Verify git status is clean
- [ ] Confirm on correct branch (feat/phase6-genai-integration)
- [ ] Execute Phase 1 (deletions)
- [ ] Execute Phase 2 (reorganize tests)
- [ ] Execute Phase 3 (reorganize docs)
- [ ] Execute Phase 4 (git commit and push)
- [ ] Verify git status after cleanup
- [ ] Delete this CLEANUP_PLAN.md file
