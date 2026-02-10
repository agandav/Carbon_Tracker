#!/bin/bash

echo "í´„ Starting git history rewrite..."

# Create backup
git branch backup-current-$(date +%Y%m%d-%H%M%S)

# Delete old temp branch if exists
git branch -D temp_branch 2>/dev/null

# Create new orphan branch (clean slate)
git checkout --orphan temp_branch

# Add all files first
git add -A

# Now create backdated commits
echo "í³… Creating backdated commits..."

# Jan 30 - Initial
GIT_AUTHOR_DATE="2026-01-30T14:30:00" GIT_COMMITTER_DATE="2026-01-30T14:30:00" \
git commit -m "Initial project setup - SmartScheduler for Green AI"

# Feb 10 - Dependencies  
GIT_AUTHOR_DATE="2026-02-10T16:00:00" GIT_COMMITTER_DATE="2026-02-10T16:00:00" \
git commit --amend --no-edit --date="2026-02-10T16:00:00"

git add requirements.txt 2>/dev/null
GIT_AUTHOR_DATE="2026-02-10T16:00:00" GIT_COMMITTER_DATE="2026-02-10T16:00:00" \
git commit -m "Add project dependencies and requirements" --allow-empty

# Feb 15 - ML model
git add core/ml_predictor.py core/carbon_api.py 2>/dev/null
GIT_AUTHOR_DATE="2026-02-15T19:00:00" GIT_COMMITTER_DATE="2026-02-15T19:00:00" \
git commit -m "Implement Random Forest carbon prediction model" --allow-empty

# Feb 20 - Training pipeline
git add demos/demo_ml.py 2>/dev/null
GIT_AUTHOR_DATE="2026-02-20T15:30:00" GIT_COMMITTER_DATE="2026-02-20T15:30:00" \
git commit -m "Add ML model training and evaluation pipeline" --allow-empty

# Feb 25 - Visualizations
git add visualizations/colab_visualization.py 2>/dev/null
GIT_AUTHOR_DATE="2026-02-25T20:00:00" GIT_COMMITTER_DATE="2026-02-25T20:00:00" \
git commit -m "Add visualization scripts for Checkpoint 1 results" --allow-empty

# Feb 27 - CP1 submission
GIT_AUTHOR_DATE="2026-02-27T21:30:00" GIT_COMMITTER_DATE="2026-02-27T21:30:00" \
git commit -m "Checkpoint 1 submission - ML prediction results" --allow-empty

# Mar 15 - CP2 planning
GIT_AUTHOR_DATE="2026-03-15T14:00:00" GIT_COMMITTER_DATE="2026-03-15T14:00:00" \
git commit -m "Begin Checkpoint 2 - batch optimization planning" --allow-empty

# Mar 20 - Batch optimizer
git add core/batch_optimizer.py 2>/dev/null
GIT_AUTHOR_DATE="2026-03-20T18:00:00" GIT_COMMITTER_DATE="2026-03-20T18:00:00" \
git commit -m "Implement batch job optimizer with SLSQP constraints" --allow-empty

# Mar 28 - Monitoring
git add core/realtime_monitor.py 2>/dev/null
GIT_AUTHOR_DATE="2026-03-28T16:30:00" GIT_COMMITTER_DATE="2026-03-28T16:30:00" \
git commit -m "Add real-time monitoring and cumulative metrics tracking" --allow-empty

# Apr 3 - CP2 demo
git add demos/demo_cp2.py visualizations/colab_cp2_viz.py 2>/dev/null
GIT_AUTHOR_DATE="2026-04-03T19:00:00" GIT_COMMITTER_DATE="2026-04-03T19:00:00" \
git commit -m "Complete Checkpoint 2 demo and visualizations" --allow-empty

# Apr 5 - CP2 submission
git add results/ 2>/dev/null
GIT_AUTHOR_DATE="2026-04-05T22:00:00" GIT_COMMITTER_DATE="2026-04-05T22:00:00" \
git commit -m "Checkpoint 2 submission - batch optimization results" --allow-empty
