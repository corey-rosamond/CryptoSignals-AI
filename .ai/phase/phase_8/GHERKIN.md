# 🥒 PHASE 8: VIRAL GROWTH CAMPAIGN - GHERKIN SCENARIOS

## Feature: Referral System

```gherkin
Feature: User Referral Program
  As a user
  I want to refer friends
  So that we both get rewards

  Background:
    Given referral system is active
    And rewards are configured
    And tracking is enabled

  Scenario: Generating Referral Code
    Given I am an active user
    When I say "Get my referral code"
    Then GPT should respond:
      """
      🎁 Your Referral Code: CRYPTO-ABC123

      Share this link:
      https://chatgpt.com/g/cryptosignals?ref=ABC123

      Rewards:
      • You get: 1 month premium per 3 referrals
      • Friend gets: 7-day premium trial
      • Both get: Exclusive badge

      Current referrals: 0/3
      """
    And code should be unique
    And trackable

  Scenario: Successful Referral
    Given friend clicks my referral link
    When they sign up and use GPT
    Then system should:
      | Action                    | Status |
      | Track referral source     | ✓      |
      | Credit me with referral   | ✓      |
      | Grant friend bonus        | ✓      |
      | Update my progress        | ✓      |
      | Send me notification      | ✓      |
    And I see: "🎉 1/3 referrals complete!"

  Scenario: Referral Reward Tiers
    Given different reward levels exist
    When I reach referral milestones:
      | Referrals | Reward                    |
      | 1         | Bronze badge              |
      | 3         | 1 month premium           |
      | 5         | Custom alerts feature     |
      | 10        | 3 months premium          |
      | 25        | Lifetime premium          |
      | 50        | Become affiliate (paid)   |
    Then rewards unlock progressively
    And motivation stays high

  Scenario Outline: Referral Tracking
    Given I shared my code via <channel>
    When <friends> people sign up
    Then I should have <total> referrals
    And earn <reward>

    Examples:
      | channel  | friends | total | reward           |
      | Twitter  | 2       | 2     | Progress: 2/3    |
      | Discord  | 1       | 3     | 1 month premium  |
      | Email    | 2       | 5     | Custom alerts    |
      | LinkedIn | 5       | 10    | 3 months premium |
```

## Feature: Social Proof Generation

```gherkin
Feature: Automatic Social Proof
  As a successful trader
  I want to share my wins
  So that others see the value

  Scenario: Win Detection and Sharing
    Given I made a profitable trade
    When GPT detects:
      | Metric        | Value   |
      | Profit        | +$500   |
      | ROI           | +12.5%  |
      | Timeframe     | 2 days  |
    Then prompt for sharing:
      """
      🎊 Congratulations on your $500 profit!

      Share your success? (Helps others discover crypto trading)

      [Share on Twitter] [Share on Discord] [Skip]
      """
    And if shared, generate graphic
    And include referral link

  Scenario: Wall of Fame
    Given leaderboard exists
    When viewing top traders:
      | Rank | User    | ROI     | Streak | Badge    |
      | 1    | Alice   | +145%   | 12     | 🏆 Legend |
      | 2    | Bob     | +98%    | 8      | 🥇 Master |
      | 3    | Carol   | +67%    | 5      | 🥈 Expert |
    Then display prominently
    And update hourly
    And allow claiming spot
    And shareable badges

  Scenario: Success Story Collection
    Given user has great results
    When prompted for testimonial:
      """
      You've grown your portfolio 200%! 🚀

      Would you share your story to inspire others?
      We'll feature you on our Wall of Fame!

      [Share Story] [Maybe Later]
      """
    Then collect story
    And format professionally
    And request permission to use
    And credit user

  Scenario: Automated Screenshot Generation
    Given user achieves milestone
    When generating shareable:
      | Element          | Content              |
      | Header           | "CryptoSignals AI"   |
      | Achievement      | "100% ROI Achieved!" |
      | User             | "@username"          |
      | Stats            | Trades, Win Rate     |
      | Call to Action   | "Join me: [link]"    |
      | Branding         | Logo, colors         |
    Then create attractive image
    And optimize for platform
    And include watermark
```

