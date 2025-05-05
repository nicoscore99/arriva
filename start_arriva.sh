#!/bin/bash

# Activate the virtual environment
source /home/pi/env_arriva/bin/activate

# Move to the script directory
cd /home/pi/arriva

# Wait for network
sleep 15

# Log start
echo "$(date) - Starting Arriva script" >> arriva.log

# Run Python script
/usr/bin/python3 arriva.py