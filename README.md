# 🚀 AI Meme Stock Predictor - Where AI Meets Meme Magic! 

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://portialabs.ai)

> **🎯 Transform social media buzz into stock insights!** An advanced AI-powered system that analyzes meme stocks using real market data, Reddit sentiment, Twitter analysis, and cutting-edge AI predictions powered by Google Gemini and Portia AI.

<div align="center">

![Demo GIF](https://via.placeholder.com/600x300/1a1a1a/ffffff?text=AI+Meme+Stock+Predictor+Demo)

**📱 Try it now on Telegram** | **🌐 Web API** | **💻 CLI Tool**

</div>

---

## 🌟 What Makes This Special?

### 🤖 **AI-Powered Intelligence**
- **Google Gemini Integration**: Advanced natural language understanding
- **Portia AI Platform**: Access to 44+ cloud-based AI tools
- **Real-time Analysis**: Web search, data synthesis, and context awareness
- **Personalized Responses**: Learns from conversations and adapts

### 📊 **Comprehensive Data Sources**
- **Reddit WallStreetBets**: Live sentiment from meme stock communities
- **Twitter/X Analysis**: Social media buzz and influencer sentiment
- **AlphaVantage Market Data**: Real-time prices, volume, and technical indicators
- **Advanced Sentiment Analysis**: VADER + FinBERT for financial sentiment

### 🎭 **Engaging User Experience**
- **Interactive Telegram Bot**: 9+ commands with personality and humor
- **Visual ASCII Charts**: 20-day price trends in beautiful text format
- **Real-time Progress**: Watch analysis happen with live updates
- **Meme-aware Responses**: Understands 🚀, 💎, HODL, and community language

---

## ⚡ Quick Start (2 minutes!)

### 🚀 Option 1: Telegram Bot (Recommended)

```bash
# 1. Clone and setup
git clone https://github.com/whyatul/AgentHack-2025.git
cd AgentHack-2025
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Add your Telegram bot token to .env
echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" >> .env

# 4. Start the magic! ✨
python start_telegram_bot.py
```

**Then message your bot**: `TSLA memes?` or `GME` or `/start`

### 🌐 Option 2: Web API

```bash
# Start the FastAPI server
uvicorn src.ai_meme_stock_predictor.web.app:app --reload

# Test it out
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":"demo","text":"TSLA memes?"}'
```

### 💻 Option 3: Command Line

```bash
python cli.py TSLA        # Quick analysis
python cli.py "GME memes" # With meme analysis
```

---

## 🎮 Telegram Bot Commands

<div align="center">

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | 🎉 Welcome & introduction | Get started with personalized greeting |
| `/help` | 📖 Complete guide | See all commands and examples |
| `/about` | 🤖 AI capabilities | Learn about data sources and AI |
| `/how` | 🔬 Behind the scenes | See how analysis works |
| `/examples` | 💬 Sample conversations | Popular tickers and responses |
| `/popular` | 🔥 Trending stocks | Most analyzed meme stocks |
| `/health` | ✅ System status | Check API connections |
| **Any ticker** | 📈 **Stock analysis** | **`TSLA`, `GME memes?`, `AMC`** |

</div>

---

## 🧠 How It Works - The Magic Behind the Scenes

### 🔄 **Analysis Pipeline**

```mermaid
graph TD
    A[User Input: "TSLA memes?"] --> B{AI Router}
    B --> C[🔍 Data Collection]
    C --> D[Reddit Posts]
    C --> E[Twitter Sentiment] 
    C --> F[Market Data]
    D --> G[🧪 Analysis Engine]
    E --> G
    F --> G
    G --> H[Meme Intensity]
    G --> I[Sentiment Score]
    G --> J[Market Signals]
    H --> K[🤖 AI Prediction]
    I --> K
    J --> K
    K --> L[📱 Personalized Response]
```

### 🎯 **What Gets Analyzed**

1. **🔴 Reddit Analysis**
   - Fetches 50+ recent posts from r/wallstreetbets
   - Analyzes meme keywords: 🚀, 💎, HODL, "to the moon"
   - Community sentiment and engagement metrics

2. **🐦 Twitter Sentiment** 
   - Recent tweets mentioning the stock
   - Influencer sentiment and viral trends
   - Social media buzz indicators

3. **📊 Market Intelligence**
   - Real-time price, volume, and volatility
   - 20-day historical trends and patterns  
   - Technical indicators and market context

4. **🤖 AI Enhancement (Google Gemini + Portia)**
   - Advanced natural language reasoning
   - Real-time web search for breaking news
   - Multi-source data synthesis
   - Context-aware response generation

---

## 📈 Sample Analysis Output

```
🚀 TESLA (TSLA) Meme Analysis Complete! 

🎯 **Prediction**: BULLISH 📈 (Confidence: 73%)

🔍 **Analysis Breakdown**:
├─ 📊 Data Sources: ✅ Reddit (47 posts) ⚠️ Twitter (rate limited) ✅ Market (live)
├─ 🎭 Meme Intensity: 0.67 (HIGH) - 🚀💎 keywords trending
├─ 😊 Social Sentiment: +0.31 (Positive) - Community optimistic  
├─ 💰 Financial Sentiment: +0.18 (Slightly positive)
└─ 🧮 Composite Score: 0.42 (Above bullish threshold of 0.30)

📊 **20-Day Price Chart**: ▁▂▃▅▆▇█▇▆▅▄ 
    Range: $185.20 - $195.80 | Current: $192.45

💡 **Key Insights**:
• Strong meme community support with diamond hands mentality
• Recent Cybertruck deliveries driving social buzz  
• Volume spike suggests increased retail interest
• Elon tweets correlation remains high

⚠️ **Risk Assessment**: HIGH volatility expected, meme stocks are unpredictable

⚡ Analysis completed in 4.2 seconds
🎭 Remember: This is for entertainment - always DYOR! 
```

---

## 🛠️ Configuration & Setup

### � **Required API Keys** (All Optional for Demo)

| API | Purpose | Cost | How to Get |
|-----|---------|------|------------|
| 📈 **AlphaVantage** | Market data | Free | [Get Key](https://www.alphavantage.co/support/#api-key) |
| 🔴 **Reddit** | WallStreetBets data | Free | [Reddit Apps](https://www.reddit.com/prefs/apps) |
| 🐦 **Twitter/X** | Social sentiment | Free tier | [Developer Portal](https://developer.twitter.com/) |
| 📱 **Telegram** | Bot interface | Free | [@BotFather](https://t.me/BotFather) |
| 🚀 **Portia AI** | Advanced AI | Paid | [Portia Labs](https://portialabs.ai) |
| 🧠 **Google Gemini** | LLM | Pay-per-use | [Google AI Studio](https://makersuite.google.com/) |

### 🔐 **.env Configuration**

```bash
# Create .env file with your keys:
cat > .env << 'EOF'
# 📈 Market Data (Recommended)
ALPHAVANTAGE_API_KEY=your_alphavantage_key

# 🔴 Reddit Analysis (Recommended)  
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=ai-meme-stock-bot-v1

# 🐦 Twitter Sentiment (Optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# 📱 Telegram Bot (For bot interface)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# 🤖 AI Enhancement (Optional but powerful!)
PORTIA_API_KEY=your_portia_api_key
GOOGLE_API_KEY=your_google_api_key

# ⚙️ Advanced Options
ENABLE_FINBERT=1  # Advanced financial sentiment (requires 400MB model)
ENV=production
EOF
```

**💡 Pro Tip**: Works great even with just one API key! Missing keys = graceful degradation.

---

## 🚀 Advanced Features

### 🧠 **AI-Powered Enhancements**

- **🔍 Smart Web Search**: Finds breaking news and market events
- **🎯 Context Awareness**: Understands conversation history  
- **🌐 Multi-source Synthesis**: Correlates data across platforms
- **📊 Dynamic Analysis**: Adapts methodology based on available data
- **🗣️ Natural Conversations**: Responds like a knowledgeable friend

### 📊 **Technical Analysis**

- **ASCII Price Charts**: Beautiful text-based visualizations
- **Volume Analysis**: Trading pattern recognition
- **Trend Detection**: Bull/bear market identification  
- **Volatility Scoring**: Risk assessment metrics
- **Smart Thresholds**: Dynamic prediction boundaries

### 🎭 **Meme Culture Integration**

- **Community Language**: Understands WSB slang and emojis
- **Viral Trend Detection**: Identifies emerging meme patterns
- **Engagement Metrics**: Analyzes post popularity and comments
- **Influencer Impact**: Tracks key community figure sentiment

---

## 📚 Documentation Deep Dive

### 📖 **Comprehensive Guides**

- **[📋 Working Principle](PROJECT_WORKING_PRINCIPLE.txt)**: Complete system explanation
- **[� Technical Flowchart](TECHNICAL_FLOWCHART.txt)**: Detailed architecture diagrams  
- **[🛠️ Setup Guide](SETUP_GUIDE.md)**: Step-by-step installation
- **[📊 Project Status](PROJECT_STATUS.md)**: Current feature status

### 🏗️ **Architecture Overview**

```
src/ai_meme_stock_predictor/
├── 🤖 agent/           # AI agents and workflow orchestration
├── 📊 analysis/        # Sentiment and meme analysis engines  
├── 📡 data_sources/    # API integrations (Reddit, Twitter, Market)
├── 🧮 models/          # Prediction algorithms and heuristics
├── 🌐 web/            # FastAPI server and Telegram bot
└── 🛠️ utils/          # Configuration, logging, and utilities
```

---

## 🧪 Testing & Development

### 🔬 **Run Tests**

```bash
# Unit tests
pytest tests/ -v

# Integration tests  
python test_apis.py        # Test API connections
python test_telegram_bot.py # Test bot functionality
```

### 🐛 **Development Mode**

```bash
# Hot reload FastAPI server
uvicorn src.ai_meme_stock_predictor.web.app:app --reload --port 8000

# Debug mode with verbose logging
ENV=dev python start_telegram_bot.py
```

---

## 🚀 Deployment Options

### 🐳 **Docker (Recommended)**

```bash
# Build and run
docker build -t ai-meme-predictor .
docker run -p 8000:8000 --env-file .env ai-meme-predictor
```

### ☁️ **Cloud Deployment**

```bash
# Heroku
git push heroku main

# Railway
railway deploy

# Google Cloud Run
gcloud run deploy --source .
```

### 🖥️ **VPS/Server**

```bash
# Production with gunicorn
gunicorn -k uvicorn.workers.UvicornWorker src.ai_meme_stock_predictor.web.app:app --bind 0.0.0.0:8000

# Systemd service
sudo cp deployment/ai-meme-predictor.service /etc/systemd/system/
sudo systemctl enable ai-meme-predictor
```

---

## 🤝 Contributing

### 🎯 **Popular Contribution Areas**

- **� New Data Sources**: Discord, StockTwits, YouTube
- **🧠 ML Models**: Replace heuristics with trained models
- **📱 UI/UX**: Web dashboard, mobile app  
- **📊 Visualizations**: Charts, graphs, interactive plots
- **🌍 Internationalization**: Multi-language support

### 📝 **How to Contribute**

1. **Fork** the repository
2. **Clone**: `git clone your-fork-url`
3. **Branch**: `git checkout -b feature/amazing-feature`
4. **Develop**: Make your changes + tests
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`  
7. **PR**: Open a Pull Request

---

## 🛟 Troubleshooting

<details>
<summary>🔧 Common Issues & Solutions</summary>

| Problem | Solution |
|---------|----------|
| 🤖 Bot not responding | Check `TELEGRAM_BOT_TOKEN` in .env |
| 📊 No market data | Add `ALPHAVANTAGE_API_KEY` |  
| 🔴 Reddit errors | Verify Reddit API credentials |
| 🐦 Twitter rate limited | Normal - analysis continues with other sources |
| 🧠 AI not working | Add `PORTIA_API_KEY` and `GOOGLE_API_KEY` |
| 📦 Import errors | Activate venv: `source .venv/bin/activate` |
| 💾 Memory issues | Disable FinBERT: `ENABLE_FINBERT=0` |

</details>

---

## ⚠️ Important Disclaimers

<div align="center">

> **🎓 EDUCATIONAL & ENTERTAINMENT PURPOSES ONLY**
> 
> This tool is designed for learning about AI, sentiment analysis, and market psychology.
> **NOT financial advice!** Always conduct your own research before making investment decisions.
> 
> Meme stock analysis ≠ Guaranteed profits 📈≠💰

</div>

---

## 📈 Roadmap & Future Features

### 🎯 **Short-term Goals**

- [ ] 📊 **Real Chart Images**: Matplotlib/Plotly integration
- [ ] 💾 **User Preferences**: Persistent settings and favorites  
- [ ] 🔔 **Price Alerts**: Notify when stocks hit thresholds
- [ ] 📱 **Discord Bot**: Expand beyond Telegram

### 🚀 **Long-term Vision**

- [ ] 🧠 **Machine Learning**: Train custom prediction models
- [ ] � **Web Dashboard**: Full browser interface
- [ ] 📊 **Portfolio Tracking**: Multi-stock management
- [ ] 🤖 **Advanced AI**: GPT-4, Claude integration
- [ ] 📈 **Options Analysis**: Derivatives sentiment
- [ ] 🌍 **Global Markets**: International stock support

---

## 📄 License & Credits

### 📜 **MIT License**
Free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

### 🙏 **Acknowledgments**

- **Portia AI**: Advanced AI tooling platform
- **Google Gemini**: Cutting-edge language models  
- **Reddit API**: Community sentiment data
- **AlphaVantage**: Reliable market data
- **WSB Community**: Inspiration and meme wisdom

---

<div align="center">

## 🎉 Built with ❤️ for the Meme Stock Revolution!

**⭐ Star this repo if it made you money (or at least smile)!**

[![GitHub stars](https://img.shields.io/github/stars/whyatul/AgentHack-2025?style=social)](https://github.com/whyatul/AgentHack-2025/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/whyatul/AgentHack-2025?style=social)](https://github.com/whyatul/AgentHack-2025/network)

**🚀 Join the community**: Share your predictions, contribute code, and let's democratize financial AI together!

---

*"In memes we trust, in data we verify, in AI we innovate!"* 🤖📈

</div>

---

## 🎯 Quick Demo (30 seconds)

Want to see it in action? Try the Telegram bot:

1. **Message any ticker**: `TSLA`, `GME memes`, `AMC`
2. **Get wait message**: "🔍 Analyzing TSLA... ⏳ This will take 15-30 seconds"
3. **Receive detailed analysis**:

   ```text
   📊 TSLA Analysis Breakdown:
   🔍 Data Sources: ✅ Reddit (50 posts) ⚠️ Twitter (rate limited)
   📈 Features: Meme Intensity: 0.1234, Social Sentiment: 0.0567
   🧮 Score: 0.5×meme + 0.3×social + 0.2×financial = 0.0787
   📊 20-Day Chart: ▁▂▃▄▅▆▇█ ($180.50 - $195.30)
   ⚡ Analysis completed in 4.2s
   ```

## 🚀 Installation & Setup

```bash
git clone https://github.com/whyatul/AgentHack-2025.git
cd AgentHack-2025
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # Add your API keys (optional for demo)
```

### Quick Start Options

#### 🤖 Telegram Bot (Recommended)

```bash
# Add TELEGRAM_BOT_TOKEN to .env, then:
python start_telegram_bot.py
# Message your bot: "TSLA memes?"
```

#### 🌐 Web API

```bash
uvicorn src.ai_meme_stock_predictor.web.app:app --reload
# Test: curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{"conversation_id":"demo","text":"GME memes?"}'
```

#### 💻 CLI

```bash
python cli.py TSLA
```

## 🎮 Telegram Bot Commands

The enhanced bot supports these commands:

- `/start` - Welcome message with full introduction
- `/help` - Complete command guide and examples  
- `/about` - Learn about AI capabilities and data sources
- `/how` - Behind-the-scenes analysis process
- `/examples` - Sample conversations and popular tickers
- `/popular` - Most popular meme stocks to analyze
- `/feedback` - How to rate and improve the bot
- `/contact` - Support and troubleshooting help
- `/health` - Check system status and API connections

**Just message any ticker**: `TSLA`, `GME memes?`, `AMC`, `NVDA memes`

## 📊 Enhanced Analysis Features

### 🔍 Data Source Transparency

- **Real-time Status**: See which APIs are working (✅) or rate-limited (⚠️)  
- **Reddit Integration**: Fetches 50 recent posts from WallStreetBets
- **Twitter Analysis**: Social sentiment when available (handles rate limits gracefully)
- **Market Data**: Live stock prices, volume, and 20-day historical data
- **FinBERT Sentiment**: Advanced financial sentiment (optional, enable with `ENABLE_FINBERT=1`)

### 📈 Comprehensive Score Breakdown

- **Meme Intensity**: Keyword density and meme slang frequency (0-1 scale)
- **Social Sentiment**: VADER sentiment analysis (-1 to +1 scale)  
- **Financial Sentiment**: FinBERT financial sentiment (-1 to +1 scale)
- **Composite Score**: Weighted calculation: `0.5×meme + 0.3×social + 0.2×financial`
- **Smart Thresholds**: Dynamic bullish/bearish thresholds based on data quality

### 📊 Visual Analysis

- **ASCII Price Charts**: 20-day trend visualization with sparklines
- **Price Range**: Current price with high/low range
- **Volume Indicators**: Trading volume with historical context
- **Performance Timing**: See how long analysis took (typically 4-6 seconds)

### ⏳ User Experience Enhancements

- **Wait Messages**: Real-time progress updates during analysis
- **Personalized Responses**: Uses your name and provides context
- **Data Quality Warnings**: Alerts when analysis is based on limited data  
- **Error Handling**: Graceful degradation when APIs are unavailable

## 🔧 Configuration (.env Setup)

Create a `.env` file with your API keys (all optional for demo mode):

```env
# Stock Market Data (recommended)
ALPHAVANTAGE_API_KEY=your_alphavantage_key_here

# Reddit Analysis (recommended) 
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret  
REDDIT_USER_AGENT=meme-stock-bot

# Twitter Sentiment (optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Telegram Bot (for bot interface)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Advanced Features
ENABLE_FINBERT=0  # Set to 1 for advanced financial sentiment (slower)
ENV=dev
```

**Missing API keys?** No problem! The bot works in demo mode with limited data.

## 🎯 How It Works

1. **User Query**: Send any ticker like "TSLA", "GME memes?", "AMC"
2. **Wait Message**: Get real-time progress: "🔍 Analyzing TSLA... ⏳ 15-30 seconds"  
3. **Data Collection**: Fetches Reddit posts, Twitter sentiment, market data
4. **AI Analysis**: Processes meme intensity, sentiment, and market signals
5. **Score Calculation**: Combines weighted features with smart thresholds
6. **Detailed Response**: Complete breakdown with visual charts and timing

## ⚠️ Important Disclaimer

**This is for educational and entertainment purposes only.**

- Not financial advice or investment recommendations
- Meme analysis doesn't predict actual stock performance  
- Always do your own research before making investment decisions
- Past performance doesn't guarantee future results

---

## 📚 Advanced Documentation

For detailed technical documentation, see the sections below from the original README:

### Architecture & Components

- **Data Flow**: Reddit → Twitter → MarketData → Features → Prediction → Response
- **Core Components**: Agent, Workflow, Data Sources, Analysis, Models, Web/Telegram interfaces
- **Extensibility**: Easy to add new data sources, features, or prediction models

### Development & Testing

```bash
# Run tests
pytest -q

# Development server with auto-reload  
uvicorn src.ai_meme_stock_predictor.web.app:app --reload --host 0.0.0.0 --port 8000

# Check health
curl http://localhost:8000/health
```

### Production Deployment

- Use gunicorn for production: `gunicorn -k uvicorn.workers.UvicornWorker src.ai_meme_stock_predictor.web.app:app`
- Docker support available with included Dockerfile
- Environment variables for production configuration

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Twitter rate limited | Normal behavior - Reddit analysis continues |
| Missing market data | Add `ALPHAVANTAGE_API_KEY` to .env |  
| FinBERT always neutral | Set `ENABLE_FINBERT=1` (downloads 400MB model) |
| Bot not responding | Check `TELEGRAM_BOT_TOKEN` and network connectivity |
| Import errors | Activate virtual environment and run from repo root |

## 🚀 Future Roadmap

- 📊 **Real Image Charts**: Matplotlib/plotly chart generation and image sending
- 🤖 **Advanced ML**: Replace heuristics with trained prediction models  
- 📱 **Discord Integration**: Expand beyond Telegram
- 🔍 **Technical Indicators**: RSI, MACD, moving averages, volume analysis
- 💾 **Persistent Storage**: User preferences and feedback history
- 🌐 **Web Dashboard**: Browser-based interface with interactive charts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`  
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request

**Popular contribution areas:**

- New data sources (Discord, Reddit alternatives)
- Advanced prediction models (ML/AI)  
- UI improvements (web dashboard)
- Additional technical indicators
- Performance optimizations

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the meme stock community**

*Remember: This is for education and entertainment. Always DYOR (Do Your Own Research)!*
