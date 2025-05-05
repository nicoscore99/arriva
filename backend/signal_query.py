import pywifi
import subprocess
import re



class SignalQueryEngine:
    """
    Class to query WiFi information.
    """
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]  # Assume first interface

    def get_current_ssid(self):
        """
        Get the current SSID of the connected WiFi network.

        Returns:
            str: The SSID of the connected network or an error message.
        """
        try:
            # Execute the command to get the SSID (-r returns only the SSID)
            ssid = subprocess.check_output("iwgetid -r", shell=True, text=True).strip()
            return ssid if ssid else "SSID not found."
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e}"
        
    def get_signal_strength(self):
        """
        Get the signal strength of the connected WiFi network.

        Returns:
            int: The signal strength in dBm or an error message.
        """
        result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, text=True)
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'Signal level' in line:
                    # Extract the signal level using regex
                    wifi_details = re.search(r'Signal level=(-?\d+)', line).group(1)

                    return int(wifi_details)
                
        return None
                
    def signal_strength_discretization(self, signal_strength):
        """
        Discretize the signal strength into categories.

        Args:
            signal_strength (int): The signal strength in dBm.

        Returns:
            int: The level of signal strength (0-5).
        """
        if signal_strength is None:
            return None  # Handle case where signal strength is not available

        if signal_strength >= -50:
            return 5
        elif signal_strength >= -60:
            return 4
        elif signal_strength >= -70:
            return 3
        elif signal_strength >= -80:
            return 2
        else:
            return 1
        
    def get_wifi_strength(self):
        """
        Get the current SSID and signal strength.

        Returns:
            tuple: A tuple containing the SSID and signal strength level (0-5).
        """
        ssid = self.get_current_ssid()
        signal_strength = self.get_signal_strength()
        signal_strength_level = self.signal_strength_discretization(signal_strength)
        
        return ssid, signal_strength_level
    
if __name__ == "__main__":

    wifi_query = SignalQueryEngine()
    ssid, signal_strength_level = wifi_query.get_wifi_strength()
    print(f"SSID: {ssid}, Signal Strength Level: {signal_strength_level}")