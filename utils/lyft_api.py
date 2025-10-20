"""
Lyft API Integration
====================
Handles communication with Lyft Rides API
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class LyftAPI:
    """Lyft Rides API client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('LYFT_API_KEY')
        self.base_url = "https://api.lyft.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_cost_estimate(
        self, 
        start_lat: float, 
        start_lng: float, 
        end_lat: float, 
        end_lng: float
    ) -> Dict:
        """
        Get cost estimates for a ride
        
        Args:
            start_lat: Pickup latitude
            start_lng: Pickup longitude
            end_lat: Dropoff latitude
            end_lng: Dropoff longitude
        
        Returns:
            dict: Cost estimates for different ride types
        """
        endpoint = f"{self.base_url}/cost"
        params = {
            "start_lat": start_lat,
            "start_lng": start_lng,
            "end_lat": end_lat,
            "end_lng": end_lng
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lyft API Error: {e}")
            return self._get_mock_data()
    
    def get_eta(self, lat: float, lng: float) -> Dict:
        """
        Get ETA for pickup
        
        Args:
            lat: Pickup latitude
            lng: Pickup longitude
        
        Returns:
            dict: ETA estimates for different ride types
        """
        endpoint = f"{self.base_url}/eta"
        params = {
            "lat": lat,
            "lng": lng
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lyft API Error: {e}")
            return {}
    
    def _get_mock_data(self) -> Dict:
        """Mock data for testing without API key"""
        return {
            "cost_estimates": [
                {
                    "display_name": "Lyft",
                    "estimated_cost_cents_min": 1400,
                    "estimated_cost_cents_max": 1800,
                    "estimated_duration_seconds": 720,
                    "estimated_distance_miles": 5.2,
                    "primetime_percentage": "0%"
                },
                {
                    "display_name": "Lyft XL",
                    "estimated_cost_cents_min": 2000,
                    "estimated_cost_cents_max": 2600,
                    "estimated_duration_seconds": 720,
                    "estimated_distance_miles": 5.2,
                    "primetime_percentage": "0%"
                },
                {
                    "display_name": "Lux",
                    "estimated_cost_cents_min": 2200,
                    "estimated_cost_cents_max": 2800,
                    "estimated_duration_seconds": 720,
                    "estimated_distance_miles": 5.2,
                    "primetime_percentage": "0%"
                }
            ]
        }

