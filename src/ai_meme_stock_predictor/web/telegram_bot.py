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
    await update.message.reply_text("Meme Stock Bot ready. Ask: 'TSLA memes?' or send feedback:<rating>:<notes>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agent = get_agent()
    text = update.message.text
    conv_id = str(update.effective_chat.id)
    result = agent.handle_query(conv_id, text)
    await update.message.reply_text(result.get('response', ''))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a ticker + 'memes?' e.g. 'GME memes?'")

async def health_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok")

def build_application():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise RuntimeError('TELEGRAM_BOT_TOKEN missing')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('health', health_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

if __name__ == '__main__':
    application = build_application()
    logger.info('Starting Telegram bot polling...')
    application.run_polling()
