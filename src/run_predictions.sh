#!/bin/bash

# Automated Prediction Runner for CryptoSignals AI
# Runs every 12 hours via cron

# Set up environment
export PATH="/usr/local/bin:/usr/bin:/bin"
SCRIPT_DIR="/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals/src"
LOG_DIR="/mnt/c/Users/rosam/Documents/Passive Income/GPT Tools/GPTs/01_Crypto_Signals/logs"
LOG_FILE="$LOG_DIR/predictions_$(date +%Y%m%d).log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log start time
echo "========================================" >> "$LOG_FILE"
echo "Starting prediction update: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run Python script
cd "$SCRIPT_DIR"
/usr/bin/python3 auto_predictions.py >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    echo "Prediction update completed successfully: $(date)" >> "$LOG_FILE"
else
    echo "ERROR: Prediction update failed: $(date)" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# Keep only last 30 days of logs
find "$LOG_DIR" -name "predictions_*.log" -mtime +30 -delete

exit 0