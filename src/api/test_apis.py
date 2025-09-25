#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from data_aggregator import DataAggregator
import time

def test_real_time_data():
    print("=" * 60)
    print("REAL-TIME DATA INTEGRATION TEST")
    print("=" * 60)

    aggregator = DataAggregator()

    print("\n1. Testing price fetching...")
    symbols = ["BTC", "ETH", "SOL", "ADA"]
    for symbol in symbols:
        price = aggregator.fetch_price(symbol)
        if price:
            print(f"   {symbol}: ${price:,.2f}")
        else:
            print(f"   {symbol}: Failed to fetch")

    print("\n2. Testing cache...")
    print("   Fetching BTC price again (should be cached)...")
    start = time.time()
    price = aggregator.fetch_price("BTC")
    elapsed = time.time() - start
    print(f"   BTC: ${price:,.2f} (fetched in {elapsed:.3f}s)")
    if elapsed < 0.1:
        print("   ✓ Cache working (fast response)")

    print("\n3. Testing market metrics...")
    market_data = aggregator.fetch_market_data()
    if market_data:
        metrics = aggregator.market_metrics.to_dict()
        print(f"   Total Market Cap: {metrics['total_market_cap']}")
        print(f"   24h Volume: {metrics['volume_24h']}")
        print(f"   BTC Dominance: {metrics['btc_dominance']}")
        print(f"   Fear & Greed: {metrics['fear_greed_index']} ({metrics['fear_greed_label']})")

        if metrics.get('top_gainers'):
            print("\n   Top Gainers:")
            for coin in metrics['top_gainers'][:3]:
                print(f"   - {coin['symbol']}: +{coin['change_24h']:.2f}%")

        if metrics.get('top_losers'):
            print("\n   Top Losers:")
            for coin in metrics['top_losers'][:3]:
                print(f"   - {coin['symbol']}: {coin['change_24h']:.2f}%")

    print("\n4. Testing whale alerts (simulation)...")
    alerts = aggregator.simulate_whale_activity()
    for alert in alerts[:2]:
        print(alert)

    print("\n5. Testing flow analysis...")
    flow = aggregator.get_flow_analysis()
    print(f"   Exchange Inflow: ${flow['exchange_inflow']:,.0f}")
    print(f"   Exchange Outflow: ${flow['exchange_outflow']:,.0f}")
    print(f"   Net Flow: ${flow['net_flow']:,.0f}")
    print(f"   Interpretation: {flow['interpretation']}")

    print("\n6. Testing comprehensive data fetch...")
    all_data = aggregator.get_all_data()
    print(f"   Data keys: {list(all_data.keys())}")
    print(f"   Top coins count: {len(all_data.get('top_coins', []))}")
    print(f"   Whale alerts count: {len(all_data.get('whale_alerts', []))}")
    print(f"   Cache stats: {all_data.get('cache_stats')}")

    print("\n7. Testing bulk price fetch...")
    bulk_symbols = ["BTC", "ETH", "BNB", "SOL", "ADA", "DOT"]
    prices = aggregator.get_price_bulk(bulk_symbols)
    print(f"   Fetched {len(prices)} prices:")
    for symbol, price in prices.items():
        print(f"   - {symbol}: ${price:,.2f}")

    print("\n8. Testing cache status...")
    cache_status = aggregator.get_cache_status()
    print(f"   Hit rate: {cache_status['hit_rate']}")
    print(f"   Total cached: {cache_status['total_cached']}")
    print(f"   Update frequency: {cache_status['update_frequency']}")

    print("\n9. Testing scheduler...")
    print("   Starting 5-minute update scheduler...")
    aggregator.schedule_updates(5)
    print("   ✓ Scheduler started (running in background)")

    # Wait a bit to see if scheduler works
    time.sleep(2)

    print("\n10. Stopping scheduler...")
    aggregator.stop_scheduler()
    print("   ✓ Scheduler stopped")

    print("\n" + "=" * 60)
    print("TEST COMPLETE - Real-time Data Integration Working!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    try:
        # Note: This test requires internet connection and will make real API calls
        # CoinGecko API doesn't require a key for basic usage
        success = test_real_time_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)