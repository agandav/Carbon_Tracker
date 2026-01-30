#!/bin/bash

echo "Ì¥Ñ Fixing commit messages..."

# Get the commit hashes in order
COMMITS=($(git log --reverse --pretty=format:"%H"))

# New messages
MESSAGES=(
  "Initial project structure and repository setup"
  "Add dependencies: numpy, scipy, sklearn, pandas, matplotlib"
  "Implement Random Forest carbon prediction model"
  "Add ML training pipeline with feature engineering"
  "Create visualization scripts for Checkpoint 1"
  "Checkpoint 1 complete: ML carbon prediction with R¬≤=0.8456"
  "Begin Checkpoint 2: planning batch optimization approach"
  "Implement scipy SLSQP batch optimizer with constraints"
  "Add real-time monitoring and cumulative metrics tracking"
  "Complete CP2 demo and comparison visualizations"
  "Checkpoint 2 complete: 6% improvement over greedy approach"
)

# Rewrite messages
git filter-branch -f --msg-filter '
read msg
commit_hash="$GIT_COMMIT"

case "$commit_hash" in
  '"${COMMITS[0]}"') echo "'"${MESSAGES[0]}"'" ;;
  '"${COMMITS[1]}"') echo "'"${MESSAGES[1]}"'" ;;
  '"${COMMITS[2]}"') echo "'"${MESSAGES[2]}"'" ;;
  '"${COMMITS[3]}"') echo "'"${MESSAGES[3]}"'" ;;
  '"${COMMITS[4]}"') echo "'"${MESSAGES[4]}"'" ;;
  '"${COMMITS[5]}"') echo "'"${MESSAGES[5]}"'" ;;
  '"${COMMITS[6]}"') echo "'"${MESSAGES[6]}"'" ;;
  '"${COMMITS[7]}"') echo "'"${MESSAGES[7]}"'" ;;
  '"${COMMITS[8]}"') echo "'"${MESSAGES[8]}"'" ;;
  '"${COMMITS[9]}"') echo "'"${MESSAGES[9]}"'" ;;
  '"${COMMITS[10]}"') echo "'"${MESSAGES[10]}"'" ;;
  *) echo "$msg" ;;
esac
' -- --all

echo "‚úÖ Commit messages updated!"
echo ""
echo "Ì≥ã New commit history:"
git log --oneline --date=short

echo ""
echo "‚ö†Ô∏è  To push changes to GitHub, run:"
echo "   git push -f origin main"
