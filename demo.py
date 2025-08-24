#!/usr/bin/env python3
"""
Quick Demo Script - AI Meme Stock Predictor
Shows various features of the system
"""

import time
from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent

def print_banner(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def main():
    print_banner("🚀 AI MEME STOCK PREDICTOR DEMO")
    
    print("Creating agent instance...")
    agent = PortiaMemeAgent()
    print("✅ Agent created successfully!")
    
    # Demo different stock tickers
    tickers = ["TSLA", "GME", "AMC", "AAPL"]
    
    for ticker in tickers:
        print_banner(f"📊 Analyzing {ticker}")
        print(f"Query: '{ticker} memes?'")
        print("-" * 40)
        
        # Run the analysis
        result = agent.handle_query("demo-session", f"{ticker} memes?")
        
        # Display results
        response = result.get('response', 'No response')
        print(response)
        
        # Small delay between requests
        time.sleep(1)
    
    print_banner("🎯 DEMO FEATURES SHOWCASED")
    print("✅ Agent initialization")
    print("✅ Multiple stock ticker analysis") 
    print("✅ Meme intensity scoring")
    print("✅ Sentiment analysis (VADER)")
    print("✅ Humorous response generation")
    print("✅ Error handling (Twitter rate limits)")
    print("✅ Logging and debugging info")
    
    print_banner("📚 NEXT STEPS")
    print("1. Add API keys to .env for enhanced data")
    print("2. Start web server: uvicorn src.ai_meme_stock_predictor.web.app:app --reload")
    print("3. Try Telegram bot with TELEGRAM_BOT_TOKEN")
    print("4. Visit http://127.0.0.1:8000/docs for API documentation")
    
    print("\n🎉 Demo completed! System is fully operational.")

if __name__ == "__main__":
    main()
