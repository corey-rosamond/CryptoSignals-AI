from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime

class DataProviderInterface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def fetch_price(self, symbol: str) -> Optional[Decimal]:
        pass

    @abstractmethod
    def fetch_volume(self, symbol: str) -> Optional[Decimal]:
        pass

    @abstractmethod
    def fetch_market_cap(self) -> Optional[Decimal]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def fetch_top_coins(self, count: int = 20) -> List[Dict]:
        pass

class RateLimit:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: List[datetime] = []

    def can_call(self) -> bool:
        now = datetime.now()
        # Remove old calls outside the window
        self.calls = [call for call in self.calls
                      if (now - call).total_seconds() < self.window_seconds]
        return len(self.calls) < self.max_calls

    def record_call(self):
        self.calls.append(datetime.now())

    def time_until_reset(self) -> int:
        if not self.calls:
            return 0
        oldest_call = min(self.calls)
        elapsed = (datetime.now() - oldest_call).total_seconds()
        return max(0, int(self.window_seconds - elapsed))