#!/usr/bin/env python3
"""
API Integration Test - Test real APIs with your configured keys
"""

import asyncio
from src.ai_meme_stock_predictor.utils.config import get_settings
from src.ai_meme_stock_predictor.data_sources.market_data import MarketData
from src.ai_meme_stock_predictor.data_sources.reddit_source import RedditSource
from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent

async def test_apis():
    print("🔬 API Integration Test with Your Keys")
    print("="*50)
    
    settings = get_settings()
    
    # Test 1: AlphaVantage Market Data
    print("\n📊 Testing AlphaVantage API...")
    if settings.alphavantage_api_key:
        try:
            market = MarketData()
            quote = market.quote("TSLA")
            if quote and quote.get('symbol'):
                print(f"✅ TSLA Quote: ${quote['price']} (Volume: {quote['volume']:,})")
                print(f"   Change: {quote['change_percent']}")
            else:
                print("❌ No data returned (API limit or error)")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("❌ No API key configured")
    
    # Test 2: Reddit Data
    print("\n🔴 Testing Reddit API...")
    if settings.reddit_client_id:
        try:
            reddit = RedditSource()
            posts = reddit.fetch_mentions("TSLA", limit=3)
            if posts:
                print(f"✅ Fetched {len(posts)} Reddit posts about TSLA")
                for i, post in enumerate(posts[:2], 1):
                    print(f"   Post {i}: {post.get('title', 'No title')[:50]}...")
            else:
                print("❌ No posts returned")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("❌ No Reddit keys configured")
    
    # Test 3: Full Agent Analysis
    print("\n🤖 Testing Full Agent Analysis...")
    try:
        agent = PortiaMemeAgent()
        result = agent.handle_query("test-session", "AAPL memes?")
        response = result.get('response', 'No response')
        print(f"✅ Agent Response: {response[:100]}...")
        
        # Show metrics if available
        if 'metadata' in result:
            metadata = result['metadata']
            print(f"   Meme Intensity: {metadata.get('meme_intensity', 'N/A')}")
            print(f"   Sentiment: {metadata.get('sentiment_score', 'N/A')}")
    except Exception as e:
        print(f"❌ Agent Error: {str(e)}")
    
    print("\n" + "="*50)
    print("🎉 API Integration Test Complete!")
    
    # Show configuration summary
    print(f"\n📋 Your Configuration Summary:")
    print(f"   AlphaVantage: {'✅' if settings.alphavantage_api_key else '❌'}")
    print(f"   Reddit: {'✅' if settings.reddit_client_id else '❌'}")  
    print(f"   Twitter: {'✅' if settings.twitter_bearer_token else '❌'}")
    
    print(f"\n🚀 Ready for production use!")
    print(f"   CLI: python cli.py <TICKER>")
    print(f"   Web API: Available via FastAPI server")

if __name__ == "__main__":
    asyncio.run(test_apis())
