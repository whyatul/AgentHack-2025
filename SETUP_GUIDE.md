# AI Meme Stock Predictor - Complete Setup Guide

This guide will walk you through setting up the complete AI Meme Stock Predictor project with checkpoints to verify each step works properly.

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Environment Setup](#2-environment-setup)
3. [Configuration](#3-configuration)
4. [Core Components Verification](#4-core-components-verification)
5. [API Setup & Testing](#5-api-setup--testing)
6. [Telegram Bot Setup](#6-telegram-bot-setup)
7. [CLI Testing](#7-cli-testing)
8. [Advanced Features](#8-advanced-features)
9. [Verification Checklist](#9-verification-checklist)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### System Requirements
- Python 3.11+ (recommended 3.12+)
- At least 2GB free disk space
- Internet connection for API calls

### Required API Keys (Optional but Recommended)
- **Reddit**: Client ID & Secret from [Reddit Apps](https://www.reddit.com/prefs/apps)
- **Twitter/X**: Bearer Token from [Twitter Developer Portal](https://developer.twitter.com/)
- **Alpha Vantage**: Free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- **Telegram**: Bot token from [@BotFather](https://t.me/BotFather)

### ✅ Checkpoint 1: Prerequisites Check
```bash
python --version  # Should show Python 3.11+
df -h            # Check available disk space
```

---

## 2. Environment Setup

### Step 2.1: Clone and Setup Virtual Environment
```bash
cd /path/to/your/projects
git clone <repository-url>
cd AgentHack-2025

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Verify virtual environment
which python  # Should point to .venv/bin/python
which pip     # Should point to .venv/bin/pip
```

### Step 2.2: Install Dependencies
```bash
# Install core dependencies first
pip install --no-cache-dir fastapi uvicorn python-dotenv pydantic pydantic-settings

# Install data source dependencies
pip install --no-cache-dir praw tweepy requests

# Install analysis dependencies
pip install --no-cache-dir vaderSentiment rich httpx cachetools

# Install additional utilities
pip install --no-cache-dir python-telegram-bot pytest
```

### ✅ Checkpoint 2: Environment Verification
```bash
# Test core imports
python -c "import fastapi, uvicorn, pydantic; print('✅ Core dependencies OK')"
python -c "import praw, tweepy, requests; print('✅ Data source dependencies OK')"
python -c "import vaderSentiment; print('✅ Analysis dependencies OK')"
```

---

## 3. Configuration

### Step 3.1: Create Environment File
```bash
# Create .env file with your API keys
cat > .env << 'EOF'
# Market Data
ALPHAVANTAGE_API_KEY=your_alphavantage_key_here

# Social Media APIs
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=meme-stock-agent-v1.0

TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Optional: Advanced Features
PORTIA_API_KEY=your_portia_key_here
ENABLE_FINBERT=0  # Set to 1 to enable heavy ML model (requires more resources)

# Environment
ENV=dev
EOF
```

### Step 3.2: Verify Configuration Loading
```bash
python -c "
from src.ai_meme_stock_predictor.utils.config import settings
print('✅ Configuration loaded successfully')
print(f'Environment: {settings.env}')
print(f'Reddit configured: {bool(settings.reddit_client_id)}')
print(f'Twitter configured: {bool(settings.twitter_bearer_token)}')
print(f'Alpha Vantage configured: {bool(settings.alphavantage_api_key)}')
print(f'Telegram configured: {bool(getattr(settings, \"telegram_bot_token\", None))}')
"
```

### ✅ Checkpoint 3: Configuration Verification
- Configuration file created
- No import errors when loading settings
- API keys properly loaded (if provided)

---

## 4. Core Components Verification

### Step 4.1: Test Data Sources
```bash
# Test Reddit connection (if configured)
python -c "
from src.ai_meme_stock_predictor.data_sources.reddit_source import RedditSource
reddit = RedditSource()
print('✅ Reddit source initialized')
"

# Test Twitter connection (if configured)
python -c "
from src.ai_meme_stock_predictor.data_sources.twitter_source import TwitterSource
twitter = TwitterSource()
print('✅ Twitter source initialized')
"

# Test Market data connection (if configured)
python -c "
from src.ai_meme_stock_predictor.data_sources.market_data import MarketData
market = MarketData()
print('✅ Market data source initialized')
"
```

### Step 4.2: Test Analysis Components
```bash
# Test sentiment analysis
python -c "
from src.ai_meme_stock_predictor.analysis.sentiment import vader_compound
score = vader_compound('This is awesome news!')
print(f'✅ Sentiment analysis working: {score}')
"

# Test meme extraction
python -c "
from src.ai_meme_stock_predictor.analysis.meme_extraction import meme_intensity
posts = [{'title': 'TSLA to the moon!', 'selftext': 'Diamond hands!', 'text': 'HODL'}]
intensity = meme_intensity(posts, 'TSLA')
print(f'✅ Meme extraction working: {intensity}')
"
```

### Step 4.3: Test Prediction Models
```bash
# Test heuristic prediction
python -c "
from src.ai_meme_stock_predictor.models.heuristics import heuristic_prediction
features = {'meme_intensity': 0.5, 'social_sentiment': 0.3, 'financial_sentiment': 0.1}
prediction = heuristic_prediction(features)
print(f'✅ Prediction model working: {prediction}')
"
```

### ✅ Checkpoint 4: Core Components Status
All core components should initialize without errors.

---

## 5. API Setup & Testing

### Step 5.1: Start the FastAPI Server
```bash
# Terminal 1: Start the server
source .venv/bin/activate
uvicorn src.ai_meme_stock_predictor.web.app:app --reload
```

### Step 5.2: Test API Endpoints
```bash
# Terminal 2: Test health endpoint
curl -s http://127.0.0.1:8000/health | jq
# Expected: {"status":"ok"}

# Test query endpoint
curl -s -X POST http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":"test","text":"TSLA memes?"}' | jq

# Expected: JSON response with prediction and details
```

### ✅ Checkpoint 5: API Verification
- ✅ Server starts without errors
- ✅ Health endpoint returns `{"status":"ok"}`
- ✅ Query endpoint returns valid JSON with prediction
- ✅ Server logs show successful requests

---

## 6. Telegram Bot Setup

### Step 6.1: Create Telegram Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose a name for your bot
4. Choose a username (must end in 'bot')
5. Copy the token and add it to your `.env` file

### Step 6.2: Test Bot Configuration
```bash
# Verify bot token is loaded
python -c "
from src.ai_meme_stock_predictor.utils.config import settings
import os
token = os.getenv('TELEGRAM_BOT_TOKEN')
if token:
    print('✅ Telegram bot token configured')
    print(f'Token length: {len(token)}')
else:
    print('❌ Telegram bot token not found')
"
```

### Step 6.3: Start Telegram Bot
```bash
# Terminal 3: Start the Telegram bot
source .venv/bin/activate
python -m src.ai_meme_stock_predictor.web.telegram_bot
```

### Step 6.4: Test Telegram Bot
1. Find your bot on Telegram using the username you created
2. Send `/start` command
3. Send `TSLA memes?`
4. Bot should respond with meme stock analysis

### ✅ Checkpoint 6: Telegram Bot Verification
- ✅ Bot starts without errors
- ✅ Bot responds to `/start` command
- ✅ Bot processes stock queries
- ✅ Bot returns formatted responses

---

## 7. CLI Testing

### Step 7.1: Test CLI Interface
```bash
# Test basic CLI functionality
python cli.py TSLA

# Test with custom conversation ID
python cli.py GME --conversation-id cli-test-session

# Test different tickers
python cli.py AAPL
python cli.py DOGE
```

### ✅ Checkpoint 7: CLI Verification
- ✅ CLI processes different stock tickers
- ✅ CLI returns formatted predictions
- ✅ CLI shows detailed explanations

---

## 8. Advanced Features

### Step 8.1: Enable FinBERT (Optional)
⚠️ **Warning**: This downloads ~400MB model and requires significant RAM

```bash
# Enable FinBERT in .env
echo "ENABLE_FINBERT=1" >> .env

# Restart services to pick up new config
# The first query will download the FinBERT model
```

### Step 8.2: Test Advanced Features
```bash
# Test feedback functionality
curl -s -X POST http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":"test","text":"feedback:good:very helpful response"}' | jq

# Test different query types
curl -s -X POST http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":"test","text":"how does this work?"}' | jq
```

### ✅ Checkpoint 8: Advanced Features Verification
- ✅ FinBERT loads successfully (if enabled)
- ✅ Feedback system processes input
- ✅ Help queries provide informative responses

---

## 9. Verification Checklist

### Complete System Check Script
```bash
#!/bin/bash
echo "🔍 Running complete system verification..."

# Check 1: Environment
echo "1. Environment Check:"
source .venv/bin/activate
python --version
echo "✅ Virtual environment active"

# Check 2: Dependencies
echo "2. Dependencies Check:"
python -c "
import fastapi, uvicorn, praw, tweepy, vaderSentiment
print('✅ All core dependencies available')
"

# Check 3: Configuration
echo "3. Configuration Check:"
python -c "
from src.ai_meme_stock_predictor.utils.config import settings
print(f'✅ Environment: {settings.env}')
"

# Check 4: Core functionality
echo "4. Core Functionality Check:"
python cli.py TSLA > /dev/null && echo "✅ CLI working"

# Check 5: API (if server is running)
echo "5. API Check:"
if curl -s http://127.0.0.1:8000/health | grep -q "ok"; then
    echo "✅ API server responding"
else
    echo "❌ API server not responding (make sure uvicorn is running)"
fi

echo "🎉 Verification complete!"
```

### Save and run the verification script:
```bash
# Save the script
cat > verify_setup.sh << 'EOF'
[paste the script above]
EOF

chmod +x verify_setup.sh
./verify_setup.sh
```

---

## 10. Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
```bash
# Problem: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
pip list  # Verify packages are installed
```

#### 2. API Connection Issues
```bash
# Problem: Twitter/Reddit API errors
# Solution: Check API keys and rate limits
python -c "
from src.ai_meme_stock_predictor.utils.config import settings
print('Reddit ID:', settings.reddit_client_id[:10] + '...' if settings.reddit_client_id else 'Not set')
print('Twitter Token:', settings.twitter_bearer_token[:20] + '...' if settings.twitter_bearer_token else 'Not set')
"
```

#### 3. Server Won't Start
```bash
# Problem: Port already in use
# Solution: Kill existing processes or use different port
pkill -f uvicorn
# OR
uvicorn src.ai_meme_stock_predictor.web.app:app --reload --port 8001
```

#### 4. Telegram Bot Issues
```bash
# Problem: Bot not responding
# Solution: Check token and network
python -c "
import os
token = os.getenv('TELEGRAM_BOT_TOKEN')
if token and len(token) > 40:
    print('✅ Token format looks correct')
else:
    print('❌ Invalid token format')
"
```

#### 5. Disk Space Issues
```bash
# Problem: No space left on device
# Solution: Clean up and install minimal packages
df -h  # Check space
pip cache purge  # Clear pip cache
# Install without heavy ML packages
```

---

## Success Indicators

When everything is working correctly, you should see:

1. **CLI**: Returns stock predictions with meme analysis
2. **FastAPI**: Responds to health checks and queries
3. **Telegram Bot**: Processes messages and returns predictions
4. **Logs**: Show successful API calls and processing
5. **No Errors**: All imports and initializations complete without issues

## Next Steps

Once your setup is verified:
- Customize humor templates in `src/ai_meme_stock_predictor/agent/prompts.py`
- Add new data sources following the existing patterns
- Experiment with different prediction weightings
- Set up monitoring and logging for production use

---

**Need Help?** Check the main [README.md](README.md) for detailed architecture information and the troubleshooting section.
