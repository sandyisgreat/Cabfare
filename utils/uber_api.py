"""
Uber API Integration
====================
Handles communication with Uber Rides API
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class UberAPI:
    """Uber Rides API client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('UBER_API_KEY')
        self.base_url = "https://api.uber.com/v1.2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_price_estimate(
        self, 
        start_lat: float, 
        start_lng: float, 
        end_lat: float, 
        end_lng: float
    ) -> Dict:
        """
        Get price estimates for a ride
        
        Args:
            start_lat: Pickup latitude
            start_lng: Pickup longitude
            end_lat: Dropoff latitude
            end_lng: Dropoff longitude
        
        Returns:
            dict: Price estimates for different ride types
        """
        endpoint = f"{self.base_url}/estimates/price"
        params = {
            "start_latitude": start_lat,
            "start_longitude": start_lng,
            "end_latitude": end_lat,
            "end_longitude": end_lng
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Uber API Error: {e}")
            return self._get_mock_data()
    
    def get_time_estimate(self, lat: float, lng: float) -> Dict:
        """
        Get time estimates for pickup
        
        Args:
            lat: Pickup latitude
            lng: Pickup longitude
        
        Returns:
            dict: Time estimates for different ride types
        """
        endpoint = f"{self.base_url}/estimates/time"
        params = {
            "start_latitude": lat,
            "start_longitude": lng
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Uber API Error: {e}")
            return {}
    
    def _get_mock_data(self) -> Dict:
        """Mock data for testing without API key"""
        return {
            "prices": [
                {
                    "localized_display_name": "UberX",
                    "estimate": "$15-20",
                    "low_estimate": 15,
                    "high_estimate": 20,
                    "surge_multiplier": 1.0,
                    "duration": 12,
                    "distance": 5.2
                },
                {
                    "localized_display_name": "UberXL",
                    "estimate": "$22-28",
                    "low_estimate": 22,
                    "high_estimate": 28,
                    "surge_multiplier": 1.0,
                    "duration": 12,
                    "distance": 5.2
                },
                {
                    "localized_display_name": "Uber Comfort",
                    "estimate": "$18-24",
                    "low_estimate": 18,
                    "high_estimate": 24,
                    "surge_multiplier": 1.0,
                    "duration": 12,
                    "distance": 5.2
                }
            ]
        }

