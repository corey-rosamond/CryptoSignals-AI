#!/usr/bin/env python3
"""
Viral Amplification System for CryptoSignals AI
Generates shareable content and tracks viral metrics
"""

import json
import random
from datetime import datetime

class ViralAmplificationSystem:
    """
    Manages viral mechanics to achieve K-factor > 1.5
    Each user should bring in 1.5+ new users on average
    """

    def __init__(self):
        self.share_templates = self.load_share_templates()
        self.achievements = self.load_achievements()
        self.viral_triggers = self.load_viral_triggers()

    def load_share_templates(self):
        """Load platform-specific share templates"""
        return {
            "twitter": [
                "🚀 Just hit a {win_streak}-day winning streak on CryptoSignals AI! My portfolio is up {roi}% this week! #CryptoTrading #AI",
                "💎 Unlocked {achievement} achievement on CryptoSignals AI! Currently #{rank} on the leaderboard! Who's next? 🎯",
                "📈 CryptoSignals AI just predicted {prediction} with {confidence}% confidence! Track record: {accuracy}% accurate! 🔥",
                "🏆 Just won the weekly paper trading competition on CryptoSignals AI! Prize: ${prize}! Join me next week? 💰",
                "🐋 WHALE ALERT from CryptoSignals AI: {whale_move}! Get real-time alerts FREE! 🚨"
            ],
            "reddit": [
                "[Achievement] Just unlocked {achievement} on CryptoSignals AI after {trades} trades!",
                "[Competition] Won this week's paper trading contest with {roi}% ROI! Here's my strategy...",
                "[Analysis] CryptoSignals AI predicted {prediction} - here's the technical breakdown...",
                "[Success Story] Started with $10K paper money, now at ${portfolio_value} in {days} days!",
                "[Free Tool] Found this AI that gives real-time crypto signals with {accuracy}% accuracy"
            ],
            "telegram": [
                "🎯 New prediction from CryptoSignals AI:\\n{prediction}\\nConfidence: {confidence}%\\nJoin: {link}",
                "📊 Weekly Stats:\\n✅ Wins: {wins}\\n❌ Losses: {losses}\\n📈 ROI: {roi}%\\nTry it FREE!",
                "🏆 Leaderboard Update:\\n1st: {first_place}\\n2nd: {second_place}\\n3rd: {third_place}\\nYou: #{your_rank}"
            ],
            "discord": [
                "**ACHIEVEMENT UNLOCKED!** 🎉\\n{achievement}\\nPoints: {points}\\nLevel: {level}",
                "**PREDICTION ALERT** 📢\\n{prediction}\\nEntry: {entry}\\nTarget: {target}\\nConfidence: {confidence}%",
                "**COMPETITION UPDATE** 🏁\\nCurrent Leader: {leader}\\nROI: {roi}%\\nTime Left: {time_left}"
            ]
        }

    def load_achievements(self):
        """Load achievement definitions"""
        return {
            "first_trade": {"name": "🎯 First Blood", "points": 10, "share_worthy": True},
            "winning_streak_3": {"name": "🔥 Hot Streak", "points": 25, "share_worthy": True},
            "winning_streak_5": {"name": "🔥🔥 On Fire", "points": 50, "share_worthy": True},
            "winning_streak_10": {"name": "🔥🔥🔥 Unstoppable", "points": 100, "share_worthy": True},
            "profit_100": {"name": "💰 Benjamin Club", "points": 30, "share_worthy": True},
            "profit_1000": {"name": "👑 Profit King", "points": 75, "share_worthy": True},
            "profit_10000": {"name": "🏆 Master Trader", "points": 200, "share_worthy": True},
            "diamond_hands": {"name": "💎🙌 Diamond Hands", "points": 100, "share_worthy": True},
            "whale_spotter": {"name": "🐋 Whale Whisperer", "points": 50, "share_worthy": True},
            "moon_shot": {"name": "🚀 To The Moon", "points": 500, "share_worthy": True},
            "perfect_week": {"name": "⚡ Perfect Week", "points": 150, "share_worthy": True},
            "competition_winner": {"name": "🥇 Champion", "points": 250, "share_worthy": True}
        }

    def load_viral_triggers(self):
        """Define events that trigger viral sharing prompts"""
        return {
            "achievement_unlock": {
                "prompt": "🎉 Amazing! Share your achievement?",
                "buttons": ["Share on Twitter", "Share on Reddit", "Skip"],
                "reward": 50  # Bonus XP for sharing
            },
            "winning_streak": {
                "prompt": "🔥 You're on fire! Let others know?",
                "buttons": ["Brag on Twitter", "Post to Discord", "Keep it humble"],
                "reward": 25
            },
            "leaderboard_top3": {
                "prompt": "🏆 Top 3! Claim your bragging rights?",
                "buttons": ["Tweet Victory", "Reddit Post", "Stay Silent"],
                "reward": 100
            },
            "big_win": {
                "prompt": "💰 Huge win! Share your success?",
                "buttons": ["Share Strategy", "Tweet Result", "Keep Secret"],
                "reward": 75
            },
            "milestone_reached": {
                "prompt": "🎯 Milestone reached! Celebrate?",
                "buttons": ["Share Journey", "Post Screenshot", "Continue"],
                "reward": 40
            }
        }

    def generate_share_content(self, event_type, platform, data):
        """Generate personalized share content"""
        templates = self.share_templates.get(platform, [])
        if not templates:
            return None

        # Select random template
        template = random.choice(templates)

        # Fill in dynamic data
        content = template.format(**data)

        # Add referral link
        referral_code = self.generate_referral_code(data.get('user_id', 'anonymous'))
        content += f"\\n\\n🔗 Try it FREE: chatgpt.com/g/cryptosignals-ai?ref={referral_code}"

        # Add hashtags for social platforms
        if platform in ['twitter', 'instagram']:
            content += "\\n#CryptoSignals #AITrading #CryptoGains #PaperTrading"

        return content

    def generate_referral_code(self, user_id):
        """Generate unique referral code"""
        timestamp = datetime.now().strftime("%m%d")
        return f"CS{timestamp}{str(user_id)[:4]}"

    def calculate_viral_coefficient(self, metrics):
        """Calculate K-factor (viral coefficient)"""
        invites_sent = metrics.get('invites_sent', 0)
        conversion_rate = metrics.get('conversion_rate', 0.02)  # 2% default

        k_factor = invites_sent * conversion_rate
        return k_factor

    def get_viral_optimization_tips(self, current_k_factor):
        """Provide tips to improve viral coefficient"""
        tips = []

        if current_k_factor < 0.5:
            tips.append("🔴 Critical: Need more share triggers")
            tips.append("Add celebration moments after wins")
            tips.append("Implement friend challenges")

        elif current_k_factor < 1.0:
            tips.append("🟡 Growing: Increase share incentives")
            tips.append("Add XP bonuses for successful referrals")
            tips.append("Create weekly share challenges")

        elif current_k_factor < 1.5:
            tips.append("🟢 Good: Optimize conversion")
            tips.append("A/B test share messages")
            tips.append("Add social proof to shares")

        else:
            tips.append("🚀 Viral: Maintain momentum")
            tips.append("Scale successful campaigns")
            tips.append("Expand to new platforms")

        return tips

    def create_competition_invite(self, competition_data):
        """Create invitation for competitions"""
        return {
            "title": f"🏆 {competition_data['name']} Challenge",
            "message": f"Join me in the {competition_data['name']}!\\n"
                      f"Prize Pool: ${competition_data['prize']}\\n"
                      f"Current Leader: {competition_data['leader']}\\n"
                      f"Spots Left: {competition_data['spots_left']}",
            "cta": "Join Competition",
            "urgency": f"Ends in {competition_data['time_left']}"
        }

    def generate_fomo_triggers(self):
        """Generate FOMO (Fear of Missing Out) messages"""
        return [
            "⚡ Only 3 spots left in top 10 this week!",
            "🔥 Current leader has 157% ROI - can you beat it?",
            "⏰ Competition ends in 2 hours!",
            "🐋 Whale alert triggered 5 minutes ago!",
            "📈 3 users just unlocked Diamond Hands!",
            "🎯 78.5% prediction accuracy this week!",
            "💰 $500 in prizes given out today!",
            "🚀 BTC prediction just hit - 12% gain!"
        ]

    def create_viral_campaign(self, campaign_type):
        """Create targeted viral campaign"""
        campaigns = {
            "new_user": {
                "day_1": "Welcome! Complete first trade for 100 XP",
                "day_2": "Try paper trading - $10K to start!",
                "day_3": "Join weekly competition - $50 prize!",
                "day_7": "Invite friend = 500 XP each!"
            },
            "retention": {
                "streak_3": "Keep streak alive! +50 XP/day",
                "inactive_3": "Miss your predictions? New features!",
                "milestone": "Almost at next level! 200 XP to go"
            },
            "competition": {
                "monday": "New week, new competition! Join now",
                "friday": "Final push! Double XP weekend",
                "sunday": "Last day! Current rank: #12"
            }
        }
        return campaigns.get(campaign_type, {})

