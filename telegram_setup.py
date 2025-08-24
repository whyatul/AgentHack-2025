#!/usr/bin/env python3
"""
Telegram Bot Setup Guide and Tester
This script helps you set up and test your Telegram bot
"""

import os
import sys
from dotenv import load_dotenv
from src.ai_meme_stock_predictor.utils.config import get_settings

def print_banner(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def create_telegram_bot_guide():
    print_banner("🤖 TELEGRAM BOT SETUP GUIDE")
    
    print("\n📋 STEP-BY-STEP INSTRUCTIONS:")
    print("-" * 40)
    
    print("\n1️⃣ CREATE A TELEGRAM BOT:")
    print("   • Open Telegram app on your phone/computer")
    print("   • Search for @BotFather (official Telegram bot)")
    print("   • Start a chat with @BotFather")
    print("   • Send command: /newbot")
    print("   • Choose a name for your bot (e.g., 'My Meme Stock Bot')")
    print("   • Choose a username ending in 'bot' (e.g., 'my_meme_stock_bot')")
    print("   • @BotFather will give you a TOKEN - COPY IT!")
    
    print("\n2️⃣ ADD TOKEN TO .ENV FILE:")
    print("   • Copy the token from @BotFather")
    print("   • Open your .env file")
    print("   • Add this line:")
    print("     TELEGRAM_BOT_TOKEN=\"your_token_here\"")
    
    print("\n3️⃣ TEST THE BOT:")
    print("   • Run: python telegram_setup.py --test")
    print("   • Start your bot: python -m src.ai_meme_stock_predictor.web.telegram_bot")
    print("   • Find your bot in Telegram and send: /start")
    
    print("\n4️⃣ BOT COMMANDS:")
    print("   • /start - Initialize the bot")
    print("   • /help - Show available commands")
    print("   • /health - Check bot status")
    print("   • Send 'TSLA memes?' - Get meme stock analysis")
    print("   • Send 'GME memes?' - Analyze GameStop")
    
    print_banner("🔧 CURRENT STATUS CHECK")
    
    settings = get_settings()
    if settings.telegram_bot_token:
        print(f"✅ Telegram bot token found: {settings.telegram_bot_token[:10]}...")
        print("   Status: Ready to start bot!")
        return True
    else:
        print("❌ No Telegram bot token found in .env file")
        print("   Please follow steps 1-2 above")
        return False

def test_telegram_bot():
    """Test if the Telegram bot can be initialized"""
    print_banner("🧪 TESTING TELEGRAM BOT")
    
    try:
        from src.ai_meme_stock_predictor.web.telegram_bot import build_application
        
        print("Creating Telegram bot application...")
        app = build_application()
        print("✅ Bot application created successfully!")
        print("✅ Ready to start polling!")
        
        print("\n📱 NEXT STEPS:")
        print("1. Run: python -m src.ai_meme_stock_predictor.web.telegram_bot")
        print("2. Open Telegram and find your bot")
        print("3. Send /start to begin chatting")
        print("4. Try: 'TSLA memes?' for analysis")
        
        return True
        
    except RuntimeError as e:
        if "TELEGRAM_BOT_TOKEN missing" in str(e):
            print("❌ Telegram bot token not found")
            print("Please add TELEGRAM_BOT_TOKEN to your .env file")
        else:
            print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def start_bot_interactive():
    """Interactively start the bot"""
    print_banner("🚀 STARTING TELEGRAM BOT")
    
    try:
        print("Starting bot in polling mode...")
        print("Press Ctrl+C to stop the bot")
        print("\n🤖 Bot is now running!")
        print("Go to Telegram and chat with your bot!")
        
        # Import and run the bot
        from src.ai_meme_stock_predictor.web.telegram_bot import build_application
        application = build_application()
        application.run_polling()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    load_dotenv()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            has_token = create_telegram_bot_guide()
            if has_token:
                test_telegram_bot()
        elif sys.argv[1] == "--start":
            start_bot_interactive()
        elif sys.argv[1] == "--guide":
            create_telegram_bot_guide()
        else:
            print("Usage: python telegram_setup.py [--guide|--test|--start]")
    else:
        # Default: show guide and test
        has_token = create_telegram_bot_guide()
        if has_token:
            print("\n" + "="*60)
            print("Run with --start to launch the bot!")
            print("="*60)

if __name__ == "__main__":
    main()
