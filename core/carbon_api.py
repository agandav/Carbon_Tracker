"""
Carbon Intensity API Module
Fetches real-time grid carbon intensity data for scheduling decisions
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CarbonIntensityAPI:
    """Interface to carbon intensity data sources"""
    
    def __init__(self, region: str = "US-MIDW-MISO"):
        """
        Initialize API client
        Args:
            region: Grid region code (e.g., US-MIDW-MISO, US-CAL-CISO)
        """
        self.region = region
        self.base_url = "https://api.electricitymap.org/v3"
        # Using mock data for demo: in production would use real API key
        self.use_mock = True
        
    def get_current_intensity(self) -> Dict:
        """Get current carbon intensity (gCO2/kWh)"""
        if self.use_mock:
            return self._get_mock_current()
        
        # Real API call would be:
        # response = requests.get(f"{self.base_url}/carbon-intensity/latest",
        #                        params={"zone": self.region})
        # return response.json()
    
    def get_forecast_24h(self) -> List[Dict]:
        """Get 24-hour carbon intensity forecast"""
        if self.use_mock:
            return self._get_mock_forecast()
    
    def _get_mock_current(self) -> Dict:
        """Mock current carbon intensity data"""
        import random
        now = datetime.now()
        
        # Simulate lower carbon during day (more solar)
        hour = now.hour
        base_intensity = 450  # gCO2/kWh baseline
        
        # Lower during sunny hours (10am-4pm)
        if 10 <= hour <= 16:
            intensity = base_intensity - random.randint(100, 200)
        # Higher during peak evening (6pm-9pm)
        elif 18 <= hour <= 21:
            intensity = base_intensity + random.randint(50, 150)
        else:
            intensity = base_intensity + random.randint(-50, 50)
            
        return {
            "zone": self.region,
            "carbonIntensity": max(200, intensity),
            "datetime": now.isoformat(),
            "fossilFreePercentage": max(0, 100 - (intensity / 10))
        }
    
    def _get_mock_forecast(self) -> List[Dict]:
        """Mock 24-hour forecast data"""
        import random
        forecast = []
        base_time = datetime.now()
        
        for hour_offset in range(24):
            timestamp = base_time + timedelta(hours=hour_offset)
            hour = timestamp.hour
            
            # Realistic daily pattern
            if 10 <= hour <= 16:  # Solar peak
                intensity = random.randint(250, 350)
            elif 18 <= hour <= 21:  # Evening peak
                intensity = random.randint(500, 650)
            elif 0 <= hour <= 6:  # Night (wind)
                intensity = random.randint(300, 450)
            else:
                intensity = random.randint(380, 480)
            
            forecast.append({
                "datetime": timestamp.isoformat(),
                "carbonIntensity": intensity,
                "zone": self.region
            })
        
        return forecast
    
    def find_greenest_window(self, duration_hours: int = 4) -> Dict:
        """
        Find the greenest time window for training
        
        Args:
            duration_hours: Required training duration in hours
            
        Returns:
            Dict with start time and avg carbon intensity
        """
        forecast = self.get_forecast_24h()
        
        best_window = None
        best_avg_intensity = float('inf')
        
        # Sliding window to find lowest average intensity
        for i in range(len(forecast) - duration_hours + 1):
            window = forecast[i:i+duration_hours]
            avg_intensity = sum(h["carbonIntensity"] for h in window) / len(window)
            
            if avg_intensity < best_avg_intensity:
                best_avg_intensity = avg_intensity
                best_window = {
                    "start_time": window[0]["datetime"],
                    "end_time": window[-1]["datetime"],
                    "avg_intensity": avg_intensity,
                    "window_hours": duration_hours
                }
        
        return best_window
