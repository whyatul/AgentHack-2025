from typing import List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from ..utils.logging_setup import get_logger

logger = get_logger(__name__)

_vader = SentimentIntensityAnalyzer()
_finbert = None

try:
    _finbert = pipeline("text-classification", model="yiyanghkust/finbert-tone", top_k=None)
except Exception as e:
    logger.warning(f"FinBERT pipeline load failed: {e}")


def vader_compound(text: str) -> float:
    return _vader.polarity_scores(text).get('compound', 0.0)


def finbert_scores(texts: List[str]) -> List[float]:
    if _finbert is None:
        return [0.0 for _ in texts]
    outputs = _finbert(texts)
    scores = []
    for out in outputs:
        # out is a list of dicts with label & score
        pos = next((d['score'] for d in out if d['label'].lower() == 'positive'), 0)
        neg = next((d['score'] for d in out if d['label'].lower() == 'negative'), 0)
        scores.append(pos - neg)
    return scores
