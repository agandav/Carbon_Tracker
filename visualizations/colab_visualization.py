"""
ML Performance Visualization for Google Colab
Run this entire script in a single Colab cell to generate Slide 7 graphs

NO EXTERNAL FILES NEEDED - All data embedded from actual run results
"""

import matplotlib.pyplot as plt
import numpy as np

# Actual metrics from running ml_predictor.py with n_samples=1000, seed=42


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

# Actual job results from test_checkpoint1 + test_checkpoint2 (seed=42)
# Baseline (greedy, hour 6): train_model=0.72 kg, process_data=0.32 kg
# Optimized: train_model=0.41 kg (hour 0), process_data=0.15 kg (hour 3)
job_results = {
    'job_names': ['Model Training', 'Data Processing'],
    'baseline_carbon':   [0.72, 0.32],   # greedy immediate execution
    'optimized_carbon':  [0.41, 0.15],   # batch optimizer result
}


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_ml_performance_dashboard():
    """4-panel ML performance dashboard"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # ------------------------------------------------------------------ #
    # PANEL 1: R2 Scores
    # ------------------------------------------------------------------ #
    models = ['Carbon\nSavings', 'Optimal\nDelay']
    r2_scores = [ml_metrics['carbon_model']['r2'], ml_metrics['delay_model']['r2']]
    colors_r2 = ['#06A77D', '#2E86AB']

    bars = ax1.bar(models, r2_scores, color=colors_r2, width=0.6, alpha=0.85,
                   edgecolor='white', linewidth=2)
    ax1.axhline(y=0.8, color='#FF6B35', linestyle='--', linewidth=2.5,
                label='Target (0.80)', alpha=0.8)
    ax1.set_ylabel('R\u00b2 Score', fontsize=13, fontweight='bold')
    ax1.set_title('Model Performance (R\u00b2)\nHigher = Better',
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim(0, 1.0)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax1.legend(fontsize=10, loc='lower right')
    ax1.set_facecolor('#F8F9FA')

    for bar, score in zip(bars, r2_scores):
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.03,
                 f'{score:.4f}', ha='center', fontsize=12, fontweight='bold')
        status = '\u2713 Good' if score > 0.8 else '\u25cb Moderate'
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() / 2,
                 status, ha='center', fontsize=10, fontweight='bold', color='white')

    # ------------------------------------------------------------------ #
    # PANEL 2: MAE
    # ------------------------------------------------------------------ #
    mae_carbon = ml_metrics['carbon_model']['mae']
    mae_delay = ml_metrics['delay_model']['mae']

    ax2.bar([0], [mae_carbon], color='#06A77D', width=0.35, alpha=0.85,
            edgecolor='white', linewidth=2)
    ax2.set_ylabel('MAE - Carbon (kg CO\u2082)', fontsize=11, fontweight='bold')
    ax2.set_title('Prediction Accuracy (MAE)\nLower = More Accurate',
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylim(0, mae_carbon * 1.35)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Carbon\nSavings', 'Optimal\nDelay'])
    ax2.set_facecolor('#F8F9FA')
    ax2.text(0, mae_carbon / 2, f'\u00b1{mae_carbon:.1f}\nkg CO\u2082',
             ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    ax2_twin = ax2.twinx()
    ax2_twin.bar([1], [mae_delay], color='#2E86AB', width=0.35, alpha=0.85,
                 edgecolor='white', linewidth=2)
    ax2_twin.set_ylabel('MAE - Delay (hours)', fontsize=11, fontweight='bold',
                        rotation=270, labelpad=20)
    ax2_twin.set_ylim(0, mae_delay * 1.35)
    ax2_twin.text(1, mae_delay / 2, f'\u00b1{mae_delay:.1f}h',
                  ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    # ------------------------------------------------------------------ #
    # PANEL 3: Feature Importance (Top 5)
    # ------------------------------------------------------------------ #
    sorted_feats = sorted(ml_metrics['feature_importance'].items(),
                          key=lambda x: x[1], reverse=True)[:5]
    feat_names = [f[0].replace('_', ' ').title() for f in sorted_feats]
    importances = [f[1] for f in sorted_feats]

    ax3.barh(np.arange(len(feat_names)), importances, color='#F4A261',
             alpha=0.85, edgecolor='white', linewidth=2)
    ax3.set_yticks(np.arange(len(feat_names)))
    ax3.set_yticklabels(feat_names, fontsize=11)
    ax3.set_xlabel('Importance Score (0\u20131)', fontsize=12, fontweight='bold')
    ax3.set_title('Top 5 Feature Importance\nWhat Drives Carbon Savings?',
                  fontsize=14, fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, axis='x', linestyle='--')
    ax3.set_facecolor('#F8F9FA')
    ax3.set_xlim(0, max(importances) * 1.2)

    for i, val in enumerate(importances):
        ax3.text(val + 0.005, i, f'{val:.3f} ({val * 100:.1f}%)',
                 va='center', fontsize=10, fontweight='bold')

    # ------------------------------------------------------------------ #
    # PANEL 4: Baseline vs Optimized carbon (actual test results)
    # ------------------------------------------------------------------ #
    jobs = job_results['job_names']
    baseline = job_results['baseline_carbon']
    optimized = job_results['optimized_carbon']

    x = np.arange(len(jobs))
    width = 0.35

    bars1 = ax4.bar(x - width / 2, baseline, width, label='Baseline (Greedy)',
                    color='#E63946', alpha=0.85, edgecolor='white', linewidth=2)
    bars2 = ax4.bar(x + width / 2, optimized, width, label='Optimized (Batch)',
                    color='#06A77D', alpha=0.85, edgecolor='white', linewidth=2)

    ax4.set_xlabel('Training Job', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Carbon Emissions (kg CO\u2082)', fontsize=12, fontweight='bold')
    ax4.set_title('Baseline vs Optimized Carbon\nActual Test Results',
                  fontsize=14, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels(jobs, fontsize=11)
    ax4.legend(fontsize=11, loc='upper right')
    ax4.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax4.set_facecolor('#F8F9FA')

    for bars_group in [bars1, bars2]:
        for bar in bars_group:
            h = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width() / 2., h + 0.008,
                     f'{h:.2f}', ha='center', va='bottom',
                     fontsize=11, fontweight='bold')

    # Savings annotation
    total_base = sum(baseline)
    total_opt = sum(optimized)
    pct = (total_base - total_opt) / total_base * 100
    ax4.text(0.5, -0.18,
             f'Total: Baseline={total_base:.2f} kg  Optimized={total_opt:.2f} kg  '
             f'Reduction={pct:.1f}%',
             transform=ax4.transAxes, ha='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.4))

    # ------------------------------------------------------------------ #
    fig.suptitle('Machine Learning Model Performance Dashboard',
                 fontsize=18, fontweight='bold', y=0.98, color='#1A2238')
    fig.text(0.5, 0.01,
             'Random Forest | 1000 training samples | seed=42 | '
             'Carbon model R\u00b2=0.8456',
             ha='center', fontsize=9, style='italic', color='#666')
    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    return fig


def create_r2_scores_only():
    fig, ax = plt.subplots(figsize=(8, 6))
    models = ['Carbon Savings\nPredictor', 'Optimal Delay\nPredictor']
    r2_scores = [ml_metrics['carbon_model']['r2'], ml_metrics['delay_model']['r2']]
    bars = ax.bar(models, r2_scores, color=['#06A77D', '#2E86AB'],
                  width=0.5, alpha=0.85, edgecolor='white', linewidth=2)
    ax.axhline(y=0.8, color='#FF6B35', linestyle='--', linewidth=2,
               label='Target (0.80)', alpha=0.8)
    ax.set_ylabel('R\u00b2 Score', fontsize=14, fontweight='bold')
    ax.set_title('Model Performance (R\u00b2 Score)', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=11)
    for bar, score in zip(bars, r2_scores):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.03,
                f'{score:.4f}', ha='center', fontsize=13, fontweight='bold')
    plt.tight_layout()
    return fig


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ML PERFORMANCE VISUALIZATION GENERATOR")
    print("=" * 70)

    print("\n Creating 4-panel dashboard...")
    fig_dash = create_ml_performance_dashboard()
    plt.savefig('ml_performance_dashboard.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print("   Saved: ml_performance_dashboard.png")
    plt.show()

    print("\n Creating R\u00b2 scores chart...")
    fig_r2 = create_r2_scores_only()
    plt.savefig('r2_scores.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   Saved: r2_scores.png")
    plt.show()

    print("\n" + "=" * 70)
    print("DATA SUMMARY (actual results, seed=42)")
    print("=" * 70)
    print(f"  Carbon model R\u00b2  : {ml_metrics['carbon_model']['r2']:.4f}")
    print(f"  Delay  model R\u00b2  : {ml_metrics['delay_model']['r2']:.4f}")
    print(f"  Baseline total  : {sum(job_results['baseline_carbon']):.2f} kg CO2")
    print(f"  Optimized total : {sum(job_results['optimized_carbon']):.2f} kg CO2")
    print("=" * 70)