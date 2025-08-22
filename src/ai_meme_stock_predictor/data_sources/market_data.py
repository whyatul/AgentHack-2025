from typing import Dict
import requests
from ..utils.config import settings
from ..utils.logging_setup import get_logger

logger = get_logger(__name__)

ALPHA_URL = "https://www.alphavantage.co/query"

class MarketData:
    def __init__(self):
        self.api_key = settings.alphavantage_api_key
        if not self.api_key:
            logger.warning("Alpha Vantage API key missing; market data will fail")

    def quote(self, symbol: str) -> Dict:
        if not self.api_key:
            return {}
        params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self.api_key}
        r = requests.get(ALPHA_URL, params=params, timeout=10)
        if r.status_code != 200:
            logger.error(f"AlphaVantage error {r.status_code}: {r.text}")
            return {}
        data = r.json().get("Global Quote", {})
        return {
            "symbol": data.get("01. symbol"),
            "price": float(data.get("05. price", 0) or 0),
            "change_percent": data.get("10. change percent"),
            "volume": int(float(data.get("06. volume", 0) or 0)),
        }
