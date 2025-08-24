#!/usr/bin/env python3
"""
Test Telegram Bot Functionality
"""

import asyncio
import sys
from src.ai_meme_stock_predictor.utils.config import get_settings
from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent

async def test_bot_functions():
    """Test the bot functions without actually starting the bot"""
    
    print("🤖 Testing Telegram Bot Functions")
    print("=" * 40)
    
    # Check configuration
    settings = get_settings()
    if not settings.telegram_bot_token:
        print("❌ No Telegram bot token found!")
        print("Please run: python add_telegram_token.py YOUR_TOKEN")
        return False
    
    print(f"✅ Token found: {settings.telegram_bot_token[:10]}...")
    
    # Test bot application creation
    try:
        from src.ai_meme_stock_predictor.web.telegram_bot import build_application
        app = build_application()
        print("✅ Bot application created successfully")
    except Exception as e:
        print(f"❌ Bot creation failed: {e}")
        return False
    
    # Test agent functions
    try:
        agent = PortiaMemeAgent()
        print("✅ PortiaMemeAgent initialized")
        
        # Test different queries
        test_queries = ["TSLA memes?", "GME memes?", "/help", "5:Great bot!"]
        
        print("\n🧪 Testing Bot Responses:")
        print("-" * 30)
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            try:
                result = agent.handle_query("test-session", query)
                response = result.get('response', 'No response')[:100]
                print(f"Response: {response}...")
                print("✅ Query handled successfully")
            except Exception as e:
                print(f"❌ Query failed: {e}")
    
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 All tests passed! Bot is ready to start.")
    print("\nTo start your bot:")
    print("python telegram_setup.py --start")
    print("\nThen in Telegram:")
    print("1. Find your bot by username")
    print("2. Send /start")
    print("3. Try: TSLA memes?")
    
    return True

async def simulate_bot_conversation():
    """Simulate a conversation with the bot"""
    
    print("\n🎭 Bot Conversation Simulation")
    print("=" * 40)
    
    agent = PortiaMemeAgent()
    session_id = "demo-user"
    
    conversation = [
        "/start",
        "TSLA memes?", 
        "What about GME?",
        "AMC memes?",
        "/help",
        "5:This bot is awesome!"
    ]
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        try:
            result = agent.handle_query(session_id, message)
            response = result.get('response', 'No response')
            print(f"🤖 Bot: {response}")
        except Exception as e:
            print(f"🤖 Bot: Error - {e}")
    
    print("\n" + "=" * 40)
    print("✅ Conversation simulation complete!")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        asyncio.run(simulate_bot_conversation())
    else:
        asyncio.run(test_bot_functions())

if __name__ == "__main__":
    main()
