from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass, field
import json

@dataclass
class LeaderEntry:
    user_id: str
    username: str
    roi: Decimal
    pnl: Decimal
    total_value: Decimal
    win_rate: Decimal
    total_trades: int
    streak: int
    last_updated: datetime
    rank: int = 0
    previous_rank: int = 0
    prize_eligible: bool = False

    def to_dict(self) -> Dict:
        return {
            "rank": self.rank,
            "username": self.username,
            "roi": f"{self.roi:.2f}%",
            "pnl": f"${self.pnl:,.2f}",
            "win_rate": f"{self.win_rate:.1f}%",
            "trades": self.total_trades,
            "streak": self.streak,
            "trend": "↑" if self.rank < self.previous_rank else "↓" if self.rank > self.previous_rank else "→",
            "prize": "🏆" if self.prize_eligible else ""
        }

class Leaderboard:
    def __init__(self):
        self.entries: Dict[str, LeaderEntry] = {}
        self.daily_snapshot: List[LeaderEntry] = []
        self.weekly_snapshot: List[LeaderEntry] = []
        self.monthly_snapshot: List[LeaderEntry] = []
        self.all_time_snapshot: List[LeaderEntry] = []
        self.last_daily_reset = datetime.now()
        self.last_weekly_reset = datetime.now()
        self.last_monthly_reset = datetime.now()
        self.competition_start = datetime.now()
        self.competition_end = self.competition_start + timedelta(days=7)
        self.prize_pool = {"first": 50, "second": 25, "third": 10}

    def add_user(self, user_id: str, portfolio) -> None:
        username = f"Trader_{user_id[:8]}"  # Simple username generation

        entry = LeaderEntry(
            user_id=user_id,
            username=username,
            roi=Decimal(0),
            pnl=Decimal(0),
            total_value=portfolio.starting_balance,
            win_rate=Decimal(0),
            total_trades=0,
            streak=0,
            last_updated=datetime.now()
        )

        self.entries[user_id] = entry
        self._update_rankings()

    def update_user(self, user_id: str, portfolio, current_prices: Dict[str, Decimal]) -> None:
        if user_id not in self.entries:
            self.add_user(user_id, portfolio)
            return

        entry = self.entries[user_id]
        entry.previous_rank = entry.rank
        entry.roi = portfolio.get_roi(current_prices)
        entry.pnl = portfolio.statistics.total_pnl + portfolio.get_unrealized_pnl(current_prices)
        entry.total_value = portfolio.get_total_value(current_prices)
        entry.win_rate = portfolio.statistics.win_rate
        entry.total_trades = portfolio.statistics.total_trades
        entry.streak = portfolio.statistics.current_streak
        entry.last_updated = datetime.now()

        self._update_rankings()
        self._check_reset_periods()

    def _update_rankings(self) -> None:
        # Sort by ROI (descending)
        sorted_entries = sorted(
            self.entries.values(),
            key=lambda x: x.roi,
            reverse=True
        )

        # Update ranks and prize eligibility
        for idx, entry in enumerate(sorted_entries, 1):
            entry.rank = idx
            entry.prize_eligible = idx <= 3 and entry.total_trades >= 10

        # Update snapshots
        self.all_time_snapshot = sorted_entries.copy()

    def _check_reset_periods(self) -> None:
        now = datetime.now()

        # Daily reset
        if (now - self.last_daily_reset).days >= 1:
            self.daily_snapshot = list(self.entries.values())
            self.last_daily_reset = now

        # Weekly reset (competition cycle)
        if (now - self.last_weekly_reset).days >= 7:
            self.weekly_snapshot = list(self.entries.values())
            self.last_weekly_reset = now
            self._distribute_prizes()
            self._start_new_competition()

        # Monthly reset
        if (now - self.last_monthly_reset).days >= 30:
            self.monthly_snapshot = list(self.entries.values())
            self.last_monthly_reset = now

    def _distribute_prizes(self) -> List[Dict]:
        winners = []
        sorted_entries = sorted(
            [e for e in self.entries.values() if e.total_trades >= 10],
            key=lambda x: x.roi,
            reverse=True
        )

        if len(sorted_entries) >= 1:
            winners.append({
                "place": 1,
                "user": sorted_entries[0].username,
                "roi": float(sorted_entries[0].roi),
                "prize": self.prize_pool["first"]
            })

        if len(sorted_entries) >= 2:
            winners.append({
                "place": 2,
                "user": sorted_entries[1].username,
                "roi": float(sorted_entries[1].roi),
                "prize": self.prize_pool["second"]
            })

        if len(sorted_entries) >= 3:
            winners.append({
                "place": 3,
                "user": sorted_entries[2].username,
                "roi": float(sorted_entries[2].roi),
                "prize": self.prize_pool["third"]
            })

        return winners

    def _start_new_competition(self) -> None:
        self.competition_start = datetime.now()
        self.competition_end = self.competition_start + timedelta(days=7)
        # Reset all portfolios for new competition (optional)

    def get_user_rank(self, user_id: str) -> Optional[int]:
        entry = self.entries.get(user_id)
        return entry.rank if entry else None

    def get_top_traders(self, count: int = 10, timeframe: str = "all") -> List[Dict]:
        if timeframe == "daily":
            snapshot = self.daily_snapshot
        elif timeframe == "weekly":
            snapshot = self.weekly_snapshot
        elif timeframe == "monthly":
            snapshot = self.monthly_snapshot
        else:
            snapshot = self.all_time_snapshot

        return [entry.to_dict() for entry in snapshot[:count]]

    def get_leaderboard(self, timeframe: str = "all") -> Dict:
        top_traders = self.get_top_traders(100, timeframe)

        competition_info = {
            "start": self.competition_start.isoformat(),
            "end": self.competition_end.isoformat(),
            "time_remaining": str(self.competition_end - datetime.now()),
            "participants": len(self.entries),
            "prize_pool": sum(self.prize_pool.values())
        }

        return {
            "timeframe": timeframe,
            "updated": datetime.now().isoformat(),
            "competition": competition_info,
            "rankings": top_traders,
            "prizes": {
                "🥇 1st": f"${self.prize_pool['first']}",
                "🥈 2nd": f"${self.prize_pool['second']}",
                "🥉 3rd": f"${self.prize_pool['third']}"
            }
        }

    def get_competition_status(self) -> Dict:
        time_remaining = self.competition_end - datetime.now()
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60

        return {
            "active": True,
            "time_remaining": f"{days}d {hours}h {minutes}m",
            "participants": len(self.entries),
            "qualified": len([e for e in self.entries.values() if e.total_trades >= 10]),
            "current_leader": self.all_time_snapshot[0].username if self.all_time_snapshot else "N/A",
            "leader_roi": f"{self.all_time_snapshot[0].roi:.2f}%" if self.all_time_snapshot else "0%"
        }