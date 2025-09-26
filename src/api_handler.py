#!/usr/bin/env python3
"""
Robust API Handler with Error Handling and Fallback Mechanisms
Ensures reliable data fetching with multiple fallback options
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class APIHandler:
    """
    Handles all API calls with retry logic, caching, and fallback sources
    """

    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes in seconds
        self.max_retries = 3
        self.retry_delay = 2  # seconds between retries

        # API endpoints (all free tier)
        self.endpoints = {
            "coingecko": "https://api.coingecko.com/api/v3",
            "coinpaprika": "https://api.coinpaprika.com/v1",
            "messari": "https://data.messari.io/api/v1",
            "binance": "https://api.binance.com/api/v3"
        }

        # Rate limits for free tiers
        self.rate_limits = {
            "coingecko": {"calls": 50, "window": 60},  # 50 calls per minute
            "coinpaprika": {"calls": 100, "window": 60},  # 100 calls per minute
            "messari": {"calls": 20, "window": 60},  # 20 calls per minute
            "binance": {"calls": 1200, "window": 60}  # 1200 calls per minute
        }

        self.call_history = {api: [] for api in self.endpoints.keys()}

    def check_rate_limit(self, api: str) -> bool:
        """Check if we're within rate limits"""
        if api not in self.rate_limits:
            return True

        limit = self.rate_limits[api]
        now = time.time()
        window_start = now - limit["window"]

        # Clean old calls from history
        self.call_history[api] = [
            t for t in self.call_history[api] if t > window_start
        ]

        # Check if under limit
        return len(self.call_history[api]) < limit["calls"]

    def wait_for_rate_limit(self, api: str):
        """Wait if rate limited"""
        if self.check_rate_limit(api):
            return

        limit = self.rate_limits[api]
        oldest_call = min(self.call_history[api])
        wait_time = (oldest_call + limit["window"]) - time.time() + 1

        if wait_time > 0:
            print(f"⏳ Rate limited on {api}. Waiting {wait_time:.1f}s...")
            time.sleep(wait_time)

    def get_from_cache(self, key: str) -> Optional[Any]:
        """Get data from cache if still valid"""
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        return None

    def save_to_cache(self, key: str, data: Any):
        """Save data to cache with timestamp"""
        self.cache[key] = (data, time.time())

    def make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️ Request failed (attempt {attempt + 1}): {e}")
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    print(f"❌ All retries failed: {e}")
                    return None

    def get_crypto_prices_coingecko(self, symbols: List[str]) -> Dict:
        """Get prices from CoinGecko"""
        # Check cache
        cache_key = f"coingecko_prices_{','.join(symbols)}"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached

        # Check rate limit
        self.wait_for_rate_limit("coingecko")

        # Map symbols to CoinGecko IDs
        id_map = {
            "BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin",
            "SOL": "solana", "ADA": "cardano", "XRP": "ripple",
            "DOT": "polkadot", "AVAX": "avalanche-2", "LINK": "chainlink",
            "MATIC": "polygon", "UNI": "uniswap", "ATOM": "cosmos"
        }

        ids = [id_map.get(s.upper(), s.lower()) for s in symbols]
        url = f"{self.endpoints['coingecko']}/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }

        data = self.make_request(url, params)
        if data:
            # Record API call
            self.call_history["coingecko"].append(time.time())
            # Save to cache
            self.save_to_cache(cache_key, data)
        return data

    def get_crypto_prices_binance(self, symbol: str) -> Optional[float]:
        """Get price from Binance as fallback"""
        # Check rate limit
        self.wait_for_rate_limit("binance")

        # Convert symbol format (BTC -> BTCUSDT)
        binance_symbol = f"{symbol.upper()}USDT"
        url = f"{self.endpoints['binance']}/ticker/price"
        params = {"symbol": binance_symbol}

        data = self.make_request(url, params)
        if data and "price" in data:
            self.call_history["binance"].append(time.time())
            return float(data["price"])
        return None

    def get_market_data_with_fallback(self, symbols: List[str]) -> Dict:
        """Get market data with multiple fallback sources"""
        result = {}

        # Try primary source (CoinGecko)
        gecko_data = self.get_crypto_prices_coingecko(symbols)
        if gecko_data:
            for symbol in symbols:
                gecko_id = self.symbol_to_gecko_id(symbol)
                if gecko_id in gecko_data:
                    result[symbol] = {
                        "price": gecko_data[gecko_id]["usd"],
                        "change_24h": gecko_data[gecko_id].get("usd_24h_change", 0),
                        "market_cap": gecko_data[gecko_id].get("usd_market_cap", 0),
                        "volume_24h": gecko_data[gecko_id].get("usd_24h_vol", 0),
                        "source": "coingecko",
                        "timestamp": datetime.now().isoformat()
                    }

        # Fallback to Binance for missing symbols
        missing_symbols = [s for s in symbols if s not in result]
        for symbol in missing_symbols:
            price = self.get_crypto_prices_binance(symbol)
            if price:
                result[symbol] = {
                    "price": price,
                    "change_24h": None,
                    "market_cap": None,
                    "volume_24h": None,
                    "source": "binance",
                    "timestamp": datetime.now().isoformat()
                }

        # Use cached/simulated data for any still missing
        still_missing = [s for s in symbols if s not in result]
        for symbol in still_missing:
            result[symbol] = self.get_simulated_price(symbol)

        return result

    def symbol_to_gecko_id(self, symbol: str) -> str:
        """Convert trading symbol to CoinGecko ID"""
        mapping = {
            "BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin",
            "SOL": "solana", "ADA": "cardano", "XRP": "ripple",
            "DOT": "polkadot", "AVAX": "avalanche-2", "LINK": "chainlink",
            "MATIC": "polygon", "UNI": "uniswap", "ATOM": "cosmos",
            "NEAR": "near", "ALGO": "algorand", "FTM": "fantom",
            "VET": "vechain", "ICP": "internet-computer", "DOGE": "dogecoin"
        }
        return mapping.get(symbol.upper(), symbol.lower())

    def get_simulated_price(self, symbol: str) -> Dict:
        """Generate simulated price data as last resort"""
        base_prices = {
            "BTC": 45000, "ETH": 2800, "BNB": 220, "SOL": 140,
            "ADA": 0.35, "XRP": 0.52, "DOT": 4.15, "AVAX": 25,
            "LINK": 11, "MATIC": 0.52, "UNI": 5.2, "ATOM": 7.8
        }

        base = base_prices.get(symbol.upper(), 10)
        # Add small random variation
        import random
        variation = random.uniform(-0.02, 0.02)  # ±2%
        price = base * (1 + variation)

        return {
            "price": price,
            "change_24h": random.uniform(-5, 5),
            "market_cap": None,
            "volume_24h": None,
            "source": "simulated",
            "timestamp": datetime.now().isoformat(),
            "note": "API unavailable - using simulated data"
        }

    def get_trending_coins(self) -> List[Dict]:
        """Get trending cryptocurrencies"""
        cache_key = "trending_coins"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached

        # Try CoinGecko trending endpoint
        self.wait_for_rate_limit("coingecko")
        url = f"{self.endpoints['coingecko']}/search/trending"

        data = self.make_request(url)
        if data and "coins" in data:
            self.call_history["coingecko"].append(time.time())
            trending = [
                {
                    "id": coin["item"]["id"],
                    "symbol": coin["item"]["symbol"],
                    "name": coin["item"]["name"],
                    "rank": coin["item"]["market_cap_rank"],
                    "price_btc": coin["item"]["price_btc"]
                }
                for coin in data["coins"]
            ]
            self.save_to_cache(cache_key, trending)
            return trending

        # Fallback trending list
        return [
            {"symbol": "BTC", "name": "Bitcoin", "source": "fallback"},
            {"symbol": "ETH", "name": "Ethereum", "source": "fallback"},
            {"symbol": "SOL", "name": "Solana", "source": "fallback"}
        ]

    def get_global_market_data(self) -> Dict:
        """Get global crypto market statistics"""
        cache_key = "global_market_data"
        cached = self.get_from_cache(cache_key)
        if cached:
            return cached

        self.wait_for_rate_limit("coingecko")
        url = f"{self.endpoints['coingecko']}/global"

        data = self.make_request(url)
        if data and "data" in data:
            self.call_history["coingecko"].append(time.time())
            global_data = {
                "total_market_cap": data["data"]["total_market_cap"]["usd"],
                "total_volume": data["data"]["total_volume"]["usd"],
                "btc_dominance": data["data"]["market_cap_percentage"]["btc"],
                "eth_dominance": data["data"]["market_cap_percentage"]["eth"],
                "active_cryptos": data["data"]["active_cryptocurrencies"],
                "markets": data["data"]["markets"]
            }
            self.save_to_cache(cache_key, global_data)
            return global_data

        # Fallback data
        return {
            "total_market_cap": 1750000000000,
            "total_volume": 95000000000,
            "btc_dominance": 45.5,
            "eth_dominance": 18.2,
            "source": "estimated"
        }

    def health_check(self) -> Dict:
        """Check API health and availability"""
        health = {}

        for api_name, base_url in self.endpoints.items():
            try:
                if api_name == "coingecko":
                    test_url = f"{base_url}/ping"
                elif api_name == "binance":
                    test_url = f"{base_url}/ping"
                else:
                    test_url = base_url

                response = requests.get(test_url, timeout=5)
                health[api_name] = {
                    "status": "online" if response.status_code == 200 else "error",
                    "response_time": response.elapsed.total_seconds(),
                    "rate_limit_remaining": self.rate_limits[api_name]["calls"] - len(
                        [t for t in self.call_history[api_name]
                         if t > time.time() - self.rate_limits[api_name]["window"]]
                    )
                }
            except:
                health[api_name] = {"status": "offline"}

        return health


# Test the API handler
if __name__ == "__main__":
    handler = APIHandler()

    print("🔍 Testing API Handler...")
    print("-" * 50)

    # Test price fetching with fallback
    symbols = ["BTC", "ETH", "SOL", "ADA"]
    print(f"\\nFetching prices for: {symbols}")
    prices = handler.get_market_data_with_fallback(symbols)

    for symbol, data in prices.items():
        print(f"\\n{symbol}:")
        print(f"  Price: ${data['price']:.2f}")
        print(f"  24h Change: {data['change_24h']:.2f}%" if data['change_24h'] else "  24h Change: N/A")
        print(f"  Source: {data['source']}")

    # Test trending coins
    print("\\n📈 Trending Coins:")
    trending = handler.get_trending_coins()
    for i, coin in enumerate(trending[:5], 1):
        print(f"  {i}. {coin.get('symbol', 'N/A')} - {coin.get('name', 'N/A')}")

    # Test global market data
    print("\\n🌍 Global Market Data:")
    global_data = handler.get_global_market_data()
    print(f"  Total Market Cap: ${global_data['total_market_cap']:,.0f}")
    print(f"  BTC Dominance: {global_data['btc_dominance']:.1f}%")

    # Health check
    print("\\n🏥 API Health Check:")
    health = handler.health_check()
    for api, status in health.items():
        print(f"  {api}: {status['status']}", end="")
        if status['status'] == 'online':
            print(f" ({status['response_time']:.2f}s, {status['rate_limit_remaining']} calls left)")
        else:
            print()