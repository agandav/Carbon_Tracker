"""
Enhanced Demo Script with ML Predictions
Shows both rule-based and ML-based scheduling recommendations
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

# Note: scheduler.py doesn't exist, so we'll skip it for now
from ml_predictor import SchedulingPredictor
from datetime import datetime, timedelta
import json

def run_ml_enhanced_demo():
    """Run demo with ML predictions"""
    
    print("=" * 80)
    print("SmartScheduler for Green AI - ML-Enhanced Demo")
    print("=" * 80)
    print()
    
    # Load trained ML model
    print("🤖 Loading ML Prediction Model...")
    try:
        predictor = SchedulingPredictor()
        predictor.load_model('/home/claude/ml_scheduler_model.pkl')
        print("   ✓ ML model loaded successfully")
        print(f"   ✓ Carbon Model R² Score: {predictor.metrics['carbon_model']['r2']:.4f}")
        print(f"   ✓ Delay Model R² Score: {predictor.metrics['delay_model']['r2']:.4f}")
    except Exception as e:
        print(f"   ⚠ Could not load model: {e}")
        print("   Training new model...")
        predictor = SchedulingPredictor()
        predictor.train(n_samples=1000)
        predictor.save_model('/home/claude/ml_scheduler_model.pkl')
    
    print()
    
    # Initialize rule-based scheduler
    scheduler = SmartScheduler(region="US-MIDW-MISO")
    print(f"✓ Initialized rule-based scheduler for region: {scheduler.region}")
    print()
    
    # Create sample jobs
    jobs = [
        TrainingJob(
            job_id="job_001",
            name="Large Language Model Fine-tuning",
            estimated_duration_hours=8.0,
            estimated_kwh=450.0,
            priority="medium",
            deadline=datetime.now() + timedelta(days=2)
        ),
        TrainingJob(
            job_id="job_002",
            name="Computer Vision Model Training",
            estimated_duration_hours=4.0,
            estimated_kwh=180.0,
            priority="low",
            deadline=datetime.now() + timedelta(days=3)
        ),
        TrainingJob(
            job_id="job_003",
            name="Recommendation System Retraining",
            estimated_duration_hours=6.0,
            estimated_kwh=320.0,
            priority="high",
            deadline=datetime.now() + timedelta(hours=24)
        ),
    ]
    
    # Add jobs
    for job in jobs:
        scheduler.add_job(job)
    print(f"✓ Added {len(jobs)} training jobs to queue")
    print()
    
    # Get rule-based recommendations
    print("📊 SCHEDULING ANALYSIS (Rule-Based + ML-Enhanced)")
    print("-" * 80)
    
    rule_based_recs = scheduler.schedule_all_jobs()
    ml_results = []
    
    for i, (rec, job) in enumerate(zip(rule_based_recs, jobs), 1):
        print(f"\n{'='*80}")
        print(f"🔷 Job {i}: {rec['job_name']}")
        print(f"{'='*80}")
        
        # Rule-based results
        print(f"\n📋 RULE-BASED ANALYSIS:")
        print(f"   Current Carbon Intensity: {rec['current_intensity']} gCO2/kWh")
        print(f"   Optimal Carbon Intensity: {rec['optimal_intensity']} gCO2/kWh")
        print(f"   Recommended Delay: {rec['delay_hours']:.1f} hours")
        print(f"   Carbon Savings: {rec['carbon_emissions']['saved_kg']} kg CO2")
        print(f"   Percent Reduction: {rec['carbon_emissions']['percent_reduction']}%")
        
        # ML prediction
        current_hour = datetime.now().hour
        job_features = {
            'duration_hours': job.estimated_duration_hours,
            'energy_kwh': job.estimated_kwh,
            'priority': {'high': 2, 'medium': 1, 'low': 0}[job.priority],
            'start_hour': current_hour,
            'day_of_week': datetime.now().weekday(),
            'month': datetime.now().month,
            'current_intensity': rec['current_intensity'],
            'is_weekend': 1 if datetime.now().weekday() >= 5 else 0,
            'is_daytime': 1 if 8 <= current_hour <= 18 else 0
        }
        
        ml_pred = predictor.predict(job_features)
        
        print(f"\n🤖 ML MODEL PREDICTION:")
        print(f"   Predicted Carbon Savings: {ml_pred['predicted_carbon_saved_kg']:.2f} kg CO2")
        print(f"   Predicted Optimal Delay: {ml_pred['predicted_optimal_delay_hours']:.1f} hours")
        print(f"   Confidence Level: {ml_pred['confidence_carbon']}")
        
        # Comparison
        rule_carbon = rec['carbon_emissions']['saved_kg']
        ml_carbon = ml_pred['predicted_carbon_saved_kg']
        diff = abs(rule_carbon - ml_carbon)
        accuracy = (1 - diff / rule_carbon) * 100 if rule_carbon > 0 else 0
        
        print(f"\n📊 MODEL COMPARISON:")
        print(f"   Rule-based carbon savings: {rule_carbon:.2f} kg CO2")
        print(f"   ML predicted savings: {ml_carbon:.2f} kg CO2")
        print(f"   Prediction accuracy: {accuracy:.1f}%")
        print(f"   {'✓ ML prediction within acceptable range' if accuracy > 80 else '⚠ Significant variance detected'}")
        
        ml_results.append({
            'job_id': job.job_id,
            'rule_based': rec,
            'ml_prediction': ml_pred,
            'accuracy': accuracy
        })
    
    # Aggregate metrics
    print("\n" + "=" * 80)
    print("AGGREGATE IMPACT METRICS")
    print("=" * 80)
    
    metrics = scheduler.get_metrics_summary(rule_based_recs)
    
    print(f"\n📈 Total Jobs Analyzed: {metrics['total_jobs']}")
    print(f"\n🌍 ENVIRONMENTAL IMPACT (Rule-Based):")
    print(f"   • Total Carbon Saved: {metrics['total_carbon_saved_kg']} kg CO2")
    print(f"   • Total Water Saved: {metrics['total_water_saved_liters']} liters")
    print(f"   • Average Reduction: {metrics['avg_carbon_reduction_percent']}%")
    
    # ML aggregate
    ml_total_carbon = sum(r['ml_prediction']['predicted_carbon_saved_kg'] for r in ml_results)
    ml_avg_accuracy = sum(r['accuracy'] for r in ml_results) / len(ml_results)
    
    print(f"\n🤖 ML MODEL PERFORMANCE:")
    print(f"   • Predicted Total Carbon: {ml_total_carbon:.2f} kg CO2")
    print(f"   • Average Prediction Accuracy: {ml_avg_accuracy:.1f}%")
    print(f"   • Model Status: {'Production Ready ✓' if ml_avg_accuracy > 80 else 'Needs Tuning ⚠'}")
    
    print(f"\n🌳 EQUIVALENT TO:")
    print(f"   • Taking {metrics['equivalent_metrics']['cars_off_road_days']} car-days off the road")
    print(f"   • Planting {metrics['equivalent_metrics']['trees_planted_equivalent']} trees")
    
    print(f"\n💵 COST SAVINGS: ${metrics['total_cost_saved_usd']}")
    
    print("\n" + "=" * 80)
    print("✓ ML-Enhanced Demo completed successfully!")
    print("=" * 80)
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "rule_based_recommendations": rule_based_recs,
        "ml_results": [{
            'job_id': r['job_id'],
            'ml_prediction': r['ml_prediction'],
            'accuracy': r['accuracy']
        } for r in ml_results],
        "aggregate_metrics": metrics,
        "ml_model_metrics": predictor.metrics
    }
    
    with open('../results/checkpoint2_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to: ml_enhanced_results.json")
    
    return results

if __name__ == "__main__":
    results = run_ml_enhanced_demo()
