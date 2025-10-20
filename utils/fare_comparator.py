"""
Fare Comparison Engine
======================
Compares fares between Uber and Lyft and provides recommendations
"""

from typing import Dict, List, Tuple
from .uber_api import UberAPI
from .lyft_api import LyftAPI


class FareComparator:
    """Compares ride fares between Uber and Lyft"""
    
    def __init__(self):
        self.uber = UberAPI()
        self.lyft = LyftAPI()
    
    def compare_fares(
        self,
        start_lat: float,
        start_lng: float,
        end_lat: float,
        end_lng: float
    ) -> Dict:
        """
        Compare fares between Uber and Lyft
        
        Args:
            start_lat: Pickup latitude
            start_lng: Pickup longitude
            end_lat: Dropoff latitude
            end_lng: Dropoff longitude
        
        Returns:
            dict: Comparison results with recommendations
        """
        # Get estimates from both services
        uber_data = self.uber.get_price_estimate(start_lat, start_lng, end_lat, end_lng)
        lyft_data = self.lyft.get_cost_estimate(start_lat, start_lng, end_lat, end_lng)
        
        # Parse and format results
        uber_options = self._parse_uber_data(uber_data)
        lyft_options = self._parse_lyft_data(lyft_data)
        
        # Find best deals
        recommendations = self._generate_recommendations(uber_options, lyft_options)
        
        return {
            "uber": uber_options,
            "lyft": lyft_options,
            "recommendations": recommendations,
            "comparison_summary": self._create_summary(uber_options, lyft_options)
        }
    
    def _parse_uber_data(self, data: Dict) -> List[Dict]:
        """Parse Uber API response"""
        options = []
        for price in data.get("prices", []):
            options.append({
                "service": "Uber",
                "ride_type": price["localized_display_name"],
                "price_min": price["low_estimate"],
                "price_max": price["high_estimate"],
                "estimate_display": price["estimate"],
                "duration_minutes": price.get("duration", 0),
                "distance_miles": price.get("distance", 0),
                "surge": price.get("surge_multiplier", 1.0),
                "avg_price": (price["low_estimate"] + price["high_estimate"]) / 2
            })
        return options
    
    def _parse_lyft_data(self, data: Dict) -> List[Dict]:
        """Parse Lyft API response"""
        options = []
        for cost in data.get("cost_estimates", []):
            min_price = cost["estimated_cost_cents_min"] / 100
            max_price = cost["estimated_cost_cents_max"] / 100
            options.append({
                "service": "Lyft",
                "ride_type": cost["display_name"],
                "price_min": min_price,
                "price_max": max_price,
                "estimate_display": f"${min_price:.0f}-{max_price:.0f}",
                "duration_minutes": cost.get("estimated_duration_seconds", 0) / 60,
                "distance_miles": cost.get("estimated_distance_miles", 0),
                "surge": cost.get("primetime_percentage", "0%"),
                "avg_price": (min_price + max_price) / 2
            })
        return options
    
    def _generate_recommendations(
        self,
        uber_options: List[Dict],
        lyft_options: List[Dict]
    ) -> Dict:
        """Generate ride recommendations based on comparison"""
        all_options = uber_options + lyft_options
        
        if not all_options:
            return {"best_value": None, "fastest": None, "luxury": None}
        
        # Sort by average price
        sorted_by_price = sorted(all_options, key=lambda x: x["avg_price"])
        best_value = sorted_by_price[0] if sorted_by_price else None
        
        # Sort by duration
        sorted_by_time = sorted(
            [opt for opt in all_options if opt["duration_minutes"] > 0],
            key=lambda x: x["duration_minutes"]
        )
        fastest = sorted_by_time[0] if sorted_by_time else None
        
        # Find luxury options
        luxury_keywords = ["xl", "lux", "comfort", "black"]
        luxury_options = [
            opt for opt in all_options
            if any(kw in opt["ride_type"].lower() for kw in luxury_keywords)
        ]
        luxury = min(luxury_options, key=lambda x: x["avg_price"]) if luxury_options else None
        
        return {
            "best_value": best_value,
            "fastest": fastest,
            "luxury": luxury
        }
    
    def _create_summary(
        self,
        uber_options: List[Dict],
        lyft_options: List[Dict]
    ) -> str:
        """Create a text summary of the comparison"""
        if not uber_options or not lyft_options:
            return "Unable to compare - missing data from one or both services."
        
        uber_cheapest = min(uber_options, key=lambda x: x["avg_price"])
        lyft_cheapest = min(lyft_options, key=lambda x: x["avg_price"])
        
        if uber_cheapest["avg_price"] < lyft_cheapest["avg_price"]:
            diff = lyft_cheapest["avg_price"] - uber_cheapest["avg_price"]
            return f"Uber is cheaper by ${diff:.2f} on average. Best option: {uber_cheapest['ride_type']}"
        elif lyft_cheapest["avg_price"] < uber_cheapest["avg_price"]:
            diff = uber_cheapest["avg_price"] - lyft_cheapest["avg_price"]
            return f"Lyft is cheaper by ${diff:.2f} on average. Best option: {lyft_cheapest['ride_type']}"
        else:
            return "Prices are similar between Uber and Lyft."

