from typing import List, Dict
from ..utils.logging_setup import get_logger

logger = get_logger(__name__)

_feedback_store: List[Dict] = []

def record_feedback(conversation_id: str, rating: str, notes: str = ""):
    _feedback_store.append({
        'conversation_id': conversation_id,
        'rating': rating,
        'notes': notes
    })
    logger.info(f"Feedback recorded: {rating} | {notes}")

def get_feedback() -> List[Dict]:
    return list(_feedback_store)
