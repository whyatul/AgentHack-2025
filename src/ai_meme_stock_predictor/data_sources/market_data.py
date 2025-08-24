from typing import Dict, List
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

    def history(self, symbol: str, days: int = 30) -> List[Dict]:
        """Fetch recent daily adjusted price history (up to `days`).
        Returns list sorted ascending by date: [{date, open, high, low, close, volume}]"""
        if not self.api_key:
            return []
        params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": symbol, "apikey": self.api_key, "outputsize": "compact"}
        try:
            r = requests.get(ALPHA_URL, params=params, timeout=15)
        except Exception as e:
            logger.error(f"AlphaVantage history network error: {e}")
            return []
        if r.status_code != 200:
            logger.error(f"AlphaVantage history error {r.status_code}: {r.text[:180]}")
            return []
        data = r.json().get("Time Series (Daily)", {})
        rows = []
        for date, vals in list(data.items())[:days]:
            try:
                rows.append({
                    "date": date,
                    "open": float(vals.get("1. open", 0) or 0),
                    "high": float(vals.get("2. high", 0) or 0),
                    "low": float(vals.get("3. low", 0) or 0),
                    "close": float(vals.get("4. close", 0) or 0),
                    "volume": int(float(vals.get("6. volume", 0) or 0))
                })
            except Exception:
                continue
        rows.sort(key=lambda x: x['date'])
        return rows
