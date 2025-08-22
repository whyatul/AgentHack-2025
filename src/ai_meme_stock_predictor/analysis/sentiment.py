from typing import List
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ..utils.logging_setup import get_logger

_ENABLE_FINBERT = os.getenv("ENABLE_FINBERT", "0").lower() in {"1", "true", "yes"}

logger = get_logger(__name__)

_vader = SentimentIntensityAnalyzer()
_finbert = None  # lazy-loaded

def _load_finbert():  # pragma: no cover - heavy download
    global _finbert
    if _finbert is not None:
        return _finbert
    if not _ENABLE_FINBERT:
        logger.info("FinBERT disabled (set ENABLE_FINBERT=1 to enable). Returning neutral scores.")
        return None
    try:
        from transformers import pipeline  # local import to avoid import cost if disabled
        logger.info("Loading FinBERT sentiment model ... this may take a while the first time.")
        _finbert = pipeline("text-classification", model="yiyanghkust/finbert-tone", top_k=None)
    except Exception as e:  # pragma: no cover
        logger.warning(f"FinBERT pipeline load failed: {e}")
        _finbert = None
    return _finbert


def vader_compound(text: str) -> float:
    return _vader.polarity_scores(text).get('compound', 0.0)


def finbert_scores(texts: List[str]) -> List[float]:
    fb = _load_finbert()
    if fb is None:
        return [0.0 for _ in texts]
    outputs = fb(texts)
    scores = []
    for out in outputs:
        # out is a list of dicts with label & score
        pos = next((d['score'] for d in out if d['label'].lower() == 'positive'), 0)
        neg = next((d['score'] for d in out if d['label'].lower() == 'negative'), 0)
        scores.append(pos - neg)
    return scores