# Test the system
if __name__ == "__main__":
    viral = ViralAmplificationSystem()

    # Example: Generate share content for achievement
    share_data = {
        "achievement": "Diamond Hands",
        "points": 100,
        "level": 15,
        "user_id": "user123",
        "roi": 45.7,
        "accuracy": 78.5,
        "win_streak": 5,
        "rank": 3,
        "confidence": 85,
        "prediction": "BTC/USD BUY @ 46,200",
        "prize": 50,
        "whale_move": "1000 BTC moved to exchange",
        "trades": 25,
        "portfolio_value": 14500,
        "days": 7,
        "wins": 18,
        "losses": 7,
        "link": "chatgpt.com/g/cryptosignals-ai",
        "entry": "$46,200",
        "target": "$47,500",
        "first_place": "@CryptoKing",
        "second_place": "@MoonTrader",
        "third_place": "@DiamondHands",
        "your_rank": 5,
        "leader": "@CryptoKing",
        "time_left": "2 hours"
    }

    # Generate content for different platforms
    for platform in ["twitter", "reddit", "discord"]:
        content = viral.generate_share_content("achievement_unlock", platform, share_data)
        print(f"\\n{platform.upper()} Share:")
        print(content)
        print("-" * 50)

    # Calculate viral coefficient
    metrics = {
        "invites_sent": 3.2,  # Average invites per user
        "conversion_rate": 0.47  # 47% conversion
    }
    k_factor = viral.calculate_viral_coefficient(metrics)
    print(f"\\nViral Coefficient (K-factor): {k_factor:.2f}")

    # Get optimization tips
    tips = viral.get_viral_optimization_tips(k_factor)
    print("\\nOptimization Tips:")
    for tip in tips:
        print(f"  • {tip}")

    # Generate FOMO triggers
    print("\\nFOMO Triggers:")
    for trigger in viral.generate_fomo_triggers()[:3]:
        print(f"  • {trigger}")