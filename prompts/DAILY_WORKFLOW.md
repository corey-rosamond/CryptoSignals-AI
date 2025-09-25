# 📅 Daily Prediction Workflow

## Morning Routine (9 AM)

### Step 1: Get Prediction from GPT
1. Open your CryptoSignals AI GPT
2. Copy the prompt from `GPT_PREDICTION_REQUEST.md`
3. Paste it to your GPT
4. Copy the 8-line response

### Step 2: Process with Claude
1. Open Claude
2. Copy the prompt from `CLAUDE_PROCESS_PROMPT.md`
3. Replace `[PASTE THE 8 LINES FROM GPT HERE]` with the GPT output
4. Send to Claude
5. Claude will automatically add it to GitHub

### Step 3: Verify
Check your GitHub repository to confirm the new prediction was added

---

## Evening Routine (9 PM)
Repeat the same 3 steps

---

## Quick Copy Guide

### For GPT (Step 1):
```
Analyze the current crypto market and give me ONE high-confidence trading prediction. Format it EXACTLY like this:

Asset: [COIN/USD]
Signal: [BUY/SELL/HOLD]
Entry: [price number only]
Target: [price number only]
StopLoss: [price number only]
Confidence: [number only, no %]
Timeframe: [1H/2H/3H/4H/6H/12H/1D]
Notes: [one line analysis]
```

### For Claude (Step 2):
```
Add this GPT prediction to GitHub:

[PASTE GPT OUTPUT HERE]

Repository: /mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals
CSV file: data/performance.csv
SSH key: /home/corey/.ssh/crypto_signals_deploy_key

Please:
1. Add it to the CSV with the next ID number
2. Use current date/time
3. Commit with message: "GPT Prediction: [ID] - [Asset] [Signal] @ [Price] ([Confidence]% confidence)"
4. Push to GitHub
5. Confirm it was added successfully
```

---

## Tips:
- Keep these prompts bookmarked
- Takes less than 2 minutes per prediction
- Claude will handle all the Git operations
- Predictions auto-update with results after their timeframe expires