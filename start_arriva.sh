#!/bin/bash
set -e  # Exit on error
set -x  # Print commands as they execute

# Activate the virtual environment
source /home/pi/env_arriva/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Move to the script directory
cd /home/pi/arriva || { echo "Failed to change directory"; exit 1; }

# Wait for network
sleep 15

# Log start
echo "$(date) - Starting Arriva script" >> arriva.log

# Run Python script
/home/pi/env_arriva/bin/python arriva.py