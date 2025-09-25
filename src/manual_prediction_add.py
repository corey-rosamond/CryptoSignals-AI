#!/usr/bin/env python3
"""
Manual Prediction Entry Tool
Allows you to manually add predictions from ChatGPT to the tracking CSV
"""

import csv
import os
import subprocess
from datetime import datetime

# Configuration
DATA_DIR = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals/data"
PREDICTIONS_FILE = f"{DATA_DIR}/performance.csv"
REPO_DIR = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals"
SSH_KEY = "/home/corey/.ssh/crypto_signals_deploy_key"

def get_next_prediction_id():
    """Get the next prediction ID from the CSV file"""
    try:
        with open(PREDICTIONS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                max_id = 0
                for row in rows:
                    try:
                        id_num = int(row['ID'].replace('PRED', ''))
                        max_id = max(max_id, id_num)
                    except:
                        pass
                return f"PRED{max_id + 1}"
    except:
        pass
    return "PRED600"

def get_user_input():
    """Interactively get prediction details from user"""
    print("\n" + "="*50)
    print("CRYPTOSIGNALS AI - MANUAL PREDICTION ENTRY")
    print("="*50)
    print("\nEnter the prediction details from ChatGPT:\n")

    # Asset
    print("Common assets: BTC/USD, ETH/USD, SOL/USD, BNB/USD, XRP/USD")
    asset = input("Asset (e.g., BTC/USD): ").strip().upper()
    if not asset:
        asset = "BTC/USD"

    # Signal
    signal = ""
    while signal not in ['BUY', 'SELL', 'HOLD']:
        signal = input("Signal (BUY/SELL/HOLD): ").strip().upper()

    # Prices
    try:
        entry = float(input("Entry price: $").strip())
        target = float(input("Target price: $").strip())
        stop_loss = float(input("Stop loss price: $").strip())
    except:
        print("Invalid price entered. Using defaults.")
        entry = 45000 if 'BTC' in asset else 2800 if 'ETH' in asset else 100
        target = entry * 1.05 if signal == 'BUY' else entry * 0.95
        stop_loss = entry * 0.97 if signal == 'BUY' else entry * 1.03

    # Confidence
    try:
        confidence = int(input("Confidence % (65-92): ").strip())
        confidence = max(65, min(92, confidence))
    except:
        confidence = 78

    # Timeframe
    print("Timeframes: 1H, 2H, 3H, 4H, 6H, 12H, 1D")
    timeframe = input("Timeframe (default 4H): ").strip().upper()
    if timeframe not in ['1H', '2H', '3H', '4H', '6H', '12H', '1D']:
        timeframe = '4H'

    # Analysis notes
    notes = input("Analysis/Notes (optional): ").strip()
    if not notes:
        if signal == 'BUY':
            notes = "Bullish setup identified"
        elif signal == 'SELL':
            notes = "Bearish pattern forming"
        else:
            notes = "Consolidation phase"

    return {
        "asset": asset,
        "signal": signal,
        "entry": entry,
        "target": target,
        "stop_loss": stop_loss,
        "confidence": confidence,
        "timeframe": timeframe,
        "notes": notes
    }

def add_prediction_to_csv(prediction):
    """Add a new prediction to the CSV file"""
    now = datetime.now()

    new_row = {
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M"),
        "ID": get_next_prediction_id(),
        "Asset": prediction["asset"],
        "Signal": prediction["signal"],
        "Entry": prediction["entry"],
        "Target": prediction["target"],
        "StopLoss": prediction["stop_loss"],
        "Confidence": f"{prediction['confidence']}%",
        "Timeframe": prediction["timeframe"],
        "Result": "PENDING",
        "ActualExit": "",
        "ROI": "",
        "Notes": prediction["notes"]
    }

    # Read existing data
    with open(PREDICTIONS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Add new prediction
    rows.append(new_row)

    # Write back to file
    with open(PREDICTIONS_FILE, 'w', newline='') as f:
        fieldnames = ["Date", "Time", "ID", "Asset", "Signal", "Entry", "Target",
                     "StopLoss", "Confidence", "Timeframe", "Result", "ActualExit", "ROI", "Notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return new_row

def git_commit_and_push(prediction_id, asset, signal):
    """Commit and push changes to GitHub"""
    try:
        os.chdir(REPO_DIR)

        # Git add
        subprocess.run(["git", "add", "data/performance.csv"], check=True,
                      capture_output=True, text=True)

        # Git commit
        commit_message = f"Manual prediction: {prediction_id} - {asset} {signal}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True,
                      capture_output=True, text=True)

        # Git push with SSH key
        push_cmd = f'GIT_SSH_COMMAND="ssh -i {SSH_KEY}" git push origin master'
        result = subprocess.run(push_cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return True
        else:
            print(f"Push error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        return False

def main():
    """Main execution function"""
    print("\n🤖 CryptoSignals AI - Manual Prediction Entry Tool")
    print("This tool helps you add predictions from ChatGPT to GitHub\n")

    # Check if user wants to continue
    print("Steps:")
    print("1. Open ChatGPT and get a prediction")
    print("2. Enter the details here")
    print("3. Auto-commit to GitHub")

    confirm = input("\nReady to add a prediction? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    # Get prediction details
    prediction = get_user_input()

    # Show summary
    print("\n" + "="*50)
    print("PREDICTION SUMMARY")
    print("="*50)
    print(f"Asset: {prediction['asset']}")
    print(f"Signal: {prediction['signal']}")
    print(f"Entry: ${prediction['entry']}")
    print(f"Target: ${prediction['target']}")
    print(f"Stop Loss: ${prediction['stop_loss']}")
    print(f"Confidence: {prediction['confidence']}%")
    print(f"Timeframe: {prediction['timeframe']}")
    print(f"Notes: {prediction['notes']}")
    print("="*50)

    confirm = input("\nAdd this prediction? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    # Add to CSV
    new_row = add_prediction_to_csv(prediction)
    print(f"\n✅ Added: {new_row['ID']} - {new_row['Asset']} {new_row['Signal']}")

    # Push to GitHub
    print("\n📤 Pushing to GitHub...")
    if git_commit_and_push(new_row['ID'], new_row['Asset'], new_row['Signal']):
        print("✅ Successfully pushed to GitHub!")
        print(f"\n🎉 Prediction {new_row['ID']} has been added and published!")
    else:
        print("⚠️ Failed to push to GitHub (but prediction was saved locally)")

    # Show current stats
    with open(PREDICTIONS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total = len(rows)
    completed = [r for r in rows if r['Result'] in ['WIN', 'LOSS']]
    if completed:
        wins = len([r for r in completed if r['Result'] == 'WIN'])
        accuracy = (wins / len(completed)) * 100
        print(f"\n📊 Current Stats:")
        print(f"Total Predictions: {total}")
        print(f"Accuracy: {accuracy:.1f}% ({wins}/{len(completed)})")

if __name__ == "__main__":
    main()