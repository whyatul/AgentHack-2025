from typing import Dict

DIRECTION_EMOJIS = {
    'up': '🚀',
    'down': '🪦',
    'flat': '🤷'
}


def heuristic_prediction(feats: Dict) -> Dict:
    meme = feats.get('meme_intensity', 0)
    social = feats.get('social_sentiment', 0)
    fin = feats.get('financial_sentiment', 0)

    score = 0.5*meme + 0.3*social + 0.2*fin

    if score > 0.2:
        direction = 'up'
    elif score < -0.2:
        direction = 'down'
    else:
        direction = 'flat'

    confidence = min(0.95, abs(score))
    return {
        'direction': direction,
        'confidence': round(confidence, 3),
        'score': round(score, 4),
        'emoji': DIRECTION_EMOJIS[direction]
    }
