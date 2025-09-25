import re
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
import json

try:
    # Try relative imports (for package use)
    from .portfolio import Portfolio
    from .leaderboard import Leaderboard
    from .achievements import AchievementSystem
    from .challenges import ChallengeManager
except ImportError:
    # Fall back to direct imports (for testing)
    from portfolio import Portfolio
    from leaderboard import Leaderboard
    from achievements import AchievementSystem
    from challenges import ChallengeManager

class PaperTradingSimulator:
    def __init__(self, starting_balance: Decimal = Decimal(10000)):
        self.starting_balance = starting_balance
        self.portfolios: Dict[str, Portfolio] = {}
        self.leaderboard = Leaderboard()
        self.achievements = AchievementSystem()
        self.challenges = ChallengeManager()
        self.current_prices: Dict[str, Decimal] = {}

    def parse_trade_command(self, command: str) -> Optional[Dict]:
        command = command.lower().strip()

        # Start paper trading
        if "start paper trading" in command:
            return {"action": "start", "balance": self.starting_balance}

        # Buy command patterns
        buy_patterns = [
            r"buy\s+([\d.]+)\s+(\w+)",
            r"purchase\s+([\d.]+)\s+(\w+)",
            r"open\s+long\s+([\d.]+)\s+(\w+)",
        ]

        for pattern in buy_patterns:
            match = re.search(pattern, command)
            if match:
                return {
                    "action": "buy",
                    "quantity": Decimal(match.group(1)),
                    "symbol": match.group(2).upper()
                }

        # Sell command patterns
        sell_patterns = [
            r"sell\s+([\d.]+)\s+(\w+)",
            r"close\s+([\d.]+)\s+(\w+)",
            r"sell\s+all\s+(\w+)",
        ]

        for pattern in sell_patterns[:-1]:
            match = re.search(pattern, command)
            if match:
                return {
                    "action": "sell",
                    "quantity": Decimal(match.group(1)),
                    "symbol": match.group(2).upper()
                }

        # Sell all pattern
        match = re.search(sell_patterns[-1], command)
        if match:
            return {
                "action": "sell_all",
                "symbol": match.group(1).upper()
            }

        # Portfolio commands
        if any(word in command for word in ["portfolio", "balance", "positions", "p&l"]):
            return {"action": "portfolio"}

        # Leaderboard command
        if "leaderboard" in command or "ranking" in command:
            return {"action": "leaderboard"}

        # Achievement command
        if "achievement" in command or "badge" in command:
            return {"action": "achievements"}

        # Reset command
        if "reset" in command and "portfolio" in command:
            return {"action": "reset"}

        return None

    def create_portfolio(self, user_id: str) -> Portfolio:
        if user_id not in self.portfolios:
            portfolio = Portfolio(user_id, self.starting_balance)
            self.portfolios[user_id] = portfolio

            # Track achievement
            self.achievements.check_and_unlock(user_id, "first_portfolio", {})

            # Add to leaderboard
            self.leaderboard.add_user(user_id, portfolio)

            return portfolio
        return self.portfolios[user_id]

    def execute_trade(self, user_id: str, trade_params: Dict) -> Dict:
        portfolio = self.portfolios.get(user_id)
        if not portfolio:
            return {"success": False, "error": "No portfolio found. Start paper trading first."}

        action = trade_params.get("action")

        if action == "buy":
            symbol = trade_params["symbol"]
            quantity = trade_params["quantity"]
            price = self.current_prices.get(symbol, Decimal(45000))  # Default price for testing

            position = portfolio.open_position(symbol, quantity, price)

            if position:
                # Check achievements
                achievement_context = {
                    "trade_count": portfolio.statistics.total_trades,
                    "balance": portfolio.balance,
                    "roi": portfolio.get_roi(self.current_prices)
                }
                unlocked = self.achievements.check_and_unlock(user_id, "trade", achievement_context)

                # Update leaderboard
                self.leaderboard.update_user(user_id, portfolio, self.current_prices)

                return {
                    "success": True,
                    "action": "BUY",
                    "symbol": symbol,
                    "quantity": float(quantity),
                    "price": float(price),
                    "total_cost": float(quantity * price),
                    "new_balance": float(portfolio.balance),
                    "achievements_unlocked": unlocked
                }
            else:
                return {"success": False, "error": "Insufficient balance"}

        elif action == "sell" or action == "sell_all":
            symbol = trade_params["symbol"]

            # Find positions for this symbol
            positions = [p for p in portfolio.positions if p.symbol == symbol]

            if not positions:
                return {"success": False, "error": f"No {symbol} positions found"}

            total_pnl = Decimal(0)
            closed_positions = []

            for position in positions:
                price = self.current_prices.get(symbol, position.entry_price * Decimal(1.05))  # 5% profit for testing
                close_data = portfolio.close_position(position.position_id, price)

                if close_data:
                    total_pnl += close_data["pnl"]
                    closed_positions.append(close_data)

            # Check achievements for profit/loss
            if total_pnl > 0:
                achievement_context = {
                    "pnl": total_pnl,
                    "streak": portfolio.statistics.current_streak,
                    "total_pnl": portfolio.statistics.total_pnl
                }
                unlocked = self.achievements.check_and_unlock(user_id, "profit", achievement_context)
            else:
                unlocked = []

            # Update leaderboard
            self.leaderboard.update_user(user_id, portfolio, self.current_prices)

            return {
                "success": True,
                "action": "SELL",
                "symbol": symbol,
                "positions_closed": len(closed_positions),
                "total_pnl": float(total_pnl),
                "new_balance": float(portfolio.balance),
                "achievements_unlocked": unlocked
            }

        return {"success": False, "error": "Invalid trade action"}

    def get_portfolio_status(self, user_id: str) -> Dict:
        portfolio = self.portfolios.get(user_id)
        if not portfolio:
            return {"error": "No portfolio found"}

        status = portfolio.to_dict(self.current_prices)
        status["rank"] = self.leaderboard.get_user_rank(user_id)
        status["achievements"] = self.achievements.get_user_achievements(user_id)
        status["daily_challenge"] = self.challenges.get_daily_challenge(user_id)

        return status

    def get_leaderboard(self, timeframe: str = "daily") -> Dict:
        return self.leaderboard.get_leaderboard(timeframe)

    def reset_portfolio(self, user_id: str) -> bool:
        portfolio = self.portfolios.get(user_id)
        if portfolio:
            portfolio.reset()
            self.leaderboard.update_user(user_id, portfolio, self.current_prices)
            return True
        return False

    def update_prices(self, prices: Dict[str, Decimal]):
        self.current_prices = prices
        # Update all portfolio values in leaderboard
        for user_id, portfolio in self.portfolios.items():
            self.leaderboard.update_user(user_id, portfolio, self.current_prices)

    def process_command(self, user_id: str, command: str) -> Dict:
        parsed = self.parse_trade_command(command)

        if not parsed:
            return {
                "success": False,
                "error": "Command not recognized",
                "help": "Try: 'Start paper trading', 'Buy 0.1 BTC', 'Sell all ETH', 'Show portfolio', 'Show leaderboard'"
            }

        action = parsed["action"]

        if action == "start":
            portfolio = self.create_portfolio(user_id)
            return {
                "success": True,
                "message": "Paper trading portfolio created!",
                "portfolio": portfolio.to_dict(self.current_prices)
            }

        elif action in ["buy", "sell", "sell_all"]:
            return self.execute_trade(user_id, parsed)

        elif action == "portfolio":
            return self.get_portfolio_status(user_id)

        elif action == "leaderboard":
            return self.get_leaderboard()

        elif action == "achievements":
            return {
                "success": True,
                "achievements": self.achievements.get_user_achievements(user_id)
            }

        elif action == "reset":
            if self.reset_portfolio(user_id):
                return {"success": True, "message": "Portfolio reset to $10,000"}
            return {"success": False, "error": "No portfolio to reset"}

        return {"success": False, "error": "Unknown action"}