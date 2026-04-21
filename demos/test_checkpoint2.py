"""
Checkpoint 2 Test: Batch Optimization with Real-time Monitoring
Multi-job optimization using scipy SLSQP
"""
import numpy as np
import sys
import os
import json

# Add core to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
CP1_RESULTS_PATH = os.path.join(RESULTS_DIR, 'checkpoint1_results.json')
CP2_RESULTS_PATH = os.path.join(RESULTS_DIR, 'checkpoint2_results.json')

from core.batch_optimizer import BatchJobOptimizer
from core.realtime_monitor import RealTimeMonitor

np.random.seed(42)  # FIXED SEED FOR CONSISTENT RESULTS

def generate_forecast():
    """24-hour carbon forecast"""
    forecast = []
    for hour in range(24):
        base = 350
        if 6 <= hour <= 9 or 17 <= hour <= 20:
            intensity = base + np.random.uniform(150, 200)
        elif 22 <= hour or hour <= 5:
            intensity = base + np.random.uniform(-100, -50)
        else:
            intensity = base + np.random.uniform(-50, 50)
        forecast.append({
            'datetime': f'2026-04-12T{hour:02d}:00:00Z',
            'value': round(intensity, 2)
        })
    return forecast

def test_checkpoint2():
    """Test CP2: Batch optimization"""
    print("=" * 60)
    print("CHECKPOINT 2: BATCH OPTIMIZATION + REAL-TIME MONITORING")
    print("=" * 60)
    
    # Get forecast
    forecast = generate_forecast()
    current_intensity = forecast[0]['value']
    
    print(f"\n Current Carbon Intensity: {current_intensity:.2f} gCO2/kWh")
    print(f"24-hour Forecast Range: {min(f['value'] for f in forecast):.2f} - {max(f['value'] for f in forecast):.2f} gCO2/kWh")
    
    # Define 2 jobs with flexible deadlines - realistic for daily batch processing
    # Total: 8 hours of work, 24 hour window - can easily avoid all peaks
    jobs = [
        {'id': 'train_model', 'duration_hours': 5.0, 'power_watts': 300, 'deadline_hours': 24, 
         'energy_kwh': (300 * 5.0) / 1000, 'priority': 1},
        {'id': 'process_data', 'duration_hours': 3.0, 'power_watts': 200, 'deadline_hours': 24,
         'energy_kwh': (200 * 3.0) / 1000, 'priority': 1}
    ]
    
    print(f"\n Jobs to Schedule: {len(jobs)}")
    for job in jobs:
        print(f"   - {job['id']}: {job['duration_hours']}h, {job['power_watts']}W, deadline {job['deadline_hours']}h")
    
    # Initialize optimizer and monitor
    optimizer = BatchJobOptimizer([f['value'] for f in forecast])
    monitor = RealTimeMonitor()
    
    # Optimize
    print("\n CHECKPOINT 2 STRATEGY: Batch Optimization (scipy SLSQP)")
    print("-" * 60)
    
    import time
    start_time = time.time()
    optimization_results = optimizer.optimize_batch(jobs)
    opt_time = time.time() - start_time
    
    # Build simple job_id -> start_hour schedule from optimizer output
    schedule = {
        jobs[item['job_index']]['id']: float(item['optimized_start_hour'])
        for item in optimization_results['job_schedule']
    }
    
    # Calculate total carbon using SAME method as optimizer (simple averaging)
    total_carbon_cp2 = 0
    
    for job_id, start_time in schedule.items():
        job = next(j for j in jobs if j['id'] == job_id)
        start_hour = int(np.round(start_time))
        duration = int(job['duration_hours'])
        energy_kwh = (job['power_watts'] * job['duration_hours']) / 1000
        
        # Simple average over integer hours
        forecast_array = np.array([f['value'] for f in forecast])
        intensity_sum = 0
        for h_offset in range(duration):
            hour_idx = start_hour + h_offset
            if hour_idx < len(forecast):
                intensity_sum += forecast_array[hour_idx]
        
        avg_intensity = intensity_sum / duration if duration > 0 else 0
        carbon_kg = (avg_intensity * energy_kwh) / 1000
        total_carbon_cp2 += carbon_kg
        
        print(f"   {job_id:<25}   Hour {start_hour}: {carbon_kg:.2f} kg CO2")
    
    print(f"\n{'=' * 60}")
    print(f"CHECKPOINT 2 TOTAL CARBON EMISSIONS: {total_carbon_cp2:.2f} kg CO2")
    print(f"{'=' * 60}")
    
    # Calculate improvement over CP1
    # Load CP1 results
    try:
        with open(CP1_RESULTS_PATH, 'r') as f:
            cp1_data = json.load(f)
            carbon_cp1 = cp1_data['total_carbon_kg']
            
        carbon_saved = carbon_cp1 - total_carbon_cp2
        percent_improvement = (carbon_saved / carbon_cp1) * 100
        
        print(f"\n IMPROVEMENT OVER CHECKPOINT 1:")
        print(f"   Carbon Saved: {carbon_saved:.2f} kg CO2")
        print(f"   Improvement: {percent_improvement:.1f}%")
    except FileNotFoundError:
        print("\n  Run test_checkpoint1.py first to compare results")
    
    # Save results
    results = {
        'checkpoint': 2,
        'strategy': 'batch_optimization',
        'total_carbon_kg': round(total_carbon_cp2, 2),
        'num_jobs': len(jobs),
        'schedule': {k: int(v) for k, v in schedule.items()},
        'optimization_time_seconds': round(opt_time, 3)
    }
    
    if 'carbon_cp1' in locals():
        results['improvement_over_cp1'] = {
            'carbon_saved_kg': round(carbon_saved, 2),
            'percent_improvement': round(percent_improvement, 1)
        }
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(CP2_RESULTS_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n Results saved to {CP2_RESULTS_PATH}")
    print(f" Optimization completed in {opt_time:.3f} seconds")
    
    return total_carbon_cp2

if __name__ == '__main__':
    carbon_cp2 = test_checkpoint2()