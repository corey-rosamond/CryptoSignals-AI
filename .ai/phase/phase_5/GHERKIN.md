# 🥒 PHASE 5: REAL-TIME DATA INTEGRATION - GHERKIN SCENARIOS

## Feature: API Integration

```gherkin
Feature: Multi-Source API Integration
  As a crypto trader
  I want real-time market data
  So that I make informed decisions

  Background:
    Given the data aggregator is configured
    And API keys are valid
    And rate limits are set

  Scenario: Primary API Connection
    Given CoinGecko API is available
    When I request price for "BTC"
    Then the response should include:
      | Field         | Type     | Example    |
      | symbol        | String   | BTC        |
      | price         | Decimal  | 45000.00   |
      | change_24h    | Percent  | +2.3%      |
      | volume_24h    | Decimal  | 28.5B      |
      | market_cap    | Decimal  | 880B       |
    And response time should be <2 seconds
    And data should be cached for 5 minutes

  Scenario: Failover to Backup API
    Given CoinGecko API is unavailable
    And CoinMarketCap API is available
    When I request market data
    Then system should automatically failover
    And use CoinMarketCap API
    And return valid data
    And log the failover event
    And notify about degraded service

  Scenario: Rate Limit Management
    Given API rate limit is 50 calls/minute
    When I make 51 requests in 60 seconds
    Then request 51 should be queued
    And wait for rate limit reset
    And execute when allowed
    And user should see "Updating..." message

  Scenario Outline: Price Fetching for Top 20
    Given I need prices for top cryptocurrencies
    When I fetch price for <symbol>
    Then I should receive current price
    And 24h change percentage
    And volume data

    Examples:
      | symbol | expected_fields |
      | BTC    | price, volume   |
      | ETH    | price, volume   |
      | BNB    | price, volume   |
      | SOL    | price, volume   |
      | ADA    | price, volume   |
```

## Feature: Market Metrics Tracking

```gherkin
Feature: Global Market Metrics
  As a market analyst
  I want comprehensive market data
  So that I understand market conditions

  Scenario: Total Market Cap Calculation
    Given individual coin market caps:
      | Coin | Market Cap |
      | BTC  | $880B     |
      | ETH  | $280B     |
      | BNB  | $85B      |
      | Others | $855B   |
    When I calculate total market cap
    Then result should be "$2.1T"
    And display with proper formatting
    And update every 5 minutes

  Scenario: Fear & Greed Index Integration
    Given Alternative.me API is available
    When I fetch Fear & Greed Index
    Then I should receive:
      | Metric      | Value        |
      | Index       | 68          |
      | Label       | Greed       |
      | Updated     | 2 hours ago |
    And interpretation should be provided:
      """
      68 - Greed: Market is optimistic
      Consider taking profits
      Watch for corrections
      """

  Scenario: BTC Dominance Tracking
    Given BTC market cap is $880B
    And total market cap is $2.1T
    When I calculate BTC dominance
    Then result should be "41.9%"
    And show trend arrow (↑ or ↓)
    And compare to 30-day average

  Scenario: Volume Analysis
    Given 24h trading volumes:
      | Exchange  | Volume    |
      | Binance   | $28B     |
      | Coinbase  | $12B     |
      | Kraken    | $8B      |
      | Others    | $41B     |
    When I aggregate total volume
    Then display "$89B total volume"
    And show volume trend
    And identify unusual spikes
```

## Feature: Whale Alert System

```gherkin
Feature: Whale Movement Detection
  As a trader
  I want to know about large transactions
  So that I can anticipate market moves

  Scenario: Large Transaction Detection
    Given whale alert monitoring is active
    When a transaction occurs:
      | Field       | Value              |
      | Amount      | 1000 BTC          |
      | USD Value   | $45,000,000       |
      | From        | Unknown Wallet    |
      | To          | Binance           |
      | Time        | 2 minutes ago     |
    Then alert should trigger
    And format message:
      """
      🐋 WHALE ALERT
      1000 BTC ($45M) transferred to Binance
      Potential sell pressure incoming
      """
    And store in alert history
    And notify active users

  Scenario: Exchange Flow Analysis
    Given monitoring exchange wallets
    When calculating daily flows:
      | Metric         | Value    |
      | Inflows        | $234M    |
      | Outflows       | $189M    |
      | Net Flow       | -$45M    |
    Then interpret as:
      """
      Net Outflow: $45M leaving exchanges
      Bullish signal - supply reduction
      Holders accumulating
      """

  Scenario: Known Wallet Tracking
    Given top 100 wallet database exists
    When transaction from known wallet:
      | Wallet         | Label           |
      | bc1qxy...      | MicroStrategy   |
      | 1A1zP1...      | Grayscale      |
      | 3FKj9x...      | Tesla          |
    Then add context to alert:
      """
      MicroStrategy moving 500 BTC
      Historical: Usually holds long-term
      Impact: Low selling probability
      """

  Scenario Outline: Alert Thresholds
    Given different alert thresholds
    When <amount> <coin> moves
    Then alert level is <level>

    Examples:
      | amount  | coin | level    |
      | 100     | BTC  | Medium   |
      | 500     | BTC  | High     |
      | 1000    | BTC  | Critical |
      | 10000   | ETH  | High     |
      | 1000000 | USDT | High     |
```

