EXPLANATION_TEMPLATE = """This playful output mixes meme intensity (how often hype slang & hashtags appear), average social sentiment (VADER), and finance-specific sentiment (FinBERT). It is NOT financial advice, only an educational illustration of how online chatter *might* correlate with perceived momentum.\n\nKey metrics:\n- Meme Intensity: {meme_intensity}\n- Social Sentiment: {social_sentiment}\n- Financial Sentiment: {financial_sentiment}\n"""

HUMOR_TEMPLATES = [
    "The {ticker} hype-o-meter says: {direction} {emoji}! Meme engines warming up.",
    "Consensus of the apes: {direction} {emoji}. Diamond hands optional.",
    "Charts? Nah. Memes predict {direction} {emoji} for {ticker}." ,
]

FEEDBACK_PROMPT = "Did this feel fun and at least a bit insightful? (yes/no/more detail)"
