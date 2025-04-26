from datetime import datetime, timedelta
import time
import os
import threading
import yaml
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'display')))

from display.displays import ConnectionsFrame, SignalFrame, ErrorFrame
from backend.connections_query import ConnectionsQueryEngine
from backend.signal_query import SignalQueryEngine
from gpiozero import Button, LED
from waveshare_epd import epd2in7_V2

# Define the GPIO pins for the buttons
BUTTON_PINS = {
    'button1': 5,
    'button2': 6,
    'button3': 13,
    'button4': 19
}

class Arriva:
    def __init__(self, config_path='config/arriva_config.yaml'):
        """
        Initialize the Arriva class with the given configuration file path.
        """

        # EPD display initialization
        self.epd = epd2in7_V2.EPD()
        self.epd.init()
        self.epd.Clear()

        # Load the configuration file
        self.config_path = config_path
        self.load_config()

        # Initialize the buttons and their callbacks
        self.status = 1  # Default status
        self.button1 = Button(BUTTON_PINS['button1'])
        self.button2 = Button(BUTTON_PINS['button2'])
        self.button3 = Button(BUTTON_PINS['button3'])
        self.button4 = Button(BUTTON_PINS['button4'])

        self.button1.when_pressed = self.button1_callback
        self.button2.when_pressed = self.button2_callback
        self.button3.when_pressed = self.button3_callback
        self.button4.when_pressed = self.button4_callback

        self.connections_query = ConnectionsQueryEngine()
        self.connections_frame = ConnectionsFrame()
        self.signal_query = SignalQueryEngine()
        self.signal_frame = SignalFrame()
        # self.error_query = ErrorQuery()
        self.error_frame = ErrorFrame()

        # First screen update
        self.update_screen()

    def load_config(self):
        """
        Load the configuration from the YAML file.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def update_screen(self):
        """
        Evaluate the frame logic based on the current status.
        """
        try:
            if self.status == 1:
                self.connections_frame_logic()
            elif self.status == 2:
                self.signal_frame_logic()
            elif self.status == 3:
                self.error_frame_logic()
        except Exception as e:
            self.error_frame_logic(e)

    def run(self):
        """
        Run the main loop to check the status and update the display accordingly.
        """
        # Main loop to check the status and update the display accordingly
        while True:
            # Check the status and display the corresponding frame
            self.update_screen()             
            
            # Wait 1 minute before checking again
            time.sleep(60)

    def connections_formatting(self, connections):
        conn_formatted = []
        for conn in connections:
        
            # Handle cases where fractional seconds are missing
            departure_time = conn['DepartureTime']
            if '.' not in departure_time:
                departure_time = departure_time.replace('Z', '.000000Z')
            
            # Calculate the time difference in minutes
            time_diff = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.utcnow()
            # Convert to minutes
            time_diff_minutes = int(time_diff.total_seconds() / 60)
            # Format the connection element
            conn_element = (conn['ServiceName'], conn['Destination'], str(time_diff_minutes))
            conn_formatted.append(conn_element)

        return conn_formatted
    
    def connections_frame_logic(self):
        """
        Logic to handle connections frame.
        """
        
        # get_connections(self, stop_point_ref, departure_time, number_of_results=4):

        stop_point_ref = self.config['Haltestelle_Didok']
        current_location = self.config['Haltestelle']
        departure_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        connections = self.connections_query.get_connections(stop_point_ref, departure_time)
        connections_formatted = self.connections_formatting(connections)
        image = self.connections_frame.get(current_location, connections_formatted)

        self.epd.display(self.epd.getbuffer(image))

    def signal_frame_logic(self):
        """
        Logic to handle signal frame.
        """
        
        # get_wifi_strength(self):
        ssid, signal_strength_level = self.signal_query.get_wifi_strength()
        image = self.signal_frame.get(ssid, signal_strength_level)

        self.epd.display(self.epd.getbuffer(image))

    def error_frame_logic(self, error=None):
        """
        Logic to handle error frame.
        """
        
        # get_error(self):
        if error:
            error_message = str(error)
        else:
            error_message = "Everything is fine!"

        image = self.error_frame.get(error_message)

        self.epd.display(self.epd.getbuffer(image))

    def button1_callback(self):
        """
        Callback function for button 1 press.
        """
        self.status = 1
        self.update_screen()
        print("Button 1 pressed")

    def button2_callback(self):
        """
        Callback function for button 2 press.
        """
        self.status = 2
        self.update_screen()
        print("Button 2 pressed")

    def button3_callback(self):
        """
        Callback function for button 3 press.
        """
        self.status = 3
        self.update_screen()
        print("Button 3 pressed")

    def button4_callback(self):
        """
        Callback function for button 4 press. This is the update button. It does not update the status, but calls the display logic again.
        """

        self.update_screen()
        print("Button 4 pressed")

if __name__ == '__main__':
    
    arriva = Arriva()
    
    threading.Thread(target=arriva.run).start()
