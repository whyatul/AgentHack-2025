from typing import List, Dict
import re
from collections import Counter

MEME_KEYWORDS = [
    "tendies", "diamond hands", "paper hands", "HODL", "YOLO", "stonks", "moon", "bagholder", "apes"
]

HASHTAG_PATTERN = re.compile(r"#\w+")


def extract_hashtags(text: str) -> List[str]:
    return HASHTAG_PATTERN.findall(text.lower())


def meme_intensity(posts: List[Dict], ticker: str) -> float:
    if not posts:
        return 0.0
    keyword_counts = 0
    total_tokens = 0
    hashtags = []
    ticker_lower = ticker.lower()
    for p in posts:
        body = (p.get('title') or '') + ' ' + (p.get('selftext') or '') + ' ' + (p.get('text') or '')
        lower = body.lower()
        tokens = re.findall(r"\w+", lower)
        total_tokens += len(tokens)
        for kw in MEME_KEYWORDS:
            if kw in lower:
                keyword_counts += 1
        if ticker_lower in lower:
            keyword_counts += 1
        hashtags.extend(extract_hashtags(lower))
    hashtag_counts = Counter(hashtags)
    top_hashtag_score = sum(c for h, c in hashtag_counts.items() if ticker_lower in h)
    base = (keyword_counts + top_hashtag_score) / max(1, total_tokens)
    scaled = min(1.0, base * 15)
    return round(scaled, 4)
