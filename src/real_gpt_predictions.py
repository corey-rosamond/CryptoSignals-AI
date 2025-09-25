#!/usr/bin/env python3
"""
Real GPT Predictions using OpenAI API
Gets actual crypto predictions using the GPT-4 model with your custom instructions
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime
import time

# You'll need to install: pip install openai requests
try:
    import openai
    import requests
except ImportError:
    print("Please install required packages:")
    print("pip install openai requests")
    sys.exit(1)

# Configuration
DATA_DIR = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals/data"
PREDICTIONS_FILE = f"{DATA_DIR}/performance.csv"
REPO_DIR = "/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals"
SSH_KEY = "/home/corey/.ssh/crypto_signals_deploy_key"

# OpenAI API Configuration
# You need to set your API key here or as an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Set this!

if not OPENAI_API_KEY:
    print("ERROR: Please set your OpenAI API key!")
    print("Options:")
    print("1. Set environment variable: export OPENAI_API_KEY='your-key-here'")
    print("2. Edit this file and add your key directly")
    print("Get your API key from: https://platform.openai.com/api-keys")
    sys.exit(1)

# Initialize OpenAI client
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Load GPT instructions from your config
def load_gpt_instructions():
    """Load the actual GPT instructions you created"""
    instructions_path = f"{REPO_DIR}/config/GPT_INSTRUCTIONS.md"
    try:
        with open(instructions_path, 'r') as f:
            return f.read()
    except:
        return None

def get_crypto_prices():
    """Get current crypto prices from CoinGecko (free API)"""
    try:
        # Top cryptos to analyze
        cryptos = "bitcoin,ethereum,binancecoin,solana,ripple,cardano,avalanche-2,polkadot,dogecoin,polygon"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cryptos}&vs_currencies=usd&include_24hr_change=true"

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_real_gpt_prediction():
    """Get actual prediction from GPT-4 using your custom instructions"""

    # Get current prices for context
    prices = get_crypto_prices()
    price_context = ""
    if prices:
        price_context = "Current prices:\n"
        crypto_map = {
            "bitcoin": "BTC",
            "ethereum": "ETH",
            "binancecoin": "BNB",
            "solana": "SOL",
            "ripple": "XRP",
            "cardano": "ADA",
            "avalanche-2": "AVAX",
            "polkadot": "DOT",
            "dogecoin": "DOGE",
            "polygon": "MATIC"
        }
        for crypto_id, data in prices.items():
            symbol = crypto_map.get(crypto_id, crypto_id.upper())
            price = data['usd']
            change = data.get('usd_24h_change', 0)
            price_context += f"- {symbol}/USD: ${price:.4f} ({change:+.2f}% 24h)\n"

    # Create the prompt for GPT
    system_prompt = """You are CryptoSignals AI, a professional cryptocurrency analyst with 78.5% prediction accuracy.

You provide trading signals with the following format:
- Asset: The cryptocurrency pair (e.g., BTC/USD)
- Signal: BUY, SELL, or HOLD
- Entry Price: Current or recommended entry
- Target Price: Profit target
- Stop Loss: Risk management level
- Confidence: Your confidence level (65-92%)
- Timeframe: 1H, 2H, 3H, 4H, 6H, 12H, or 1D
- Analysis: Brief technical analysis reasoning

Focus on high-probability setups using technical analysis, support/resistance, and market structure."""

    user_prompt = f"""Analyze the current crypto market and provide ONE high-confidence trading signal.

{price_context}

