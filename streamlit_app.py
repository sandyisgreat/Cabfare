"""
Cabfare - AI-Powered Ride Comparison
=====================================
Streamlit interface for comparing Uber and Lyft fares using LLM
"""

import streamlit as st
import os
from dotenv import load_dotenv
from utils.fare_comparator import FareComparator
from utils.chatbot import CabfareChatbot

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cabfare - AI Ride Comparison",
    page_icon="🚖",
    layout="wide"
)

# Initialize session state
if "comparator" not in st.session_state:
    st.session_state.comparator = FareComparator()

if "chatbot" not in st.session_state:
    st.session_state.chatbot = CabfareChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_comparison" not in st.session_state:
    st.session_state.last_comparison = None

# App title
st.title("🚖 Cabfare - AI Ride Comparison")
st.markdown("*Compare Uber and Lyft fares instantly with AI assistance*")

# Sidebar for location input
with st.sidebar:
    st.header("📍 Trip Details")
    
    # You can replace this with actual geocoding in production
    st.subheader("Pickup Location")
    pickup_lat = st.number_input("Latitude", value=37.7749, format="%.6f", key="pickup_lat")
    pickup_lng = st.number_input("Longitude", value=-122.4194, format="%.6f", key="pickup_lng")
    
    st.subheader("Dropoff Location")
    dropoff_lat = st.number_input("Latitude", value=37.7849, format="%.6f", key="dropoff_lat")
    dropoff_lng = st.number_input("Longitude", value=-122.4094, format="%.6f", key="dropoff_lng")
    
    if st.button("🔍 Compare Fares", type="primary", use_container_width=True):
        with st.spinner("Fetching fares from Uber and Lyft..."):
            comparison = st.session_state.comparator.compare_fares(
                pickup_lat, pickup_lng, dropoff_lat, dropoff_lng
            )
            st.session_state.last_comparison = comparison
            
            # Generate AI summary
            summary = st.session_state.chatbot.generate_summary(comparison)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"I've compared the fares for your trip!\n\n{summary}"
            })
    
    st.markdown("---")
    st.caption("💡 Tip: Chat with the AI for personalized recommendations!")

# Main content area
if st.session_state.last_comparison:
    # Display comparison results
    st.header("📊 Fare Comparison")
    
    comparison = st.session_state.last_comparison
    
    # Summary card
    st.info(f"📈 {comparison['comparison_summary']}")
    
    # Three columns for recommendations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("💰 Best Value")
        if comparison["recommendations"]["best_value"]:
            bv = comparison["recommendations"]["best_value"]
            st.metric(
                label=f"{bv['service']} {bv['ride_type']}",
                value=bv['estimate_display'],
                delta=f"{bv['duration_minutes']:.0f} min"
            )
    
    with col2:
        st.subheader("⚡ Fastest")
        if comparison["recommendations"]["fastest"]:
            fast = comparison["recommendations"]["fastest"]
            st.metric(
                label=f"{fast['service']} {fast['ride_type']}",
                value=f"{fast['duration_minutes']:.0f} min",
                delta=fast['estimate_display']
            )
    
    with col3:
        st.subheader("✨ Luxury")
        if comparison["recommendations"]["luxury"]:
            lux = comparison["recommendations"]["luxury"]
            st.metric(
                label=f"{lux['service']} {lux['ride_type']}",
                value=lux['estimate_display'],
                delta=f"{lux['duration_minutes']:.0f} min"
            )
    
    st.markdown("---")
    
    # Detailed comparison tables
    tab1, tab2 = st.tabs(["🟦 Uber Options", "🟪 Lyft Options"])
    
    with tab1:
        if comparison["uber"]:
            st.table([
                {
                    "Ride Type": opt["ride_type"],
                    "Price": opt["estimate_display"],
                    "Duration": f"{opt['duration_minutes']:.0f} min",
                    "Distance": f"{opt['distance_miles']:.1f} mi",
                    "Surge": f"{opt['surge']}x" if opt['surge'] > 1 else "No surge"
                }
                for opt in comparison["uber"]
            ])
        else:
            st.warning("No Uber options available")
    
    with tab2:
        if comparison["lyft"]:
            st.table([
                {
                    "Ride Type": opt["ride_type"],
                    "Price": opt["estimate_display"],
                    "Duration": f"{opt['duration_minutes']:.0f} min",
                    "Distance": f"{opt['distance_miles']:.1f} mi",
                    "Surge": opt['surge']
                }
                for opt in comparison["lyft"]
            ])
        else:
            st.warning("No Lyft options available")

# Chat interface
st.header("💬 Chat with Cabfare AI")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your ride options..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chatbot.chat(
                prompt,
                fare_data=st.session_state.last_comparison
            )
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.caption("🚖 Cabfare - Powered by OpenAI GPT | Data from Uber & Lyft APIs")

# Clear chat button in sidebar
with st.sidebar:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chatbot.reset_conversation()
        st.rerun()

