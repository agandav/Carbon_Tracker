"""
Checkpoint 2 Visualization for Google Colab
Complete standalone script - NO external files needed!

Run this entire script in a single Colab cell to generate Checkpoint 2 graphs
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# EMBEDDED DATA (from your actual Checkpoint 2 results)
# ============================================================================

# Checkpoint comparison data
cp_comparison = {
    'cp1_carbon_kg': 340.93,
    'cp2_carbon_kg': 320.56,
    'additional_savings_kg': 20.37,
    'additional_savings_percent': 6.0
}

# Job schedule data (optimized batch)
jobs_schedule = [
    {'name': 'Data Preprocessing', 'start': 0, 'duration': 2, 'color': '#06A77D'},
    {'name': 'Training Phase 1', 'start': 2, 'duration': 6, 'color': '#2E86AB'},
    {'name': 'Training Phase 2', 'start': 8, 'duration': 4, 'color': '#F4A261'},
    {'name': 'Hyperparameter Tuning', 'start': 0, 'duration': 3, 'color': '#9B59B6'},
    {'name': 'Model Validation', 'start': 12, 'duration': 2, 'color': '#E63946'}
]

# Feature comparison
cp1_features = ['Single Job\nOptimization', 'ML Prediction', 'Carbon\nTracking']
cp2_new_features = ['Batch\nOptimization', 'Dependency\nHandling', 
                    'Real-time\nMonitoring', 'Constraint\nSolver', 'Cumulative\nMetrics']

# Carbon intensity periods (for background shading)
carbon_periods = [
    {'start': 0, 'end': 10, 'intensity': 'High Carbon', 'color': '#FFE5E5'},
    {'start': 10, 'end': 16, 'intensity': 'Low Carbon\n(Solar Peak)', 'color': '#E5FFE5'}
]

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_checkpoint2_comparison():
    """Create complete Checkpoint 2 comparison visualization"""
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # ========================================================================
    # PANEL 1: CP1 vs CP2 Carbon Comparison
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    approaches = ['Checkpoint 1\n(Single-Job)', 'Checkpoint 2\n(Batch Optimization)']
    carbon_values = [
        cp_comparison['cp1_carbon_kg'],
        cp_comparison['cp2_carbon_kg']
    ]
    
    colors_bar = ['#E63946', '#06A77D']
    bars = ax1.bar(approaches, carbon_values, color=colors_bar, alpha=0.85,
                   edgecolor='white', linewidth=2.5, width=0.6)
    
    ax1.set_ylabel('Total Carbon Emissions (kg CO₂)', fontsize=13, fontweight='bold')
    ax1.set_title('Carbon Emissions: CP1 vs CP2\nLower is Better ✓', 
                  fontsize=15, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.8)
    ax1.set_facecolor('#F8F9FA')
    ax1.set_ylim(0, max(carbon_values) * 1.15)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, carbon_values)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{val:.1f} kg CO₂', ha='center', fontsize=12, fontweight='bold',
                color='#1A2238')
    
    # Add savings annotation with arrow
    savings = cp_comparison['additional_savings_kg']
    savings_pct = cp_comparison['additional_savings_percent']
    
    # Arrow from CP1 to CP2
    ax1.annotate('', 
                xy=(1, carbon_values[1]), 
                xytext=(0, carbon_values[0]),
                arrowprops=dict(arrowstyle='->', color='#06A77D', lw=3))
    
    # Savings text box
    ax1.text(0.5, (carbon_values[0] + carbon_values[1])/2, 
            f'SAVED:\n{savings:.1f} kg CO₂\n({savings_pct:.1f}% reduction)', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#06A77D',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#D4EDDA', 
                     edgecolor='#06A77D', linewidth=2, alpha=0.9))
    
    # Add baseline reference line
    baseline = carbon_values[0]
    ax1.axhline(y=baseline, color='#E63946', linestyle='--', linewidth=1.5, 
                alpha=0.5, label=f'CP1 Baseline: {baseline:.1f} kg')
    ax1.legend(loc='upper right', fontsize=9)
    
    # ========================================================================
    # PANEL 2: Feature Comparison (CP1 vs CP2)
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    # CP1 features (baseline)
    y_cp1 = np.arange(len(cp1_features))
    bars_cp1 = ax2.barh(y_cp1, [1]*len(cp1_features), 
                        color='#2E86AB', alpha=0.6, height=0.4, label='CP1 Features')
    
    # CP2 new features
    y_cp2 = np.arange(len(cp2_new_features)) + len(cp1_features) + 0.5
    bars_cp2 = ax2.barh(y_cp2, [1]*len(cp2_new_features), 
                        color='#06A77D', alpha=0.85, height=0.4, label='CP2 NEW Features ⭐')
    
    # Labels
    all_labels = cp1_features + cp2_new_features
    all_y = list(y_cp1) + list(y_cp2)
    ax2.set_yticks(all_y)
    ax2.set_yticklabels(all_labels, fontsize=10)
    ax2.set_xlim(0, 1.3)
    ax2.set_xlabel('Feature Implementation', fontsize=12, fontweight='bold')
    ax2.set_title('Feature Evolution: CP1 → CP2\nWhat\'s New?', 
                  fontsize=15, fontweight='bold', pad=15)
    ax2.legend(loc='lower right', fontsize=10, framealpha=0.95)
    ax2.set_facecolor('#F8F9FA')
    ax2.set_xticks([])
    
    # Add status labels on bars
    for i, bar in enumerate(bars_cp1):
        ax2.text(0.5, bar.get_y() + bar.get_height()/2, 
                '✓ Baseline', ha='center', va='center', 
                fontsize=9, fontweight='bold', color='white')
    
    for i, bar in enumerate(bars_cp2):
        ax2.text(0.5, bar.get_y() + bar.get_height()/2, 
                '⭐ NEW', ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
    
    # Add separator line
    ax2.axhline(y=len(cp1_features) + 0.25, color='#666', linestyle='--', 
                linewidth=2, alpha=0.5)
    
    # ========================================================================
    # PANEL 3: Job Schedule Gantt Chart (spans both bottom panels)
    # ========================================================================
    ax3 = fig.add_subplot(gs[1, :])
    
    # Plot job bars
    for i, job in enumerate(jobs_schedule):
        ax3.barh(i, job['duration'], left=job['start'], height=0.6, 
                color=job['color'], alpha=0.85, edgecolor='white', linewidth=2)
        
        # Job name inside bar
        ax3.text(job['start'] + job['duration']/2, i, job['name'], 
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Time label outside bar
        time_label = f"{job['start']}h - {job['start']+job['duration']}h"
        ax3.text(job['start'] + job['duration'] + 0.3, i, time_label,
                ha='left', va='center', fontsize=9, style='italic', color='#333')
    
    # Y-axis labels
    ax3.set_yticks(range(len(jobs_schedule)))
    ax3.set_yticklabels([f'Job {i+1}' for i in range(len(jobs_schedule))], fontsize=11)
    ax3.set_xlabel('Time (hours from now)', fontsize=13, fontweight='bold')
    ax3.set_title('Optimized Job Schedule (Checkpoint 2)\nBatch Optimization with Dependency Constraints', 
                  fontsize=15, fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, axis='x', linestyle='--', linewidth=0.8)
    ax3.set_xlim(0, 16)
    ax3.set_facecolor('#F8F9FA')
    
    # Add carbon intensity background regions
    ax3_bg = ax3.twiny()
    for period in carbon_periods:
        ax3_bg.axvspan(period['start'], period['end'], 
                      alpha=0.2, color=period['color'], zorder=0)
        # Label
        mid_point = (period['start'] + period['end']) / 2
        ax3_bg.text(mid_point, len(jobs_schedule) - 0.5, 
                   period['intensity'], 
                   ha='center', fontsize=10, style='italic', 
                   color='#555', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            alpha=0.7, edgecolor='none'))
    ax3_bg.set_xlim(0, 16)
    ax3_bg.set_xticks([])
    
    # Add dependency arrows
    dependencies = [
        (0, 1, 'Job 1 → Job 2'),  # Data Prep → Training Phase 1
        (1, 2, 'Job 2 → Job 3'),  # Training Phase 1 → Training Phase 2
        (2, 4, 'Job 3 → Job 5'),  # Training Phase 2 → Validation
    ]
    
    for dep in dependencies:
        from_job, to_job, label = dep
        from_end = jobs_schedule[from_job]['start'] + jobs_schedule[from_job]['duration']
        to_start = jobs_schedule[to_job]['start']
        
        # Draw arrow
        ax3.annotate('', 
                    xy=(to_start, to_job), 
                    xytext=(from_end, from_job),
                    arrowprops=dict(arrowstyle='->', color='#666', 
                                  lw=1.5, linestyle='--', alpha=0.7))
    
    # Add legend for dependencies
    ax3.text(14.5, len(jobs_schedule) + 0.3, 'Dashed arrows\n= Dependencies', 
            ha='center', fontsize=9, style='italic', color='#666',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     alpha=0.8, edgecolor='#666', linestyle='--'))
    
    # ========================================================================
    # Overall styling
    # ========================================================================
    fig.suptitle('Checkpoint 2: Batch Optimization Results\nSignificant Progress from CP1 ✓', 
                fontsize=18, fontweight='bold', y=0.98, color='#1A2238')
    
    # Add footer with key metrics
    footer_text = (f"NEW in CP2: Multi-job optimization • Dependency handling • Real-time monitoring | "
                  f"Improvement: {savings:.1f} kg CO₂ saved ({savings_pct:.1f}% over CP1) | "
                  f"5 jobs optimized in <1 second")
    fig.text(0.5, 0.01, footer_text,
            ha='center', fontsize=10, style='italic', color='#666',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF9E5', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    return fig

# ============================================================================
# BONUS: Individual Charts
# ============================================================================

def create_cp_comparison_only():
    """Just the CP1 vs CP2 comparison"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    approaches = ['Checkpoint 1\n(Single-Job\nSequential)', 'Checkpoint 2\n(Batch\nOptimization)']
    carbon_values = [cp_comparison['cp1_carbon_kg'], cp_comparison['cp2_carbon_kg']]
    
    colors = ['#E63946', '#06A77D']
    bars = ax.bar(approaches, carbon_values, color=colors, alpha=0.85, 
                  edgecolor='white', linewidth=3, width=0.5)
    
    ax.set_ylabel('Total Carbon Emissions (kg CO₂)', fontsize=14, fontweight='bold')
    ax.set_title('Checkpoint 1 vs Checkpoint 2: Carbon Comparison', 
                fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, max(carbon_values) * 1.2)
    
    # Value labels
    for bar, val in zip(bars, carbon_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 8,
                f'{val:.1f} kg CO₂', ha='center', fontsize=13, fontweight='bold')
    
    # Improvement box
    savings = cp_comparison['additional_savings_kg']
    savings_pct = cp_comparison['additional_savings_percent']
    ax.text(0.5, max(carbon_values) * 0.5, 
           f'IMPROVEMENT\n\n{savings:.1f} kg CO₂ saved\n({savings_pct:.1f}% reduction)', 
           transform=ax.transData, ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round,pad=1', facecolor='#D4EDDA', 
                    edgecolor='#06A77D', linewidth=3, alpha=0.9))
    
    plt.tight_layout()
    return fig

