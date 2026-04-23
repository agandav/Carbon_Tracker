"""
ML Prediction Model
Predicts optimal scheduling outcomes using Random Forest
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from datetime import datetime, timedelta
import json
import pickle

class SchedulingPredictor:
    """
    ML model that predicts carbon savings and optimal start times.
    Uses Random Forest to learn from historical scheduling data
    """
    
    def __init__(self):
        # Two models one for carbon savings and one for optimal delay
        self.carbon_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.delay_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.is_trained = False
        self.feature_names = None
        
    def generate_training_data(self, n_samples=1000):
        """
        Generate synthetic training data based on realistic patterns
        In production, this would be real historical data
        """
        print(f"Generating {n_samples} training samples...")
        
        data = []
        for _ in range(n_samples):
            # Jobs
            duration = np.random.choice([2, 4, 6, 8, 12, 16, 24])  # hours
            energy_kwh = duration * np.random.uniform(30, 80)  # kWh
            priority = np.random.choice([0, 1, 2])  # low=0, med=1, high=2
            
            # Time features
            start_hour = np.random.randint(0, 24)
            day_of_week = np.random.randint(0, 7)
            month = np.random.randint(1, 13)
            
            # Grid conditions
            current_intensity = self._simulate_carbon_intensity(start_hour)
            
            # Simulate finding the optimal window
            optimal_hour = self._find_optimal_hour_pattern(start_hour, duration)
            optimal_intensity = self._simulate_carbon_intensity(optimal_hour)
            
            # Calculate the outcomes
            delay_hours = (optimal_hour - start_hour) % 24
            immediate_emissions = energy_kwh * current_intensity / 1000
            optimal_emissions = energy_kwh * optimal_intensity / 1000
            carbon_saved = immediate_emissions - optimal_emissions
            percent_saved = (carbon_saved / immediate_emissions * 100) if immediate_emissions > 0 else 0
            
            data.append({
                # Features (x value)
                'duration_hours': duration,
                'energy_kwh': energy_kwh,
                'priority': priority,
                'start_hour': start_hour,
                'day_of_week': day_of_week,
                'month': month,
                'current_intensity': current_intensity,
                'is_weekend': 1 if day_of_week >= 5 else 0,
                'is_daytime': 1 if 8 <= start_hour <= 18 else 0,
                
                # Targets (y value)
                'carbon_saved_kg': carbon_saved,
                'optimal_delay_hours': delay_hours,
                'percent_saved': percent_saved
            })
        
        return pd.DataFrame(data)
    
    def _simulate_carbon_intensity(self, hour):
        """Simulate realistic carbon intensity patterns"""
        # Base intensity
        base = 450
        
        # Solar peak (10am - 4pm): lower intensity
        if 10 <= hour <= 16:
            base -= np.random.uniform(100, 200)
        # Evening peak (6pm - 9pm): higher intensity
        elif 18 <= hour <= 21:
            base += np.random.uniform(50, 150)
        # Night: moderate
        else:
            base += np.random.uniform(-50, 50)
            
        return max(200, base + np.random.normal(0, 30))
    
    def _find_optimal_hour_pattern(self, current_hour, duration):
        """Simulate finding optimal hour (typically midday for solar)"""
        # Best windows are usually  10am - 3pm
        optimal_candidates = list(range(10, 16))
        return np.random.choice(optimal_candidates)
    
    def train(self, n_samples=1000):
        """Train the ML models"""
        print("\n" + "="*60)
        print("TRAINING ML PREDICTION MODELS")
        print("="*60)
        
        # Generate training data
        df = self.generate_training_data(n_samples)
        
        # Prepare features and targets
        feature_cols = ['duration_hours', 'energy_kwh', 'priority', 'start_hour',
                       'day_of_week', 'month', 'current_intensity', 'is_weekend', 'is_daytime']
        self.feature_names = feature_cols
        
        X = df[feature_cols]
        y_carbon = df['carbon_saved_kg']
        y_delay = df['optimal_delay_hours']
        
        # Split data
        X_train, X_test, y_carbon_train, y_carbon_test, y_delay_train, y_delay_test = \
            train_test_split(X, y_carbon, y_delay, test_size=0.2, random_state=42)
        
        print(f"\nTraining set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Train carbon savings model
        print("\n[1/2] Training Carbon Savings Predictor...")
        self.carbon_model.fit(X_train, y_carbon_train)
        carbon_pred = self.carbon_model.predict(X_test)
        
        carbon_mse = mean_squared_error(y_carbon_test, carbon_pred)
        carbon_mae = mean_absolute_error(y_carbon_test, carbon_pred)
        carbon_r2 = r2_score(y_carbon_test, carbon_pred)
        
        print(f"   [OK] MSE: {carbon_mse:.2f}")
        print(f"   [OK] MAE: {carbon_mae:.2f} kg CO2")
        print(f"   [OK] R2 Score: {carbon_r2:.4f}")
        
        # Train delay prediction model
        print("\n[2/2] Training Optimal Delay Predictor...")
        self.delay_model.fit(X_train, y_delay_train)
        delay_pred = self.delay_model.predict(X_test)
        
        delay_mse = mean_squared_error(y_delay_test, delay_pred)
        delay_mae = mean_absolute_error(y_delay_test, delay_pred)
        delay_r2 = r2_score(y_delay_test, delay_pred)
        
        print(f"   [OK] MSE: {delay_mse:.2f}")
        print(f"   [OK] MAE: {delay_mae:.2f} hours")
        print(f"   [OK] R2 Score: {delay_r2:.4f}")
        
        # Feature importance
        print("\n[CHART] Feature Importance (Carbon Savings):")
        importances = self.carbon_model.feature_importances_
        for name, imp in sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True):
            print(f"   - {name}: {imp:.3f}")
        
        self.is_trained = True
        
        # Stores metrics
        self.metrics = {
            'carbon_model': {
                'mse': float(carbon_mse),
                'mae': float(carbon_mae),
                'r2': float(carbon_r2)
            },
            'delay_model': {
                'mse': float(delay_mse),
                'mae': float(delay_mae),
                'r2': float(delay_r2)
            },
            'feature_importance': {name: float(imp) for name, imp in zip(feature_cols, importances)}
        }
        
        print("\n[OK] Training complete!")
        print("="*60)
        
        return self.metrics
    
    def predict(self, job_features):
        """
        Predict outcomes for a job
        
        Args:
            job_features: dict with keys matching feature_names
            
        Returns:
            dict with predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction!")
        
        # Prepares features
        X = pd.DataFrame([job_features])[self.feature_names]
        
        # Makes predictions
        carbon_saved = self.carbon_model.predict(X)[0]
        optimal_delay = self.delay_model.predict(X)[0]
        
        return {
            'predicted_carbon_saved_kg': float(carbon_saved),
            'predicted_optimal_delay_hours': float(optimal_delay),
            'confidence_carbon': 'high' if self.metrics['carbon_model']['r2'] > 0.8 else 'medium',
            'confidence_delay': 'high' if self.metrics['delay_model']['r2'] > 0.8 else 'medium'
        }
    
    def save_model(self, filepath='ml_scheduler_model.pkl'):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving!")
        
        model_data = {
            'carbon_model': self.carbon_model,
            'delay_model': self.delay_model,
            'feature_names': self.feature_names,
            'metrics': self.metrics
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"[OK] Model saved to {filepath}")
    
    def load_model(self, filepath='ml_scheduler_model.pkl'):
        """Load trained model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.carbon_model = model_data['carbon_model']
        self.delay_model = model_data['delay_model']
        self.feature_names = model_data['feature_names']
        self.metrics = model_data['metrics']
        self.is_trained = True
        
        print(f"[OK] Model loaded from {filepath}")


def train_and_evaluate():
    """Train model and show evaluation results"""
    predictor = SchedulingPredictor()
    
    # Trains models
    metrics = predictor.train(n_samples=1000)
    
    # Saves model
    predictor.save_model('/home/claude/ml_scheduler_model.pkl')
    
    # Saves metrics to JSON form for easy access
    with open('/home/claude/ml_model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("\n[FOLDER] Saved:")
    print("   - ml_scheduler_model.pkl (trained model)")
    print("   - ml_model_metrics.json (evaluation metrics)")
    
    # Test predictions
    print("\n" + "="*60)
    print("TESTING PREDICTIONS")
    print("="*60)
    
    test_job = {
        'duration_hours': 8,
        'energy_kwh': 450,
        'priority': 1,
        'start_hour': 20,  # 8 PM (24 hour format)
        'day_of_week': 2,  # Wednesday (Starting from 0=Monday)
        'month': 2,
        'current_intensity': 580,
        'is_weekend': 0,
        'is_daytime': 0
    }
    
    prediction = predictor.predict(test_job)
    
    print("\n[LIST] Test Job:")
    print(f"   Duration: {test_job['duration_hours']} hours")
    print(f"   Energy: {test_job['energy_kwh']} kWh")
    print(f"   Current time: {test_job['start_hour']}:00 (8 PM)")
    print(f"   Current carbon intensity: {test_job['current_intensity']} gCO2/kWh")
    
    print("\n[AI] ML Predictions:")
    print(f"   Predicted carbon savings: {prediction['predicted_carbon_saved_kg']:.2f} kg CO2")
    print(f"   Predicted optimal delay: {prediction['predicted_optimal_delay_hours']:.1f} hours")
    print(f"   Confidence (carbon): {prediction['confidence_carbon']}")
    print(f"   Confidence (delay): {prediction['confidence_delay']}")
    
    print("\n[OK] Prediction test complete!")
    print("="*60)
    
    return predictor, metrics


if __name__ == "__main__":
    predictor, metrics = train_and_evaluate()
