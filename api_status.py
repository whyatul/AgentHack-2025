#!/usr/bin/env python3
"""
API Configuration Status Dashboard
Shows which APIs are configured and their status
"""

import os
from dotenv import load_dotenv
from src.ai_meme_stock_predictor.utils.config import get_settings
from src.ai_meme_stock_predictor.data_sources.market_data import MarketData
from src.ai_meme_stock_predictor.data_sources.reddit_source import RedditSource

def print_banner(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_api_status():
    print_banner("🔧 API CONFIGURATION STATUS")
    
    # Load settings
    settings = get_settings()
    
    print("\n📋 CONFIGURED API KEYS:")
    print("-" * 30)
    
    # Check AlphaVantage
    if settings.alphavantage_api_key:
        print(f"✅ AlphaVantage: {settings.alphavantage_api_key[:8]}...")
        try:
            market_data = MarketData()
            print("   Status: Ready for stock market data")
        except Exception as e:
            print(f"   Status: Error - {str(e)[:50]}...")
    else:
        print("❌ AlphaVantage: Not configured")
    
    # Check Reddit
    if settings.reddit_client_id and settings.reddit_client_secret:
        print(f"✅ Reddit: {settings.reddit_client_id[:8]}...")
        print(f"   User Agent: {settings.reddit_user_agent}")
        try:
            reddit_source = RedditSource()
            print("   Status: Ready for Reddit data")
        except Exception as e:
            print(f"   Status: Error - {str(e)[:50]}...")
    else:
        print("❌ Reddit: Not configured")
    
    # Check Twitter
    if settings.twitter_bearer_token:
        print(f"✅ Twitter: {settings.twitter_bearer_token[:20]}...")
        print("   Status: Configured (may hit rate limits)")
    else:
        print("❌ Twitter: Not configured")
    
    # Check Telegram
    if settings.telegram_bot_token:
        print(f"✅ Telegram: {settings.telegram_bot_token[:10]}...")
        print("   Status: Ready for bot deployment")
    else:
        print("❌ Telegram: Not configured")
    
    # Check Portia
    if settings.portia_api_key:
        print(f"✅ Portia: {settings.portia_api_key[:8]}...")
    else:
        print("❌ Portia: Not configured (optional)")
    
    print_banner("🚀 FUNCTIONALITY STATUS")
    
    configured_count = sum([
        bool(settings.alphavantage_api_key),
        bool(settings.reddit_client_id and settings.reddit_client_secret),
        bool(settings.twitter_bearer_token)
    ])
    
    print(f"📊 API Integration Level: {configured_count}/3 core APIs configured")
    print()
    
    if configured_count >= 2:
        print("🎉 EXCELLENT: Multiple data sources available!")
        print("   • Rich meme stock analysis possible")
        print("   • Cross-platform sentiment tracking")
        print("   • Enhanced prediction accuracy")
    elif configured_count == 1:
        print("✅ GOOD: Basic functionality available!")
        print("   • Limited data sources")
        print("   • Consider adding more APIs for better analysis")
    else:
        print("⚠️  BASIC: Mock data mode")
        print("   • Add API keys for enhanced functionality")
    
    print_banner("🛠️ AVAILABLE FEATURES")
    
    features = [
        ("CLI Interface", "✅ Always available", "python cli.py TSLA"),
        ("Web API", "✅ Always available", "uvicorn src.ai_meme_stock_predictor.web.app:app --reload"),
        ("Real Stock Data", "✅ Available" if settings.alphavantage_api_key else "❌ Need AlphaVantage key", ""),
        ("Reddit Analysis", "✅ Available" if settings.reddit_client_id else "❌ Need Reddit keys", ""),
        ("Twitter Sentiment", "✅ Available" if settings.twitter_bearer_token else "❌ Need Twitter key", ""),
        ("Telegram Bot", "✅ Available" if settings.telegram_bot_token else "❌ Need Telegram key", "python -m src.ai_meme_stock_predictor.web.telegram_bot")
    ]
    
    for feature, status, command in features:
        print(f"{status} {feature}")
        if command:
            print(f"   Command: {command}")
    
    print_banner("🔍 QUICK TEST COMMANDS")
    print("# Test with enhanced data:")
    print("python cli.py GME")
    print("python cli.py AMC") 
    print("python cli.py AAPL")
    print()
    print("# Start web server:")
    print("uvicorn src.ai_meme_stock_predictor.web.app:app --reload")
    print("# Then visit: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    check_api_status()
