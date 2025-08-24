from typing import List, Dict
import praw
import warnings
from ..utils.config import settings
from ..utils.logging_setup import get_logger

# Suppress PRAW async warnings since we handle it properly
warnings.filterwarnings("ignore", message="It appears that you are using PRAW in an asynchronous environment")

logger = get_logger(__name__)

class RedditSource:
    def __init__(self):
        if not settings.reddit_client_id:
            logger.warning("Reddit credentials missing; RedditSource disabled")
            self._client = None
        else:
            self._client = praw.Reddit(
                client_id=settings.reddit_client_id,
                client_secret=settings.reddit_client_secret,
                user_agent=settings.reddit_user_agent,
            )

    def fetch_mentions(self, ticker: str, limit: int = 50) -> List[Dict]:
        if not self._client:
            logger.warning("Reddit client not configured")
            return []
        
        try:
            query = f"{ticker}"
            submissions = self._client.subreddit("wallstreetbets").search(query, limit=limit, sort="new")
            results = []
            for s in submissions:
                results.append({
                    "id": s.id,
                    "title": s.title,
                    "selftext": s.selftext,
                    "score": s.score,
                    "num_comments": s.num_comments,
                    "created_utc": s.created_utc,
                    "url": s.url,
                })
            logger.info(f"Reddit fetched {len(results)} posts for {ticker}")
            return results
        except Exception as e:
            logger.error(f"Reddit API error for {ticker}: {e}")
            return []