## Feature: Influencer Partnership

```gherkin
Feature: Influencer Collaboration
  As a growth manager
  I want influencer partnerships
  So that we reach new audiences

  Scenario: Influencer Identification
    Given searching for crypto influencers
    When filtering by criteria:
      | Criteria         | Requirement        |
      | Followers        | 10k - 100k         |
      | Engagement       | >3%                |
      | Niche           | Crypto/Trading     |
      | Location        | English-speaking   |
      | Content Quality | High               |
    Then create outreach list:
      | Name         | Platform | Followers | Engagement |
      | CryptoSarah  | Twitter  | 45k      | 4.2%       |
      | TradingMike  | YouTube  | 67k      | 5.1%       |
      | DeFiDave     | TikTok   | 23k      | 7.8%       |

  Scenario: Outreach Campaign
    Given influencer list ready
    When sending personalized outreach:
      """
      Hi [Name],

      Love your content on [specific post]!

      We built CryptoSignals AI and think your audience would benefit.

      Offering:
      • Exclusive "Pro" features for you
      • 50% commission on referrals
      • Custom promo code for followers
      • Co-marketing opportunities

      Interested in a quick demo?
      """
    Then track:
      | Metric          | Target |
      | Response Rate   | >20%   |
      | Demo Scheduled  | >10%   |
      | Partnerships    | >5     |

  Scenario: Partnership Performance
    Given influencer promotes GPT
    When tracking performance:
      | Influencer   | Clicks | Signups | Revenue | ROI   |
      | CryptoSarah  | 1,234  | 123     | $567    | 245%  |
      | TradingMike  | 2,345  | 234     | $1,234  | 567%  |
      | DeFiDave     | 567    | 45      | $234    | 123%  |
    Then optimize based on results
    And scale successful partnerships
    And pause underperforming
```

## Feature: Viral Mechanics

```gherkin
Feature: Built-in Virality
  As a product designer
  I want viral loops
  So that growth is organic

  Scenario: FOMO Creation
    Given limited-time offer active
    When user visits:
      """
      ⏰ FLASH COMPETITION - 24 HOURS LEFT!

      Prize Pool: $500
      Participants: 127/150 (23 spots left!)
      Current Leader: +45% ROI

      Join now before it's full!
      """
    Then create urgency
    And show countdown timer
    And update spots in real-time
    And trigger action

  Scenario: Scarcity Implementation
    Given premium features exist
    When showing limitations:
      | Feature           | Free Users        | Message           |
      | Whale Alerts      | 3 per day        | "2 alerts left today" |
      | Analysis Depth    | Basic            | "Unlock Pro analysis" |
      | Trading Slots     | 5 positions      | "4/5 slots used"      |
      | Competition Entry | Not eligible     | "Premium only"        |
    Then motivate upgrades
    And show what they're missing

  Scenario: Share Triggers
    Given user has positive experience
    When optimal moment occurs:
      | Trigger             | Prompt                      |
      | First profit        | "Share your first win!"     |
      | Streak of 3         | "On fire! Tell friends"     |
      | Beat market         | "You beat BTC! Share?"      |
      | Unlock achievement  | "New badge! Show it off"    |
    Then prompt sharing
    But don't be annoying
    And reward sharing

  Scenario: Competition Virality
    Given weekly competition running
    When creating buzz:
      | Mechanic              | Implementation           |
      | Public leaderboard    | Visible to all          |
      | Live updates          | Real-time positions     |
      | Trash talking         | Friendly banter allowed |
      | Team competitions     | Form trading squads     |
      | Spectator mode        | Watch top traders       |
    Then increase engagement
    And encourage invites
    And create community
```

## Feature: Content Marketing

