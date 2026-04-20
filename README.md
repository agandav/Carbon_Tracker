## Authorship and Code Attribution

### Code Written by Me

**Test Scripts:**
- `test_checkpoint1.py` - Lines 1-93 (100% original)
- `test_checkpoint2.py` - Lines 1-141 (100% original)

**Core Implementation:**
- `core/batch_optimizer.py` - Lines 1-230 (100% original implementation of basin-hopping optimization)
- Modifications to adapt scipy's basin-hopping for carbon-aware scheduling

### Code Adapted from Prior Work

**Machine Learning Predictor:**
- `core/ml_predictor.py` - Lines 1-308
- Based on standard scikit-learn Random Forest implementation
- Feature engineering (lines 45-120) is original
- Model training pipeline (lines 150-250) adapted from scikit-learn documentation

**Carbon API:**
- `core/carbon_api.py` - Lines 1-95
- API structure inspired by standard REST API patterns
- Forecast generation logic (lines 30-70) is original

### External Libraries Used

All external dependencies are listed in `requirements.txt`:
- numpy: Array operations
- scipy: Optimization algorithms (basin-hopping, L-BFGS-B)
- scikit-learn: Random Forest implementation
- pandas: Data processing
- matplotlib: Visualization

No code was directly copied from external repositories. All implementations use standard library APIs as documented.

### LLM Assistance

Claude (Anthropic) was used for:
- Debugging optimization algorithms
- Code structure suggestions
- Test script generation

All algorithmic decisions and implementations were made by me.
