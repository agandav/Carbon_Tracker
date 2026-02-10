"""
Batch Job Optimizer - NEW for Checkpoint 2
Optimizes scheduling for multiple jobs simultaneously using constraint optimization
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from scipy.optimize import minimize
import pandas as pd

class BatchJobOptimizer:
    """
    Advanced batch optimization using constrained optimization
    NEW COMPONENT for Checkpoint 2 - goes beyond single-job scheduling
    """
    
    def __init__(self, carbon_forecast: List[float], forecast_hours: int = 24):
        """
        Initialize batch optimizer
        
        Args:
            carbon_forecast: 24-hour carbon intensity forecast (gCO2/kWh)
            forecast_hours: Forecast window in hours
        """
        self.carbon_forecast = np.array(carbon_forecast)
        self.forecast_hours = forecast_hours
        self.optimization_results = None
        
    def optimize_batch(self, jobs: List[Dict]) -> Dict:
        """
        Optimize scheduling for multiple jobs simultaneously
        Considers job dependencies, resource constraints, and carbon minimization
        
        Args:
            jobs: List of job dictionaries with:
                - duration_hours: float
                - energy_kwh: float
                - priority: int (0=low, 1=med, 2=high)
                - deadline_hours: float (hours from now)
                - dependencies: List[int] (job indices that must finish first)
        
        Returns:
            Optimization results with start times and carbon savings
        """
        n_jobs = len(jobs)
        
        # Objective: minimize total carbon emissions
        def objective(start_times):
            total_carbon = 0
            for i, job in enumerate(jobs):
                start = int(start_times[i])
                duration = int(job['duration_hours'])
                end = min(start + duration, self.forecast_hours)
                
                # Calculate carbon for this job's window
                job_carbon = 0
                for hour in range(start, end):
                    job_carbon += self.carbon_forecast[hour]
                
                job_carbon = (job_carbon / duration) * job['energy_kwh'] / 1000
                total_carbon += job_carbon
            
            return total_carbon
        
        # Constraints
        constraints = []
        
        # 1. Deadline constraints
        for i, job in enumerate(jobs):
            if job.get('deadline_hours'):
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x, i=i, job=job: 
                        job['deadline_hours'] - (x[i] + job['duration_hours'])
                })
        
        # 2. Dependency constraints (job j must start after job i finishes)
        for i, job in enumerate(jobs):
            if job.get('dependencies'):
                for dep_idx in job['dependencies']:
                    constraints.append({
                        'type': 'ineq',
                        'fun': lambda x, i=i, dep=dep_idx: 
                            x[i] - (x[dep] + jobs[dep]['duration_hours'])
                    })
        
        # Bounds: all jobs must start within forecast window
        bounds = [(0, self.forecast_hours - job['duration_hours']) 
                 for job in jobs]
        
        # Initial guess: start all jobs immediately
        x0 = np.zeros(n_jobs)
        
        # Run optimization
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000}
        )
        
        # Calculate results
        optimized_starts = result.x
        baseline_carbon = objective(x0)  # All jobs start now
        optimized_carbon = result.fun
        carbon_saved = baseline_carbon - optimized_carbon
        
        # Prepare detailed results
        job_results = []
        for i, job in enumerate(jobs):
            start_time = optimized_starts[i]
            job_results.append({
                'job_index': i,
                'optimized_start_hour': float(start_time),
                'delay_hours': float(start_time),
                'duration': job['duration_hours'],
                'deadline_met': (start_time + job['duration_hours']) <= 
                               job.get('deadline_hours', float('inf'))
            })
        
        self.optimization_results = {
            'total_jobs': n_jobs,
            'baseline_carbon_kg': float(baseline_carbon),
            'optimized_carbon_kg': float(optimized_carbon),
            'carbon_saved_kg': float(carbon_saved),
            'percent_reduction': float((carbon_saved / baseline_carbon) * 100),
            'optimization_success': result.success,
            'job_schedule': job_results
        }
        
        return self.optimization_results