## Feature: Cache Management

```gherkin
Feature: Intelligent Caching System
  As a system administrator
  I want efficient caching
  So that API costs stay low

  Scenario: Cache Hit
    Given price data cached 3 minutes ago
    And cache TTL is 5 minutes
    When user requests BTC price
    Then return cached data
    And show "Updated 3 min ago"
    And don't call external API
    And response time <100ms

  Scenario: Cache Miss
    Given no cached data exists
    When user requests ETH price
    Then fetch from primary API
    And store in cache with timestamp
    And set TTL to 5 minutes
    And return fresh data

  Scenario: Cache Invalidation
    Given cached data exists
    But significant price movement detected (>5%)
    When system checks cache validity
    Then invalidate current cache
    And fetch fresh data
    And update all dependent calculations

  Scenario: Stale Data Handling
    Given all APIs are down
    And cached data is 30 minutes old
    When user requests data
    Then return stale data with warning:
      """
      ⚠️ Data may be outdated (30 min old)
      External services temporarily unavailable
      Showing last known prices
      """

  Scenario: Cache Performance
    Given 1000 concurrent users
    When all request data simultaneously
    Then cache should handle load:
      | Metric           | Target    |
      | Response Time    | <200ms    |
      | Hit Rate         | >90%      |
      | Memory Usage     | <100MB    |
      | CPU Usage        | <10%      |
```

## Feature: Update Scheduling

```gherkin
Feature: Automated Update Cycles
  As a system
  I want scheduled updates
  So that data stays fresh

  Scenario: 5-Minute Update Cycle
    Given scheduler is configured
    When 5 minutes pass
    Then automatically:
      | Action                    | Status |
      | Fetch top 20 prices       | ✓     |
      | Update market metrics     | ✓     |
      | Check whale alerts        | ✓     |
      | Refresh Fear & Greed      | ✓     |
      | Clear expired cache       | ✓     |
    And log update completion

  Scenario: Priority Updates
    Given critical event detected
    When whale alert triggers
    Then immediately:
      1. Fetch affected coin price
      2. Update relevant metrics
      3. Bypass regular schedule
      4. Notify users instantly

  Scenario: Update Failure Recovery
    Given update cycle fails
    When retry mechanism activates
    Then:
      | Attempt | Delay | Action           |
      | 1       | 10s   | Retry primary    |
      | 2       | 30s   | Try backup API   |
      | 3       | 60s   | Use cached data  |
    And alert admin if all fail
```

## Success Criteria

```gherkin
Feature: Phase 5 Success Validation
  As a product owner
  I want to verify integration works
  So that users get real-time data

  Scenario: Data Accuracy
    Given real-time integration active
    When comparing our data to exchanges
    Then accuracy should be:
      | Metric         | Accuracy |
      | Price          | >99%     |
      | Volume         | >95%     |
      | Market Cap     | >98%     |
    And update within 5 minutes

  Scenario: System Reliability
    Given 24-hour monitoring period
    When measuring uptime
    Then achieve:
      | Metric         | Target  | Actual |
      | Uptime         | 99%     | ✓      |
      | API Failures   | <1%     | ✓      |
      | Cache Hit Rate | >90%    | ✓      |
      | Response Time  | <2s     | ✓      |

  Scenario: User Experience
    Given users interacting with GPT
    When they request market data
    Then experience should be:
      | Aspect         | Result            |
      | Data Freshness | Always <5 min old |
      | Load Speed     | Instant (<2s)     |
      | Accuracy       | Matches exchanges |
      | Whale Alerts   | Within 5 minutes  |
    And user satisfaction >90%
```