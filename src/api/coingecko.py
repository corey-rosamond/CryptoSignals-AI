import requests
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import time

try:
    from .base import DataProviderInterface, RateLimit
except ImportError:
    from base import DataProviderInterface, RateLimit

class CoinGeckoAPI(DataProviderInterface):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.coingecko.com/api/v3"
        self.rate_limit = RateLimit(max_calls=50, window_seconds=60)  # 50 calls per minute
        self.priority = 1  # Primary API
        self.last_error = None

    def get_name(self) -> str:
        return "CoinGecko"

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        if not self.rate_limit.can_call():
            wait_time = self.rate_limit.time_until_reset()
            print(f"Rate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        url = f"{self.base_url}/{endpoint}"
        headers = {}

        if self.api_key:
            headers["x-cg-api-key"] = self.api_key

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
        # Map common symbols to CoinGecko IDs
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana",
            "ADA": "cardano",
            "USDT": "tether",
            "XRP": "ripple",
            "DOGE": "dogecoin",
            "DOT": "polkadot",
            "AVAX": "avalanche-2"
        }

        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        data = self._make_request(f"simple/price", {
            "ids": coin_id,
            "vs_currencies": "usd"
        })

        if data and coin_id in data:
            return Decimal(str(data[coin_id]["usd"]))
        return None

    def fetch_volume(self, symbol: str) -> Optional[Decimal]:
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana",
            "ADA": "cardano"
        }

        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        data = self._make_request(f"simple/price", {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_vol": "true"
        })

        if data and coin_id in data:
            return Decimal(str(data[coin_id].get("usd_24h_vol", 0)))
        return None

    def fetch_market_cap(self) -> Optional[Decimal]:
        data = self._make_request("global")

        if data and "data" in data:
            return Decimal(str(data["data"]["total_market_cap"]["usd"]))
        return None

    def fetch_top_coins(self, count: int = 20) -> List[Dict]:
        data = self._make_request("coins/markets", {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": count,
            "page": 1,
            "sparkline": "false"
        })

        if not data:
            return []

        coins = []
        for coin in data:
            coins.append({
                "symbol": coin["symbol"].upper(),
                "name": coin["name"],
                "price": Decimal(str(coin["current_price"])),
                "change_24h": Decimal(str(coin["price_change_percentage_24h"])),
                "volume_24h": Decimal(str(coin["total_volume"])),
                "market_cap": Decimal(str(coin["market_cap"])),
                "rank": coin["market_cap_rank"]
            })

        return coins

    def fetch_fear_greed_index(self) -> Optional[Dict]:
        # Note: Fear & Greed Index is provided by Alternative.me, not CoinGecko
        # This is a placeholder - would need to integrate with Alternative.me API
        return {
            "value": 65,
            "label": "Greed",
            "timestamp": datetime.now().isoformat(),
            "description": "Market is greedy, be cautious"
        }

    def fetch_historical_data(self, symbol: str, days: int = 30) -> Optional[List[Dict]]:
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana"
        }

        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        data = self._make_request(f"coins/{coin_id}/market_chart", {
            "vs_currency": "usd",
            "days": days
        })

        if data and "prices" in data:
            prices = []
            for timestamp, price in data["prices"]:
                prices.append({
                    "timestamp": datetime.fromtimestamp(timestamp / 1000).isoformat(),
                    "price": Decimal(str(price))
                })
            return prices
        return None

    def is_available(self) -> bool:
        # Simple ping to check if API is available
        data = self._make_request("ping")
        return data is not None

    def get_global_metrics(self) -> Optional[Dict]:
        data = self._make_request("global")

        if data and "data" in data:
            metrics = data["data"]
            return {
                "total_market_cap": Decimal(str(metrics["total_market_cap"]["usd"])),
                "total_volume_24h": Decimal(str(metrics["total_volume"]["usd"])),
                "btc_dominance": Decimal(str(metrics["market_cap_percentage"]["btc"])),
                "eth_dominance": Decimal(str(metrics["market_cap_percentage"]["eth"])),
                "active_cryptocurrencies": metrics["active_cryptocurrencies"],
                "markets": metrics["markets"],
                "market_cap_change_24h": Decimal(str(metrics["market_cap_change_percentage_24h_usd"]))
            }
        return None