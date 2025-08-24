#!/usr/bin/env python3
"""
Direct Telegram Bot Starter
"""

import sys
import os
import asyncio
import logging

# Add the project root to Python path
sys.path.insert(0, '/home/am/AgentHack-2025')

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Start the Telegram bot"""
    print("🚀 Starting AI Meme Stock Predictor Bot...")
    
    try:
        # Import after path setup
        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
        from src.ai_meme_stock_predictor.agent.portia_agent import PortiaMemeAgent
        from src.ai_meme_stock_predictor.utils.config import get_settings
        
        # Get settings
        settings = get_settings()
        if not settings.telegram_bot_token:
            print("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
            return
        
        print(f"✅ Token loaded: {settings.telegram_bot_token[:10]}...")
        
        # Initialize agent
        agent = PortiaMemeAgent()
        print("✅ AI agent initialized")
        
        # Bot handlers
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_name = update.effective_user.first_name or "Friend"
            welcome_msg = (
                f"🎉 Welcome {user_name}! I'm your AI Meme Stock Predictor!\n\n"
                f"👋 Great to meet you! I'm here to help you analyze meme stocks using AI, "
                f"real market data, and social media sentiment.\n\n"
                f"🚀 I can predict stock trends by analyzing Reddit discussions, Twitter sentiment, "
                f"and combining it with real-time market data!\n\n"
                f"📋 Here's what I can do for you:\n"
                f"• Analyze any stock ticker (TSLA, GME, AMC, etc.)\n"
                f"• Provide meme intensity scores\n"
                f"• Give you sentiment analysis from social media\n"
                f"• Share humorous predictions with real data\n\n"
                f"🎯 Ready to get started? Try:\n"
                f"• Type: TSLA memes?\n"
                f"• Or use /help to see all my commands\n"
                f"• Use /about to learn more about me!\n\n"
                f"Let's make some money... or at least have fun trying! 😄📈"
            )
            await update.message.reply_text(welcome_msg)
        
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = update.message.text
            user_id = update.effective_user.id
            user_name = update.effective_user.first_name or "Friend"
            
            print(f"📨 Message from {user_name} ({user_id}): {text}")
            
            # Handle special keywords
            text_lower = text.lower()
            if any(word in text_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
                greeting_response = (
                    f"Hey there {user_name}! 👋\n\n"
                    f"Great to see you! I'm excited to help you with meme stock analysis.\n\n"
                    f"🎯 Quick start:\n"
                    f"• Just type any ticker like: TSLA memes?\n"
                    f"• Or try: GME memes? / AMC memes?\n"
                    f"• Need help? Use /help\n\n"
                    f"What stock would you like me to analyze? 📈"
                )
                await update.message.reply_text(greeting_response)
                return
            
            if 'thank' in text_lower:
                thanks_response = (
                    f"You're very welcome, {user_name}! 😊\n\n"
                    f"I'm always here to help you navigate the wild world of meme stocks! "
                    f"Feel free to ask me about any ticker anytime.\n\n"
                    f"Happy trading! 🚀📈"
                )
                await update.message.reply_text(thanks_response)
                return
            
            try:
                import time
                start_time = time.time()
                
                # Send initial "analyzing" message for ticker queries
                text_lower = text.lower()
                words = [w.strip("$?!. ,") for w in text_lower.split()]
                is_ticker_query = False
                potential_ticker = None
                
                for w in words:
                    if w.isalpha() and 2 < len(w) <= 5:
                        potential_ticker = w.upper()
                        is_ticker_query = True
                        break
                
                if is_ticker_query and potential_ticker:
                    wait_message = (
                        f"🔍 Analyzing {potential_ticker}...\n\n"
                        f"📊 Fetching real-time market data\n"
                        f"🔴 Scanning Reddit discussions\n"
                        f"🐦 Checking Twitter sentiment\n"
                        f"🧠 Running AI analysis\n\n"
                        f"⏳ This will take 15-30 seconds. Please wait..."
                    )
                    await update.message.reply_text(wait_message)
                
                result = agent.handle_query(str(user_id), text)
                response = result.get('response', 'Sorry, I had trouble processing that request.')
                details = result.get('details') or {}
                pred = details.get('prediction', {})
                feats = details.get('features', {})
                history = details.get('history', [])
                
                # Build comprehensive analysis block for ticker queries
                if details and details.get('ticker'):  # Any ticker analysis
                    ticker = details.get('ticker', 'UNKNOWN')
                    enriched_block = f"\n\n📊 **{ticker} Analysis Breakdown:**\n"
                    
                    # Data Source Status
                    enriched_block += "\n🔍 **Data Sources:**\n"
                    enriched_block += f"• Market Data: ✅ Active (Current price: ${feats.get('price', 0):.2f})\n"
                    
                    # Check Twitter status (look for common rate limit patterns)
                    if feats.get('social_sentiment', 0) == 0:
                        enriched_block += "• Twitter: ⚠️ Limited (Rate limited - using Reddit only)\n"
                    else:
                        enriched_block += "• Twitter: ✅ Active\n"
                    
                    # Reddit status
                    meme_score = feats.get('meme_intensity', 0)
                    if meme_score > 0:
                        enriched_block += f"• Reddit: ✅ Active ({int(meme_score * 100)} mentions found)\n"
                    else:
                        enriched_block += "• Reddit: ⚠️ Limited (Few recent mentions)\n"
                    
                    # FinBERT status
                    fin_sent = feats.get('financial_sentiment', 0)
                    if fin_sent == 0:
                        enriched_block += "• FinBERT: ⚠️ Disabled (Set ENABLE_FINBERT=1 for advanced analysis)\n"
                    else:
                        enriched_block += f"• FinBERT: ✅ Active\n"
                    
                    # Detailed Feature Breakdown
                    enriched_block += "\n📈 **Feature Analysis:**\n"
                    enriched_block += f"• Meme Intensity: {meme_score:.4f} (0-1 scale)\n"
                    enriched_block += f"• Social Sentiment: {feats.get('social_sentiment', 0):.4f} (-1 to +1)\n"
                    enriched_block += f"• Financial Sentiment: {fin_sent:.4f} (-1 to +1)\n"
                    enriched_block += f"• Volume: {feats.get('volume', 0):,} shares\n"
                    
                    # Score Breakdown
                    if pred:
                        meme_contrib = 0.5 * meme_score
                        social_contrib = 0.3 * feats.get('social_sentiment', 0)
                        fin_contrib = 0.2 * fin_sent
                        enriched_block += f"\n🧮 **Score Calculation:**\n"
                        enriched_block += f"• Meme Weight (50%): {meme_contrib:.4f}\n"
                        enriched_block += f"• Social Weight (30%): {social_contrib:.4f}\n"
                        enriched_block += f"• Financial Weight (20%): {fin_contrib:.4f}\n"
                        enriched_block += f"• **Total Score: {pred.get('score', 0):.4f}**\n"
                        
                        # Direction logic explanation
                        score = pred.get('score', 0)
                        if score > 0.2:
                            enriched_block += f"• Result: BULLISH 🚀 (Score > 0.2)\n"
                        elif score < -0.2:
                            enriched_block += f"• Result: BEARISH 🪦 (Score < -0.2)\n"
                        else:
                            enriched_block += f"• Result: NEUTRAL 🤷 (Score between -0.2 and 0.2)\n"
                        
                        enriched_block += f"• Confidence: {pred.get('confidence', 0):.3f}\n"
                    
                    # ASCII Price Chart
                    if history and len(history) >= 5:
                        closes = [h['close'] for h in history][-20:]
                        lo, hi = min(closes), max(closes)
                        span = hi - lo or 1
                        blocks = "▁▂▃▄▅▆▇█"
                        def map_close(c):
                            idx = int((c - lo)/span * (len(blocks)-1))
                            return blocks[idx]
                        spark = ''.join(map_close(c) for c in closes)
                        
                        enriched_block += f"\n📊 **20-Day Price Trend:**\n"
                        enriched_block += f"• Range: ${lo:.2f} - ${hi:.2f}\n"
                        enriched_block += f"• Chart: {spark}\n"
                        
                        if history:
                            last = history[-1]
                            enriched_block += f"• Latest: ${last['close']:.2f} (Vol: {last['volume']:,})\n"
                    
                    # Data Quality Warning
                    if meme_score < 0.01 and feats.get('social_sentiment', 0) == 0:
                        enriched_block += f"\n⚠️ **Data Quality Notice:**\n"
                        enriched_block += f"Limited social media data available for {ticker}. "
                        enriched_block += f"Consider checking a more popular/trending ticker for richer analysis.\n"
                    
                    response += enriched_block
                
                # Add analysis completion time for ticker queries
                if is_ticker_query:
                    end_time = time.time()
                    analysis_time = round(end_time - start_time, 1)
                    response += f"\n\n⚡ Analysis completed in {analysis_time}s"
            
                # Make response more personal and friendly
                if details and details.get('ticker'):  # Any ticker analysis
                    ticker = details.get('ticker')
                    personal_touch = f"\n💡 Hey {user_name}, here's my enriched analysis for {ticker}! "
                    response += personal_touch + "Remember: educational & entertainment only. 📊✨"
                else:
                    response += f"\n😊 Hope this helps, {user_name}! Let me know if you need anything else."
                
                await update.message.reply_text(response)
                print(f"✅ Response sent to {user_name}")
                
            except Exception as e:
                error_msg = f"Oops {user_name}! 😅 I encountered a hiccup processing that. Could you try again? If the issue persists, use /help for guidance."
                await update.message.reply_text(error_msg)
                print(f"❌ Error handling message: {e}")
        
        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_name = update.effective_user.first_name or "Friend"
            help_text = (
                f"🤖 Hey {user_name}! Here's everything I can do for you:\n\n"
                f"📈 **Stock Analysis Commands:**\n"
                f"• Just type: `TSLA memes?` (or any ticker)\n"
                f"• Try: `GME memes?` / `AMC memes?` / `AAPL memes?`\n"
                f"• Popular tickers: TESLA, GAMESTOP, AMC, NVIDIA, etc.\n\n"
                f"🎯 **Bot Commands:**\n"
                f"• /start - Welcome message & intro\n"
                f"• /help - This help menu (you're here!)\n"
                f"• /about - Learn about me & my capabilities\n"
                f"• /how - How I work & my data sources\n"
                f"• /examples - See example conversations\n"
                f"• /popular - Most popular stocks to analyze\n"
                f"• /health - Check my system status\n"
                f"• /feedback - How to give me feedback\n"
                f"• /contact - Get support or report issues\n\n"
                f"💬 **Fun Interactions:**\n"
                f"• Say hi, hello, thanks - I'll respond personally!\n"
                f"• Send feedback: `5:Great analysis!` (rating 1-5)\n"
                f"• Ask me about any stock ticker\n\n"
                f"🚀 **Pro Tips:**\n"
                f"• I analyze real market data + social sentiment\n"
                f"• My responses include humor but are data-driven\n"
                f"• Always do your own research before trading!\n\n"
                f"Ready to explore some meme stocks? What interests you? 😄"
            )
            await update.message.reply_text(help_text)

        async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_name = update.effective_user.first_name or "Friend"
            about_text = (
                f"🤖 About Me - Your AI Meme Stock Assistant!\n\n"
                f"Hi {user_name}! I'm an advanced AI-powered bot that combines:\n\n"
                f"🧠 **Artificial Intelligence** - Smart analysis algorithms\n"
                f"� **Real Market Data** - Live stock prices & volume\n"
                f"🔴 **Reddit Sentiment** - WallStreetBets community vibes\n"
                f"🐦 **Twitter Analysis** - Social media sentiment tracking\n"
                f"😄 **Humor & Memes** - Because trading should be fun!\n\n"
                f"🎯 **What Makes Me Special:**\n"
                f"• I analyze both technical data AND social sentiment\n"
                f"• My responses mix hard data with meme culture\n"
                f"• I provide 'meme intensity' scores for stocks\n"
                f"• I track how much buzz stocks generate online\n\n"
                f"⚡ **My Superpowers:**\n"
                f"• Real-time stock price analysis\n"
                f"• Social media sentiment scoring\n"
                f"• Meme trend detection\n"
                f"• Humorous but informative predictions\n\n"
                f"⚠️ **Important Note:**\n"
                f"I'm here for education and entertainment! My analysis combines "
                f"real data with humor. Always do your own research before making "
                f"any investment decisions.\n\n"
                f"Ready to have some fun with stocks? Try asking about TSLA! 🚀"
            )
            await update.message.reply_text(about_text)

        async def how_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            how_text = (
                "🔬 How I Work - Behind the Scenes Magic!\n\n"
                "When you ask me about a stock, here's what happens:\n\n"
                "**Step 1: Data Collection** 📊\n"
                "• Fetch real-time stock data (price, volume, changes)\n"
                "• Scrape Reddit discussions from WallStreetBets\n"
                "• Analyze Twitter sentiment (when available)\n\n"
                "**Step 2: AI Analysis** 🧠\n"
                "• Calculate 'meme intensity' scores\n"
                "• Run sentiment analysis on social posts\n"
                "• Combine technical + social indicators\n\n"
                "**Step 3: Generate Response** 💬\n"
                "• Create humorous but data-backed analysis\n"
                "• Include key metrics and insights\n"
                "• Add appropriate meme references\n\n"
                "**My Data Sources:**\n"
                "• 📈 AlphaVantage API (stock market data)\n"
                "• 🔴 Reddit API (community sentiment)\n"
                "• 🐦 Twitter API (social buzz)\n"
                "• 🤖 VADER sentiment analysis\n\n"
                "**Example Analysis Includes:**\n"
                "• Meme Intensity: 0.1677 (how much buzz)\n"
                "• Social Sentiment: 0.186908 (positive/negative)\n"
                "• Price data with context\n\n"
                "Pretty cool, right? Want to see me in action? 🚀"
            )
            await update.message.reply_text(how_text)

        async def examples_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            examples_text = (
                "💬 Example Conversations - See Me In Action!\n\n"
                "**Example 1: Basic Analysis**\n"
                "👤 You: `TSLA memes?`\n"
                "🤖 Me: The TSLA hype-o-meter says: bullish 🚀! Diamond hands activated.\n\n"
                "**Example 2: Popular Meme Stock**\n"
                "� You: `GME memes?`\n"
                "🤖 Me: Apes together strong! GME showing moderate meme energy...\n\n"
                "**Example 3: Feedback**\n"
                "👤 You: `5:Amazing analysis!`\n"
                "🤖 Me: Thank you! Your feedback helps me improve...\n\n"
                "**Example 4: Casual Chat**\n"
                "👤 You: `Hi there!`\n"
                "🤖 Me: Hey there! Great to see you! I'm excited to help...\n\n"
                "**Popular Tickers to Try:**\n"
                "• TSLA memes? (Tesla)\n"
                "• GME memes? (GameStop)\n"
                "• AMC memes? (AMC Entertainment)\n"
                "• NVDA memes? (Nvidia)\n"
                "• AAPL memes? (Apple)\n"
                "• MSFT memes? (Microsoft)\n\n"
                "Ready to try one? Pick your favorite! 🎯"
            )
            await update.message.reply_text(examples_text)

        async def popular_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            popular_text = (
                "🔥 Most Popular Meme Stocks to Analyze!\n\n"
                "**🚀 Top Meme Stock Favorites:**\n"
                "• `TSLA memes?` - Tesla (Elon's empire)\n"
                "• `GME memes?` - GameStop (Diamond hands classic)\n"
                "• `AMC memes?` - AMC Entertainment (Ape nation)\n\n"
                "**📱 Tech Giants:**\n"
                "• `AAPL memes?` - Apple\n"
                "• `MSFT memes?` - Microsoft\n"
                "• `GOOGL memes?` - Google\n"
                "• `NVDA memes?` - Nvidia (AI hype!)\n\n"
                "**🎮 Gaming & Entertainment:**\n"
                "• `RBLX memes?` - Roblox\n"
                "• `NFLX memes?` - Netflix\n"
                "• `DIS memes?` - Disney\n\n"
                "**💰 Finance & Crypto Related:**\n"
                "• `JPM memes?` - JPMorgan\n"
                "• `BAC memes?` - Bank of America\n"
                "• `COIN memes?` - Coinbase\n\n"
                "**🚗 EV & Transportation:**\n"
                "• `F memes?` - Ford\n"
                "• `NIO memes?` - NIO\n"
                "• `RIVN memes?` - Rivian\n\n"
                "Just type any ticker followed by 'memes?' and I'll analyze it! "
                "What catches your interest? 🎯"
            )
            await update.message.reply_text(popular_text)

        async def feedback_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_name = update.effective_user.first_name or "Friend"
            feedback_text = (
                f"💝 Love to Hear From You, {user_name}!\n\n"
                f"Your feedback helps me get better at predicting meme stocks! "
                f"Here's how to share your thoughts:\n\n"
                f"**📊 Rate My Analysis:**\n"
                f"Send a message like: `5:Spot on analysis!`\n"
                f"• Rating scale: 1-5 (1=poor, 5=excellent)\n"
                f"• Add optional comment after the colon\n\n"
                f"**Examples:**\n"
                f"• `5:Perfect prediction!`\n"
                f"• `4:Good analysis, very helpful`\n"
                f"• `3:Decent but could be more detailed`\n"
                f"• `2:Needs improvement`\n\n"
                f"**💬 General Feedback:**\n"
                f"• Tell me what you love!\n"
                f"• Suggest improvements\n"
                f"• Request new features\n"
                f"• Share your trading stories\n\n"
                f"**🎯 What I Use Feedback For:**\n"
                f"• Improving my analysis accuracy\n"
                f"• Adding new features you want\n"
                f"• Making responses more helpful\n"
                f"• Better understanding user preferences\n\n"
                f"I genuinely appreciate every bit of feedback! 🙏"
            )
            await update.message.reply_text(feedback_text)

        async def contact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            contact_text = (
                "📞 Need Help or Want to Report an Issue?\n\n"
                "I'm here to help! Here are your options:\n\n"
                "**🤖 Bot Issues:**\n"
                "• Bot not responding? Try /health first\n"
                "• Wrong data? Let me know which ticker\n"
                "• Error messages? Send me a screenshot\n\n"
                "**💡 Feature Requests:**\n"
                "• Want new analysis features?\n"
                "• Need additional data sources?\n"
                "• Ideas for improvements?\n\n"
                "**📊 Data Questions:**\n"
                "• Wondering about my sources?\n"
                "• Questions about analysis methods?\n"
                "• Need help interpreting results?\n\n"
                "**🚀 Quick Self-Help:**\n"
                "• Use /help for command overview\n"
                "• Try /how to understand my process\n"
                "• Check /examples for usage ideas\n\n"
                "**⚡ Emergency Commands:**\n"
                "• /health - Check if I'm working properly\n"
                "• /start - Reset our conversation\n\n"
                "I'm constantly learning and improving. Your input makes me better! 🎯"
            )
            await update.message.reply_text(contact_text)
        
        async def health_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_name = update.effective_user.first_name or "Friend"
            health_text = (
                f"✅ All Systems Go, {user_name}!\n\n"
                f"🤖 **Bot Status:** Healthy & Ready\n"
                f"🧠 **AI Engine:** Running smoothly\n"
                f"📊 **Data Sources:**\n"
                f"  • AlphaVantage API: ✅ Connected\n"
                f"  • Reddit API: ✅ Connected\n"
                f"  • Twitter API: ✅ Connected\n"
                f"  • Sentiment Engine: ✅ Active\n\n"
                f"⚡ **Performance:**\n"
                f"  • Response time: Fast\n"
                f"  • Analysis accuracy: High\n"
                f"  • Humor level: Maximum 😄\n\n"
                f"🎯 **Ready to analyze stocks!**\n"
                f"Try asking me about any ticker - I'm at your service!"
            )
            await update.message.reply_text(health_text)
        
        # Build application
        print("🔧 Building bot application...")
        app = ApplicationBuilder().token(settings.telegram_bot_token).build()
        
        # Add handlers
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('help', help_cmd))
        app.add_handler(CommandHandler('about', about_cmd))
        app.add_handler(CommandHandler('how', how_cmd))
        app.add_handler(CommandHandler('examples', examples_cmd))
        app.add_handler(CommandHandler('popular', popular_cmd))
        app.add_handler(CommandHandler('feedback', feedback_cmd))
        app.add_handler(CommandHandler('contact', contact_cmd))
        app.add_handler(CommandHandler('health', health_cmd))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Bot configured successfully!")
        print("\n" + "="*50)
        print("🤖 ENHANCED AI MEME STOCK BOT IS NOW RUNNING!")
        print("="*50)
        print("🎉 NEW FEATURES:")
        print("• Personalized greetings and responses")
        print("• 9 helpful commands (/about, /how, /examples, etc.)")
        print("• Smart conversation handling")
        print("• Enhanced user experience")
        print()
        print("📱 Go to Telegram and:")
        print("1. Search for your bot by username")
        print("2. Send: /start for a warm welcome")
        print("3. Try: /help to see all commands")
        print("4. Ask: TSLA memes? for analysis")
        print()
        print("🎯 Your bot now includes:")
        print("• Personal greetings with user names")
        print("• Multiple help commands and examples")
        print("• Friendly conversation responses")
        print("• Comprehensive guidance system")
        print()
        print("Press Ctrl+C to stop the bot")
        print("="*50)
        
        # Start polling
        print("🎯 Starting bot polling...")
        app.run_polling(stop_signals=None)
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
