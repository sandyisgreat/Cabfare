# 🚖 Cabfare - AI-Powered Ride Comparison

## Overview
An **LLM-powered application** that compares ride fares between **Uber** and **Lyft** in real-time, helping users make informed decisions about their ride-sharing choices.

## 🎯 Key Features

### ✅ Current Features
- LLM-powered conversational interface
- Natural language ride requests
- Intelligent fare comparison

### 🚧 In Development
- [ ] Uber API integration
- [ ] Lyft API integration  
- [ ] Real-time fare comparison
- [ ] Surge pricing detection
- [ ] Ride time estimation
- [ ] Cost optimization recommendations
- [ ] Historical price tracking

## Tech Stack
- **LLM**: OpenAI GPT-4 / GPT-3.5
- **APIs**: Uber API, Lyft API
- **UI**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, plotly

## Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key
- Uber API credentials (optional for demo)
- Lyft API credentials (optional for demo)

```

### Usage

#### 🚀 Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```

Features:
- 💬 Chat with AI assistant
- 📊 Visual fare comparisons
- 🗺️ Interactive trip planning
- 📈 Real-time recommendations

#### 🖥️ CLI Version
```bash
python app.py
```

## 🏗️ Project Structure

```
Cabfare/
├── streamlit_app.py          # Interactive web interface
├── app.py                    # CLI application
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── README.md                # This file
│
├── utils/
│   ├── __init__.py          # Package init
│   ├── uber_api.py          # Uber API integration
│   ├── lyft_api.py          # Lyft API integration
│   ├── fare_comparator.py   # Comparison engine
│   └── chatbot.py           # LLM interface
│
├── data/                    # Trip data storage
├── models/                  # ML models (future)
└── notebooks/               # Analysis notebooks
```

## 🤖 How It Works

1. **User Input**: Enter pickup/dropoff locations or chat naturally
2. **API Integration**: Fetches real-time fares from Uber & Lyft APIs
3. **AI Analysis**: LLM analyzes options and provides recommendations
4. **Smart Comparison**: Shows best value, fastest, and luxury options
5. **Interactive Chat**: Ask follow-up questions for personalized advice

## 💡 Example Queries

**To the AI Assistant:**
- "What's the cheapest option?"
- "I'm in a hurry, what's fastest?"
- "Compare luxury rides"
- "Is there surge pricing?"
- "How much would I save with Lyft?"

**Note:** The app includes mock data for testing without API keys!

## 🚀 Features

### Current
- ✅ LLM-powered chat interface
- ✅ Uber & Lyft API integration
- ✅ Real-time fare comparison
- ✅ Smart recommendations (best value, fastest, luxury)
- ✅ Mock data for testing
- ✅ Web & CLI interfaces

### Coming Soon
- [ ] Google Maps integration for addresses
- [ ] Historical price tracking
- [ ] Route optimization
- [ ] Calendar integration
- [ ] Price alerts
- [ ] Multi-city support

## 🤝 Contributing
Contributions welcome! Please feel free to submit a Pull Request.

