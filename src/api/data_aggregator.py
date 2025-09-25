from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from decimal import Decimal
import threading
import time

try:
    from .base import DataProviderInterface
    from .coingecko import CoinGeckoAPI
    from .coinmarketcap import CoinMarketCapAPI
    from .whale_alert import WhaleAlertSimulator
    from .cache_manager import CacheManager
except ImportError:
    from base import DataProviderInterface
    from coingecko import CoinGeckoAPI
    from coinmarketcap import CoinMarketCapAPI
    from whale_alert import WhaleAlertSimulator
    from cache_manager import CacheManager

class MarketMetrics:
    def __init__(self):
        self.total_market_cap = Decimal(0)
        self.volume_24h = Decimal(0)
        self.btc_dominance = Decimal(0)
        self.eth_dominance = Decimal(0)
        self.fear_greed_index = 50
        self.fear_greed_label = "Neutral"
        self.market_trend = "neutral"
        self.top_gainers = []
        self.top_losers = []
        self.last_updated = datetime.now()

    def update(self, data: Dict):
        if "total_market_cap" in data:
            self.total_market_cap = data["total_market_cap"]
        if "total_volume_24h" in data:
            self.volume_24h = data["total_volume_24h"]
        if "btc_dominance" in data:
            self.btc_dominance = data["btc_dominance"]
        if "eth_dominance" in data:
            self.eth_dominance = data["eth_dominance"]
        if "fear_greed" in data:
            self.fear_greed_index = data["fear_greed"]["value"]
            self.fear_greed_label = data["fear_greed"]["label"]

        self.last_updated = datetime.now()

    def get_trend(self) -> str:
        if self.fear_greed_index >= 75:
            return "extreme_greed"
        elif self.fear_greed_index >= 60:
            return "greed"
        elif self.fear_greed_index >= 40:
            return "neutral"
        elif self.fear_greed_index >= 25:
            return "fear"
        else:
            return "extreme_fear"

    def to_dict(self) -> Dict:
        return {
            "total_market_cap": f"${float(self.total_market_cap) / 1e12:.2f}T" if self.total_market_cap > 0 else "$0T",
            "volume_24h": f"${float(self.volume_24h) / 1e9:.2f}B" if self.volume_24h > 0 else "$0B",
            "btc_dominance": f"{float(self.btc_dominance):.1f}%" if self.btc_dominance > 0 else "0%",
            "eth_dominance": f"{float(self.eth_dominance):.1f}%" if self.eth_dominance > 0 else "0%",
            "fear_greed_index": self.fear_greed_index,
            "fear_greed_label": self.fear_greed_label,
            "market_trend": self.get_trend(),
            "top_gainers": self.top_gainers[:3],
            "top_losers": self.top_losers[:3],
            "last_updated": self.last_updated.isoformat()
        }

