from typing import Dict
from ..data_sources.reddit_source import RedditSource
from ..data_sources.twitter_source import TwitterSource
from ..data_sources.market_data import MarketData
from ..analysis.features import build_features
from ..models.predictor import MemeStockPredictor
from ..agent.prompts import EXPLANATION_TEMPLATE, HUMOR_TEMPLATES
from ..utils.logging_setup import get_logger
import random

logger = get_logger(__name__)

class MemeStockWorkflow:
    def __init__(self):
        self.reddit = RedditSource()
        self.twitter = TwitterSource()
        self.market = MarketData()
        self.predictor = MemeStockPredictor()

    def run(self, ticker: str) -> Dict:
        logger.info(f"Workflow run for ticker {ticker}")
        reddit_posts = self.reddit.fetch_mentions(ticker)
        tweets = self.twitter.fetch_mentions(ticker)
        quote = self.market.quote(ticker)
        feats = build_features(ticker, reddit_posts, tweets, quote)
        pred = self.predictor.predict(feats)
        humor = random.choice(HUMOR_TEMPLATES).format(ticker=ticker.upper(), **pred)
        explanation = EXPLANATION_TEMPLATE.format(**feats)
        return {
            'ticker': ticker.upper(),
            'features': feats,
            'prediction': pred,
            'message': humor,
            'explanation': explanation
        }
