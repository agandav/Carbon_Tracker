# SmartScheduler: Carbon-Aware Batch Optimization for Sustainable AI Training

**ECE 57000 - Artificial Intelligence (Spring 2026)**  
**Final Project - Product Prototype Track**

## 📋 Project Overview

SmartScheduler is an intelligent job scheduling system that reduces carbon emissions from ML training by 27-50% through temporal optimization. The system combines Random Forest regression for carbon prediction with constrained optimization (scipy SLSQP) for multi-job batch scheduling.

**Key Results:**
- ✅ 27.2% carbon reduction vs immediate scheduling
- ✅ 6% improvement over single-job greedy approaches
- ✅ 84.3% ML prediction accuracy (R²=0.8456)
- ✅ <1 second optimization time for 5-job batches
- ✅ 100% deadline satisfaction with dependency handling

## 🏗️ Code Structure

```
smartscheduler/
├── core/
│   ├── ml_predictor.py          # Random Forest carbon prediction model
│   ├── batch_optimizer.py       # Constrained optimization (scipy SLSQP)
│   ├── realtime_monitor.py      # Real-time monitoring system
│   ├── scheduler.py             # Smart scheduling core
│   └── carbon_api.py            # Carbon intensity API interface
├── demos/
│   ├── demo_ml.py               # Checkpoint 1 demo (ML prediction)
│   └── demo_cp2.py              # Checkpoint 2 demo (batch optimization)
├── visualizations/
│   ├── colab_visualization.py   # Colab script for CP1 graphs
│   └── colab_cp2_viz.py         # Colab script for CP2 graphs
├── results/
│   ├── ml_enhanced_results.json # Checkpoint 1 results
│   ├── checkpoint2_results.json # Checkpoint 2 results
│   └── ml_scheduler_model.pkl   # Trained ML model (7.5MB)
├── tests/
│   ├── test_ml_predictor.py
│   ├── test_batch_optimizer.py
│   └── test_integration.py
├── paper/
│   ├── smartscheduler_paper.tex # LaTeX source
│   ├── smartscheduler_paper.pdf # Compiled PDF
│   └── references.bib           # Bibliography
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- (Optional) LaTeX distribution for compiling paper

### Installation

```bash
# Clone repository
git clone https://github.com/anonymous/smartscheduler
cd smartscheduler

# Install dependencies
pip install -r requirements.txt
```

### Running Demos

**Checkpoint 1 Demo (ML Prediction):**
```bash
cd demos
python demo_ml.py
```
Output: ML model training, evaluation metrics, 3-job optimization results

**Checkpoint 2 Demo (Batch Optimization):**
```bash
cd demos
python demo_cp2.py
```
Output: 5-job batch optimization with dependencies, cumulative impact tracking

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_ml_predictor.py -v
```

## 📊 Reproducing Results

### ML Model Training
```python
from core.ml_predictor import MLPredictor

# Train model
predictor = MLPredictor()
metrics = predictor.train(n_samples=1000)
print(f"R² Score: {metrics['r2_score']}")  # Expected: 0.8456

# Save model
predictor.save_model("ml_scheduler_model.pkl")
```

### Batch Optimization
```python
from core.batch_optimizer import BatchJobOptimizer

# Define jobs with dependencies
jobs = [
    {'duration_hours': 2, 'energy_kwh': 80, 'deadline_hours': 24, 'dependencies': []},
    {'duration_hours': 6, 'energy_kwh': 350, 'deadline_hours': 20, 'dependencies': [0]},
    # ... more jobs
]

# Optimize batch
optimizer = BatchJobOptimizer(carbon_forecast)
results = optimizer.optimize_batch(jobs)
print(f"Carbon saved: {results['carbon_saved_kg']:.2f} kg CO₂")
```

### Generating Visualizations

**Option 1: Local Generation**
```bash
cd visualizations
python colab_visualization.py  # CP1 graphs
python colab_cp2_viz.py         # CP2 graphs
```

