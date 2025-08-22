from src.ai_meme_stock_predictor.models.heuristics import heuristic_prediction

def test_heuristic_direction_up():
    feats = {"meme_intensity": 0.6, "social_sentiment": 0.4, "financial_sentiment": 0.2}
    pred = heuristic_prediction(feats)
    assert pred['direction'] == 'up'

def test_heuristic_direction_flat():
    feats = {"meme_intensity": 0.0, "social_sentiment": 0.0, "financial_sentiment": 0.0}
    pred = heuristic_prediction(feats)
    assert pred['direction'] == 'flat'

def test_heuristic_direction_down():
    feats = {"meme_intensity": -0.7, "social_sentiment": -0.5, "financial_sentiment": -0.3}
    pred = heuristic_prediction(feats)
    assert pred['direction'] == 'down'
