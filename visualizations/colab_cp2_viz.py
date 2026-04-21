"""
Checkpoint 2 Visualization for Google Colab
Complete standalone script - NO external files needed!

Run this entire script in a single Colab cell to generate Checkpoint 2 graphs
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# ACTUAL DATA from test_checkpoint1.py and test_checkpoint2.py results
# ============================================================================

cp_comparison = {
    'cp1_carbon_kg': 1.04,       # from results/checkpoint1_results.json
    'cp2_carbon_kg': 0.57,       # from results/checkpoint2_results.json
    'additional_savings_kg': 0.47,
    'additional_savings_percent': 44.9
}

# Actual 2-job schedule from checkpoint2_results.json
# train_model starts hour 0, process_data starts hour 3
jobs_schedule = [
    {'name': 'Model Training (5h)',   'start': 0,  'duration': 5, 'color': '#2E86AB'},
    {'name': 'Data Processing (3h)',  'start': 3,  'duration': 3, 'color': '#06A77D'},
]

# Baseline: both jobs start at hour 6 (greedy)
jobs_baseline = [
    {'name': 'Model Training (5h)',  'start': 6, 'duration': 5, 'color': '#E63946'},
    {'name': 'Data Processing (3h)', 'start': 6, 'duration': 3, 'color': '#F4A261'},
]

# Carbon intensity profile (same seed=42 pattern used in test scripts)
# Hour 0-5: low (night), 6-9: high peak, 10-16: medium, 17-20: high peak, 21-23: low
carbon_periods = [
    {'start': 0,  'end': 6,  'label': 'Low Carbon\n(Night)',  'color': '#E5FFE5'},
    {'start': 6,  'end': 10, 'label': 'High Carbon\n(Morning Peak)', 'color': '#FFE5E5'},
    {'start': 17, 'end': 21, 'label': 'High Carbon\n(Evening Peak)', 'color': '#FFE5E5'},
]

cp1_features = ['ML Carbon\nPrediction', 'Single-Job\nScheduling', 'Greedy\nBaseline']
cp2_new_features = ['Batch\nOptimization', 'Dependency\nHandling',
                    'Real-time\nMonitoring', 'Constraint\nSolver', 'Penalty-based\nFeasibility']


# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def create_checkpoint2_comparison():
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)

    # ------------------------------------------------------------------ #
    # PANEL 1: CP1 vs CP2 Carbon Bar Chart
    # ------------------------------------------------------------------ #
    ax1 = fig.add_subplot(gs[0, 0])

    approaches = ['Checkpoint 1\n(Greedy)', 'Checkpoint 2\n(Batch Opt.)']
    carbon_values = [cp_comparison['cp1_carbon_kg'], cp_comparison['cp2_carbon_kg']]
    colors_bar = ['#E63946', '#06A77D']

    bars = ax1.bar(approaches, carbon_values, color=colors_bar, alpha=0.85,
                   edgecolor='white', linewidth=2.5, width=0.6)

    ax1.set_ylabel('Total Carbon Emissions (kg CO\u2082)', fontsize=13, fontweight='bold')
    ax1.set_title('Carbon Emissions: CP1 vs CP2\nLower is Better \u2713',
                  fontsize=15, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax1.set_facecolor('#F8F9FA')
    ax1.set_ylim(0, max(carbon_values) * 1.3)

    for bar, val in zip(bars, carbon_values):
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.02,
                 f'{val:.2f} kg CO\u2082', ha='center', fontsize=12, fontweight='bold')

    savings = cp_comparison['additional_savings_kg']
    pct = cp_comparison['additional_savings_percent']
    ax1.text(0.5, (carbon_values[0] + carbon_values[1]) / 2,
             f'SAVED:\n{savings:.2f} kg CO\u2082\n({pct:.1f}% reduction)',
             ha='center', va='center', fontsize=11, fontweight='bold', color='#06A77D',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#D4EDDA',
                       edgecolor='#06A77D', linewidth=2, alpha=0.9))

    ax1.axhline(y=carbon_values[0], color='#E63946', linestyle='--',
                linewidth=1.5, alpha=0.5, label=f'CP1 baseline: {carbon_values[0]:.2f} kg')
    ax1.legend(loc='upper right', fontsize=9)

    # ------------------------------------------------------------------ #
    # PANEL 2: Feature Evolution CP1 -> CP2
    # ------------------------------------------------------------------ #
    ax2 = fig.add_subplot(gs[0, 1])

    y_cp1 = np.arange(len(cp1_features))
    y_cp2 = np.arange(len(cp2_new_features)) + len(cp1_features) + 0.5

    ax2.barh(y_cp1, [1] * len(cp1_features), color='#2E86AB',
             alpha=0.6, height=0.4, label='CP1 Features')
    bars_new = ax2.barh(y_cp2, [1] * len(cp2_new_features), color='#06A77D',
                        alpha=0.85, height=0.4, label='CP2 NEW Features \u2b50')

    all_labels = cp1_features + cp2_new_features
    all_y = list(y_cp1) + list(y_cp2)
    ax2.set_yticks(all_y)
    ax2.set_yticklabels(all_labels, fontsize=10)
    ax2.set_xlim(0, 1.3)
    ax2.set_title('Feature Evolution: CP1 \u2192 CP2', fontsize=15, fontweight='bold', pad=15)
    ax2.legend(loc='lower right', fontsize=10)
    ax2.set_facecolor('#F8F9FA')
    ax2.set_xticks([])
    ax2.axhline(y=len(cp1_features) + 0.25, color='#666', linestyle='--',
                linewidth=2, alpha=0.5)

    # ------------------------------------------------------------------ #
    # PANEL 3: Gantt - spans bottom row
    # ------------------------------------------------------------------ #
    ax3 = fig.add_subplot(gs[1, :])

    # Optimized schedule (green)
    for i, job in enumerate(jobs_schedule):
        ax3.barh(i + 0.2, job['duration'], left=job['start'], height=0.35,
                 color=job['color'], alpha=0.9, edgecolor='white', linewidth=2,
                 label='Optimized' if i == 0 else '')
        ax3.text(job['start'] + job['duration'] / 2, i + 0.2,
                 job['name'], ha='center', va='center',
                 fontsize=10, fontweight='bold', color='white')
        ax3.text(job['start'] + job['duration'] + 0.3, i + 0.2,
                 f"{job['start']}h\u2192{job['start'] + job['duration']}h",
                 ha='left', va='center', fontsize=9, color='#333')

    # Baseline schedule (red/orange)
    for i, job in enumerate(jobs_baseline):
        ax3.barh(i - 0.2, job['duration'], left=job['start'], height=0.35,
                 color=job['color'], alpha=0.6, edgecolor='white', linewidth=2,
                 label='Baseline (Greedy)' if i == 0 else '')

    ax3.set_yticks(range(len(jobs_schedule)))
    ax3.set_yticklabels([f'Job {i + 1}' for i in range(len(jobs_schedule))], fontsize=11)
    ax3.set_xlabel('Hour of Day', fontsize=13, fontweight='bold')
    ax3.set_title('Optimized vs Baseline Schedule (Checkpoint 2)\n'
                  'Green = optimized  |  Faded = greedy baseline',
                  fontsize=14, fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, axis='x', linestyle='--')
    ax3.set_xlim(0, 24)
    ax3.set_facecolor('#F8F9FA')

    # Background shading for high/low carbon periods
    for period in carbon_periods:
        ax3.axvspan(period['start'], period['end'], alpha=0.12,
                    color='#FFB3B3' if 'High' in period['label'] else '#B3FFB3')

    ax3.legend(loc='upper right', fontsize=10)

    # ------------------------------------------------------------------ #
    # Overall
    # ------------------------------------------------------------------ #
    fig.suptitle('Checkpoint 2: Batch Optimization Results',
                 fontsize=18, fontweight='bold', y=0.98, color='#1A2238')

    footer = (f"Actual results | CP1: {cp_comparison['cp1_carbon_kg']:.2f} kg  "
              f"CP2: {cp_comparison['cp2_carbon_kg']:.2f} kg  |  "
              f"{cp_comparison['additional_savings_percent']:.1f}% reduction  |  "
              f"Optimization: <1 second")
    fig.text(0.5, 0.01, footer, ha='center', fontsize=10, style='italic',
             color='#666', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9E5', alpha=0.8))

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig


# ============================================================================
# INDIVIDUAL CHARTS
# ============================================================================

def create_cp_comparison_only():
    fig, ax = plt.subplots(figsize=(8, 6))
    approaches = ['Checkpoint 1\n(Greedy)', 'Checkpoint 2\n(Optimized)']
    carbon_values = [cp_comparison['cp1_carbon_kg'], cp_comparison['cp2_carbon_kg']]
    bars = ax.bar(approaches, carbon_values, color=['#E63946', '#06A77D'],
                  alpha=0.85, edgecolor='white', linewidth=3, width=0.5)
    ax.set_ylabel('Total Carbon Emissions (kg CO\u2082)', fontsize=14, fontweight='bold')
    ax.set_title('CP1 vs CP2: Carbon Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, max(carbon_values) * 1.35)
    for bar, val in zip(bars, carbon_values):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.02,
                f'{val:.2f} kg', ha='center', fontsize=13, fontweight='bold')
    ax.text(0.5, sum(carbon_values) / 2,
            f'{cp_comparison["additional_savings_kg"]:.2f} kg saved\n'
            f'({cp_comparison["additional_savings_percent"]:.1f}% reduction)',
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#D4EDDA',
                      edgecolor='#06A77D', linewidth=2, alpha=0.9))
    plt.tight_layout()
    return fig


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CHECKPOINT 2 VISUALIZATION GENERATOR")
    print("=" * 70)

    print("\n Creating 2-panel dashboard...")
    fig_main = create_checkpoint2_comparison()
    plt.savefig('checkpoint2_comparison.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print("   Saved: checkpoint2_comparison.png")
    plt.show()

    print("\n Creating comparison-only chart...")
    fig_comp = create_cp_comparison_only()
    plt.savefig('cp1_vs_cp2.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   Saved: cp1_vs_cp2.png")
    plt.show()

    print("\n" + "=" * 70)
    print("DATA SUMMARY (actual results)")
    print("=" * 70)
    print(f"  CP1 baseline : {cp_comparison['cp1_carbon_kg']:.2f} kg CO2")
    print(f"  CP2 optimized: {cp_comparison['cp2_carbon_kg']:.2f} kg CO2")
    print(f"  Saved        : {cp_comparison['additional_savings_kg']:.2f} kg CO2"
          f" ({cp_comparison['additional_savings_percent']:.1f}%)")
    print(f"  Schedule     : train_model starts hour 0, process_data starts hour 3")
    print("=" * 70)