class DataAggregator:
    def __init__(self):
        self.providers: List[DataProviderInterface] = []
        self.cache = CacheManager(default_ttl=300)  # 5 minutes
        self.whale_simulator = WhaleAlertSimulator()  # Educational simulator only
        self.market_metrics = MarketMetrics()
        self.scheduler_thread = None
        self.scheduler_running = False
        self.last_update = datetime.now()

        # Initialize providers
        self._init_providers()

    def _init_providers(self):
        # Add CoinGecko as primary provider
        self.providers.append(CoinGeckoAPI())

        # Add CoinMarketCap as backup (requires API key)
        # cmc = CoinMarketCapAPI(api_key="YOUR_API_KEY")
        # self.providers.append(cmc)

        # Sort by priority
        self.providers.sort(key=lambda x: x.priority)

    def fetch_price(self, symbol: str) -> Optional[Decimal]:
        # Check cache first
        cache_key = f"price_{symbol}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        # Try each provider
        for provider in self.providers:
            if provider.is_available():
                try:
                    price = provider.fetch_price(symbol)
                    if price:
                        self.cache.set(cache_key, price)
                        return price
                except Exception as e:
                    print(f"Error fetching from {provider.get_name()}: {e}")

        return None

    def fetch_market_data(self) -> Dict:
        cache_key = "market_data"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        market_data = {}

        for provider in self.providers:
            if provider.is_available():
                try:
                    # Get top coins
                    coins = provider.fetch_top_coins(20)
                    if coins:
                        market_data["top_coins"] = coins

                        # Calculate gainers and losers
                        sorted_by_change = sorted(coins, key=lambda x: x["change_24h"], reverse=True)
                        self.market_metrics.top_gainers = sorted_by_change[:3]
                        self.market_metrics.top_losers = sorted_by_change[-3:]

                    # Get global metrics
                    global_metrics = provider.get_global_metrics()
                    if global_metrics:
                        self.market_metrics.update(global_metrics)
                        market_data["global_metrics"] = global_metrics

                    # Get Fear & Greed Index
                    if hasattr(provider, 'fetch_fear_greed_index'):
                        fg = provider.fetch_fear_greed_index()
                        if fg:
                            self.market_metrics.update({"fear_greed": fg})
                            market_data["fear_greed"] = fg

                    self.cache.set(cache_key, market_data)
                    return market_data

                except Exception as e:
                    print(f"Error fetching market data from {provider.get_name()}: {e}")

        return market_data

    def get_whale_alerts_simulation(self, hours: int = 1) -> List[Dict]:
        """Get simulated whale alerts for educational purposes."""
        alerts = self.whale_simulator.get_recent_alerts(hours)
        return [{**alert.to_dict(), "is_simulation": True} for alert in alerts]

    def get_flow_analysis_simulation(self) -> Dict:
        """Get simulated flow analysis for educational purposes."""
        analysis = self.whale_simulator.analyze_flow(24)
        analysis["is_simulation"] = True
        analysis["note"] = "Educational simulation - not real data"
        return analysis

    def generate_educational_whale_alerts(self):
        """Generate educational whale movement examples."""
        transactions = self.whale_simulator.generate_educational_alerts(3)
        alerts = [tx.format_alert() for tx in transactions]
        return [f"📚 EDUCATIONAL SIMULATION{alert}" for alert in alerts]

    def schedule_updates(self, interval_minutes: int = 5):
        if self.scheduler_running:
            return

        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._update_loop, args=(interval_minutes,))
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

    def _update_loop(self, interval_minutes: int):
        while self.scheduler_running:
            try:
                # Fetch fresh market data
                self.fetch_market_data()

                # Update last update time
                self.last_update = datetime.now()

                print(f"Data updated at {self.last_update}")

            except Exception as e:
                print(f"Error in update loop: {e}")

            # Wait for next update
            time.sleep(interval_minutes * 60)

    def stop_scheduler(self):
        self.scheduler_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)

    def get_all_data(self) -> Dict:
        # Get comprehensive data for GPT
        market_data = self.fetch_market_data()

        return {
            "market_metrics": self.market_metrics.to_dict(),
            "top_coins": market_data.get("top_coins", [])[:10],
            "whale_alerts_simulation": self.get_whale_alerts_simulation(1),
            "flow_analysis_simulation": self.get_flow_analysis_simulation(),
            "cache_stats": self.cache.get_stats(),
            "last_update": self.last_update.isoformat(),
            "data_age_minutes": (datetime.now() - self.last_update).total_seconds() / 60,
            "note": "Whale alerts are educational simulations"
        }

    def get_price_bulk(self, symbols: List[str]) -> Dict[str, Decimal]:
        prices = {}
        for symbol in symbols:
            price = self.fetch_price(symbol)
            if price:
                prices[symbol] = price
        return prices

    def clear_cache(self):
        self.cache.clear_all()

    def get_cache_status(self) -> Dict:
        stats = self.cache.get_stats()
        stats["update_frequency"] = "5 minutes"
        stats["last_update"] = self.last_update.isoformat()
        stats["next_update"] = (self.last_update + timedelta(minutes=5)).isoformat()
        return stats