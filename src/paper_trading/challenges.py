from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from dataclasses import dataclass
import random

@dataclass
class Challenge:
    id: str
    name: str
    description: str
    requirement: str
    reward_points: int
    category: str
    target_value: any
    expires_at: datetime

    def to_dict(self) -> Dict:
        time_remaining = self.expires_at - datetime.now()
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60

        return {
            "name": self.name,
            "description": self.description,
            "requirement": self.requirement,
            "reward": f"{self.reward_points} points",
            "category": self.category,
            "expires_in": f"{hours}h {minutes}m"
        }

class ChallengeManager:
    def __init__(self):
        self.daily_challenges: Dict[str, Challenge] = {}
        self.user_progress: Dict[str, Dict] = {}
        self.user_streaks: Dict[str, int] = {}
        self.completed_challenges: Dict[str, List[str]] = {}
        self.last_reset = datetime.now()
        self.challenge_templates = self._initialize_challenge_templates()

    def _initialize_challenge_templates(self) -> List[Dict]:
        return [
            {
                "name": "Profit Master",
                "description": "Make profitable trades today",
                "requirement": "Complete 3 profitable trades",
                "category": "profit",
                "target_value": 3,
                "reward_points": 50
            },
            {
                "name": "Volume Trader",
                "description": "Trade significant volume",
                "requirement": "Trade $50,000 in volume",
                "category": "volume",
                "target_value": 50000,
                "reward_points": 30
            },
            {
                "name": "Prediction Pro",
                "description": "Achieve high accuracy",
                "requirement": "Maintain 70% win rate (min 5 trades)",
                "category": "accuracy",
                "target_value": 70,
                "reward_points": 100
            },
            {
                "name": "Quick Fingers",
                "description": "Execute trades rapidly",
                "requirement": "Complete 10 trades",
                "category": "trades",
                "target_value": 10,
                "reward_points": 40
            },
            {
                "name": "Big Winner",
                "description": "Make a significant profit",
                "requirement": "Earn $500+ on a single trade",
                "category": "big_win",
                "target_value": 500,
                "reward_points": 75
            },
            {
                "name": "Diversifier",
                "description": "Trade multiple assets",
                "requirement": "Trade at least 5 different cryptocurrencies",
                "category": "diversity",
                "target_value": 5,
                "reward_points": 60
            },
            {
                "name": "Risk Manager",
                "description": "Maintain controlled risk",
                "requirement": "Keep all trades under 10% of portfolio",
                "category": "risk",
                "target_value": 10,
                "reward_points": 80
            },
            {
                "name": "Early Bird",
                "description": "Start trading early",
                "requirement": "Make first trade before 9 AM",
                "category": "timing",
                "target_value": 9,
                "reward_points": 25
            },
            {
                "name": "Comeback Champion",
                "description": "Recover from loss",
                "requirement": "Turn a losing position into profit",
                "category": "comeback",
                "target_value": 1,
                "reward_points": 100
            },
            {
                "name": "Steady Growth",
                "description": "Consistent gains",
                "requirement": "Increase portfolio value by 5%",
                "category": "growth",
                "target_value": 5,
                "reward_points": 70
            }
        ]

    def get_daily_challenge(self, user_id: str) -> Dict:
        self._check_daily_reset()

        # Generate challenge for user if not exists
        if user_id not in self.daily_challenges:
            self._generate_daily_challenge(user_id)

        challenge = self.daily_challenges[user_id]
        progress = self.user_progress.get(user_id, {})

        return {
            "challenge": challenge.to_dict(),
            "progress": progress.get("current", 0),
            "target": challenge.target_value,
            "completed": progress.get("completed", False),
            "streak": self.user_streaks.get(user_id, 0),
            "streak_bonus": self._calculate_streak_bonus(self.user_streaks.get(user_id, 0))
        }

    def _generate_daily_challenge(self, user_id: str) -> None:
        # Select random challenge template
        template = random.choice(self.challenge_templates)

        # Create challenge instance
        challenge = Challenge(
            id=f"daily_{user_id}_{datetime.now().strftime('%Y%m%d')}",
            name=template["name"],
            description=template["description"],
            requirement=template["requirement"],
            reward_points=template["reward_points"],
            category=template["category"],
            target_value=template["target_value"],
            expires_at=datetime.now().replace(hour=23, minute=59, second=59)
        )

        self.daily_challenges[user_id] = challenge
        self.user_progress[user_id] = {
            "current": 0,
            "completed": False,
            "started_at": datetime.now()
        }

    def _check_daily_reset(self) -> None:
        now = datetime.now()
        if (now - self.last_reset).days >= 1:
            # Process completed challenges before reset
            for user_id, progress in self.user_progress.items():
                if progress.get("completed", False):
                    self._update_streak(user_id, True)
                else:
                    self._update_streak(user_id, False)

            # Reset daily challenges
            self.daily_challenges = {}
            self.user_progress = {}
            self.last_reset = now

    def _update_streak(self, user_id: str, completed: bool) -> None:
        if completed:
            self.user_streaks[user_id] = self.user_streaks.get(user_id, 0) + 1
        else:
            self.user_streaks[user_id] = 0

    def _calculate_streak_bonus(self, streak: int) -> float:
        if streak >= 30:
            return 3.0  # 3x multiplier
        elif streak >= 7:
            return 2.0  # 2x multiplier
        elif streak >= 3:
            return 1.5  # 1.5x multiplier
        return 1.0  # No multiplier

    def update_progress(self, user_id: str, update_type: str, value: any) -> Optional[Dict]:
        if user_id not in self.daily_challenges:
            return None

        challenge = self.daily_challenges[user_id]
        progress = self.user_progress.get(user_id, {})

        # Update progress based on challenge category
        if challenge.category == "profit" and update_type == "profitable_trade":
            progress["current"] = progress.get("current", 0) + 1

        elif challenge.category == "volume" and update_type == "trade_volume":
            progress["current"] = progress.get("current", 0) + value

        elif challenge.category == "accuracy" and update_type == "win_rate":
            progress["current"] = value

        elif challenge.category == "trades" and update_type == "trade_completed":
            progress["current"] = progress.get("current", 0) + 1

        elif challenge.category == "big_win" and update_type == "trade_profit":
            if value >= challenge.target_value:
                progress["current"] = challenge.target_value

        elif challenge.category == "diversity" and update_type == "unique_assets":
            progress["current"] = value

        elif challenge.category == "growth" and update_type == "portfolio_change":
            progress["current"] = value

        # Check if challenge is completed
        if progress["current"] >= challenge.target_value and not progress.get("completed", False):
            progress["completed"] = True
            streak_bonus = self._calculate_streak_bonus(self.user_streaks.get(user_id, 0))
            reward = int(challenge.reward_points * streak_bonus)

            # Track completion
            if user_id not in self.completed_challenges:
                self.completed_challenges[user_id] = []
            self.completed_challenges[user_id].append(challenge.id)

            self.user_progress[user_id] = progress

            return {
                "challenge_completed": True,
                "name": challenge.name,
                "reward": reward,
                "streak_bonus": streak_bonus,
                "new_streak": self.user_streaks.get(user_id, 0) + 1
            }

        self.user_progress[user_id] = progress
        return None

    def get_weekly_challenges(self) -> List[Dict]:
        # Return special weekly challenges (harder, more rewarding)
        return [
            {
                "name": "Weekly Warrior",
                "requirement": "Complete 5 daily challenges this week",
                "reward": "200 points + Special Badge",
                "progress": "2/5 completed"
            },
            {
                "name": "Consistency King",
                "requirement": "Maintain positive ROI for 7 days",
                "reward": "300 points + Exclusive Title",
                "progress": "3/7 days"
            },
            {
                "name": "Volume Master",
                "requirement": "Trade $500,000 total volume this week",
                "reward": "500 points + VIP Status",
                "progress": "$234,000/$500,000"
            }
        ]

    def get_challenge_stats(self, user_id: str) -> Dict:
        return {
            "daily_streak": self.user_streaks.get(user_id, 0),
            "total_completed": len(self.completed_challenges.get(user_id, [])),
            "current_multiplier": self._calculate_streak_bonus(self.user_streaks.get(user_id, 0)),
            "next_milestone": self._get_next_milestone(self.user_streaks.get(user_id, 0))
        }

    def _get_next_milestone(self, current_streak: int) -> Dict:
        if current_streak < 3:
            return {"days": 3 - current_streak, "reward": "1.5x multiplier"}
        elif current_streak < 7:
            return {"days": 7 - current_streak, "reward": "2x multiplier"}
        elif current_streak < 30:
            return {"days": 30 - current_streak, "reward": "3x multiplier"}
        else:
            return {"days": 0, "reward": "Max multiplier achieved!"}