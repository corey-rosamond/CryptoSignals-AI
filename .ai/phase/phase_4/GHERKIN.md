# 🥒 PHASE 4: PAPER TRADING SIMULATOR - GHERKIN SCENARIOS

## Feature: Paper Trading Simulator

```gherkin
Feature: Paper Trading Simulator
  As a trader wanting to practice
  I want to trade with virtual money
  So that I can improve without financial risk

  Background:
    Given the paper trading system is active
    And the starting balance is $10,000
    And real market prices are used

  Scenario: Creating Virtual Portfolio
    Given I am a new user
    When I say "Start paper trading with $10K"
    Then a virtual portfolio should be created
    And I should see:
      | Field          | Value    |
      | Balance        | $10,000  |
      | Positions      | 0        |
      | Total Value    | $10,000  |
      | P&L            | $0       |
      | ROI            | 0%       |
    And I should receive instructions
    And my portfolio ID should be saved

  Scenario: Executing Buy Order
    Given I have $10,000 balance
    And BTC price is $45,000
    When I say "Buy 0.1 BTC"
    Then the trade should execute:
      | Field          | Value    |
      | Action         | BUY      |
      | Symbol         | BTC      |
      | Quantity       | 0.1      |
      | Price          | $45,000  |
      | Total Cost     | $4,500   |
      | New Balance    | $5,500   |
    And position should be added to portfolio
    And trade history should be updated

  Scenario: Tracking Profit and Loss
    Given I bought 0.1 BTC at $45,000
    And current BTC price is $47,000
    When I check my portfolio
    Then I should see:
      | Metric         | Value    |
      | Position Value | $4,700   |
      | Unrealized P&L | $200     |
      | ROI            | 4.44%    |
      | Total Value    | $10,200  |
    And profit should be highlighted green

  Scenario: Closing Position
    Given I have 0.1 BTC bought at $45,000
    And current price is $47,000
    When I say "Sell all BTC"
    Then the position should close:
      | Field          | Value    |
      | Sale Price     | $47,000  |
      | Quantity       | 0.1      |
      | Proceeds       | $4,700   |
      | Realized P&L   | $200     |
      | New Balance    | $10,200  |
    And position should be removed
    And P&L should be recorded

  Scenario Outline: Multiple Trading Scenarios
    Given I have <balance> available
    When I execute trade: <action> <quantity> <symbol>
    Then my portfolio should show:
      | New Balance | Position Count | Status   |
      | <new_bal>   | <positions>    | <status> |

    Examples:
      | balance | action | quantity | symbol | new_bal | positions | status  |
      | $10,000 | BUY    | 0.2      | BTC    | $1,000  | 1         | Success |
      | $5,000  | BUY    | 2        | ETH    | $1,000  | 2         | Success |
      | $1,000  | BUY    | 10       | SOL    | $500    | 3         | Success |
```

## Feature: Leaderboard System

```gherkin
Feature: Leaderboard System
  As a competitive trader
  I want to see rankings
  So that I can compare my performance

  Scenario: Viewing Leaderboard
    Given multiple users are trading
    When I check the leaderboard
    Then I should see:
      | Rank | User     | ROI     | P&L      | Trades |
      | 1    | Alice    | +15.2%  | +$1,520  | 23     |
      | 2    | Bob      | +12.8%  | +$1,280  | 18     |
      | 3    | Charlie  | +10.5%  | +$1,050  | 31     |
      | ...  | ...      | ...     | ...      | ...    |
    And my position should be highlighted
    And update time should be shown

  Scenario: Real-time Ranking Updates
    Given I am ranked #5 with 8% ROI
    When I make a profitable trade increasing ROI to 11%
    Then my ranking should update
    And I should move to #3
    And the change should be animated
    And other users should see update

  Scenario: Multiple Timeframe Views
    Given leaderboard has different periods
    When I switch views:
      | View    | My Rank | Leader  | Leader ROI |
      | Daily   | #12     | David   | +5.2%      |
      | Weekly  | #8      | Alice   | +15.2%     |
      | Monthly | #15     | Eve     | +42.3%     |
      | All-Time| #23     | Frank   | +189.5%    |
    Then each view should show different data
    And rankings should be independent
```

## Feature: Achievement System

