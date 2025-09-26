#!/usr/bin/env python3
"""
Enhanced Prediction Tracking Automation System
Validates predictions, calculates performance, and auto-updates GitHub
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
import time
import requests

class PredictionTracker:
    """Automated prediction tracking and validation system"""

    def __init__(self):
        self.data_dir = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals/data"
        self.predictions_file = f"{self.data_dir}/performance.csv"
        self.repo_dir = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals"
        self.ssh_key = "/home/corey/.ssh/crypto_signals_deploy_key"

    def get_crypto_prices(self, symbols):
        """Get current prices from CoinGecko API"""
        try:
            # Map common symbols to CoinGecko IDs
            id_map = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "BNB": "binancecoin",
                "SOL": "solana",
                "ADA": "cardano",
                "XRP": "ripple",
                "DOT": "polkadot",
                "AVAX": "avalanche-2",
                "LINK": "chainlink",
                "MATIC": "polygon",
                "UNI": "uniswap",
                "ATOM": "cosmos",
                "NEAR": "near",
                "ALGO": "algorand",
                "FTM": "fantom",
                "VET": "vechain",
                "ICP": "internet-computer",
                "DOGE": "dogecoin"
            }

            # Build IDs list
            ids = []
            for symbol in symbols:
                base_symbol = symbol.replace("/USD", "").upper()
                if base_symbol in id_map:
                    ids.append(id_map[base_symbol])

            if not ids:
                return {}

            # Fetch prices
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": ",".join(ids),
                "vs_currencies": "usd",
                "include_24hr_change": "true"
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Map back to symbols
                result = {}
                for symbol in symbols:
                    base_symbol = symbol.replace("/USD", "").upper()
                    if base_symbol in id_map:
                        gecko_id = id_map[base_symbol]
                        if gecko_id in data:
                            result[symbol] = data[gecko_id]["usd"]
                return result

        except Exception as e:
            print(f"Error fetching prices: {e}")
            return {}

    def validate_prediction(self, prediction):
        """Validate if a prediction hit target or stop loss"""
        # Skip if already has result or is HOLD
        if prediction["Result"] not in ["PENDING", ""] or prediction["Signal"] == "HOLD":
            return prediction

        # Parse prediction time
        pred_date = datetime.strptime(prediction["Date"], "%Y-%m-%d")
        pred_time = datetime.strptime(prediction["Time"], "%H:%M")
        pred_datetime = pred_date.replace(hour=pred_time.hour, minute=pred_time.minute)

        # Check if enough time has passed based on timeframe
        timeframe_hours = {
            "1H": 1, "2H": 2, "3H": 3, "4H": 4,
            "6H": 6, "12H": 12, "1D": 24, "3D": 72
        }
        hours = timeframe_hours.get(prediction["Timeframe"], 4)

        if datetime.now() < pred_datetime + timedelta(hours=hours):
            return prediction  # Not enough time passed

        # Get current price
        prices = self.get_crypto_prices([prediction["Asset"]])
        if prediction["Asset"] not in prices:
            return prediction  # Could not get price

        current_price = prices[prediction["Asset"]]
        entry = float(prediction["Entry"])
        target = float(prediction["Target"])
        stop_loss = float(prediction["StopLoss"])

        # Check if target or stop loss hit
        if prediction["Signal"] == "BUY":
            if current_price >= target:
                prediction["Result"] = "WIN"
                prediction["ActualExit"] = str(target)
                roi = ((target - entry) / entry) * 100
                prediction["ROI"] = f"{roi:.2f}%"
            elif current_price <= stop_loss:
                prediction["Result"] = "LOSS"
                prediction["ActualExit"] = str(stop_loss)
                roi = ((stop_loss - entry) / entry) * 100
                prediction["ROI"] = f"{roi:.2f}%"

        elif prediction["Signal"] == "SELL":
            if current_price <= target:
                prediction["Result"] = "WIN"
                prediction["ActualExit"] = str(target)
                roi = ((entry - target) / entry) * 100
                prediction["ROI"] = f"{roi:.2f}%"
            elif current_price >= stop_loss:
                prediction["Result"] = "LOSS"
                prediction["ActualExit"] = str(stop_loss)
                roi = ((entry - stop_loss) / entry) * 100
                prediction["ROI"] = f"{roi:.2f}%"

        return prediction

    def calculate_statistics(self, predictions):
        """Calculate performance statistics"""
        stats = {
            "total_predictions": 0,
            "wins": 0,
            "losses": 0,
            "pending": 0,
            "holds": 0,
            "win_rate": 0,
            "average_roi": 0,
            "total_roi": 0,
            "best_trade": None,
            "worst_trade": None,
            "current_streak": 0,
            "best_streak": 0
        }

        rois = []
        streak = 0

        for pred in predictions:
            if pred["Signal"] == "HOLD":
                stats["holds"] += 1
                continue

            stats["total_predictions"] += 1

            if pred["Result"] == "WIN":
                stats["wins"] += 1
                streak += 1
                stats["best_streak"] = max(stats["best_streak"], streak)

                if pred["ROI"]:
                    roi = float(pred["ROI"].replace("%", ""))
                    rois.append(roi)
                    if not stats["best_trade"] or roi > float(stats["best_trade"]["ROI"].replace("%", "")):
                        stats["best_trade"] = pred

            elif pred["Result"] == "LOSS":
                stats["losses"] += 1
                streak = 0

                if pred["ROI"]:
                    roi = float(pred["ROI"].replace("%", ""))
                    rois.append(roi)
                    if not stats["worst_trade"] or roi < float(stats["worst_trade"]["ROI"].replace("%", "")):
                        stats["worst_trade"] = pred

            elif pred["Result"] == "PENDING":
                stats["pending"] += 1

        stats["current_streak"] = streak

        # Calculate rates
        if stats["wins"] + stats["losses"] > 0:
            stats["win_rate"] = (stats["wins"] / (stats["wins"] + stats["losses"])) * 100

        if rois:
            stats["average_roi"] = sum(rois) / len(rois)
            stats["total_roi"] = sum(rois)

        return stats

    def update_predictions_file(self):
        """Update predictions file with validation results"""
        # Read existing predictions
        predictions = []
        with open(self.predictions_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Validate pending predictions
                updated_row = self.validate_prediction(row)
                predictions.append(updated_row)

        # Write back updated predictions
        with open(self.predictions_file, 'w', newline='') as f:
            fieldnames = ["Date", "Time", "ID", "Asset", "Signal", "Entry",
                         "Target", "StopLoss", "Confidence", "Timeframe",
                         "Result", "ActualExit", "ROI", "Notes"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(predictions)

        return predictions

    def generate_performance_report(self, stats):
        """Generate markdown performance report"""
        report = f"""# 📊 CryptoSignals AI Performance Report
