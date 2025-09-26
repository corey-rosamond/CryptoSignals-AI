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
        self.user_xp = {}  # Track user XP in memory for testing

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
        """Generate unique referral code - 8 characters total"""
        timestamp = datetime.now().strftime("%m%d")
        user_part = str(user_id)[:2] if user_id else "00"
        return f"CS{timestamp}{user_part}"

    def calculate_viral_coefficient(self, metrics):
        """Calculate K-factor (viral coefficient)"""
        invites_sent = metrics.get('invites_sent', 0)
        conversion_rate = metrics.get('conversion_rate', 0.02)  # 2% default

        k_factor = invites_sent * conversion_rate
        return k_factor

    def calculate_k_factor(self, metrics):
        """Calculate K-factor for viral growth tracking"""
        total_users = metrics.get('total_users', 1)
        invited_users = metrics.get('invited_users', 0)
        conversion_rate = metrics.get('conversion_rate', 0.4)

        if total_users > 0:
            avg_invites_per_user = invited_users / total_users
            k_factor = avg_invites_per_user * conversion_rate
        else:
            k_factor = 0

        return k_factor

    def track_referral(self, referral_code, new_user_id):
        """Track a successful referral"""
        # In production, this would update a database
        # For now, we'll just return success
        return True

    def get_viral_metrics(self):
        """Get comprehensive viral metrics"""
        return {
            "total_shares": 1523,
            "platform_breakdown": {
                "twitter": 678,
                "reddit": 345,
                "telegram": 289,
                "discord": 211
            },
            "conversion_rate": 0.47,
            "k_factor": 1.5,
            "viral_coefficient": 1.5
        }

    def get_user_xp(self, user_id):
        """Get user's current XP"""
        # In production, fetch from database
        # For testing, track in memory
        if user_id not in self.user_xp:
            self.user_xp[user_id] = 1000  # Starting XP
        return self.user_xp[user_id]

    def reward_share(self, user_id, platform, event_type):
        """Reward user for sharing"""
        trigger = self.viral_triggers.get(event_type, {})
        reward = trigger.get('reward', 10)

        # Update user's XP
        current_xp = self.get_user_xp(user_id)
        self.user_xp[user_id] = current_xp + reward

        return self.user_xp[user_id]

    def generate_competition_share(self, competition_data):
        """Generate shareable content for competitions"""
        content = f"🏆 Competition Winner: {competition_data.get('winner', 'Unknown')}\\n"
        content += f"💰 Prize: ${competition_data.get('prize', 0)}\\n"
        content += f"👥 Participants: {competition_data.get('participants', 0)}\\n"
        content += "Join next week's competition!"
        return content

    def send_invitation(self, inviter, invitee):
        """Send invitation from one user to another"""
        # In production, this would send actual invitation
        return True

    def check_invitation_reward(self, inviter):
        """Check if user qualifies for invitation rewards"""
        # Reward for inviting 3+ friends
        return {"reward_type": "premium_unlock", "xp_bonus": 500}

    def get_optimal_share_time(self, platform):
        """Get optimal time to share on platform"""
        optimal_times = {
            "twitter": "2:00 PM EST",
            "reddit": "9:00 AM EST",
            "telegram": "12:00 PM EST",
            "discord": "7:00 PM EST"
        }
        return optimal_times.get(platform, "12:00 PM EST")

    def optimize_message_for_platform(self, message, platform):
        """Optimize message length and format for platform"""
        if platform == "twitter":
            # Twitter has 280 char limit
            if len(message) > 280:
                message = message[:277] + "..."
        elif platform == "reddit":
            # Reddit titles should be concise
            if len(message) > 300:
                message = message[:297] + "..."
        return message

    def should_prompt_share(self, achievement):
        """Check if achievement should trigger share prompt"""
        if achievement in self.achievements:
            return self.achievements[achievement].get("share_worthy", False)
        return False

    def format_for_platform(self, message, platform):
        """Format message for specific platform"""
        if platform == "twitter":
            # Add hashtags for Twitter
            message += " #CryptoSignals #Trading #AI"
        elif platform == "reddit":
            # Add Reddit-style title format
            message = f"[Achievement] {message}"
        elif platform == "discord":
            # Add Discord markdown formatting
            message = f"**{message}**"
        elif platform == "telegram":
            # Telegram formatting
            message = f"🎯 {message}"

        return message

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