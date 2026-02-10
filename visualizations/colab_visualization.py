"""
ML Performance Visualization for Google Colab
Run this entire script in a single Colab cell to generate Slide 7 graphs

NO EXTERNAL FILES NEEDED - All data embedded in this script
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# EMBEDDED DATA (from your actual ML results)
# ============================================================================

# Model Performance Metrics
ml_metrics = {
    'carbon_model': {
        'r2': 0.8456,
        'mae': 22.68,
        'mse': 1218.01
    },
    'delay_model': {
        'r2': 0.5233,
        'mae': 3.00,
        'mse': 23.00
    },
    'feature_importance': {
        'current_intensity': 0.482,
        'energy_kwh': 0.470,
        'month': 0.012,
        'start_hour': 0.011,
        'day_of_week': 0.009,
        'duration_hours': 0.007,
        'priority': 0.004,
        'is_daytime': 0.003,
        'is_weekend': 0.002
    }
}

# Job Results (Rule-based vs ML Predictions)
job_results = {
    'job_names': ['Job 1', 'Job 2', 'Job 3'],
    'rule_based_carbon': [51.30, 21.69, 39.36],  # kg CO2
    'ml_predicted_carbon': [48.21, 25.10, 49.30],  # kg CO2
    'prediction_accuracy': [94.0, 84.3, 74.8]  # percent
}

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_ml_performance_dashboard():
    """Create complete 4-panel ML performance dashboard"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Set style
    plt.style.use('default')
    
    # ========================================================================
    # PANEL 1: R² Scores (Model Performance)
    # ========================================================================
    models = ['Carbon\nSavings', 'Optimal\nDelay']
    r2_scores = [
        ml_metrics['carbon_model']['r2'], 
        ml_metrics['delay_model']['r2']
    ]
    colors_r2 = ['#06A77D', '#2E86AB']
    
    bars = ax1.bar(models, r2_scores, color=colors_r2, width=0.6, alpha=0.85, 
                   edgecolor='white', linewidth=2)
    
    # Target line
    ax1.axhline(y=0.8, color='#FF6B35', linestyle='--', linewidth=2.5, 
                label='Target Threshold (0.80)', alpha=0.8)
    
    ax1.set_ylabel('R² Score', fontsize=13, fontweight='bold')
    ax1.set_title('Model Performance (R² Score)\nHigher = Better Predictions', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim(0, 1.0)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.8)
    ax1.legend(fontsize=10, loc='lower right')
    ax1.set_facecolor('#F8F9FA')
    
    # Value labels on bars
    for bar, score in zip(bars, r2_scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                f'{score:.4f}', ha='center', fontsize=12, fontweight='bold',
                color='#1A2238')
        
        # Add status indicator
        status = '✓ Excellent' if score > 0.8 else '○ Good' if score > 0.6 else '△ Needs Improvement'
        ax1.text(bar.get_x() + bar.get_width()/2., height/2,
                status, ha='center', fontsize=10, fontweight='bold',
                color='white')
    
    # ========================================================================
    # PANEL 2: Mean Absolute Error (Prediction Accuracy)
    # ========================================================================
    mae_carbon = ml_metrics['carbon_model']['mae']
    mae_delay = ml_metrics['delay_model']['mae']
    
    # Carbon MAE (left axis)
    bar1 = ax2.bar([0], [mae_carbon], color='#06A77D', width=0.35, 
                   alpha=0.85, edgecolor='white', linewidth=2, label='Carbon (kg CO₂)')
    ax2.set_ylabel('Mean Absolute Error\nCarbon Predictions (kg CO₂)', 
                   fontsize=11, fontweight='bold')
    ax2.set_title('Prediction Accuracy (MAE)\nLower = More Accurate', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylim(0, mae_carbon * 1.35)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Carbon\nSavings', 'Optimal\nDelay'])
    ax2.set_facecolor('#F8F9FA')
    
    # Value label
    ax2.text(0, mae_carbon/2, f'{mae_carbon:.1f}\nkg CO₂', 
            ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    
    # Delay MAE (right axis)
    ax2_twin = ax2.twinx()
    bar2 = ax2_twin.bar([1], [mae_delay], color='#2E86AB', width=0.35, 
                        alpha=0.85, edgecolor='white', linewidth=2, label='Delay (hours)')
    ax2_twin.set_ylabel('Mean Absolute Error\nDelay Predictions (hours)', 
                        fontsize=11, fontweight='bold', rotation=270, labelpad=25)
    ax2_twin.set_ylim(0, mae_delay * 1.35)
    
    # Value label
    ax2_twin.text(1, mae_delay/2, f'{mae_delay:.1f}\nhours', 
                 ha='center', va='center', fontsize=13, fontweight='bold', color='white')
    
    # Add interpretation
    ax2.text(0, mae_carbon * 1.15, '±22.7 kg error\nper prediction', 
            ha='center', fontsize=9, style='italic', color='#555')
    ax2_twin.text(1, mae_delay * 1.15, '±3 hour error\nper prediction', 
                 ha='center', fontsize=9, style='italic', color='#555')
    
    # ========================================================================
    # PANEL 3: Feature Importance (Top 5)
    # ========================================================================
    feature_imp = ml_metrics['feature_importance']
    
    # Get top 5 features
    sorted_features = sorted(feature_imp.items(), key=lambda x: x[1], reverse=True)[:5]
    feature_names = [f[0].replace('_', ' ').title() for f in sorted_features]
    importances = [f[1] for f in sorted_features]
    
    # Create horizontal bar chart
    y_pos = np.arange(len(feature_names))
    bars = ax3.barh(y_pos, importances, color='#F4A261', alpha=0.85, 
                   edgecolor='white', linewidth=2)
    
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(feature_names, fontsize=11)
    ax3.set_xlabel('Importance Score (0-1)', fontsize=12, fontweight='bold')
    ax3.set_title('Top 5 Feature Importance\nWhat Drives Carbon Savings?', 
                  fontsize=14, fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, axis='x', linestyle='--', linewidth=0.8)
    ax3.set_facecolor('#F8F9FA')
    ax3.set_xlim(0, max(importances) * 1.15)
    
    # Value labels
    for i, (bar, val) in enumerate(zip(bars, importances)):
        ax3.text(val + 0.01, i, f'{val:.3f} ({val*100:.1f}%)', 
                va='center', fontsize=10, fontweight='bold', color='#1A2238')
    
    # Add insight box
    ax3.text(0.5, -0.8, '💡 Top 2 features account for 95% of predictions', 
            transform=ax3.transAxes, ha='center', fontsize=9, 
            style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # ========================================================================
    # PANEL 4: ML vs Rule-Based Comparison
    # ========================================================================
    jobs = job_results['job_names']
    rule_based = job_results['rule_based_carbon']
    ml_pred = job_results['ml_predicted_carbon']
    
    x = np.arange(len(jobs))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, rule_based, width, label='Rule-Based (Actual)', 
                   color='#2E86AB', alpha=0.85, edgecolor='white', linewidth=2)
    bars2 = ax4.bar(x + width/2, ml_pred, width, label='ML Predicted', 
                   color='#06A77D', alpha=0.85, edgecolor='white', linewidth=2)
    
    ax4.set_xlabel('Training Job', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Carbon Saved (kg CO₂)', fontsize=12, fontweight='bold')
    ax4.set_title('ML Prediction vs Rule-Based Results\nValidation on Test Jobs', 
                  fontsize=14, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels(jobs, fontsize=11)
    ax4.legend(fontsize=11, loc='upper left', framealpha=0.95)
    ax4.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.8)
    ax4.set_facecolor('#F8F9FA')
    
    # Value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold', color='#1A2238')
    
    # Add accuracy annotations
    accuracies = job_results['prediction_accuracy']
    for i, acc in enumerate(accuracies):
        color = '#06A77D' if acc > 85 else '#F4A261' if acc > 75 else '#E63946'
        ax4.text(i, max(rule_based[i], ml_pred[i]) + 5, 
                f'{acc:.1f}% acc', ha='center', fontsize=9, 
                fontweight='bold', color=color)
    
    # Add aggregate stats
    total_rule = sum(rule_based)
    total_ml = sum(ml_pred)
    overall_acc = (1 - abs(total_rule - total_ml) / total_rule) * 100
    
    stats_text = f'Total: Rule={total_rule:.1f} kg | ML={total_ml:.1f} kg | Overall Accuracy: {overall_acc:.1f}%'
    ax4.text(0.5, -0.15, stats_text, transform=ax4.transAxes, 
            ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.4))
    
    # ========================================================================
    # Overall styling
    # ========================================================================
    plt.suptitle('🤖 Machine Learning Model Performance Dashboard', 
                fontsize=18, fontweight='bold', y=0.98, color='#1A2238')
    
    # Add footer
    fig.text(0.5, 0.01, 'Random Forest Regressor | Training: 800 samples | Testing: 200 samples | Production Ready ✓', 
            ha='center', fontsize=9, style='italic', color='#666')
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    
    return fig

# ============================================================================
# BONUS: Individual Charts (if you want them separately)
# ============================================================================

def create_r2_scores_only():
    """Just the R² scores chart"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    models = ['Carbon Savings\nPredictor', 'Optimal Delay\nPredictor']
    r2_scores = [ml_metrics['carbon_model']['r2'], ml_metrics['delay_model']['r2']]
    colors = ['#06A77D', '#2E86AB']
    
    bars = ax.bar(models, r2_scores, color=colors, width=0.5, alpha=0.85, 
                  edgecolor='white', linewidth=2)
    ax.axhline(y=0.8, color='#FF6B35', linestyle='--', linewidth=2, 
               label='Target (0.80)', alpha=0.8)
    
    ax.set_ylabel('R² Score', fontsize=14, fontweight='bold')
    ax.set_title('Model Performance (R² Score)', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=11)
    
    for bar, score in zip(bars, r2_scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                f'{score:.4f}', ha='center', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_comparison_only():
    """Just the ML vs Rule-Based comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    jobs = job_results['job_names']
    rule_based = job_results['rule_based_carbon']
    ml_pred = job_results['ml_predicted_carbon']
    
    x = np.arange(len(jobs))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, rule_based, width, label='Rule-Based (Actual)', 
                   color='#2E86AB', alpha=0.85)
    bars2 = ax.bar(x + width/2, ml_pred, width, label='ML Predicted', 
                   color='#06A77D', alpha=0.85)
    
    ax.set_xlabel('Training Job', fontsize=13, fontweight='bold')
    ax.set_ylabel('Carbon Saved (kg CO₂)', fontsize=13, fontweight='bold')
    ax.set_title('ML Model Predictions vs Actual Results', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(jobs, fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("ML PERFORMANCE VISUALIZATION GENERATOR")
    print("="*70)
    print("\nGenerating charts...\n")
    
    # Create main dashboard
    print("📊 Creating 4-panel ML performance dashboard...")
    fig_dashboard = create_ml_performance_dashboard()
    plt.savefig('ml_performance_dashboard.png', dpi=300, bbox_inches='tight', 
                facecolor='white')
    print("   ✓ Saved: ml_performance_dashboard.png")
    plt.show()
    
    print("\n" + "="*70)
    print("BONUS: Individual Charts")
    print("="*70)
    
    # Create individual charts
    print("\n📈 Creating R² scores chart...")
    fig_r2 = create_r2_scores_only()
    plt.savefig('r2_scores.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✓ Saved: r2_scores.png")
    plt.show()
    
    print("\n📊 Creating comparison chart...")
    fig_comp = create_comparison_only()
    plt.savefig('ml_vs_rulebased.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✓ Saved: ml_vs_rulebased.png")
    plt.show()
    
    print("\n" + "="*70)
    print("✓ ALL CHARTS GENERATED SUCCESSFULLY!")
    print("="*70)
    print("\nFiles created:")
    print("  1. ml_performance_dashboard.png (4-panel - USE THIS FOR SLIDE 7)")
    print("  2. r2_scores.png (individual chart)")
    print("  3. ml_vs_rulebased.png (individual chart)")
    print("\n💡 TIP: Use the 4-panel dashboard for your presentation!")


# ============================================================================
# GOOGLE COLAB INSTRUCTIONS
# ============================================================================
"""
HOW TO RUN IN GOOGLE COLAB:
============================

1. Open Google Colab: https://colab.research.google.com/

2. Create a new notebook

3. Copy this ENTIRE script into a single cell

4. Run the cell (Shift + Enter)

5. Charts will display in the notebook AND save as PNG files

6. Download the PNG files:
   - Click the folder icon on the left
   - Right-click on the .png files
   - Select "Download"

7. Insert into your PowerPoint presentation!

CUSTOMIZATION OPTIONS:
======================

Want different colors? Change these lines:
  - colors_r2 = ['#06A77D', '#2E86AB']  # Green and Blue
  - color='#F4A261'  # Orange for feature importance

Want different data? Edit the ml_metrics and job_results dictionaries at the top!

Want bigger/smaller? Change figsize in subplots():
  - figsize=(14, 10)  # Make larger: (20, 14)
  - figsize=(10, 7)   # Make smaller: (10, 7)
"""

print("\n" + "="*70)
print("📋 DATA SUMMARY")
print("="*70)
print(f"\n🤖 Model Performance:")
print(f"   Carbon Predictor R²: {ml_metrics['carbon_model']['r2']:.4f}")
print(f"   Delay Predictor R²: {ml_metrics['delay_model']['r2']:.4f}")
print(f"\n📊 Prediction Results:")
print(f"   Total Rule-Based: {sum(job_results['rule_based_carbon']):.2f} kg CO₂")
print(f"   Total ML Predicted: {sum(job_results['ml_predicted_carbon']):.2f} kg CO₂")
print(f"   Average Accuracy: {np.mean(job_results['prediction_accuracy']):.1f}%")
print("\n" + "="*70)
