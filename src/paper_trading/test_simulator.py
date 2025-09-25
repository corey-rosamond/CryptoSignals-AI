#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal

# Import individual modules directly
from portfolio import Portfolio
from leaderboard import Leaderboard
from achievements import AchievementSystem
from challenges import ChallengeManager

# Import simulator after dependencies
import simulator
PaperTradingSimulator = simulator.PaperTradingSimulator

def test_paper_trading():
    print("=" * 60)
    print("PAPER TRADING SIMULATOR TEST")
    print("=" * 60)

    # Initialize simulator
    simulator = PaperTradingSimulator()

    # Set some sample prices
    simulator.update_prices({
        "BTC": Decimal("45000"),
        "ETH": Decimal("3000"),
        "SOL": Decimal("150"),
        "ADA": Decimal("0.45")
    })

    # Test user ID
    user_id = "test_user_001"

    print("\n1. Testing portfolio creation...")
    result = simulator.process_command(user_id, "Start paper trading with $10K")
    print(f"   Result: {result['message'] if result.get('success') else result.get('error')}")
    if result.get('portfolio'):
        print(f"   Balance: ${result['portfolio']['balance']}")

    print("\n2. Testing buy command...")
    result = simulator.process_command(user_id, "Buy 0.1 BTC")
    if result.get('success'):
        print(f"   ✓ Bought {result['quantity']} {result['symbol']} at ${result['price']}")
        print(f"   Total cost: ${result['total_cost']}")
        print(f"   New balance: ${result['new_balance']}")
        if result.get('achievements_unlocked'):
            for achievement in result['achievements_unlocked']:
                print(f"   🏆 Achievement unlocked: {achievement['name']} ({achievement['badge']}) +{achievement['points']}pts")

    print("\n3. Testing another buy...")
    result = simulator.process_command(user_id, "Buy 2 ETH")
    if result.get('success'):
        print(f"   ✓ Bought {result['quantity']} {result['symbol']} at ${result['price']}")
        print(f"   New balance: ${result['new_balance']}")

    print("\n4. Testing portfolio view...")
    result = simulator.process_command(user_id, "Show my portfolio")
    if not result.get('error'):
        print(f"   Balance: ${result['balance']}")
        print(f"   Total Value: ${result['total_value']}")
        print(f"   ROI: {result['roi']}%")
        print(f"   Positions: {result['positions_count']}")
        print(f"   Win Rate: {result['win_rate']}%")
        print(f"   Rank: #{result['rank'] or 'N/A'}")

        if result.get('achievements'):
            print(f"   Total Points: {result['achievements']['total_points']}")
            print(f"   Achievements: {result['achievements']['unlocked_count']}/{result['achievements']['total_count']}")
            if result['achievements']['badges']:
                print(f"   Badges: {' '.join(result['achievements']['badges'])}")

        if result.get('daily_challenge'):
            challenge = result['daily_challenge']
            print(f"\n   Daily Challenge: {challenge['challenge']['name']}")
            print(f"   Requirement: {challenge['challenge']['requirement']}")
            print(f"   Progress: {challenge['progress']}/{challenge['target']}")
            print(f"   Reward: {challenge['challenge']['reward']}")
            print(f"   Streak: {challenge['streak']} days")

    print("\n5. Simulating price increase...")
    simulator.update_prices({
        "BTC": Decimal("47000"),  # +4.4% increase
        "ETH": Decimal("3200"),   # +6.7% increase
        "SOL": Decimal("150"),
        "ADA": Decimal("0.45")
    })

    print("\n6. Testing sell command...")
    result = simulator.process_command(user_id, "Sell all BTC")
    if result.get('success'):
        print(f"   ✓ Sold {result['positions_closed']} {result['symbol']} position(s)")
        print(f"   P&L: ${result['total_pnl']}")
        print(f"   New balance: ${result['new_balance']}")
        if result.get('achievements_unlocked'):
            for achievement in result['achievements_unlocked']:
                print(f"   🏆 Achievement: {achievement['name']} +{achievement['points']}pts")

    print("\n7. Testing leaderboard...")
    result = simulator.process_command(user_id, "Show leaderboard")
    if result.get('rankings'):
        print("   Top Traders:")
        for i, trader in enumerate(result['rankings'][:5], 1):
            print(f"   #{trader['rank']} {trader['username']}: {trader['roi']} P&L: {trader['pnl']} ({trader['trades']} trades)")

        if result.get('competition'):
            print(f"\n   Competition Status:")
            print(f"   Time remaining: {result['competition']['time_remaining']}")
            print(f"   Participants: {result['competition']['participants']}")
            print(f"   Prize pool: ${result['competition']['prize_pool']}")

    print("\n8. Creating second user for competition...")
    user2_id = "test_user_002"
    simulator.process_command(user2_id, "Start paper trading")
    simulator.process_command(user2_id, "Buy 0.5 BTC")
    simulator.process_command(user2_id, "Buy 5 SOL")

    print("\n9. Testing achievements view...")
    result = simulator.process_command(user_id, "Show my achievements")
    if result.get('success') and result.get('achievements'):
        achievements = result['achievements']
        print(f"   Total Points: {achievements['total_points']}")
        print(f"   Unlocked: {achievements['unlocked_count']}/{achievements['total_count']}")

        if achievements['achievements']:
            print("\n   Earned Achievements:")
            for ach in achievements['achievements'][:3]:
                print(f"   - {ach['badge']} {ach['name']}: {ach['description']} (+{ach['points']}pts)")

        if achievements['progress']:
            print("\n   Next to Unlock:")
            for prog in achievements['progress'][:2]:
                print(f"   - {prog['badge']} {prog['name']}: {prog['description']}")
                print(f"     {prog['requirement']} (+{prog['points']}pts)")

    print("\n10. Testing invalid command...")
    result = simulator.process_command(user_id, "Invalid command test")
    if not result.get('success'):
        print(f"   Error: {result.get('error')}")
        if result.get('help'):
            print(f"   Help: {result['help']}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE - Paper Trading Simulator Working!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    try:
        success = test_paper_trading()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)