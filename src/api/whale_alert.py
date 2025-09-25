"""
WHALE ALERT SIMULATOR
This is a demonstration feature that simulates whale movements for educational purposes.
Real whale tracking requires expensive APIs ($99+/month).
This simulation helps users understand whale impact without the cost.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass
import random

@dataclass
class WhaleTransaction:
    transaction_id: str
    timestamp: datetime
    from_address: str
    to_address: str
    symbol: str
    amount: Decimal
    usd_value: Decimal
    transaction_type: str  # "transfer", "exchange_inflow", "exchange_outflow"
    from_label: Optional[str] = None
    to_label: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.transaction_id,
            "time": self.timestamp.isoformat(),
            "from": self.from_label or self.from_address[:10] + "...",
            "to": self.to_label or self.to_address[:10] + "...",
            "symbol": self.symbol,
            "amount": f"{self.amount:,.2f}",
            "usd_value": f"${self.usd_value:,.0f}",
            "type": self.transaction_type
        }

    def format_alert(self) -> str:
        emoji = "🐋"
        if self.usd_value >= 10_000_000:
            emoji = "🐋🐋🐋"
        elif self.usd_value >= 5_000_000:
            emoji = "🐋🐋"

        direction = ""
        if self.transaction_type == "exchange_inflow":
            direction = "→ EXCHANGE (potential sell pressure)"
        elif self.transaction_type == "exchange_outflow":
            direction = "← FROM EXCHANGE (bullish accumulation)"
        else:
            direction = f"from {self.from_label or 'Unknown'} to {self.to_label or 'Unknown'}"

        return f"""
{emoji} WHALE ALERT
{self.amount:,.2f} {self.symbol} (${self.usd_value:,.0f})
{direction}
Time: {self.timestamp.strftime('%H:%M UTC')}
"""

class WhaleAlertSimulator:
    """
    Educational whale movement simulator.
    Generates realistic-looking whale alerts for learning purposes.
    NOT real data - for demonstration and education only.
    """

    def __init__(self, threshold_usd: Decimal = Decimal(1_000_000)):
        self.threshold_usd = threshold_usd
        self.recent_transactions: List[WhaleTransaction] = []
        self.known_wallets = self._load_known_wallets()
        self.exchange_wallets = self._load_exchange_wallets()
        self.is_simulation = True  # Always true - this is a simulator

    def _load_known_wallets(self) -> Dict[str, str]:
        return {
            # Bitcoin addresses
            "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh": "MicroStrategy",
            "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ": "Grayscale Bitcoin Trust",
            "3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6": "Tesla",
            "bc1qa5wkgaew2dkv56kfvj49j0av5nml45x9ek9hz6": "Block.one",

            # Ethereum addresses
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "WETH Contract",
            "0x00000000219ab540356cBB839Cbe05303d7705Fa": "ETH 2.0 Deposit",
            "0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503": "Unknown Whale #1",
            "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8": "Binance 7",
        }

    def _load_exchange_wallets(self) -> Dict[str, str]:
        return {
            # Bitcoin
            "3FKj9x2HNXJvGmSNLYw8f8LCvVGdBEiVMg": "Binance Cold Wallet",
            "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h": "Binance Hot Wallet",
            "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s": "Coinbase Cold",
            "3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6": "Kraken",

            # Ethereum
            "0x28C6c06298d514Db089934071355E5743bf21d60": "Binance 14",
            "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d": "Binance 16",
            "0x71660c4005BA5E2F1D5C5c5e4b6ED4a77d0554cC": "Coinbase 1",
            "0x503828976D22510aad0201ac7EC88293211D23Da": "Coinbase 2",
        }

    def check_transaction(self, tx_data: Dict) -> Optional[WhaleTransaction]:
        # Parse transaction data
        amount = Decimal(str(tx_data.get("amount", 0)))
        symbol = tx_data.get("symbol", "BTC")
        price = Decimal(str(tx_data.get("price", 45000)))  # Current price
        usd_value = amount * price

        # Check if meets threshold
        if usd_value < self.threshold_usd:
            return None

        from_addr = tx_data.get("from", "unknown")
        to_addr = tx_data.get("to", "unknown")

        # Determine transaction type
        tx_type = "transfer"
        if to_addr in self.exchange_wallets:
            tx_type = "exchange_inflow"
        elif from_addr in self.exchange_wallets:
            tx_type = "exchange_outflow"

        transaction = WhaleTransaction(
            transaction_id=tx_data.get("id", f"tx_{datetime.now().timestamp()}"),
            timestamp=datetime.now(),
            from_address=from_addr,
            to_address=to_addr,
            symbol=symbol,
            amount=amount,
            usd_value=usd_value,
            transaction_type=tx_type,
            from_label=self.known_wallets.get(from_addr) or self.exchange_wallets.get(from_addr),
            to_label=self.known_wallets.get(to_addr) or self.exchange_wallets.get(to_addr)
        )

        self.recent_transactions.append(transaction)
        self._cleanup_old_transactions()

        return transaction

    def _cleanup_old_transactions(self):
        # Keep only last 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        self.recent_transactions = [
            tx for tx in self.recent_transactions
            if tx.timestamp > cutoff
        ]

    def get_recent_alerts(self, hours: int = 1) -> List[WhaleTransaction]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            tx for tx in self.recent_transactions
            if tx.timestamp > cutoff
        ]

    def analyze_flow(self, hours: int = 24) -> Dict:
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [tx for tx in self.recent_transactions if tx.timestamp > cutoff]

        inflow = sum(tx.usd_value for tx in recent if tx.transaction_type == "exchange_inflow")
        outflow = sum(tx.usd_value for tx in recent if tx.transaction_type == "exchange_outflow")
        net_flow = outflow - inflow

        return {
            "exchange_inflow": float(inflow),
            "exchange_outflow": float(outflow),
            "net_flow": float(net_flow),
            "interpretation": self._interpret_flow(net_flow),
            "transaction_count": len(recent),
            "largest_tx": max(recent, key=lambda x: x.usd_value).to_dict() if recent else None
        }

    def _interpret_flow(self, net_flow: Decimal) -> str:
        if net_flow > 10_000_000:
            return "🟢 Strong accumulation - Very Bullish"
        elif net_flow > 5_000_000:
            return "🟢 Accumulation phase - Bullish"
        elif net_flow > 0:
            return "🟡 Slight accumulation - Neutral to Bullish"
        elif net_flow > -5_000_000:
            return "🟡 Slight distribution - Neutral to Bearish"
        elif net_flow > -10_000_000:
            return "🔴 Distribution phase - Bearish"
        else:
            return "🔴 Heavy selling pressure - Very Bearish"

    def generate_educational_alerts(self, count: int = 3) -> List[WhaleTransaction]:
        """
        Generate educational whale movement examples.
        These are SIMULATED for learning purposes - not real transactions.
        """
        simulated = []
        symbols = ["BTC", "ETH", "BNB", "SOL"]

        # Use more realistic current prices (will be updated from real API)
        prices = {"BTC": 100000, "ETH": 4000, "BNB": 700, "SOL": 250}

        for _ in range(count):
            symbol = random.choice(symbols)
            amount = Decimal(random.randint(100, 5000) if symbol == "BTC" else random.randint(1000, 50000))
            price = Decimal(prices[symbol])

            tx_data = {
                "id": f"sim_{datetime.now().timestamp()}_{random.randint(1000, 9999)}",
                "amount": amount,
                "symbol": symbol,
                "price": price,
                "from": random.choice(list(self.known_wallets.keys()) + ["unknown"]),
                "to": random.choice(list(self.exchange_wallets.keys()) + ["unknown"])
            }

            transaction = self.check_transaction(tx_data)
            if transaction:
                simulated.append(transaction)

        return simulated

    def get_statistics(self) -> Dict:
        last_24h = self.get_recent_alerts(24)
        last_1h = self.get_recent_alerts(1)

        return {
            "alerts_24h": len(last_24h),
            "alerts_1h": len(last_1h),
            "total_volume_24h": sum(tx.usd_value for tx in last_24h),
            "avg_transaction_size": sum(tx.usd_value for tx in last_24h) / len(last_24h) if last_24h else 0,
            "top_symbols": self._get_top_symbols(last_24h),
            "flow_analysis": self.analyze_flow(24),
            "is_simulation": True,
            "note": "Educational simulation - not real whale data"
        }

    def _get_top_symbols(self, transactions: List[WhaleTransaction]) -> List[Dict]:
        symbol_volumes = {}
        for tx in transactions:
            if tx.symbol not in symbol_volumes:
                symbol_volumes[tx.symbol] = {"count": 0, "volume": Decimal(0)}
            symbol_volumes[tx.symbol]["count"] += 1
            symbol_volumes[tx.symbol]["volume"] += tx.usd_value

        sorted_symbols = sorted(symbol_volumes.items(), key=lambda x: x[1]["volume"], reverse=True)

        return [
            {
                "symbol": symbol,
                "transaction_count": data["count"],
                "total_volume": float(data["volume"])
            }
            for symbol, data in sorted_symbols[:5]
        ]