*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC*

## 📈 Overall Statistics
- **Total Predictions:** {stats['total_predictions']}
- **Wins:** {stats['wins']} ✅
- **Losses:** {stats['losses']} ❌
- **Pending:** {stats['pending']} ⏳
- **Win Rate:** {stats['win_rate']:.1f}% 🎯
- **Average ROI:** {stats['average_roi']:.2f}%
- **Total ROI:** {stats['total_roi']:.2f}%

## 🔥 Streaks
- **Current Streak:** {stats['current_streak']}
- **Best Streak:** {stats['best_streak']}

## 🏆 Notable Trades
"""

        if stats['best_trade']:
            report += f"""### Best Trade
- **{stats['best_trade']['Asset']}** - {stats['best_trade']['Signal']}
- **ROI:** {stats['best_trade']['ROI']}
- **Date:** {stats['best_trade']['Date']}
"""

        if stats['worst_trade']:
            report += f"""### Worst Trade
- **{stats['worst_trade']['Asset']}** - {stats['worst_trade']['Signal']}
- **ROI:** {stats['worst_trade']['ROI']}
- **Date:** {stats['worst_trade']['Date']}
"""

        report += """
---
*Disclaimer: Past performance does not guarantee future results. Educational purposes only.*
"""
        return report

    def commit_and_push(self):
        """Commit changes and push to GitHub"""
        try:
            os.chdir(self.repo_dir)

            # Configure git
            subprocess.run(["git", "config", "user.email", "ai@cryptosignals.com"], check=True)
            subprocess.run(["git", "config", "user.name", "CryptoSignals AI"], check=True)

            # Add changes
            subprocess.run(["git", "add", "data/performance.csv"], check=True)
            subprocess.run(["git", "add", "data/PERFORMANCE_REPORT.md"], check=True)

            # Commit
            commit_msg = f"Update predictions - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)

            # Push with SSH key
            env = os.environ.copy()
            env["GIT_SSH_COMMAND"] = f"ssh -i {self.ssh_key}"
            subprocess.run(["git", "push", "origin", "master"], env=env, check=True)

            print("✅ Successfully pushed to GitHub")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False

    def run_automation(self):
        """Main automation workflow"""
        print("🚀 Starting prediction automation...")

        # Update predictions
        print("📊 Validating predictions...")
        predictions = self.update_predictions_file()

        # Calculate statistics
        print("📈 Calculating statistics...")
        stats = self.calculate_statistics(predictions)

        # Generate report
        print("📝 Generating performance report...")
        report = self.generate_performance_report(stats)

        # Save report
        report_file = f"{self.data_dir}/PERFORMANCE_REPORT.md"
        with open(report_file, 'w') as f:
            f.write(report)

        # Display summary
        print(f"""
✨ Automation Complete!
- Total Predictions: {stats['total_predictions']}
- Win Rate: {stats['win_rate']:.1f}%
- Current Streak: {stats['current_streak']}
- Pending: {stats['pending']}
        """)

        # Optionally push to GitHub
        # self.commit_and_push()

        return stats


# Run if executed directly
if __name__ == "__main__":
    tracker = PredictionTracker()
    tracker.run_automation()