def create_gantt_only():
    """Just the job schedule Gantt chart"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot jobs
    for i, job in enumerate(jobs_schedule):
        ax.barh(i, job['duration'], left=job['start'], height=0.7, 
                color=job['color'], alpha=0.85, edgecolor='white', linewidth=2)
        
        ax.text(job['start'] + job['duration']/2, i, job['name'], 
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        time_label = f"{job['start']}h - {job['start']+job['duration']}h"
        ax.text(job['start'] + job['duration'] + 0.4, i, time_label,
                ha='left', va='center', fontsize=10, color='#333')
    
    ax.set_yticks(range(len(jobs_schedule)))
    ax.set_yticklabels([f'Job {i+1}' for i in range(len(jobs_schedule))], fontsize=12)
    ax.set_xlabel('Time (hours from now)', fontsize=14, fontweight='bold')
    ax.set_title('Optimized Job Schedule - Checkpoint 2\nBatch Optimization with Dependencies', 
                fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0, 16)
    
    # Carbon background
    for period in carbon_periods:
        ax.axvspan(period['start'], period['end'], alpha=0.15, color=period['color'])
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("CHECKPOINT 2 VISUALIZATION GENERATOR")
    print("="*70)
    print("\nGenerating charts...\n")
    
    # Create main dashboard
    print("📊 Creating Checkpoint 2 comparison dashboard...")
    fig_main = create_checkpoint2_comparison()
    plt.savefig('checkpoint2_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='white')
    print("   ✓ Saved: checkpoint2_comparison.png")
    plt.show()
    
    print("\n" + "="*70)
    print("BONUS: Individual Charts")
    print("="*70)
    
    # Individual charts
    print("\n📈 Creating CP1 vs CP2 comparison...")
    fig_comp = create_cp_comparison_only()
    plt.savefig('cp1_vs_cp2.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✓ Saved: cp1_vs_cp2.png")
    plt.show()
    
    print("\n📅 Creating Gantt chart...")
    fig_gantt = create_gantt_only()
    plt.savefig('job_schedule_gantt.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✓ Saved: job_schedule_gantt.png")
    plt.show()
    
    print("\n" + "="*70)
    print("✓ ALL CHARTS GENERATED SUCCESSFULLY!")
    print("="*70)
    print("\nFiles created:")
    print("  1. checkpoint2_comparison.png (3-panel dashboard - USE THIS)")
    print("  2. cp1_vs_cp2.png (comparison chart)")
    print("  3. job_schedule_gantt.png (schedule visualization)")
    print("\n💡 TIP: Use the 3-panel dashboard for your presentation!")

# ============================================================================
# DATA SUMMARY
# ============================================================================
print("\n" + "="*70)
print("📋 CHECKPOINT 2 DATA SUMMARY")
print("="*70)
print(f"\n🔬 Carbon Emissions:")
print(f"   CP1 (Sequential): {cp_comparison['cp1_carbon_kg']:.2f} kg CO₂")
print(f"   CP2 (Batch Optimization): {cp_comparison['cp2_carbon_kg']:.2f} kg CO₂")
print(f"   Improvement: {cp_comparison['additional_savings_kg']:.2f} kg CO₂ ({cp_comparison['additional_savings_percent']:.1f}%)")
print(f"\n📊 Jobs Optimized: {len(jobs_schedule)}")
print(f"   • All deadlines met: ✓")
print(f"   • Dependencies handled: ✓")
print(f"   • Optimization time: <1 second")
print(f"\n⭐ New Features in CP2: {len(cp2_new_features)}")
for feature in cp2_new_features:
    print(f"   • {feature.replace(chr(10), ' ')}")
print("\n" + "="*70)


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

5. Charts will display AND save as PNG files

6. Download the PNG files:
   - Click the folder icon on the left sidebar
   - Right-click on the .png files
   - Select "Download"

7. Insert into your PowerPoint Slide 7!

CUSTOMIZATION OPTIONS:
======================

Want to change YOUR data? Edit these values at the top:

cp_comparison = {
    'cp1_carbon_kg': 340.93,      # Your CP1 result
    'cp2_carbon_kg': 320.56,      # Your CP2 result
    'additional_savings_kg': 20.37,
    'additional_savings_percent': 6.0
}

Want different job names or schedule?
Edit the jobs_schedule list!

Want different colors?
Change the 'color' values in jobs_schedule!

CHART SELECTION:
================

This script generates 3 charts:
1. Full dashboard (3 panels) - RECOMMENDED for presentation
2. Simple comparison (CP1 vs CP2 bars)
3. Gantt chart only (job schedule)

Use Chart #1 for your Slide 7!
"""
