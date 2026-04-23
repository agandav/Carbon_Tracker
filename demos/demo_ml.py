"""
Enhanced Demo Script with ML Predictions
Shows both rule-based and ML-based scheduling recommendations
"""

import sys
import os
import json
import numpy as np
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'core'))

from ml_predictor import SchedulingPredictor
from batch_optimizer import BatchJobOptimizer

np.random.seed(42)


def generate_forecast():
    """24-hour carbon forecast (same logic as test scripts)"""
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


def run_ml_enhanced_demo():
    """Run demo with ML predictions alongside batch optimization"""

    print("=" * 80)
    print("SmartScheduler for Green AI - Demo")
    print("=" * 80)

    # Load or train ML model
    predictor = SchedulingPredictor()
    model_path = os.path.join(PROJECT_ROOT, 'ml_scheduler_model.pkl')
    try:
        predictor.load_model(model_path)
        print(f"   Carbon Model R2: {predictor.metrics['carbon_model']['r2']:.4f}")
        print(f"   Delay  Model R2: {predictor.metrics['delay_model']['r2']:.4f}")
    except Exception:
        print("   Model not found - training now...")
        predictor.train(n_samples=1000)
        predictor.save_model(model_path)

    # Build forecast and optimizer
    forecast = generate_forecast()
    forecast_values = [f['value'] for f in forecast]
    current_intensity = forecast_values[6]  # Jobs arrive at hour 6

    print(f"\n Current carbon intensity (6 AM): {current_intensity:.2f} gCO2/kWh")
    print(f" 24-hour range: {min(forecast_values):.2f} - {max(forecast_values):.2f} gCO2/kWh")

    # Define jobs (same as test scripts)
    jobs = [
        {
            'id': 'train_model',
            'duration_hours': 5.0,
            'power_watts': 300,
            'deadline_hours': 24,
            'energy_kwh': (300 * 5.0) / 1000,
            'priority': 1,
        },
        {
            'id': 'process_data',
            'duration_hours': 3.0,
            'power_watts': 200,
            'deadline_hours': 24,
            'energy_kwh': (200 * 3.0) / 1000,
            'priority': 1,
        },
    ]

    print(f"\n Jobs: {len(jobs)}")
    for j in jobs:
        print(f"   {j['id']}: {j['duration_hours']}h, {j['power_watts']}W, "
              f"deadline {j['deadline_hours']}h")

    
    # Greedy immediate execution at hour 6
    print("\n" + "-" * 80)
    print(" BASELINE (Greedy - immediate execution at hour 6)")
    print("-" * 80)

    forecast_arr = np.array(forecast_values)
    ARRIVAL = 6
    baseline_carbon = 0.0

    for job in jobs:
        start = ARRIVAL
        dur = int(job['duration_hours'])
        energy = job['energy_kwh']
        avg_intensity = float(np.mean(forecast_arr[start:start + dur]))
        carbon = (avg_intensity * energy) / 1000
        baseline_carbon += carbon
        print(f"   {job['id']:<20} start={start:02d}h  "
              f"avg_intensity={avg_intensity:.1f}  carbon={carbon:.4f} kg CO2")

    print(f"\n   Baseline total: {baseline_carbon:.4f} kg CO2")

    # Batch optimizer
    print("\n" + "-" * 80)
    print(" OPTIMIZED (Batch optimization)")
    print("-" * 80)

    optimizer = BatchJobOptimizer(forecast_values)
    opt_results = optimizer.optimize_batch(jobs)

    schedule = {
        jobs[item['job_index']]['id']: float(item['optimized_start_hour'])
        for item in opt_results['job_schedule']
    }

    optimized_carbon = 0.0
    for job_id, start_time in schedule.items():
        job = next(j for j in jobs if j['id'] == job_id)
        start = int(np.round(start_time))
        dur = int(job['duration_hours'])
        energy = job['energy_kwh']
        avg_intensity = float(np.mean(forecast_arr[start:start + dur]))
        carbon = (avg_intensity * energy) / 1000
        optimized_carbon += carbon
        print(f"   {job_id:<20} start={start:02d}h  "
              f"avg_intensity={avg_intensity:.1f}  carbon={carbon:.4f} kg CO2")

    carbon_saved = baseline_carbon - optimized_carbon
    pct_saved = (carbon_saved / baseline_carbon) * 100
    print(f"\n   Optimized total: {optimized_carbon:.4f} kg CO2")
    print(f"   Saved:           {carbon_saved:.4f} kg CO2 ({pct_saved:.1f}%)")



    print("\n" + "-" * 80)
    print(" ML MODEL PREDICTIONS")
    print("-" * 80)

    current_hour = ARRIVAL
    ml_results = []

    for job in jobs:
        features = {
            'duration_hours': job['duration_hours'],
            'energy_kwh': job['energy_kwh'],
            'priority': job['priority'],
            'start_hour': current_hour,
            'day_of_week': datetime.now().weekday(),
            'month': datetime.now().month,
            'current_intensity': current_intensity,
            'is_weekend': 1 if datetime.now().weekday() >= 5 else 0,
            'is_daytime': 1 if 8 <= current_hour <= 18 else 0,
        }
        pred = predictor.predict(features)
        ml_results.append({'job_id': job['id'], 'prediction': pred})

        print(f"\n   Job: {job['id']}")
        print(f"     Predicted carbon saved : "
              f"{pred['predicted_carbon_saved_kg']:.4f} kg CO2")
        print(f"     Predicted optimal delay: "
              f"{pred['predicted_optimal_delay_hours']:.1f} h")
        print(f"     Confidence             : {pred['confidence_carbon']}")

   
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print(f"   Baseline carbon  : {baseline_carbon:.4f} kg CO2")
    print(f"   Optimized carbon : {optimized_carbon:.4f} kg CO2")
    print(f"   Reduction        : {pct_saved:.1f}%")
    print(f"   Optimizer time   : {optimizer.optimization_time:.3f} s")

    # Save results
    results_dir = os.path.join(PROJECT_ROOT, 'results')
    os.makedirs(results_dir, exist_ok=True)
    output = {
        'timestamp': datetime.now().isoformat(),
        'baseline_carbon_kg': round(baseline_carbon, 4),
        'optimized_carbon_kg': round(optimized_carbon, 4),
        'carbon_saved_kg': round(carbon_saved, 4),
        'percent_reduction': round(pct_saved, 1),
        'schedule': {k: int(v) for k, v in schedule.items()},
        'ml_predictions': [
            {'job_id': r['job_id'],
             'predicted_carbon_saved_kg': r['prediction']['predicted_carbon_saved_kg'],
             'predicted_delay_hours': r['prediction']['predicted_optimal_delay_hours']}
            for r in ml_results
        ],
    }
    out_path = os.path.join(results_dir, 'ml_enhanced_results.json')
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n   Results saved to: {out_path}")
    print("=" * 80)

    return output


if __name__ == "__main__":
    run_ml_enhanced_demo()