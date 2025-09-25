from typing import Dict, List, Optional
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass, field

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    badge: str
    points: int
    category: str
    requirement_type: str
    requirement_value: any
    hidden: bool = False

    def check_requirement(self, context: Dict) -> bool:
        if self.requirement_type == "first_portfolio":
            return True  # Always true when creating first portfolio

        elif self.requirement_type == "trade_count":
            return context.get("trade_count", 0) >= self.requirement_value

        elif self.requirement_type == "profit_amount":
            return context.get("pnl", Decimal(0)) >= Decimal(self.requirement_value)

        elif self.requirement_type == "roi_percent":
            return context.get("roi", Decimal(0)) >= Decimal(self.requirement_value)

        elif self.requirement_type == "win_streak":
            return context.get("streak", 0) >= self.requirement_value

        elif self.requirement_type == "total_pnl":
            return context.get("total_pnl", Decimal(0)) >= Decimal(self.requirement_value)

        elif self.requirement_type == "whale_spot":
            return context.get("whale_spotted", False)

        elif self.requirement_type == "hold_duration":
            return context.get("hold_days", 0) >= self.requirement_value

        return False

class AchievementSystem:
    def __init__(self):
        self.achievements = self._initialize_achievements()
        self.user_achievements: Dict[str, List[str]] = {}
        self.user_points: Dict[str, int] = {}
        self.user_badges: Dict[str, List[str]] = {}

    def _initialize_achievements(self) -> Dict[str, Achievement]:
        return {
            # Trading Achievements
            "first_portfolio": Achievement(
                id="first_portfolio",
                name="Getting Started",
                description="Create your first paper trading portfolio",
                badge="🎯",
                points=10,
                category="trading",
                requirement_type="first_portfolio",
                requirement_value=None
            ),
            "first_trade": Achievement(
                id="first_trade",
                name="First Trade",
                description="Execute your first trade",
                badge="📈",
                points=10,
                category="trading",
                requirement_type="trade_count",
                requirement_value=1
            ),
            "trade_10": Achievement(
                id="trade_10",
                name="Active Trader",
                description="Complete 10 trades",
                badge="⚡",
                points=25,
                category="trading",
                requirement_type="trade_count",
                requirement_value=10
            ),
            "trade_100": Achievement(
                id="trade_100",
                name="Trade Master",
                description="Complete 100 trades",
                badge="🎖️",
                points=100,
                category="trading",
                requirement_type="trade_count",
                requirement_value=100
            ),

            # Profit Achievements
            "first_profit": Achievement(
                id="first_profit",
                name="First Profit",
                description="Make your first profitable trade",
                badge="💰",
                points=15,
                category="profit",
                requirement_type="profit_amount",
                requirement_value=1
            ),
            "profit_100": Achievement(
                id="profit_100",
                name="Century Club",
                description="Make $100 profit on a single trade",
                badge="💵",
                points=30,
                category="profit",
                requirement_type="profit_amount",
                requirement_value=100
            ),
            "profit_1000": Achievement(
                id="profit_1000",
                name="Profit King",
                description="Make $1,000 profit on a single trade",
                badge="👑",
                points=75,
                category="profit",
                requirement_type="profit_amount",
                requirement_value=1000
            ),
            "total_profit_10000": Achievement(
                id="total_profit_10000",
                name="Wealth Builder",
                description="Accumulate $10,000 in total profits",
                badge="🏆",
                points=200,
                category="profit",
                requirement_type="total_pnl",
                requirement_value=10000
            ),

            # ROI Achievements
            "roi_10": Achievement(
                id="roi_10",
                name="Smart Investor",
                description="Achieve 10% ROI",
                badge="📊",
                points=25,
                category="roi",
                requirement_type="roi_percent",
                requirement_value=10
            ),
            "roi_50": Achievement(
                id="roi_50",
                name="Market Genius",
                description="Achieve 50% ROI",
                badge="🧠",
                points=75,
                category="roi",
                requirement_type="roi_percent",
                requirement_value=50
            ),
            "roi_100": Achievement(
                id="roi_100",
                name="Doubler",
                description="Double your portfolio (100% ROI)",
                badge="2️⃣",
                points=150,
                category="roi",
                requirement_type="roi_percent",
                requirement_value=100
            ),
            "roi_1000": Achievement(
                id="roi_1000",
                name="To The Moon",
                description="10x your portfolio (1000% ROI)",
                badge="🚀",
                points=500,
                category="roi",
                requirement_type="roi_percent",
                requirement_value=1000
            ),

            # Streak Achievements
            "streak_3": Achievement(
                id="streak_3",
                name="Hot Streak",
                description="3 winning trades in a row",
                badge="🔥",
                points=20,
                category="streak",
                requirement_type="win_streak",
                requirement_value=3
            ),
            "streak_5": Achievement(
                id="streak_5",
                name="On Fire",
                description="5 winning trades in a row",
                badge="🔥🔥",
                points=35,
                category="streak",
                requirement_type="win_streak",
                requirement_value=5
            ),
            "streak_10": Achievement(
                id="streak_10",
                name="Unstoppable",
                description="10 winning trades in a row",
                badge="🔥🔥🔥",
                points=75,
                category="streak",
                requirement_type="win_streak",
                requirement_value=10
            ),
            "streak_20": Achievement(
                id="streak_20",
                name="Legendary Streak",
                description="20 winning trades in a row",
                badge="⚡🔥⚡",
                points=200,
                category="streak",
                requirement_type="win_streak",
                requirement_value=20
            ),

            # Special Achievements
            "diamond_hands": Achievement(
                id="diamond_hands",
                name="Diamond Hands",
                description="Hold a position through 100% gain",
                badge="💎🙌",
                points=100,
                category="special",
                requirement_type="roi_percent",
                requirement_value=100,
                hidden=True
            ),
            "whale_spotter": Achievement(
                id="whale_spotter",
                name="Whale Spotter",
                description="Trade based on whale alert",
                badge="🐋",
                points=50,
                category="special",
                requirement_type="whale_spot",
                requirement_value=True
            ),
            "perfect_timing": Achievement(
                id="perfect_timing",
                name="Perfect Timing",
                description="Buy at daily low and sell at daily high",
                badge="⏰",
                points=150,
                category="special",
                requirement_type="perfect_timing",
                requirement_value=True,
                hidden=True
            ),
            "comeback_kid": Achievement(
                id="comeback_kid",
                name="Comeback Kid",
                description="Recover from -50% to profit",
                badge="💪",
                points=200,
                category="special",
                requirement_type="comeback",
                requirement_value=True,
                hidden=True
            )
        }

    def check_and_unlock(self, user_id: str, trigger_type: str, context: Dict) -> List[Dict]:
        unlocked = []

        if user_id not in self.user_achievements:
            self.user_achievements[user_id] = []
            self.user_points[user_id] = 0
            self.user_badges[user_id] = []

        for achievement_id, achievement in self.achievements.items():
            # Skip if already unlocked
            if achievement_id in self.user_achievements[user_id]:
                continue

            # Check if this achievement should be checked for this trigger
            if trigger_type == "first_portfolio" and achievement.id != "first_portfolio":
                continue
            elif trigger_type == "trade" and achievement.category not in ["trading"]:
                continue
            elif trigger_type == "profit" and achievement.category not in ["profit", "roi", "streak", "special"]:
                continue

            # Check if requirement is met
            if achievement.check_requirement(context):
                self.user_achievements[user_id].append(achievement_id)
                self.user_points[user_id] += achievement.points
                self.user_badges[user_id].append(achievement.badge)

                unlocked.append({
                    "name": achievement.name,
                    "description": achievement.description,
                    "badge": achievement.badge,
                    "points": achievement.points,
                    "category": achievement.category
                })

        return unlocked

    def get_user_achievements(self, user_id: str) -> Dict:
        if user_id not in self.user_achievements:
            return {
                "total_points": 0,
                "unlocked_count": 0,
                "total_count": len(self.achievements),
                "badges": [],
                "achievements": [],
                "progress": []
            }

        unlocked_achievements = []
        for achievement_id in self.user_achievements[user_id]:
            achievement = self.achievements[achievement_id]
            unlocked_achievements.append({
                "name": achievement.name,
                "description": achievement.description,
                "badge": achievement.badge,
                "points": achievement.points,
                "category": achievement.category,
                "unlocked_at": datetime.now().isoformat()  # Would need to track this properly
            })

        # Calculate progress for locked achievements
        progress = []
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in self.user_achievements[user_id] and not achievement.hidden:
                progress.append({
                    "name": achievement.name,
                    "description": achievement.description,
                    "badge": "🔒",
                    "points": achievement.points,
                    "category": achievement.category,
                    "requirement": f"Requirement: {achievement.requirement_value}"
                })

        return {
            "total_points": self.user_points[user_id],
            "unlocked_count": len(self.user_achievements[user_id]),
            "total_count": len([a for a in self.achievements.values() if not a.hidden]),
            "badges": self.user_badges[user_id],
            "achievements": unlocked_achievements,
            "progress": progress[:5]  # Show next 5 achievements to unlock
        }

    def get_achievement_leaderboard(self) -> List[Dict]:
        leaderboard = []
        for user_id, points in sorted(self.user_points.items(), key=lambda x: x[1], reverse=True):
            leaderboard.append({
                "user_id": user_id[:8],
                "points": points,
                "achievements": len(self.user_achievements[user_id]),
                "badges": " ".join(self.user_badges[user_id][:5])  # Show first 5 badges
            })
        return leaderboard[:10]  # Top 10 users