```gherkin
Feature: Achievement System
  As a gamer-trader
  I want to unlock achievements
  So that I feel progress and accomplishment

  Scenario: Unlocking First Trade Achievement
    Given I have never traded before
    When I execute my first trade
    Then I should unlock:
      | Achievement  | Description           | Points | Badge |
      | First Trade  | Complete first trade  | 10     | 🎯    |
    And notification should appear
    And achievement should be permanent
    And points should be added to score

  Scenario: Streak Achievements
    Given I want to build winning streaks
    When I have consecutive profitable trades:
      | Streak | Achievement      | Points | Badge |
      | 3      | Hot Streak       | 20     | 🔥    |
      | 5      | On Fire          | 35     | 🔥🔥  |
      | 10     | Unstoppable      | 75     | 🔥🔥🔥|
    Then achievements should unlock progressively
    And each should stack
    And total points should accumulate

  Scenario Outline: Various Achievement Triggers
    Given I perform <action>
    When the system checks achievements
    Then I should unlock <achievement>
    And receive <points> points

    Examples:
      | action                    | achievement    | points |
      | First profitable trade    | First Profit   | 15     |
      | Hold through 100% gain    | Diamond Hands  | 100    |
      | Spot whale movement       | Whale Spotter  | 50     |
      | 1000% portfolio gain      | To The Moon    | 500    |
      | Complete all tutorials    | Scholar        | 25     |

  Scenario: Achievement Progress Tracking
    Given achievements have requirements
    When I check my progress:
      | Achievement    | Current | Required | Progress |
      | Trade Master   | 47      | 100      | 47%      |
      | Profit King    | $4,500  | $10,000  | 45%      |
      | Streak Legend  | 8       | 20       | 40%      |
    Then I should see progress bars
    And estimated completion time
    And next milestone rewards
```

## Feature: Weekly Competition

```gherkin
Feature: Weekly Competition
  As a competitive trader
  I want to participate in contests
  So that I can win prizes

  Scenario: Joining Competition
    Given a weekly competition is active
    When I opt-in to participate
    Then I should be registered
    And see competition details:
      | Detail           | Value                |
      | Start Time       | Monday 00:00 UTC     |
      | End Time         | Sunday 23:59 UTC     |
      | Participants     | 127                  |
      | Prize Pool       | $175                 |
      | Current Leader   | Alice (+22.3%)       |

  Scenario: Competition Rules
    Given I want to understand rules
    When I view competition info
    Then I should see:
      """
      Weekly Trading Competition Rules:

      1. Start with $10,000 virtual balance
      2. Highest ROI% wins
      3. Minimum 10 trades required
      4. All markets allowed
      5. Resets every Monday

      Prizes:
      🥇 1st Place: $50 credit
      🥈 2nd Place: $25 credit
      🥉 3rd Place: $10 credit
      """

  Scenario: Prize Distribution
    Given the week has ended
    And final rankings are:
      | Rank | User    | ROI    | Prize |
      | 1    | Alice   | +32.1% | $50   |
      | 2    | Bob     | +28.7% | $25   |
      | 3    | Charlie | +25.3% | $10   |
    When prizes are distributed
    Then winners should receive credits
    And announcement should be posted
    And badges should be awarded
    And next competition should start

  Scenario: Live Competition Updates
    Given I am participating
    When I check competition status
    Then I should see:
      | Metric              | Value        |
      | My Current Rank     | #7           |
      | ROI to Beat #3      | +3.2%        |
      | Time Remaining      | 2d 14h 23m   |
      | Trades Completed    | 18/10        |
      | Prize Position      | $0 (need #3) |
```

## Feature: Daily Challenges

```gherkin
Feature: Daily Challenges
  As an engaged user
  I want daily objectives
  So that I stay motivated

  Scenario: Receiving Daily Challenge
    Given a new day starts
    When I check my challenges
    Then I should see today's challenge:
      | Challenge           | Requirement      | Reward      |
      | Profit Master       | Make 3 profits   | 50 points   |
      | Volume Trader       | Trade $50K volume| 30 points   |
      | Prediction Pro      | 70% accuracy     | 100 points  |

  Scenario: Completing Challenge
    Given today's challenge is "Make 3 profitable trades"
    When I complete 3 profitable trades
    Then the challenge should be marked complete
    And I should receive 50 points
    And progress should update
    And next challenge should unlock

  Scenario: Challenge Streak Bonus
    Given I complete challenges daily
    When I maintain streak:
      | Days | Bonus Multiplier |
      | 3    | 1.5x            |
      | 7    | 2x              |
      | 30   | 3x              |
    Then rewards should be multiplied
    And streak counter should show
    And special badge should be earned
```

## Success Criteria

```gherkin
Feature: Phase 4 Success Criteria
  As a project manager
  I want to verify gamification works
  So that engagement increases

  Scenario: Simulator Functionality
    Given Phase 4 is complete
    When I test the simulator
    Then I should verify:
      | Feature               | Working | Tested |
      | Portfolio creation    | Yes     | ✓      |
      | Trade execution       | Yes     | ✓      |
      | P&L calculation       | Yes     | ✓      |
      | Position tracking     | Yes     | ✓      |
      | Balance updates       | Yes     | ✓      |

  Scenario: Engagement Metrics
    Given gamification is active
    When I measure engagement:
      | Metric                | Before | After  |
      | Daily active users    | 50     | 250    |
      | Avg session time      | 5 min  | 18 min |
      | Trades per user       | 2      | 12     |
      | Return rate           | 20%    | 65%    |
    Then engagement should increase 3-5x
    And retention should improve
    And community should be excited

  Scenario: Competition Success
    Given weekly competition launched
    When I check results:
      | Week | Participants | Engagement | Revenue |
      | 1    | 50          | High       | +20%    |
      | 2    | 125         | Very High  | +45%    |
      | 3    | 200         | Extreme    | +80%    |
    Then growth should be exponential
    And viral effect should occur
    And monetization should increase
```