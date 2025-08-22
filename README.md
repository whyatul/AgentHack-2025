# AI Meme Stock Predictor

Playful educational agent that fuses meme culture signals with market + sentiment data to produce humorous, explainable pseudo-predictions.

## High-Level Architecture

User -> (Telegram / Web UI) -> Portia Agent Orchestrator

Portia Agent orchestrates:
- Social/Meme Data collectors (Twitter/X, Reddit, Meme aggregators [extensible])
- Market Data collectors (Alpha Vantage, Yahoo Finance fallback)
- Sentiment & Meme Analysis (VADER, FinBERT, keyword & hashtag frequency)
- Prediction + Humor Generation (rule ensemble + light ML model)
- Feedback logging + adaptive humor tuning

## Directory Structure
```
src/ai_meme_stock_predictor/
  data_sources/
  analysis/
  models/
  agent/
  utils/
  web/
    app.py (FastAPI API)
    telegram_bot.py (Telegram adapter)
```

## Environment Variables (.env)
```
ALPHAVANTAGE_API_KEY=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=meme-stock-agent
TWITTER_BEARER_TOKEN=...
PORTIA_API_KEY=...
TELEGRAM_BOT_TOKEN=...
ENV=dev
```

## Install & Run (Dev)
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.ai_meme_stock_predictor.web.app:app --reload
```
Visit: http://localhost:8000/health

### Quickstart (Detailed)
1. Clone repo & enter directory.
2. Create & activate virtualenv (see above).
3. Copy `.env` template and fill any keys you have:
  ```bash
  cat > .env <<'EOF'
  ALPHAVANTAGE_API_KEY=
  REDDIT_CLIENT_ID=
  REDDIT_CLIENT_SECRET=
  REDDIT_USER_AGENT=meme-stock-agent
  TWITTER_BEARER_TOKEN=
  PORTIA_API_KEY=
  TELEGRAM_BOT_TOKEN=
  ENV=dev
  # Optional heavy model toggle (FinBERT). Leave 0 for faster startup.
  ENABLE_FINBERT=0
  EOF
  ```
4. (Optional) Enable FinBERT sentiment model (downloads ~400MB first run):
  ```bash
  ENABLE_FINBERT=1 uvicorn src.ai_meme_stock_predictor.web.app:app --reload
  ```
  If disabled (`0` / unset) FinBERT scores return neutral and startup is instant.
5. Basic health check:
  ```bash
  curl http://127.0.0.1:8000/health
  ```
6. Query the API (example ticker prompt):
  ```bash
  curl -X POST http://127.0.0.1:8000/query \
    -H 'Content-Type: application/json' \
    -d '{"conversation_id":"demo1","text":"TSLA memes?"}'
  ```
7. Run tests:
  ```bash
  pytest -q
  ```

### Common Issues
- Module import error for `src`: ensure you run commands from repo root & virtualenv active.
- Slow startup: FinBERT model downloading; set `ENABLE_FINBERT=0` to skip.
- Missing data (warnings about Reddit/Twitter/AlphaVantage): supply keys in `.env` to enable those sources.

### Telegram Bot
```
python -m src.ai_meme_stock_predictor.web.telegram_bot
```
Then in chat: `TSLA memes?`

## Portia SDK Integration
`portia_agent.py` attempts to import `portia` (placeholder `portia-sdk` dependency). Provide real SDK package name if different. Interaction logging uses `log_interaction` (adjust to actual method signature).

## Docker
A `Dockerfile` (to be added) will enable container build:
```
docker build -t meme-stock .
docker run --env-file .env -p 8000:8000 meme-stock
```

## Testing
```
pytest -q
```

## Disclaimer
Not financial advice. Entertainment & educational use only.

## Roadmap
- Discord adapter
- Advanced meme image / OCR
- Fine-tuned meme slang sentiment model
- Feedback-driven humor reinforcement

MIT License
