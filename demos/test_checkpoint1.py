"""
Checkpoint 1 Test: ML Carbon Prediction Only
Greedy single-job scheduling (immediate execution)
"""
import numpy as np
import sys
import os

# Add core to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'core'))
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')
CP1_RESULTS_PATH = os.path.join(RESULTS_DIR, 'checkpoint1_results.json')

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

def test_checkpoint1():
    """Test CP1: Greedy immediate execution"""
    print("=" * 60)
    print("CHECKPOINT 1: ML CARBON PREDICTION (GREEDY SCHEDULING)")
    print("=" * 60)
    
    # Get forecast
    forecast = generate_forecast()
    current_intensity = forecast[0]['value']
    
    print(f"\n Current Carbon Intensity: {current_intensity:.2f} gCO2/kWh")
    print(f"24-hour Forecast Range: {min(f['value'] for f in forecast):.2f} - {max(f['value'] for f in forecast):.2f} gCO2/kWh")
    
    # Define 2 jobs with flexible deadlines - realistic for daily batch processing
    # Total: 8 hours of work, 24 hour window - can easily avoid all peaks
    jobs = [
        {'id': 'train_model', 'duration': 5.0, 'power': 300, 'deadline': 24},
        {'id': 'process_data', 'duration': 3.0, 'power': 200, 'deadline': 24}
    ]
    
    print(f"\n Jobs to Schedule: {len(jobs)}")
    for job in jobs:
        print(f"   - {job['id']}: {job['duration']}h, {job['power']}W, deadline {job['deadline']}h")
    
    # CHECKPOINT 1 APPROACH: Jobs arrive at hour 6 (business hours), run immediately (greedy)
    # This represents naive scheduling that doesn't consider carbon
    ARRIVAL_HOUR = 6
    
    total_carbon_cp1 = 0
    print(f"\n CHECKPOINT 1 STRATEGY: Jobs arrive at hour {ARRIVAL_HOUR}, execute immediately (greedy)")
    print("-" * 60)
    
    forecast_array = np.array([f['value'] for f in forecast])
    
    for job in jobs:
        # Execute immediately when job arrives (hour 6)
        start_hour = ARRIVAL_HOUR
        duration = int(job['duration'])
        energy_kwh = (job['power'] * duration) / 1000
        
        # Simple average over integer hours
        intensity_sum = 0
        for h_offset in range(duration):
            hour_idx = start_hour + h_offset
            if hour_idx < len(forecast):
                intensity_sum += forecast_array[hour_idx]
        
        avg_intensity = intensity_sum / duration if duration > 0 else 0
        carbon_kg = (avg_intensity * energy_kwh) / 1000
        total_carbon_cp1 += carbon_kg
        
        print(f"   {job['id']:<25}   Hour {start_hour}: {carbon_kg:.2f} kg CO2")
    
    print(f"\n{'=' * 60}")
    print(f"CHECKPOINT 1 TOTAL CARBON EMISSIONS: {total_carbon_cp1:.2f} kg CO2")
    print(f"{'=' * 60}")
    
    # Save results
    results = {
        'checkpoint': 1,
        'strategy': 'greedy_immediate',
        'total_carbon_kg': round(total_carbon_cp1, 2),
        'num_jobs': len(jobs),
        'current_intensity': round(current_intensity, 2)
    }
    
    import json
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(CP1_RESULTS_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n Results saved to {CP1_RESULTS_PATH}")
    
    return total_carbon_cp1

if __name__ == '__main__':
    carbon_cp1 = test_checkpoint1()