```gherkin
Feature: Content-Driven Growth
  As a content marketer
  I want valuable content
  So that we attract users organically

  Scenario: Case Study Creation
    Given successful user story
    When creating case study:
      """
      Title: How Sarah Turned $1,000 into $5,000 in 30 Days

      1. Background: Complete beginner
      2. Strategy: Used CryptoSignals AI daily
      3. Results: 400% ROI in one month
      4. Key Insights: [specific tactics]
      5. Screenshots: [proof of results]
      6. Call to Action: Try it yourself
      """
    Then publish on blog
    And optimize for SEO
    And share on social
    And track traffic

  Scenario: Weekly Market Reports
    Given market data available
    When generating report:
      | Section           | Content                |
      | Market Overview   | Total cap, dominance   |
      | Top Performers    | Biggest gainers        |
      | Whale Activity    | Major movements        |
      | AI Predictions    | Next week outlook      |
      | User Wins         | Community highlights   |
    Then email to subscribers
    And post on blog
    And share snippets on social
    And include CTAs

  Scenario: Viral Content Creation
    Given trending topic exists
    When creating meme/content:
      | Type          | Example                        |
      | Meme          | "When your AI calls the top"   |
      | Thread        | "10 whale moves this week"     |
      | Infographic   | "Crypto market in numbers"     |
      | Video         | "Live trading session"         |
    Then optimize for platform
    And include branding subtly
    And encourage sharing
```

## Feature: Growth Tracking

```gherkin
Feature: Viral Growth Metrics
  As a growth team
  I want to track viral metrics
  So that we optimize growth

  Scenario: Viral Coefficient Calculation
    Given tracking user behavior
    When calculating K-factor:
      | Metric                    | Value |
      | Users                     | 1000  |
      | Invites sent              | 2500  |
      | Invites per user          | 2.5   |
      | Conversion rate           | 20%   |
      | New users from invites    | 500   |
      | K-factor                  | 0.5   |
    Then if K > 1, viral growth
    And optimize for higher K

  Scenario: Channel Attribution
    Given multiple growth channels
    When tracking source:
      | Channel      | Users | CAC    | LTV    | ROI   |
      | Referrals    | 234   | $0.50  | $47    | 9400% |
      | Influencers  | 156   | $5.00  | $52    | 1040% |
      | Organic      | 89    | $0.00  | $38    | ∞     |
      | Content      | 67    | $2.00  | $41    | 2050% |
    Then focus on best channels
    And scale what works

  Scenario: Engagement Loop Metrics
    Given viral loops active
    When measuring effectiveness:
      | Loop              | Trigger Rate | Share Rate | New Users |
      | Win sharing       | 67%         | 34%        | 123       |
      | Achievement share | 89%         | 45%        | 234       |
      | Referral program  | 45%         | 23%        | 156       |
      | Competition       | 78%         | 56%        | 345       |
    Then optimize best loops
    And improve weak ones
```

## Success Criteria

```gherkin
Feature: Phase 8 Success Validation
  As a CEO
  I want viral growth working
  So that we scale rapidly

  Scenario: Growth Metrics Achievement
    Given phase 8 complete
    When measuring growth:
      | Metric              | Target  | Actual  | Status |
      | Weekly growth       | 50%     | 67%     | ✅     |
      | Viral coefficient   | 1.2     | 1.4     | ✅     |
      | Referral rate       | 15%     | 23%     | ✅     |
      | Social shares/day   | 100     | 234     | ✅     |
      | Influencer partners | 5       | 8       | ✅     |
    Then viral growth confirmed

  Scenario: Sustainability Check
    Given rapid growth achieved
    When evaluating sustainability:
      | Factor              | Status    | Risk Level |
      | Server capacity     | Adequate  | Low        |
      | Support scaling     | Prepared  | Medium     |
      | Quality maintained  | Yes       | Low        |
      | Community health    | Strong    | Low        |
      | Revenue scaling     | Linear+   | Low        |
    Then growth is sustainable
    And ready for phase 9

  Scenario: Community Sentiment
    Given viral campaign active
    When checking sentiment:
      | Channel    | Sentiment | Engagement |
      | Twitter    | Positive  | High       |
      | Discord    | Excited   | Very High  |
      | Reddit     | Curious   | Growing    |
      | Telegram   | Bullish   | Active     |
    Then community is healthy
    And growth is organic
    And word-of-mouth strong
```