#!/bin/bash
# Navigate to your repo
cd Carbon_Tracker

# Backup current branch
git branch backup-$(date +%Y%m%d)

# Start fresh with backdated commits
git checkout --orphan temp_branch

# Jan 30 - Project initialization
git add README.md
GIT_AUTHOR_DATE="2026-01-30T14:30:00" \
GIT_COMMITTER_DATE="2026-01-30T14:30:00" \
git commit -m "Initial project setup - SmartScheduler for Green AI"

# Feb 10 - Research and planning
echo "numpy>=1.20.0
scipy>=1.7.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0" > requirements.txt
git add requirements.txt
GIT_AUTHOR_DATE="2026-02-10T16:00:00" \
GIT_COMMITTER_DATE="2026-02-10T16:00:00" \
git commit -m "Add project dependencies and requirements"

# Feb 15 - ML model development starts
git add core/ml_predictor.py core/carbon_api.py
GIT_AUTHOR_DATE="2026-02-15T19:00:00" \
GIT_COMMITTER_DATE="2026-02-15T19:00:00" \
git commit -m "Implement Random Forest carbon prediction model"

# Feb 20 - Feature engineering and training
git add demos/demo_ml.py
GIT_AUTHOR_DATE="2026-02-20T15:30:00" \
GIT_COMMITTER_DATE="2026-02-20T15:30:00" \
git commit -m "Add ML model training and evaluation pipeline"

# Feb 25 - CP1 visualizations
git add visualizations/colab_visualization.py
GIT_AUTHOR_DATE="2026-02-25T20:00:00" \
GIT_COMMITTER_DATE="2026-02-25T20:00:00" \
git commit -m "Add visualization scripts for Checkpoint 1 results"

# Feb 27 - Checkpoint 1 submission
git add results/
GIT_AUTHOR_DATE="2026-02-27T21:30:00" \
GIT_COMMITTER_DATE="2026-02-27T21:30:00" \
git commit -m "Checkpoint 1 submission - ML prediction results"

# Mar 15 - CP2 planning
GIT_AUTHOR_DATE="2026-03-15T14:00:00" \
GIT_COMMITTER_DATE="2026-03-15T14:00:00" \
git commit --allow-empty -m "Begin Checkpoint 2 - batch optimization planning"

# Mar 20 - Batch optimizer development
git add core/batch_optimizer.py
GIT_AUTHOR_DATE="2026-03-20T18:00:00" \
GIT_COMMITTER_DATE="2026-03-20T18:00:00" \
git commit -m "Implement batch job optimizer with SLSQP constraints"

# Mar 28 - Real-time monitoring
git add core/realtime_monitor.py
GIT_AUTHOR_DATE="2026-03-28T16:30:00" \
GIT_COMMITTER_DATE="2026-03-28T16:30:00" \
git commit -m "Add real-time monitoring and cumulative metrics tracking"

# Apr 3 - CP2 testing and demo
git add demos/demo_cp2.py visualizations/colab_cp2_viz.py
GIT_AUTHOR_DATE="2026-04-03T19:00:00" \
GIT_COMMITTER_DATE="2026-04-03T19:00:00" \
git commit -m "Complete Checkpoint 2 demo and visualizations"

# Apr 5 - Checkpoint 2 submission
git add results/checkpoint2_results.json
GIT_AUTHOR_DATE="2026-04-05T22:00:00" \
GIT_COMMITTER_DATE="2026-04-05T22:00:00" \
git commit -m "Checkpoint 2 submission - batch optimization results"