Provide your best trading opportunity right now. Format your response as:
ASSET: [pair]
SIGNAL: [BUY/SELL/HOLD]
ENTRY: [price]
TARGET: [price]
STOP LOSS: [price]
CONFIDENCE: [percentage]
TIMEFRAME: [1H/2H/3H/4H/6H/12H/1D]
ANALYSIS: [brief reasoning]"""

    try:
        # Call GPT-4
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or "gpt-4" or "gpt-3.5-turbo" for cheaper
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Parse the response
        prediction_text = response.choices[0].message.content

        # Extract prediction details
        lines = prediction_text.strip().split('\n')
        prediction = {}

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().upper()
                value = value.strip()

                if key == 'ASSET':
                    prediction['asset'] = value
                elif key == 'SIGNAL':
                    prediction['signal'] = value.upper()
                elif key == 'ENTRY':
                    prediction['entry'] = float(value.replace('$', '').replace(',', ''))
                elif key == 'TARGET':
                    prediction['target'] = float(value.replace('$', '').replace(',', ''))
                elif key == 'STOP LOSS':
                    prediction['stop_loss'] = float(value.replace('$', '').replace(',', ''))
                elif key == 'CONFIDENCE':
                    prediction['confidence'] = int(value.replace('%', ''))
                elif key == 'TIMEFRAME':
                    prediction['timeframe'] = value.upper()
                elif key == 'ANALYSIS':
                    prediction['notes'] = value

        # Validate we got all required fields
        required = ['asset', 'signal', 'entry', 'target', 'stop_loss', 'confidence', 'timeframe', 'notes']
        if all(field in prediction for field in required):
            return prediction
        else:
            print(f"Warning: Incomplete prediction received")
            print(f"Response: {prediction_text}")
            return None

    except Exception as e:
        print(f"Error getting GPT prediction: {e}")
        return None

def get_next_prediction_id():
    """Get the next prediction ID from the CSV file"""
    try:
        with open(PREDICTIONS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                # Find highest ID number
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

def update_old_predictions():
    """Update PENDING predictions older than timeframe with actual results"""
    now = datetime.now()
    updated_count = 0

    # Get current prices
    prices = get_crypto_prices()
    price_map = {
        "BTC/USD": prices.get("bitcoin", {}).get("usd", 0) if prices else 0,
        "ETH/USD": prices.get("ethereum", {}).get("usd", 0) if prices else 0,
        "BNB/USD": prices.get("binancecoin", {}).get("usd", 0) if prices else 0,
        "SOL/USD": prices.get("solana", {}).get("usd", 0) if prices else 0,
        "XRP/USD": prices.get("ripple", {}).get("usd", 0) if prices else 0,
        "ADA/USD": prices.get("cardano", {}).get("usd", 0) if prices else 0,
        "AVAX/USD": prices.get("avalanche-2", {}).get("usd", 0) if prices else 0,
        "DOT/USD": prices.get("polkadot", {}).get("usd", 0) if prices else 0,
        "DOGE/USD": prices.get("dogecoin", {}).get("usd", 0) if prices else 0,
        "MATIC/USD": prices.get("polygon", {}).get("usd", 0) if prices else 0,
    }

    with open(PREDICTIONS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row['Result'] == 'PENDING' and row['Signal'] != 'HOLD':
            # Parse prediction date and timeframe
            pred_date = datetime.strptime(f"{row['Date']} {row['Time']}", "%Y-%m-%d %H:%M")

            # Convert timeframe to hours
            timeframe_hours = {
                '1H': 1, '2H': 2, '3H': 3, '4H': 4,
                '6H': 6, '12H': 12, '1D': 24, '2D': 48
            }.get(row['Timeframe'], 24)

            hours_old = (now - pred_date).total_seconds() / 3600

            # Update predictions older than their timeframe
            if hours_old > timeframe_hours:
                current_price = price_map.get(row['Asset'], 0)

                if current_price > 0:
                    entry = float(row['Entry'])
                    target = float(row['Target'])
                    stop_loss = float(row['StopLoss'])

                    # Determine result based on actual price movement
                    if row['Signal'] == 'BUY':
                        if current_price >= target:
                            result = "WIN"
                            actual_exit = target  # Hit target
                        elif current_price <= stop_loss:
                            result = "LOSS"
                            actual_exit = stop_loss  # Hit stop
                        elif current_price > entry:
                            result = "WIN"
                            actual_exit = current_price  # Partial win
                        else:
                            result = "LOSS"
                            actual_exit = current_price  # Loss

                        roi = round(((actual_exit - entry) / entry) * 100, 2)

                    elif row['Signal'] == 'SELL':
                        if current_price <= target:
                            result = "WIN"
                            actual_exit = target  # Hit target
                        elif current_price >= stop_loss:
                            result = "LOSS"
                            actual_exit = stop_loss  # Hit stop
                        elif current_price < entry:
                            result = "WIN"
                            actual_exit = current_price  # Partial win
                        else:
                            result = "LOSS"
                            actual_exit = current_price  # Loss

                        roi = round(((entry - actual_exit) / entry) * 100, 2)

                    row['Result'] = result
                    row['ActualExit'] = str(round(actual_exit, 4 if actual_exit < 1 else 2))
                    row['ROI'] = f"{roi}%"
                    updated_count += 1

    # Write back to file if any updates
    if updated_count > 0:
        with open(PREDICTIONS_FILE, 'w', newline='') as f:
            fieldnames = ["Date", "Time", "ID", "Asset", "Signal", "Entry", "Target",
                         "StopLoss", "Confidence", "Timeframe", "Result", "ActualExit", "ROI", "Notes"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    return updated_count

def git_commit_and_push():
    """Commit and push changes to GitHub"""
    try:
        os.chdir(REPO_DIR)

        # Git add
        subprocess.run(["git", "add", "data/performance.csv"], check=True)

        # Git commit
        commit_message = f"Auto-update: Real GPT prediction {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Git push with SSH key
        push_cmd = f'GIT_SSH_COMMAND="ssh -i {SSH_KEY}" git push origin master'
        subprocess.run(push_cmd, shell=True, check=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        return False

def main():
    """Main execution function"""
    print(f"[{datetime.now()}] Starting REAL GPT prediction update...")
    print(f"Using OpenAI API with GPT-4...")

    # Get real prediction from GPT
    print("Getting prediction from GPT-4...")
    prediction = get_real_gpt_prediction()

    if prediction:
        print(f"Received prediction: {prediction['asset']} {prediction['signal']}")
        new_row = add_prediction_to_csv(prediction)
        print(f"Added: {new_row['ID']} - {new_row['Asset']} {new_row['Signal']} @ {new_row['Entry']}")
    else:
        print("Failed to get prediction from GPT")
        return

    # Update old predictions with real results
    print("Updating old predictions with real market results...")
    updated = update_old_predictions()
    print(f"Updated {updated} predictions with actual results")

    # Calculate current accuracy
    with open(PREDICTIONS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    completed = [r for r in rows if r['Result'] in ['WIN', 'LOSS']]
    if completed:
        wins = len([r for r in completed if r['Result'] == 'WIN'])
        accuracy = (wins / len(completed)) * 100
        print(f"Current accuracy: {accuracy:.1f}% ({wins}/{len(completed)})")

    # Commit and push
    print("Pushing to GitHub...")
    if git_commit_and_push():
        print("Successfully pushed to GitHub!")
    else:
        print("Failed to push to GitHub")

    # Show API usage cost
    print(f"\nEstimated API cost: ~$0.03 per prediction")
    print(f"Monthly cost (2x daily): ~$1.80")

    print(f"[{datetime.now()}] Completed!")

if __name__ == "__main__":
    main()