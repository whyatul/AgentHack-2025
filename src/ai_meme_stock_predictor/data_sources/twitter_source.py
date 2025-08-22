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

    def fetch_mentions(self, ticker: str, limit: int = 50) -> List[Dict]:
        if not self.bearer:
            return []
        headers = {"Authorization": f"Bearer {self.bearer}"}
        params = {
            "query": f"{ticker} (stock OR shares OR tendies OR moon OR 🚀)",
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,public_metrics,lang",
        }
        r = requests.get(TWITTER_SEARCH_URL, headers=headers, params=params, timeout=10)
        if r.status_code != 200:
            logger.error(f"Twitter API error {r.status_code}: {r.text}")
            return []
        data = r.json().get("data", [])
        results = []
        for t in data:
            results.append({
                "id": t["id"],
                "text": t.get("text", ""),
                "created_at": t.get("created_at"),
                "retweet_count": t.get("public_metrics", {}).get("retweet_count"),
                "like_count": t.get("public_metrics", {}).get("like_count"),
            })
        logger.debug(f"Twitter fetched {len(results)} tweets for {ticker}")
        return results
