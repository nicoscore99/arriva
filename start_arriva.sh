#!/bin/bash

# Move to the script directory
cd "$(dirname "$0")"

# Wait for network
sleep 15

# Log start
echo "$(date) - Starting arriva.py" >> startup.log

# Run Python script
/usr/bin/python3 arriva.py >> arriva.log 2>&1