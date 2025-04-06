import pywifi
from pywifi import const
import time
import subprocess
import re

def get_current_wifi_strength():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assume first interface
    iface.scan()  # Start scanning
    time.sleep(2)  # Wait for scan results
    results = iface.scan_results()
    for network in results:
        # Here you can access network.signal for signal strength
        print(f"SSID: {network.ssid}, Signal: {network.signal}")

def get_current_ssid_linux():
    try:
        # Execute the command to get the SSID (-r returns only the SSID)
        ssid = subprocess.check_output("iwgetid -r", shell=True, text=True).strip()
        return ssid if ssid else "SSID not found."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    get_current_wifi_strength()
    print(get_current_ssid_linux())