# 🤖 TELEGRAM BOT SETUP - DETAILED INSTRUCTIONS

## 🎯 Quick Summary
You need to create a Telegram bot using @BotFather, get a token, and add it to your .env file.

## 📱 Step 1: Create Your Bot with @BotFather

### Option A: On Mobile/Desktop Telegram App
1. Open Telegram
2. Search for **@BotFather** (verified account with blue checkmark)
3. Start a conversation
4. Send: `/newbot`
5. BotFather will ask for a bot name: `AI Meme Stock Predictor`
6. BotFather will ask for a username: `your_username_meme_bot` (must end in 'bot')
7. **COPY THE TOKEN** that BotFather gives you!

### Option B: Via Telegram Web
1. Go to https://web.telegram.org
2. Search for **@BotFather**
3. Follow the same steps as above

## 🔧 Step 2: Add Token to Configuration

Once you have your token, add it to your `.env` file:

```bash
# Add this line to your .env file:
TELEGRAM_BOT_TOKEN="1234567890:ABCDEF1234567890abcdef1234567890ABC"
```

**Example .env file:**
```properties
ALPHAVANTAGE_API_KEY="7N1KWAJ7MJRGFG0R"
REDDIT_CLIENT_ID="gWykzN2BoN30bEUq0SwpEw"
REDDIT_CLIENT_SECRET="cZuXzXnUdmsPFsUpFxKlU3PMI7OGCw"
REDDIT_USER_AGENT="python:meme-stock-predictor:v1.0:Slow-Coat-3408"
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAM%2Fb3gEAAAAAXggwkvi4vZxfOoH%2FEsV73DXyLrU%3DHI6Ftt3nMc6LcHZC5Grm6GPjpKuHqffDc5nxcHlckgyfke3hHT"
TELEGRAM_BOT_TOKEN="your_token_from_botfather_here"
```

## 🧪 Step 3: Test Your Setup

After adding the token, test it:
```bash
python telegram_setup.py --test
```

## 🚀 Step 4: Start Your Bot

Start the bot server:
```bash
python -m src.ai_meme_stock_predictor.web.telegram_bot
```

## 💬 Step 5: Chat with Your Bot

1. In Telegram, search for your bot by the username you chose
2. Start a conversation
3. Send: `/start`
4. Try: `TSLA memes?`

## 🎮 Bot Commands

Your bot will support these commands:
- `/start` - Welcome message and setup
- `/help` - Show available commands  
- `/health` - Check bot status
- `<TICKER> memes?` - Analyze any stock (TSLA, GME, AMC, etc.)
- Feedback format: `5:Great analysis!`

## 🔧 Advanced Configuration (Optional)

### Set Bot Description
Send to @BotFather:
```
/setdescription
[Select your bot]
AI-powered meme stock sentiment analyzer. Send ticker symbols like "TSLA memes?" for analysis.
```

### Set Bot Commands Menu
Send to @BotFather:
```
/setcommands
[Select your bot]
start - Initialize the bot
help - Show available commands
health - Check bot status
```

### Set Bot Profile Picture
Send to @BotFather:
```
/setuserpic
[Select your bot]
[Upload an image]
```

## 🛠️ Troubleshooting

### Token Format
- Should look like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
- Contains numbers, colon, then letters/numbers/hyphens

### Common Issues
1. **"TELEGRAM_BOT_TOKEN missing"** → Add token to .env file
2. **"Unauthorized"** → Check token is correct
3. **Bot doesn't respond** → Make sure bot is running and you clicked "Start"

### Testing Commands
```bash
# Check configuration
python api_status.py

# Test bot setup
python telegram_setup.py --test

# Start bot
python telegram_setup.py --start
```

## ✅ Success Indicators

You'll know it's working when:
1. ✅ `python telegram_setup.py --test` passes
2. ✅ Bot starts without errors
3. ✅ You can send `/start` in Telegram
4. ✅ Bot responds to `TSLA memes?`

---

**Next**: Once you have your token, let me know and I'll help you test and start the bot!
