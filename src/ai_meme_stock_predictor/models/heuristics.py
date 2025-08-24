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
    price = feats.get('price', 0)
    volume = feats.get('volume', 0)

    # Standard weighted score
    score = 0.5*meme + 0.3*social + 0.2*fin
    
    # Adjust thresholds based on data availability
    # If we have very limited data, make it easier to get non-flat predictions
    data_sources = 0
    if meme > 0.001:  # Some meme activity
        data_sources += 1
    if abs(social) > 0.001:  # Some social sentiment
        data_sources += 1
    if abs(fin) > 0.001:  # Some financial sentiment
        data_sources += 1
    
    # More sensitive thresholds when data is limited
    if data_sources <= 1:
        up_threshold = 0.1
        down_threshold = -0.1
    else:
        up_threshold = 0.2
        down_threshold = -0.2
    
    # Add slight volume boost for high-volume stocks
    if volume > 10_000_000:  # 10M+ volume
        volume_boost = 0.05
    elif volume > 1_000_000:  # 1M+ volume
        volume_boost = 0.02
    else:
        volume_boost = 0
    
    # Apply volume boost to positive scores only
    if score > 0:
        score += volume_boost

    if score > up_threshold:
        direction = 'up'
    elif score < down_threshold:
        direction = 'down'
    else:
        direction = 'flat'

    # Confidence based on data quality and score magnitude
    base_confidence = min(0.95, abs(score))
    
    # Reduce confidence when we have limited data
    if data_sources <= 1:
        confidence = base_confidence * 0.7
    elif data_sources == 2:
        confidence = base_confidence * 0.85
    else:
        confidence = base_confidence
    
    return {
        'direction': direction,
        'confidence': round(confidence, 3),
        'score': round(score, 4),
        'emoji': DIRECTION_EMOJIS[direction],
        'data_sources': data_sources,
        'thresholds_used': {'up': up_threshold, 'down': down_threshold}
    }
