# 📊 PHASE 5: REAL-TIME DATA INTEGRATION - UML DIAGRAMS

## Data Integration Architecture

```mermaid
classDiagram
    class DataAggregator {
        -List~DataProvider~ providers
        -CacheManager cache
        -ErrorHandler errorHandler
        -UpdateScheduler scheduler
        +fetchPrice(symbol)
        +fetchMarketData()
        +getWhaleAlerts()
        +scheduleUpdates()
    }

    class DataProvider {
        <<interface>>
        +getName()
        +fetchPrice(symbol)
        +fetchVolume(symbol)
        +fetchMarketCap()
        +isAvailable()
    }

    class CoinGeckoAPI {
        -String apiKey
        -RateLimit rateLimit
        -Integer priority
        +fetchPrice(symbol)
        +fetchVolume(symbol)
        +fetchMarketCap()
        +getHistoricalData()
    }

    class CoinMarketCapAPI {
        -String apiKey
        -RateLimit rateLimit
        -Integer priority
        +fetchPrice(symbol)
        +fetchVolume(symbol)
        +fetchMarketCap()
        +getGlobalMetrics()
    }

    class WhaleAlertAPI {
        -String apiKey
        -WebSocket connection
        +subscribeToAlerts()
        +getRecentTransactions()
        +analyzeFlow()
    }

    class CacheManager {
        -Map~String_CachedData~ cache
        -Integer ttl
        +get(key)
        +set(key, value, ttl)
        +invalidate(key)
        +isValid(key)
    }

    class MarketMetrics {
        -Decimal totalMarketCap
        -Decimal volume24h
        -Decimal btcDominance
        -Integer fearGreedIndex
        -Map~String_Decimal~ prices
        +update()
        +getTrend()
    }

    DataAggregator --> DataProvider
    DataProvider <|-- CoinGeckoAPI
    DataProvider <|-- CoinMarketCapAPI
    DataAggregator --> WhaleAlertAPI
    DataAggregator --> CacheManager
    DataAggregator --> MarketMetrics
```

## Real-Time Update Flow

```mermaid
sequenceDiagram
    participant Scheduler
    participant Aggregator
    participant Cache
    participant Primary[CoinGecko]
    participant Backup[CoinMarketCap]
    participant WhaleAlert
    participant GPT

    Scheduler->>Aggregator: Trigger Update (5 min)

    Aggregator->>Cache: Check Cache
    Cache-->>Aggregator: Expired/Miss

    Aggregator->>Primary: Fetch Prices
    Primary-->>Aggregator: Price Data

    alt Primary Fails
        Aggregator->>Backup: Fetch Prices
        Backup-->>Aggregator: Price Data
    end

    Aggregator->>WhaleAlert: Check Alerts
    WhaleAlert-->>Aggregator: Large Transactions

    Aggregator->>Cache: Store Data (5 min TTL)
    Cache-->>Aggregator: Cached

    Aggregator->>GPT: Update Market Data
    GPT-->>GPT: Process & Store
```

## Whale Alert System

```mermaid
graph TB
    subgraph "Whale Detection"
        Monitor[Transaction Monitor]
        Filter[Size Filter >$1M]
        Analyze[Flow Analysis]
    end

    subgraph "Alert Processing"
        Context[Add Context]
        Impact[Assess Impact]
        Format[Format Alert]
    end

    subgraph "Notification"
        Store[Store Alert]
        Notify[Notify Users]
        Display[Display in GPT]
    end

    Monitor --> Filter
    Filter --> Analyze
    Analyze --> Context
    Context --> Impact
    Impact --> Format
    Format --> Store
    Store --> Notify
    Notify --> Display
```

## Cache Strategy

```mermaid
flowchart TD
    Request([Data Request]) --> CheckCache{In Cache?}

    CheckCache -->|Yes| ValidCheck{Still Valid?}
    CheckCache -->|No| FetchData[Fetch from API]

    ValidCheck -->|Yes| ReturnCached[Return Cached Data]
    ValidCheck -->|No| InvalidateCache[Invalidate Entry]

    InvalidateCache --> FetchData

    FetchData --> RateCheck{Rate Limit OK?}

    RateCheck -->|Yes| CallAPI[Call API]
    RateCheck -->|No| UseBackup{Backup Available?}

    UseBackup -->|Yes| CallBackupAPI[Call Backup API]
    UseBackup -->|No| ReturnStale[Return Stale Data + Warning]

    CallAPI --> UpdateCache[Update Cache]
    CallBackupAPI --> UpdateCache

    UpdateCache --> SetTTL[Set TTL 5 min]
    SetTTL --> ReturnFresh[Return Fresh Data]
```

## Market Metrics Dashboard

```mermaid
graph LR
    subgraph "Global Metrics"
        MCap[Market Cap: $2.1T]
        Vol[24h Volume: $89B]
        BTC[BTC Dom: 52.3%]
        ETH[ETH Dom: 16.8%]
    end

    subgraph "Sentiment Indicators"
        FG[Fear/Greed: 68]
        Trend[Trend: Bullish]
        Mom[Momentum: Strong]
    end

    subgraph "Top Movers"
        Gain[Top Gainer: SOL +12%]
        Loss[Top Loser: ADA -8%]
        Volume[Most Volume: BTC]
    end

    subgraph "Whale Activity"
        Large[Large Txs: 47]
        Inflow[Exchange In: $234M]
        Outflow[Exchange Out: $189M]
        Net[Net Flow: -$45M]
    end

    MCap --> Display[GPT Response]
    Vol --> Display
    BTC --> Display
    ETH --> Display
    FG --> Display
    Trend --> Display
    Mom --> Display
    Gain --> Display
    Loss --> Display
    Volume --> Display
    Large --> Display
    Inflow --> Display
    Outflow --> Display
    Net --> Display
```

## API Failover Strategy

```mermaid
stateDiagram-v2
    [*] --> Primary: Start

    Primary --> CheckPrimary: Health Check
    CheckPrimary --> PrimaryOK: Available
    CheckPrimary --> PrimaryFail: Unavailable

    PrimaryOK --> FetchFromPrimary: Use CoinGecko
    PrimaryFail --> Secondary: Failover

    Secondary --> CheckSecondary: Health Check
    CheckSecondary --> SecondaryOK: Available
    CheckSecondary --> SecondaryFail: Unavailable

    SecondaryOK --> FetchFromSecondary: Use CoinMarketCap
    SecondaryFail --> Tertiary: Failover

    Tertiary --> CheckCache: Check Cache
    CheckCache --> CacheValid: Has Recent Data
    CheckCache --> CacheStale: Only Old Data

    CacheValid --> UseCached: Return Cached
    CacheStale --> ReturnWithWarning: Return + Warning

    FetchFromPrimary --> UpdateCache: Success
    FetchFromSecondary --> UpdateCache: Success
    UpdateCache --> [*]: Complete

    UseCached --> [*]: Complete
    ReturnWithWarning --> [*]: Complete
```