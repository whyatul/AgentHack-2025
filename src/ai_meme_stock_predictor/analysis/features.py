from typing import Dict, List
from .sentiment import vader_compound, finbert_scores
from .meme_extraction import meme_intensity


def build_features(ticker: str, reddit_posts: List[Dict], tweets: List[Dict], quote: Dict) -> Dict:
    combined_texts = []
    for p in reddit_posts:
        combined_texts.append((p.get('title') or '') + ' ' + (p.get('selftext') or ''))
    for t in tweets:
        combined_texts.append(t.get('text') or '')

    vader_vals = [vader_compound(t) for t in combined_texts]
    finbert_vals = finbert_scores(combined_texts) if combined_texts else []

    meme_score = meme_intensity(reddit_posts + tweets, ticker)
    avg_vader = sum(vader_vals)/len(vader_vals) if vader_vals else 0
    avg_finbert = sum(finbert_vals)/len(finbert_vals) if finbert_vals else 0

    return {
        "meme_intensity": meme_score,
        "social_sentiment": avg_vader,
        "financial_sentiment": avg_finbert,
        "price": quote.get('price', 0),
        "volume": quote.get('volume', 0),
    }
