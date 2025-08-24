from typing import List, Dict
import requests
from ..utils.config import settings
from ..utils.logging_setup import get_logger

logger = get_logger(__name__)

TWITTER_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

class TwitterSource:
    def __init__(self):
        self.bearer = settings.twitter_bearer_token
        if not self.bearer:
            logger.warning("Twitter bearer token missing; TwitterSource disabled")

    def fetch_mentions(self, ticker: str, limit: int = 10) -> List[Dict]:
        if not self.bearer:
            logger.warning("Twitter bearer token missing")
            return []
        
        headers = {"Authorization": f"Bearer {self.bearer}"}
        params = {
            "query": f"({ticker} OR ${ticker}) -is:retweet lang:en",
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,author_id,public_metrics"
        }
        
        try:
            r = requests.get(TWITTER_SEARCH_URL, headers=headers, params=params, timeout=10)
            if r.status_code == 429:
                logger.warning(f"Twitter API rate limit reached for {ticker} - returning empty list")
                return []
            elif r.status_code == 403:
                logger.warning(f"Twitter API access forbidden for {ticker} - check credentials")
                return []
            elif r.status_code != 200:
                logger.error(f"Twitter API error {r.status_code} for {ticker}: {r.text[:200]}")
                return []
                
            data = r.json().get('data', [])
            results = []
            for tweet in data:
                results.append({
                    'text': tweet.get('text', ''),
                    'created_at': tweet.get('created_at', ''),
                    'author_id': tweet.get('author_id', ''),
                    'retweets': tweet.get('public_metrics', {}).get('retweet_count', 0),
                    'likes': tweet.get('public_metrics', {}).get('like_count', 0)
                })
            
            logger.info(f"Fetched {len(results)} tweets for {ticker}")
            return results
            
        except requests.exceptions.Timeout:
            logger.warning(f"Twitter API timeout for {ticker}")
            return []
        except Exception as e:
            logger.error(f"Twitter API error for {ticker}: {e}")
            return []
