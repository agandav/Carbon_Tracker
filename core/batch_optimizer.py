"""
Batch Job Optimizer - NEW for Checkpoint 2
Optimizes scheduling for multiple jobs simultaneously using constraint optimization
"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from scipy.optimize import minimize, basinhopping
import pandas as pd
import time

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
        self.optimization_time = 0.0
        
    def optimize_batch(self, jobs: List[Dict]) -> Dict:
        """
        Optimize scheduling for multiple jobs simultaneously
        
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
        
        start_opt = time.time()
        
        # Objective: minimize total carbon emissions
        def objective(start_times):
            total_carbon = 0
            for i, job in enumerate(jobs):
                # Round to nearest integer hour
                start_hour = int(np.round(start_times[i]))
                duration = int(job['duration_hours'])
                
                # Simple average over integer hours the job runs
                intensity_sum = 0
                for h_offset in range(duration):
                    hour_idx = start_hour + h_offset
                    if hour_idx < self.forecast_hours:
                        intensity_sum += self.carbon_forecast[hour_idx]
                
                avg_intensity = intensity_sum / duration if duration > 0 else 0
                job_carbon = (avg_intensity * job['energy_kwh']) / 1000  # kg CO2
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
        
        # Use basin-hopping for global optimization
        def constrained_objective(start_times):
            carbon = objective(start_times)
            
            # Add penalty for constraint violations
            penalty = 0
            for i, job in enumerate(jobs):
                # Deadline constraint
                if job.get('deadline_hours'):
                    violation = (start_times[i] + job['duration_hours']) - job['deadline_hours']
                    if violation > 0:
                        penalty += violation * 10000
                
                # Dependency constraints
                if job.get('dependencies'):
                    for dep_idx in job['dependencies']:
                        violation = (start_times[dep_idx] + jobs[dep_idx]['duration_hours']) - start_times[i]
                        if violation > 0:
                            penalty += violation * 10000
                
                # Bounds penalty
                if start_times[i] < bounds[i][0]:
                    penalty += (bounds[i][0] - start_times[i]) * 10000
                if start_times[i] > bounds[i][1]:
                    penalty += (start_times[i] - bounds[i][1]) * 10000
            
            return carbon + penalty
        
        # Custom step-taking function
        class BoundedStep:
            def __init__(self, stepsize=0.5, bounds=None):
                self.stepsize = stepsize
                self.bounds = bounds
            
            def __call__(self, x):
                x_new = x + np.random.uniform(-self.stepsize, self.stepsize, x.shape)
                if self.bounds is not None:
                    for i in range(len(x_new)):
                        x_new[i] = np.clip(x_new[i], self.bounds[i][0], self.bounds[i][1])
                return x_new
        
        # Try multiple initial guesses
        best_result = None
        best_carbon = float('inf')
        
        for x0_trial in [np.zeros(n_jobs), 
                        np.array([b[1]/2 for b in bounds]),
                        np.array([b[1] for b in bounds])]:
            
            result_trial = basinhopping(
                constrained_objective,
                x0_trial,
                niter=200,
                T=1.0,
                stepsize=2.0,
                take_step=BoundedStep(stepsize=3.0, bounds=bounds),
                minimizer_kwargs={'method': 'L-BFGS-B', 'bounds': bounds},
                seed=42
            )
            
            if result_trial.fun < best_carbon:
                best_carbon = result_trial.fun
                best_result = result_trial
        
        result = best_result
        
        # Calculate results
        optimized_starts = result.x
        baseline_carbon = objective(np.zeros(n_jobs))  # Baseline: all jobs start immediately
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
        
        self.optimization_time = time.time() - start_opt
        
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
    
    def get_schedule(self, jobs: List[Dict]) -> Dict[str, float]:
        """
        Get simple job_id -> start_time mapping from optimization results
        
        Args:
            jobs: Original job list with 'id' field
            
        Returns:
            Dict mapping job IDs to start times in hours
        """
        if not self.optimization_results:
            raise ValueError("Must call optimize_batch() first")
        
        schedule = {}
        for job_result in self.optimization_results['job_schedule']:
            job_idx = job_result['job_index']
            start_time = job_result['optimized_start_hour']
            job_id = jobs[job_idx]['id']
            schedule[job_id] = start_time
        
        return schedule