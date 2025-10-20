"""
Cabfare - AI-Powered Ride Comparison
=====================================
CLI interface for comparing Uber and Lyft fares
"""

import sys
from utils.fare_comparator import FareComparator
from utils.chatbot import CabfareChatbot

def main():
    """Main CLI application"""
    print("=" * 70)
    print("🚖 CABFARE - AI-Powered Ride Comparison")
    print("=" * 70)
    print("\nCompare Uber and Lyft fares with AI assistance!\n")
    
    # Initialize components
    comparator = FareComparator()
    
    # Check if OpenAI API key is available
    import os
    has_openai_key = bool(os.getenv('OPENAI_API_KEY'))
    chatbot = CabfareChatbot() if has_openai_key else None
    
    # Example comparison (San Francisco)
    print("📍 Example: Downtown SF to Airport")
    print("-" * 70)
    
    pickup_lat, pickup_lng = 37.7749, -122.4194  # SF Downtown
    dropoff_lat, dropoff_lng = 37.6213, -122.3790  # SFO Airport
    
    print(f"\n🔍 Fetching fares from Uber and Lyft...")
    comparison = comparator.compare_fares(
        pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
    )
    
    # Display results
    print("\n" + "=" * 70)
    print("📊 COMPARISON RESULTS")
    print("=" * 70)
    
    print(f"\n💡 {comparison['comparison_summary']}\n")
    
    # Show recommendations
    recs = comparison["recommendations"]
    
    if recs["best_value"]:
        bv = recs["best_value"]
        print(f"💰 Best Value: {bv['service']} {bv['ride_type']} - {bv['estimate_display']}")
    
    if recs["fastest"]:
        fast = recs["fastest"]
        print(f"⚡ Fastest: {fast['service']} {fast['ride_type']} - {fast['duration_minutes']:.0f} min")
    
    if recs["luxury"]:
        lux = recs["luxury"]
        print(f"✨ Luxury: {lux['service']} {lux['ride_type']} - {lux['estimate_display']}")
    
    # Show detailed options
    print("\n" + "-" * 70)
    print("UBER OPTIONS:")
    for opt in comparison["uber"]:
        print(f"  • {opt['ride_type']}: {opt['estimate_display']} "
              f"({opt['duration_minutes']:.0f} min, {opt['distance_miles']:.1f} mi)")
    
    print("\nLYFT OPTIONS:")
    for opt in comparison["lyft"]:
        print(f"  • {opt['ride_type']}: {opt['estimate_display']} "
              f"({opt['duration_minutes']:.0f} min, {opt['distance_miles']:.1f} mi)")
    
    # AI Summary (if available)
    # if chatbot:
    #     print("\n" + "=" * 70)
    #     print("🤖 AI ASSISTANT SUMMARY")
    #     print("=" * 70)
    #     summary = chatbot.generate_summary(comparison)
    #     print(f"\n{summary}\n")
    # else:
    #     print("\n" + "=" * 70)
    #     print("💡 TIP: Add OPENAI_API_KEY to .env for AI-powered insights")
    #     print("=" * 70)
    
    print("=" * 70)
    print("✅ Comparison Complete!")
    print("=" * 70)
    
    print("\n💡 For interactive comparison, run:")
    print("   streamlit run streamlit_app.py")
    print()


if __name__ == "__main__":
    main()

