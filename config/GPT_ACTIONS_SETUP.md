# 🔌 GPT Actions Setup Guide - Enable Real-Time Data

## 📋 Quick Setup Steps

### Step 1: Open Your GPT Configuration
1. Go to https://chatgpt.com/gpts/editor
2. Select your "CryptoSignals AI" GPT
3. Click "Configure" tab

### Step 2: Add Actions
1. Scroll down to "Actions" section
2. Click "Create new action"
3. Click "Import from URL" OR paste the schema below

### Step 3: Configure the Action

#### Option A: Direct CoinGecko Integration (FREE - Recommended)
1. Copy the entire contents of `openapi_schema.json`
2. Paste into the Schema field
3. No authentication needed for CoinGecko free tier
4. Test with "Test" button

#### Option B: Use Our Proxy Server (Better Rate Limits)
If you want to avoid rate limits, use our proxy:
- Server URL: `https://crypto-gpt-proxy.vercel.app` (you'd need to deploy this)
- Includes caching and combines multiple APIs

### Step 4: Update Privacy Policy (Required)
Add to your GPT's description:
```
This GPT fetches real-time cryptocurrency data from CoinGecko API. No personal data is collected or stored.
```

### Step 5: Test the Actions
Click "Test" next to each action:
1. `getCurrentPrices` - Test with "bitcoin,ethereum"
2. `getMarketData` - Test with default parameters
3. `getGlobalData` - No parameters needed
4. `getTrendingCoins` - No parameters needed

---

## 🚀 How to Use in Your GPT

### Update Your GPT Instructions
Add these instructions to handle real-time data:

```markdown
## Real-Time Data Protocol

When users ask for current prices or market data:
1. Use the getCurrentPrices action for specific coins
2. Use getMarketData for top 20 coins
3. Use getGlobalData for market overview
4. Always mention data is real-time from CoinGecko

Example queries to handle:
- "What's the current price of Bitcoin?" → Use getCurrentPrices with ids=bitcoin
- "Show me top 10 cryptocurrencies" → Use getMarketData with per_page=10
- "What's the total market cap?" → Use getGlobalData
- "What coins are trending?" → Use getTrendingCoins

Format responses with:
- Exact prices with 2-4 decimal places
- Percentage changes with + or - signs
- Market cap in billions/trillions
- Last updated timestamp
```

---

## 📊 Available Actions & Examples

### 1. getCurrentPrices
**Purpose:** Get real-time prices for specific cryptocurrencies

**Example Request:**
```json
{
  "ids": "bitcoin,ethereum,solana",
  "vs_currencies": "usd",
  "include_24hr_change": true
}
```

**Example Response:**
```json
{
  "bitcoin": {
    "usd": 45234.67,
    "usd_24h_change": 2.34
  },
  "ethereum": {
    "usd": 2567.89,
    "usd_24h_change": -1.23
  }
}
```

### 2. getMarketData
**Purpose:** Get detailed data for top cryptocurrencies

**Parameters:**
- `vs_currency`: "usd" (default)
- `per_page`: 1-250 (default 20)
- `order`: "market_cap_desc" (default)

### 3. getGlobalData
**Purpose:** Get total market cap, dominance, etc.

**No parameters needed**

Returns:
- Total market cap
- BTC/ETH dominance
- Number of active cryptocurrencies
- 24h market change

### 4. getTrendingCoins
**Purpose:** Get currently trending coins

**No parameters needed**

---

## ⚠️ Important Notes

### Rate Limits
- CoinGecko Free: 10-50 calls/minute
- Each GPT conversation typically uses 2-5 calls
- Cache responses in conversation for efficiency

### Best Practices
1. **Batch requests** - Get multiple coins in one call
2. **Cache in context** - Reuse data within same conversation
3. **Graceful failures** - Have fallback responses if API fails
4. **Update timestamps** - Always show when data was fetched

### Common Issues & Solutions

**Issue:** "Rate limit exceeded"
**Solution:** Use fewer API calls, implement 5-minute caching in responses

**Issue:** "Action failed"
**Solution:** Check if CoinGecko is down at status.coingecko.com

**Issue:** "Coin not found"
**Solution:** Use correct coin IDs (bitcoin not BTC, ethereum not ETH)

---

## 🔄 Alternative: Deploy Your Own Proxy

If you need better rate limits or want to hide API keys, deploy a simple proxy:

### Vercel Deployment (Free)
1. Create `api/crypto.js`:
```javascript
export default async function handler(req, res) {
  const { endpoint, ...params } = req.query;

  // Add caching headers
  res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate');

  // Fetch from CoinGecko
  const response = await fetch(
    `https://api.coingecko.com/api/v3/${endpoint}?${new URLSearchParams(params)}`
  );

  const data = await response.json();
  res.status(200).json(data);
}
```

2. Deploy to Vercel (free tier)
3. Update OpenAPI schema with your Vercel URL
4. Benefit: Built-in caching, no rate limits for your GPT

---

## ✅ Testing Checklist

- [ ] Actions imported successfully
- [ ] Test button works for each action
- [ ] GPT can fetch Bitcoin price
- [ ] GPT can get top 20 coins
- [ ] GPT can get market cap data
- [ ] Responses include real-time timestamps
- [ ] Error handling works gracefully

---

## 📝 Final GPT Instruction Update

Replace the "REAL-TIME DATA CAPABILITIES" section in your GPT instructions with:

```markdown
## 📡 REAL-TIME DATA CAPABILITIES (Via Actions)
**Live Market Data - Actually Real-Time:**
- Current prices updated on every request
- Data sourced from CoinGecko API
- No caching - fresh data every time
- Covers 10,000+ cryptocurrencies

**Available Data Points:**
- Real-time price in USD
- 24h change percentage
- Market capitalization
- Trading volume
- Trending coins
- Global market metrics

**How to Request Data:**
Just ask naturally:
- "Current Bitcoin price"
- "Top 10 cryptocurrencies"
- "Market cap and dominance"
- "Trending coins today"
```

---

## 🎉 Success!

Once configured, your GPT will have TRUE real-time data access. No more simulations or fake data - actual live cryptocurrency prices on demand!

**Next Steps:**
1. Test thoroughly with various queries
2. Update marketing to highlight "Real-Time Data"
3. Remove all references to "simulated" data
4. Monitor API usage to stay within free tier