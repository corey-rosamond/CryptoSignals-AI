import requests
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import time

try:
    from .base import DataProviderInterface, RateLimit
except ImportError:
    from base import DataProviderInterface, RateLimit

class CoinMarketCapAPI(DataProviderInterface):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.rate_limit = RateLimit(max_calls=333, window_seconds=60)  # Basic plan: 333/min
        self.priority = 2  # Backup API
        self.last_error = None

    def get_name(self) -> str:
        return "CoinMarketCap"

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        if not self.api_key:
            self.last_error = "API key required for CoinMarketCap"
            return None

        if not self.rate_limit.can_call():
            wait_time = self.rate_limit.time_until_reset()
            print(f"Rate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        url = f"{self.base_url}/{endpoint}"
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            self.rate_limit.record_call()

            if response.status_code == 200:
                self.last_error = None
                return response.json()
            else:
                self.last_error = f"API returned status {response.status_code}"
                return None

        except requests.exceptions.RequestException as e:
            self.last_error = str(e)
            return None

    def fetch_price(self, symbol: str) -> Optional[Decimal]:
        data = self._make_request("cryptocurrency/quotes/latest", {
            "symbol": symbol.upper(),
            "convert": "USD"
        })

        if data and "data" in data:
            symbol_data = data["data"].get(symbol.upper())
            if symbol_data:
                return Decimal(str(symbol_data["quote"]["USD"]["price"]))
        return None

    def fetch_volume(self, symbol: str) -> Optional[Decimal]:
        data = self._make_request("cryptocurrency/quotes/latest", {
            "symbol": symbol.upper(),
            "convert": "USD"
        })

        if data and "data" in data:
            symbol_data = data["data"].get(symbol.upper())
            if symbol_data:
                return Decimal(str(symbol_data["quote"]["USD"]["volume_24h"]))
        return None

    def fetch_market_cap(self) -> Optional[Decimal]:
        data = self._make_request("global-metrics/quotes/latest")

        if data and "data" in data:
            return Decimal(str(data["data"]["quote"]["USD"]["total_market_cap"]))
        return None

    def fetch_top_coins(self, count: int = 20) -> List[Dict]:
        data = self._make_request("cryptocurrency/listings/latest", {
            "limit": count,
            "convert": "USD"
        })

        if not data or "data" not in data:
            return []

        coins = []
        for coin in data["data"]:
            quote = coin["quote"]["USD"]
            coins.append({
                "symbol": coin["symbol"],
                "name": coin["name"],
                "price": Decimal(str(quote["price"])),
                "change_24h": Decimal(str(quote["percent_change_24h"])),
                "volume_24h": Decimal(str(quote["volume_24h"])),
                "market_cap": Decimal(str(quote["market_cap"])),
                "rank": coin["cmc_rank"]
            })

        return coins

    def is_available(self) -> bool:
        if not self.api_key:
            return False

        # Check API status
        data = self._make_request("key/info")
        return data is not None

    def get_global_metrics(self) -> Optional[Dict]:
        data = self._make_request("global-metrics/quotes/latest")

        if data and "data" in data:
            metrics = data["data"]
            quote = metrics["quote"]["USD"]
            return {
                "total_market_cap": Decimal(str(quote["total_market_cap"])),
                "total_volume_24h": Decimal(str(quote["total_volume_24h"])),
                "btc_dominance": Decimal(str(metrics["btc_dominance"])),
                "eth_dominance": Decimal(str(metrics["eth_dominance"])),
                "active_cryptocurrencies": metrics["active_cryptocurrencies"],
                "active_exchanges": metrics["active_exchanges"],
                "market_cap_change_24h": Decimal(str(quote["total_market_cap_yesterday_percentage_change"]))
            }
        return None