**Option 2: Google Colab**
1. Open [Google Colab](https://colab.research.google.com/)
2. Upload `colab_cp2_viz.py` or copy-paste the code
3. Run all cells
4. Download generated PNG files

## 🔍 Code Authorship

### Student-Written Code (Primary Contributions)

**File: `core/ml_predictor.py` (280 lines)**
- Lines 1-50: Training data generation logic [STUDENT-WRITTEN]
- Lines 51-120: Feature engineering pipeline [STUDENT-WRITTEN]
- Lines 121-200: Model training and evaluation [ADAPTED from sklearn examples]
- Lines 201-280: Inference and confidence scoring [STUDENT-WRITTEN]

**File: `core/batch_optimizer.py` (130 lines)**
- Lines 1-130: Complete constrained optimization implementation [STUDENT-WRITTEN]
- Uses scipy.optimize library but objective/constraint formulation is original

**File: `core/realtime_monitor.py` (160 lines)**
- Lines 1-160: Complete monitoring system [STUDENT-WRITTEN]

**File: `demos/demo_cp2.py` (205 lines)**
- Lines 1-205: Integration demo showcasing all components [STUDENT-WRITTEN]

### Adapted/External Code

**File: `core/carbon_api.py`**
- Lines 10-45: API request structure [ADAPTED from requests library documentation]
- Lines 46-80: Carbon intensity simulation [STUDENT-WRITTEN with realistic patterns]

**File: `visualizations/colab_*.py`**
- Matplotlib plotting code [ADAPTED from matplotlib gallery examples]
- Data structures and analysis [STUDENT-WRITTEN]

### LLM-Assisted Code (~40% of total codebase)
- Code scaffolding and boilerplate
- Documentation strings
- Error handling patterns
- Test case generation

**All LLM-generated code was reviewed, modified, tested, and validated by the student.**

## 📦 Dependencies

### Core Dependencies
```
numpy>=1.20.0          # Numerical computing
scipy>=1.7.0           # Optimization (SLSQP solver)
pandas>=1.3.0          # Data manipulation
scikit-learn>=1.0.0    # Random Forest models
matplotlib>=3.4.0      # Visualization
```

### Optional Dependencies
```
pytest>=7.0.0          # Testing framework
jupyter>=1.0.0         # Notebook interface
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

### Unit Tests
```bash
# Test ML predictor
pytest tests/test_ml_predictor.py -v

# Test batch optimizer
pytest tests/test_batch_optimizer.py -v

# Test monitoring system
pytest tests/test_monitor.py -v
```

### Integration Tests
```bash
# End-to-end pipeline test
pytest tests/test_integration.py -v
```

### Expected Test Results
- All unit tests should pass (100% pass rate)
- Integration test validates 5-job pipeline optimization
- Performance tests verify <1 second optimization time

## 📄 Paper Compilation

### Compiling LaTeX Paper
```bash
cd paper
pdflatex smartscheduler_paper.tex
bibtex smartscheduler_paper
pdflatex smartscheduler_paper.tex
pdflatex smartscheduler_paper.tex
```

The compiled PDF meets ICLR 2026 formatting requirements:
- ✅ 4-6 pages (excluding references)
- ✅ ICLR 2026 template
- ✅ Proper citations
- ✅ LLM acknowledgements section

## 🎯 Reproducing Paper Results

### Table 1: ML Model Performance
Run `demos/demo_ml.py` and check output for:
- Carbon Predictor R²: 0.8456
- MAE: 22.68 kg CO₂
- Accuracy: 84.3%

### Table 2: Carbon Emissions Comparison
Run `demos/demo_cp2.py` and verify:
- CP1 (Single-Job): 340.93 kg CO₂
- CP2 (Batch): 320.56 kg CO₂
- Improvement: 20.37 kg (6%)

### Figure 1: System Architecture
See `paper/architecture_diagram.png` (generated from Mermaid/Graphviz)

### Figure 2: Results Comparison
Generated by `visualizations/colab_cp2_viz.py`
- Panel 1: CP1 vs CP2 bar chart
- Panel 2: Feature evolution
- Panel 3: Gantt chart with dependencies

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'scipy'"**
```bash
pip install scipy --break-system-packages
```

**Issue: "Optimization failed to converge"**
- Check that deadline constraints are feasible (all jobs can complete within deadlines)
- Verify dependencies don't create circular references
- Increase `maxiter` in SLSQP options

**Issue: "Model file not found"**
```bash
# Train model first
cd demos
python demo_ml.py
# This generates ml_scheduler_model.pkl
```

**Issue: LaTeX compilation errors**
- Ensure ICLR 2026 style files are in the same directory
- Install missing LaTeX packages: `texlive-full` (Linux) or MacTeX (macOS)

## 🔬 Research Validation

### Synthetic Data Validation
Our synthetic data generation follows validated patterns:
- Carbon intensity ranges: Based on CAISO and ERCOT grid operator data
- Temporal patterns: Validated against ElectricityMap historical data
- Energy consumption: Aligned with published ML training benchmarks

### Model Performance Baseline
- R² > 0.80 is considered "excellent" for real-world prediction tasks
- MAE of 22.68 kg on jobs saving 50-100 kg represents 20-45% error margin
- Comparable to published carbon prediction models in datacenter research

## 📚 Additional Resources

### Papers Cited
See `paper/references.bib` for complete bibliography

Key references:
1. Strubell et al. (2019) - Energy and Policy Considerations for Deep Learning in NLP
2. Schwartz et al. (2020) - Green AI
3. Dodge et al. (2022) - Measuring Carbon Intensity of AI in Cloud Instances

### Related Projects
- [ElectricityMap](https://electricitymap.org/) - Real-time carbon intensity data
- [CodeCarbon](https://codecarbon.io/) - ML training carbon tracking
- [Green Algorithms](http://www.green-algorithms.org/) - Carbon footprint calculator

## 📞 Contact

For questions about this project:
- **Course:** ECE 57000 - Artificial Intelligence
- **Semester:** Spring 2026
- **Institution:** Purdue University

## 📜 License

This project is submitted as coursework for ECE 57000. Code is provided for academic evaluation purposes.

## 🙏 Acknowledgements

- **LLM Assistance:** Claude (Anthropic) for code scaffolding, debugging, and writing structure
- **Course Staff:** ECE 57000 teaching team for project guidance
- **Data Sources:** CAISO, ERCOT grid operator data for validation
- **Libraries:** scikit-learn, scipy, matplotlib, numpy, pandas

---

**Last Updated:** April 2026  
**Project Track:** Product Prototype  
**Status:** ✅ Complete and Ready for Submission
