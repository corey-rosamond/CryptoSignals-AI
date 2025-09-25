# 🧪 TEST THE AUTOMATION SYSTEM

## Step 1: Enable GitHub Actions

1. Go to: https://github.com/corey-rosamond/CryptoSignals-AI/settings/actions
2. Under "Actions permissions", select **"Allow all actions and reusable workflows"**
3. Click **Save**

## Step 2: Create a Test Prediction

1. Go to: https://github.com/corey-rosamond/CryptoSignals-AI/issues/new
2. Select **"📊 Track Prediction"** template
3. Fill in test data:
   - Asset: `BTC/USD`
   - Signal: `BUY`
   - Entry Price: `112000`
   - Target Price: `115000`
   - Stop Loss: `110000`
   - Confidence: `85`
   - Timeframe: `4H`
   - Notes: `Test prediction to verify automation`
4. Click **Submit new issue**

## Step 3: Watch the Magic Happen

1. Go to: https://github.com/corey-rosamond/CryptoSignals-AI/actions
2. You should see **"Track Prediction"** workflow running
3. Check the issue for an automatic comment confirming tracking
4. Check `data/performance.csv` for the new entry

## Step 4: Trigger Daily Stats Update

1. Go to: https://github.com/corey-rosamond/CryptoSignals-AI/actions/workflows/update_stats.yml
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Watch it calculate statistics and update README

## What Happens Automatically:

✅ **Every new prediction issue** → Added to CSV instantly
✅ **Every day at midnight** → Stats recalculated, README updated
✅ **Every Sunday** → Weekly performance report created
✅ **No manual work needed!**

## Verify It Worked:

Check these locations:
- `data/performance.csv` - Should have new PRED entry
- `data/statistics.json` - Should have updated stats
- `README.md` - Should show current accuracy %
- GitHub Actions tab - Should show successful runs

## Update Your GPT:

Add this to your GPT instructions:
```
After making predictions, track them automatically:
1. Navigate to: https://github.com/corey-rosamond/CryptoSignals-AI/issues/new
2. Select "Track Prediction" template
3. Fill in all prediction details
4. Submit the issue
```

---

**🎉 Congratulations! You now have a FULLY AUTOMATED performance tracking system at $0/month!**