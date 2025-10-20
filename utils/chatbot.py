"""
LLM Chatbot Interface
======================
Handles natural language interaction for ride comparison
"""

import os
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class CabfareChatbot:
    """LLM-powered chatbot for ride comparison"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.conversation_history = []
        
        # System prompt
        self.system_prompt = """You are Cabfare AI, a helpful assistant that compares ride fares 
between Uber and Lyft. You help users find the best ride options based on their needs and preferences.

You can:
- Compare prices between Uber and Lyft
- Recommend the best value option
- Suggest fastest rides
- Find luxury options
- Explain surge pricing
- Provide travel tips

Be friendly, concise, and helpful. Always present fare information clearly with specific prices.
When presenting comparisons, use emojis and formatting to make it easy to read."""
    
    def chat(self, user_message: str, fare_data: Optional[Dict] = None) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's input message
            fare_data: Optional fare comparison data to include in context
        
        Returns:
            str: AI-generated response
        """
        # Add fare data to context if available
        if fare_data:
            context = self._format_fare_data(fare_data)
            enhanced_message = f"{user_message}\n\nFare Data:\n{context}"
        else:
            enhanced_message = user_message
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": enhanced_message
        })
        
        # Generate response
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            ai_response = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _format_fare_data(self, fare_data: Dict) -> str:
        """Format fare comparison data for LLM context"""
        uber_options = fare_data.get("uber", [])
        lyft_options = fare_data.get("lyft", [])
        recommendations = fare_data.get("recommendations", {})
        
        formatted = "UBER OPTIONS:\n"
        for opt in uber_options:
            formatted += f"- {opt['ride_type']}: {opt['estimate_display']} "
            formatted += f"(~{opt['duration_minutes']:.0f} min, {opt['distance_miles']:.1f} mi)\n"
        
        formatted += "\nLYFT OPTIONS:\n"
        for opt in lyft_options:
            formatted += f"- {opt['ride_type']}: {opt['estimate_display']} "
            formatted += f"(~{opt['duration_minutes']:.0f} min, {opt['distance_miles']:.1f} mi)\n"
        
        formatted += "\nRECOMMENDATIONS:\n"
        if recommendations.get("best_value"):
            bv = recommendations["best_value"]
            formatted += f"💰 Best Value: {bv['service']} {bv['ride_type']} - {bv['estimate_display']}\n"
        
        if recommendations.get("fastest"):
            fast = recommendations["fastest"]
            formatted += f"⚡ Fastest: {fast['service']} {fast['ride_type']} - {fast['duration_minutes']:.0f} min\n"
        
        return formatted
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def generate_summary(self, fare_data: Dict) -> str:
        """Generate a natural language summary of fare comparison"""
        prompt = f"""Based on this fare data, provide a brief, friendly summary 
comparing Uber and Lyft options. Keep it under 100 words.

{self._format_fare_data(fare_data)}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"

