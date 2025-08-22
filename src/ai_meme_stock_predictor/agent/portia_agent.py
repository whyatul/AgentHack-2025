from typing import Dict, List
from .workflow import MemeStockWorkflow
from .feedback import record_feedback
from ..utils.logging_setup import get_logger
from ..utils.config import settings

# Lazy / defensive Portia SDK import handling
try:  # attempt common package names
    import portia  # hypothetical official sdk
except Exception:  # pragma: no cover
    portia = None

logger = get_logger(__name__)

class PortiaMemeAgent:
    def __init__(self):
        self.workflow = MemeStockWorkflow()
        self._history: Dict[str, List[Dict]] = {}
        if portia and settings.portia_api_key:
            try:
                # Hypothetical client initialization; adjust to real SDK
                self._portia_client = portia.Client(api_key=settings.portia_api_key)
            except Exception as e:  # pragma: no cover
                logger.warning(f"Portia client init failed: {e}")
                self._portia_client = None
        else:
            self._portia_client = None

    def _append_history(self, conversation_id: str, role: str, content: str):
        self._history.setdefault(conversation_id, []).append({"role": role, "content": content})
        # Optional trim
        if len(self._history[conversation_id]) > 50:
            self._history[conversation_id] = self._history[conversation_id][-50:]

    def handle_query(self, conversation_id: str, text: str) -> Dict:
        self._append_history(conversation_id, "user", text)
        lower = text.lower().strip()

        if lower.startswith("feedback"):
            parts = lower.split(":", 2)
            rating = parts[1] if len(parts) > 1 else "none"
            notes = parts[2] if len(parts) > 2 else ""
            record_feedback(conversation_id, rating, notes)
            response = {"response": "Feedback appreciated!"}
            self._append_history(conversation_id, "assistant", response["response"])
            self._send_to_portia(conversation_id, text, response["response"], meta={"type": "feedback"})
            return response

        if any(k in lower for k in ["explain", "methodology", "how"]):
            msg = "Ask about a ticker like 'TSLA memes?' to get a playful sentiment+memes analysis."
            self._append_history(conversation_id, "assistant", msg)
            self._send_to_portia(conversation_id, text, msg, meta={"type": "help"})
            return {"response": msg}

        words = [w.strip("$?!. ,") for w in lower.split()]
        ticker = None
        for w in words:
            if w.isalpha() and 2 < len(w) <= 5:
                ticker = w.upper()
                break
        if not ticker:
            msg = "Please specify a ticker (e.g., 'GME memes?')."
            self._append_history(conversation_id, "assistant", msg)
            self._send_to_portia(conversation_id, text, msg, meta={"type": "no_ticker"})
            return {"response": msg}

        result = self.workflow.run(ticker)
        message = result['message']
        self._append_history(conversation_id, "assistant", message)
        self._send_to_portia(conversation_id, text, message, meta={"type": "analysis", "ticker": ticker, **result.get('prediction', {})})
        return {"response": message, "details": result}

    def _send_to_portia(self, conversation_id: str, user_text: str, assistant_text: str, meta: Dict):  # pragma: no cover
        if not self._portia_client:
            return
        try:
            # Hypothetical API usage; adjust to real method names
            self._portia_client.log_interaction(
                conversation_id=conversation_id,
                user_message=user_text,
                assistant_message=assistant_text,
                metadata=meta,
            )
        except Exception as e:
            logger.debug(f"Portia log_interaction failed: {e}")
