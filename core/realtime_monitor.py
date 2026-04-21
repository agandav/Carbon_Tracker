"""
Real-Time Monitoring Dashboard - NEW for Checkpoint 2
Tracks live carbon intensity and provides real-time recommendations
"""

import time
from datetime import datetime
from typing import Dict, List
import json

class RealTimeMonitor:
    """
    Real-time monitoring system that tracks:
    - Live carbon intensity updates
    - Active job status
    - Cumulative savings metrics
    - Alert system for optimal scheduling windows
    """
    
    def __init__(self, update_interval_seconds: int = 300):
        """
        Initialize real-time monitor
        
        Args:
            update_interval_seconds: How often to check carbon intensity
        """
        self.update_interval = update_interval_seconds
        self.active_jobs = {}
        self.completed_jobs = []
        self.cumulative_savings = {
            'total_carbon_saved_kg': 0.0,
            'total_water_saved_liters': 0.0,
            'total_cost_saved_usd': 0.0,
            'jobs_optimized': 0
        }
        self.alerts = []
        
    def register_job(self, job_id: str, job_info: Dict):
        """Register a new job for monitoring"""
        self.active_jobs[job_id] = {
            'info': job_info,
            'registered_at': datetime.now().isoformat(),
            'status': 'waiting',
            'carbon_intensity_at_start': None,
            'actual_carbon_used': None
        }
        
    def start_job(self, job_id: str, current_carbon_intensity: float):
        """Mark job as started and record carbon intensity"""
        if job_id in self.active_jobs:
            self.active_jobs[job_id]['status'] = 'running'
            self.active_jobs[job_id]['started_at'] = datetime.now().isoformat()
            self.active_jobs[job_id]['carbon_intensity_at_start'] = current_carbon_intensity
            
    def complete_job(self, job_id: str, actual_energy_kwh: float, 
                    avg_carbon_intensity: float):
        """
        Mark job as complete and calculate actual savings
        
        Args:
            job_id: Job identifier
            actual_energy_kwh: Actual energy consumed
            avg_carbon_intensity: Average carbon intensity during execution
        """
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            job['status'] = 'completed'
            job['completed_at'] = datetime.now().isoformat()
            
            # Calculate actual carbon used
            actual_carbon = (actual_energy_kwh * avg_carbon_intensity) / 1000
            job['actual_carbon_kg'] = actual_carbon
            
            # Calculate savings vs immediate start
            immediate_carbon_intensity = job['info'].get('immediate_intensity', 
                                                         avg_carbon_intensity + 100)
            immediate_carbon = (actual_energy_kwh * immediate_carbon_intensity) / 1000
            carbon_saved = immediate_carbon - actual_carbon
            
            # Update cumulative metrics
            self.cumulative_savings['total_carbon_saved_kg'] += carbon_saved
            self.cumulative_savings['total_water_saved_liters'] += carbon_saved * 1.8
            self.cumulative_savings['total_cost_saved_usd'] += carbon_saved * 0.05
            self.cumulative_savings['jobs_optimized'] += 1
            
            # Move to completed
            self.completed_jobs.append(job)
            del self.active_jobs[job_id]
            
    def check_green_window_alert(self, current_intensity: float, 
                                 threshold: float = 300) -> Dict:
        """
        Check if current carbon intensity is in a green window
        
        Args:
            current_intensity: Current carbon intensity (gCO2/kWh)
            threshold: Threshold for "green" window
            
        Returns:
            Alert dictionary if green window detected
        """
        if current_intensity < threshold and len(self.active_jobs) > 0:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': 'green_window',
                'carbon_intensity': current_intensity,
                'message': f'Optimal scheduling window detected! '
                          f'Intensity: {current_intensity} gCO2/kWh',
                'waiting_jobs': len([j for j in self.active_jobs.values() 
                                   if j['status'] == 'waiting'])
            }
            self.alerts.append(alert)
            return alert
        return None
    
    def get_dashboard_state(self) -> Dict:
        """
        Get current dashboard state for visualization
        
        Returns:
            Complete dashboard state with all metrics
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'active_jobs': {
                'total': len(self.active_jobs),
                'waiting': len([j for j in self.active_jobs.values() 
                              if j['status'] == 'waiting']),
                'running': len([j for j in self.active_jobs.values() 
                              if j['status'] == 'running'])
            },
            'completed_jobs': len(self.completed_jobs),
            'cumulative_savings': self.cumulative_savings,
            'recent_alerts': self.alerts[-5:],  # Last 5 alerts
            'active_job_details': list(self.active_jobs.values())
        }
    
    def generate_report(self) -> str:
        """Generate human-readable monitoring report"""
        state = self.get_dashboard_state()
        
        report = f"""
        +=========================================================+
        |        SMARTSCHEDULER REAL-TIME MONITORING REPORT       |
        +=========================================================+
        | Timestamp: {state['timestamp'][:19]}                    |
        +=========================================================+
        | ACTIVE JOBS                                             |
        |   - Total Active: {state['active_jobs']['total']}                                     |
        |   - Waiting: {state['active_jobs']['waiting']}                                         |
        |   - Running: {state['active_jobs']['running']}                                         |
        |                                                         |
        | COMPLETED JOBS: {state['completed_jobs']}                                         |
        +=========================================================+
        | CUMULATIVE ENVIRONMENTAL IMPACT                         |
        |   - Carbon Saved: {state['cumulative_savings']['total_carbon_saved_kg']:.2f} kg CO2                  |
        |   - Water Saved: {state['cumulative_savings']['total_water_saved_liters']:.2f} liters                |
        |   - Cost Saved: ${state['cumulative_savings']['total_cost_saved_usd']:.2f}                           |
        |   - Jobs Optimized: {state['cumulative_savings']['jobs_optimized']}                                  |
        +=========================================================+
        | RECENT ALERTS: {len(state['recent_alerts'])}                                        |
        +=========================================================+
        """
        return report
