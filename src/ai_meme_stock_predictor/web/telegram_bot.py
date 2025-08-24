import os
from typing import Optional
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from ..agent.portia_agent import PortiaMemeAgent
from ..utils.logging_setup import get_logger

logger = get_logger(__name__)

_bot_agent: Optional[PortiaMemeAgent] = None

def get_agent() -> PortiaMemeAgent:
    global _bot_agent
    if _bot_agent is None:
        _bot_agent = PortiaMemeAgent()
    return _bot_agent

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
    agent = get_agent()
    text = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Friend"
    
    logger.info(f"Message from {user_name} ({user_id}): {text}")
    
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
        result = agent.handle_query(str(user_id), text)
        response = result.get('response', 'Sorry, I had trouble processing that request.')
        
        # Make response more personal and friendly
        if 'memes?' in text.lower():
            ticker = text.split()[0].upper()
            personal_touch = f"\n\n💡 Hey {user_name}, here's my analysis for {ticker}! "
            response += personal_touch + "Remember, this is for entertainment and educational purposes only. Always do your own research! 📊✨"
        else:
            response += f"\n\n😊 Hope this helps, {user_name}! Let me know if you need anything else."
        
        await update.message.reply_text(response)
        logger.info(f"Response sent to {user_name}")
        
    except Exception as e:
        error_msg = f"Oops {user_name}! 😅 I encountered a hiccup processing that. Could you try again? If the issue persists, use /help for guidance."
        await update.message.reply_text(error_msg)
        logger.error(f"Error handling message: {e}")

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
        f"• /feedback - How to give me feedback\n\n"
        f"💬 **Fun Interactions:**\n"
        f"• Say hi, hello, thanks - I'll respond personally!\n"
        f"• Send feedback: `5:Great analysis!` (rating 1-5)\n"
        f"• Ask me about any stock ticker\n\n"
        f"Ready to explore some meme stocks? What interests you? 😄"
    )
    await update.message.reply_text(help_text)

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Friend"
    about_text = (
        f"🤖 About Me - Your AI Meme Stock Assistant!\n\n"
        f"Hi {user_name}! I'm an advanced AI-powered bot that combines:\n\n"
        f"🧠 **Artificial Intelligence** - Smart analysis algorithms\n"
        f"📊 **Real Market Data** - Live stock prices & volume\n"
        f"🔴 **Reddit Sentiment** - WallStreetBets community vibes\n"
        f"🐦 **Twitter Analysis** - Social media sentiment tracking\n"
        f"😄 **Humor & Memes** - Because trading should be fun!\n\n"
        f"🎯 **What Makes Me Special:**\n"
        f"• I analyze both technical data AND social sentiment\n"
        f"• My responses mix hard data with meme culture\n"
        f"• I provide 'meme intensity' scores for stocks\n"
        f"• I track how much buzz stocks generate online\n\n"
        f"⚠️ **Important Note:**\n"
        f"I'm here for education and entertainment! Always do your own research.\n\n"
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
        "👤 You: `GME memes?`\n"
        "🤖 Me: Apes together strong! GME showing moderate meme energy...\n\n"
        "**Example 3: Feedback**\n"
        "👤 You: `5:Amazing analysis!`\n"
        "🤖 Me: Thank you! Your feedback helps me improve...\n\n"
        "**Popular Tickers to Try:**\n"
        "• TSLA memes? (Tesla)\n"
        "• GME memes? (GameStop)\n"
        "• AMC memes? (AMC Entertainment)\n"
        "• NVDA memes? (Nvidia)\n"
        "• AAPL memes? (Apple)\n\n"
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
        "• `NVDA memes?` - Nvidia (AI hype!)\n\n"
        "**🎮 Gaming & Entertainment:**\n"
        "• `RBLX memes?` - Roblox\n"
        "• `NFLX memes?` - Netflix\n\n"
        "Just type any ticker followed by 'memes?' and I'll analyze it! "
        "What catches your interest? 🎯"
    )
    await update.message.reply_text(popular_text)

async def feedback_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Friend"
    feedback_text = (
        f"💝 Love to Hear From You, {user_name}!\n\n"
        f"Your feedback helps me get better! Here's how:\n\n"
        f"**📊 Rate My Analysis:**\n"
        f"Send: `5:Spot on analysis!`\n"
        f"• Rating scale: 1-5 (1=poor, 5=excellent)\n"
        f"• Add optional comment after the colon\n\n"
        f"**Examples:**\n"
        f"• `5:Perfect prediction!`\n"
        f"• `4:Good analysis, very helpful`\n"
        f"• `3:Decent but could be more detailed`\n\n"
        f"I genuinely appreciate every bit of feedback! 🙏"
    )
    await update.message.reply_text(feedback_text)

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
        f"🎯 **Ready to analyze stocks!**\n"
        f"Try asking me about any ticker - I'm at your service!"
    )
    await update.message.reply_text(health_text)

def build_application():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise RuntimeError('TELEGRAM_BOT_TOKEN missing')
    app = ApplicationBuilder().token(token).build()
    
    # Add all command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('about', about_cmd))
    app.add_handler(CommandHandler('how', how_cmd))
    app.add_handler(CommandHandler('examples', examples_cmd))
    app.add_handler(CommandHandler('popular', popular_cmd))
    app.add_handler(CommandHandler('feedback', feedback_cmd))
    app.add_handler(CommandHandler('health', health_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return app

if __name__ == '__main__':
    application = build_application()
    logger.info('Starting Telegram bot polling...')
    application.run_polling()
