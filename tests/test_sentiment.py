from src.ai_meme_stock_predictor.analysis.sentiment import vader_compound


def test_vader_compound_range():
    score = vader_compound("This is great and awesome!")
    assert -1.0 <= score <= 1.0
