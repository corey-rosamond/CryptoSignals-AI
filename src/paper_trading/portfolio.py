from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal
import uuid

@dataclass
class Position:
    position_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str = ""
    quantity: Decimal = Decimal(0)
    entry_price: Decimal = Decimal(0)
    open_time: datetime = field(default_factory=datetime.now)
    position_type: str = "long"

    def get_current_value(self, current_price: Decimal) -> Decimal:
        return self.quantity * current_price

    def get_pnl(self, current_price: Decimal) -> Decimal:
        current_value = self.get_current_value(current_price)
        cost_basis = self.quantity * self.entry_price
        return current_value - cost_basis

    def get_pnl_percent(self, current_price: Decimal) -> Decimal:
        if self.entry_price == 0:
            return Decimal(0)
        return ((current_price - self.entry_price) / self.entry_price) * 100

    def close(self, exit_price: Decimal) -> Dict:
        return {
            "position_id": self.position_id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "exit_price": exit_price,
            "pnl": self.get_pnl(exit_price),
            "pnl_percent": self.get_pnl_percent(exit_price),
            "open_time": self.open_time,
            "close_time": datetime.now()
        }

@dataclass
class Trade:
    trade_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    symbol: str = ""
    trade_type: str = ""  # "buy" or "sell"
    quantity: Decimal = Decimal(0)
    price: Decimal = Decimal(0)
    total_value: Decimal = Decimal(0)
    pnl: Decimal = Decimal(0)
    balance_after: Decimal = Decimal(0)

@dataclass
class Statistics:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_pnl: Decimal = Decimal(0)
    best_trade: Decimal = Decimal(0)
    worst_trade: Decimal = Decimal(0)
    win_rate: Decimal = Decimal(0)
    current_streak: int = 0
    best_streak: int = 0

    def update_win_rate(self):
        if self.total_trades > 0:
            self.win_rate = Decimal(self.winning_trades) / Decimal(self.total_trades) * 100

class Portfolio:
    def __init__(self, user_id: str, starting_balance: Decimal = Decimal(10000)):
        self.user_id = user_id
        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.positions: List[Position] = []
        self.trade_history: List[Trade] = []
        self.statistics = Statistics()
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

    def open_position(self, symbol: str, quantity: Decimal, price: Decimal) -> Optional[Position]:
        total_cost = quantity * price

        if total_cost > self.balance:
            return None

        position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            position_type="long"
        )

        self.positions.append(position)
        self.balance -= total_cost

        trade = Trade(
            symbol=symbol,
            trade_type="buy",
            quantity=quantity,
            price=price,
            total_value=total_cost,
            balance_after=self.balance
        )
        self.trade_history.append(trade)

        self.statistics.total_trades += 1
        self.last_updated = datetime.now()

        return position

    def close_position(self, position_id: str, current_price: Decimal) -> Optional[Dict]:
        position = next((p for p in self.positions if p.position_id == position_id), None)

        if not position:
            return None

        close_data = position.close(current_price)
        proceeds = position.quantity * current_price
        pnl = close_data["pnl"]

        self.balance += proceeds
        self.positions.remove(position)

        trade = Trade(
            symbol=position.symbol,
            trade_type="sell",
            quantity=position.quantity,
            price=current_price,
            total_value=proceeds,
            pnl=pnl,
            balance_after=self.balance
        )
        self.trade_history.append(trade)

        # Update statistics
        self.statistics.total_trades += 1
        self.statistics.total_pnl += pnl

        if pnl > 0:
            self.statistics.winning_trades += 1
            self.statistics.current_streak = max(0, self.statistics.current_streak) + 1
            self.statistics.best_streak = max(self.statistics.best_streak, self.statistics.current_streak)
            if pnl > self.statistics.best_trade:
                self.statistics.best_trade = pnl
        else:
            self.statistics.losing_trades += 1
            self.statistics.current_streak = min(0, self.statistics.current_streak) - 1
            if pnl < self.statistics.worst_trade:
                self.statistics.worst_trade = pnl

        self.statistics.update_win_rate()
        self.last_updated = datetime.now()

        return close_data

    def get_total_value(self, current_prices: Dict[str, Decimal]) -> Decimal:
        positions_value = sum(
            position.get_current_value(current_prices.get(position.symbol, position.entry_price))
            for position in self.positions
        )
        return self.balance + positions_value

    def get_roi(self, current_prices: Dict[str, Decimal]) -> Decimal:
        total_value = self.get_total_value(current_prices)
        roi = ((total_value - self.starting_balance) / self.starting_balance) * 100
        return roi

    def get_unrealized_pnl(self, current_prices: Dict[str, Decimal]) -> Decimal:
        return sum(
            position.get_pnl(current_prices.get(position.symbol, position.entry_price))
            for position in self.positions
        )

    def reset(self):
        self.balance = self.starting_balance
        self.positions = []
        self.trade_history = []
        self.statistics = Statistics()
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

    def to_dict(self, current_prices: Optional[Dict[str, Decimal]] = None) -> Dict:
        if current_prices is None:
            current_prices = {}

        return {
            "user_id": self.user_id,
            "balance": float(self.balance),
            "starting_balance": float(self.starting_balance),
            "total_value": float(self.get_total_value(current_prices)),
            "roi": float(self.get_roi(current_prices)),
            "unrealized_pnl": float(self.get_unrealized_pnl(current_prices)),
            "realized_pnl": float(self.statistics.total_pnl),
            "positions_count": len(self.positions),
            "total_trades": self.statistics.total_trades,
            "win_rate": float(self.statistics.win_rate),
            "current_streak": self.statistics.current_streak,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }