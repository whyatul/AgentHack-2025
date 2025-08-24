#!/usr/bin/env python3
"""
Add Telegram Bot Token to .env file
"""

import os
import sys

def add_telegram_token():
    """Helper to add Telegram token to .env file"""
    
    if len(sys.argv) < 2:
        print("🤖 Telegram Token Setup")
        print("=" * 30)
        print("\nUsage: python add_telegram_token.py YOUR_BOT_TOKEN")
        print("\nExample:")
        print("python add_telegram_token.py 123456789:ABCDEF1234567890abcdef1234567890ABC")
        print("\nTo get a token:")
        print("1. Message @BotFather on Telegram")  
        print("2. Send /newbot")
        print("3. Follow the instructions")
        print("4. Copy the token and run this script")
        return
    
    token = sys.argv[1]
    
    # Validate token format
    if not ":" in token or len(token) < 20:
        print("❌ Invalid token format!")
        print("Token should look like: 123456789:ABCDEF1234567890abcdef1234567890ABC")
        return
    
    env_file = "/home/am/AgentHack-2025/.env"
    
    # Read current .env content
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
    else:
        content = ""
    
    # Check if TELEGRAM_BOT_TOKEN already exists
    if "TELEGRAM_BOT_TOKEN=" in content:
        print("⚠️  TELEGRAM_BOT_TOKEN already exists in .env file")
        response = input("Do you want to update it? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
        
        # Replace existing token
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('TELEGRAM_BOT_TOKEN=') or line.startswith('# TELEGRAM_BOT_TOKEN='):
                new_lines.append(f'TELEGRAM_BOT_TOKEN="{token}"')
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
    else:
        # Add new token
        if content and not content.endswith('\n'):
            content += '\n'
        content += f'TELEGRAM_BOT_TOKEN="{token}"\n'
    
    # Write updated content
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Telegram bot token added to {env_file}")
    print(f"Token: {token[:10]}...{token[-10:]}")
    
    # Test the configuration
    print("\n🧪 Testing configuration...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from src.ai_meme_stock_predictor.utils.config import get_settings
        settings = get_settings()
        
        if settings.telegram_bot_token == token:
            print("✅ Token successfully loaded!")
            
            # Test bot creation
            try:
                from src.ai_meme_stock_predictor.web.telegram_bot import build_application
                app = build_application()
                print("✅ Bot application created successfully!")
                
                print("\n🚀 Ready to start your bot!")
                print("Run: python telegram_setup.py --start")
                print("Or: python -m src.ai_meme_stock_predictor.web.telegram_bot")
                
            except Exception as e:
                print(f"❌ Bot creation failed: {e}")
        else:
            print("❌ Token not loaded correctly")
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")

if __name__ == "__main__":
    add_telegram_token()
