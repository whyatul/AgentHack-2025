from src.ai_meme_stock_predictor.analysis.meme_extraction import meme_intensity


def test_meme_intensity_empty():
    assert meme_intensity([], 'TSLA') == 0.0


def test_meme_intensity_basic():
    posts = [
        {"title": "TSLA to the moon", "selftext": "Diamond hands HODL", "text": ""},
        {"title": "Random", "selftext": "tendies stonks", "text": "TSLA YOLO"},
    ]
    val = meme_intensity(posts, 'TSLA')
    assert 0 < val <= 1.0
