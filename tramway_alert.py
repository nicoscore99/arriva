# Import libraries
import re
import subprocess
import yaml
import socket
import requests
import epd2in7
import xml.etree.ElementTree as ET

from datetime import datetime
from signal import pause
from time import sleep
from PIL import Image, ImageDraw, ImageFont
# from gpiozero import Button, LED

class networkHandler:
    def __init__(self):
        pass

    def check_network_status(self):
        try:
            # Check if the device is connected to the internet
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False
        
    def check_wifi_details(self):
        # Get the SSID of the connected network
        try:
            ssid = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
            signal_strength = subprocess.check_output(['iwgetid', '-s']).decode('utf-8').strip()
            return ssid, signal_strength
        except subprocess.CalledProcessError:
            return None, None

    def __del__(self):
        pass


class scheduleHandler:
    def __init__(self):
        # global variables
        self.api_url = 'https://api.opentransportdata.swiss/trias2020'
        self.api_key = 'eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImIwODQ1ZGI2MTdjMDRmNzhhMDAwMWMwZjMwOTllYTZhIiwiaCI6Im11cm11cjEyOCJ9'

        # Define the namespaces used in the XML document
        self.namespaces = {
            'trias': 'http://www.vdv.de/trias',
            'siri': 'http://www.siri.org.uk/siri'
        }

    def decode_schedule(self, xml_data):

        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Initialize lists to hold the times
        service_arrival_times = []
        service_departure_times = []

        # Iterate through the document and extract all ServiceArrival and ServiceDeparture times
        for service_arrival in root.findall('.//trias:ServiceArrival/trias:TimetabledTime', self.namespaces):
            service_arrival_times.append(service_arrival.text)

        for service_departure in root.findall('.//trias:ServiceDeparture/trias:TimetabledTime', self.namespaces):
            service_departure_times.append(service_departure.text)

        return service_arrival_times, service_departure_times

    def query_schedule(self, origin_id, destination_id, dep_arr_time):
        # Your XML data
        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
        <Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <ServiceRequest>
                <siri:RequestTimestamp>{datetime.now().isoformat()}</siri:RequestTimestamp>
                 <siri:RequestorRef>API-Explorer</siri:RequestorRef>
                <RequestPayload>
                    <StopEventRequest>
                        <Location>
                            <LocationRef>
                                <StopPointRef>{origin_id}</StopPointRef>
                            </LocationRef>
                            <DepArrTime>{dep_arr_time}</DepArrTime>
                        </Location>
                        <Params>
                            <NumberOfResults>1</NumberOfResults>
                            <StopEventType>departure</StopEventType>
                            <IncludePreviousCalls>true</IncludePreviousCalls>
                            <IncludeOnwardCalls>true</IncludeOnwardCalls>
                            <IncludeRealtimeData>true</IncludeRealtimeData>
                        </Params>
                    </StopEventRequest>
                </RequestPayload>
            </ServiceRequest>
        </Trias>'''

        # Additional headers with the Authorization header
        headers = {
            'Content-Type': 'application/xml',  # This header is important for telling the server the type of the content
            'Authorization': f'Bearer {self.api_key}'  # API key for authorization
        }

        # Sending the request
        response = requests.post(self.api_url, data=xml_data, headers=headers)

        # Checking the response
        if response.status_code != 200:
            print("Error:", response.status_code)
            return None
        else:
            print("Successful response")

            # TODO: There might be an issue here since the response is not saved to a file
            return self.decode_schedule(response)

    def __del__(self):
        pass

class displayHandler:
    def __init__(self):
        self.epd = epd2in7.EPD()
        self.epd.init()
        print("Clear...")

        self.HBlackImage = Image.new('1', (self.epd.height, self.epd.width), 255)
        self.draw = ImageDraw.Draw(self.HBlackImage)
        self.font = ImageFont.truetype('arial.ttf', 24)
        self.font = ImageFont.truetype('arial.ttf', 18)  # Create our font, passing in the font file and font size
        self.fontsmall = ImageFont.truetype('arial.ttf', 12)  # Create our font, passing in the font file and font size
        self.fontsupersmall = ImageFont.truetype('arial.ttf', 8)  # Create our font, passing in the font file and font size

    def display_text(self, text):
        self.draw.rectangle((0, 0, self.epd.height, self.epd.width), fill = 255)
        self.draw.text((10, 10), text, font = self.font, fill = 0)
        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def side_bar(self):
        # This is the left section of the screen with key descriptions
        self.draw.line((34, 0, 34, 180), fill=0)  # Draw Vertical Key lines
        self.draw.line((35, 0, 35, 180), fill=0)  # Draw Vertical Key lines (make thicker)
        self.draw.text((2, 2), f"""Network \nInfo """, font=self.fontsupersmall, fill=0)  # Key1 Text
        self.draw.rectangle((0, 0, 34, 44), outline=0)  # Boxes around the key1 description
        self.draw.text((2, 52), f"""Network \nStats """, font=self.fontsupersmall, fill=0)  # Key2 Text
        self.draw.rectangle((0, 44, 34, 88), outline=0)  # Boxes around the key2 description
        self.draw.text((2, 102), f"""CPU \nInfo """, font=self.fontsupersmall, fill=0)  # Key3 Text
        self.draw.rectangle((0, 88, 34, 132), outline=0)  # Boxes around the key3 description
        self.draw.text((2, 152), f"""System \nTools """, font=self.fontsupersmall, fill=0)  # Key4 Text
        self.draw.rectangle((0, 132, 34, 176), outline=0)  # Boxes around the key4 description

    def headline(self):
        self.draw.line((34, 22, 264, 22), fill=0)  # Draw top line
        self.draw.line((34, 23, 264, 23), fill=0)  # Draw top line (make thicker)

    def footnote(self):
        # This is the bottom section of the screen with the date and time
        now = datetime.now()  # Gets the date and time now
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")  # Defines the layout of the datetime string
        self.draw.line((34, 158, 264, 158), fill=0)  # Draw bottom line
        self.draw.line((34, 159, 264, 159), fill=0)  # Draw bottom line (make thicker)
        self.draw.text((40, 160), f"Last Updated: {dt_string}     ", font=self.fontsmall, fill=0)  # Date Time String at bottom

    def set_title(self, title):
        self.draw.text((40, 2), title, font=self.font, fill=0)

    def set_text(self, text):
        self.draw.text((40, 24), text, font=self.font, fill=0)

    def display_welcome(self):
        pass

    def display_connection(self, connection, arrival_time, departure_time):
        self.side_bar()
        self.headline()
        self.footnote()
        
        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def display_connection_not_found(self, connection):
        self.side_bar()
        self.headline()
        self.footnote()

        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def display_network_status(self, network_status, ssid, signal_strength):
        self.side_bar()
        self.headline()
        self.footnote()

        title = "NETWORK STATUS"
        self.set_title(title)
   
        text = f"Network found\nSSID: {ssid}\nSignal strength: {signal_strength}"
        self.set_text(text)

        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def display_network_status_not_found(self):
        self.side_bar()
        self.headline()
        self.footnote()

        title = "NETWORK STATUS"
        self.set_title(title)

        text = "No network found"
        self.set_text(text)
        

        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def unexpected_error(self):
        self.side_bar()
        self.headline()
        self.footnote()

        title = "ERROR"
        self.set_title(title)

        text = "An unexpected error occurred"
        self.set_text(text)

        self.epd.display(self.epd.getbuffer(self.HBlackImage))

    def clear_display(self):
        self.epd.init()
        self.epd.Clear()

    def __del__(self):
        self.epd.sleep()
        del self.epd

class buttonHandler:
    def __init__(self, dispH, queryH, netwH, cfg):

        self.displayHandle = dispH
        self.queryHandle = queryH
        self.networkHandle = netwH
        self.config = cfg

        self.key1 = Button(5)
        self.key2 = Button(6)
        self.key3 = Button(13)
        self.key4 = Button(19)

        self.key1.when_pressed = self.key1_handler
        self.key2.when_pressed = self.key2_handler
        self.key3.when_pressed = self.key3_handler
        self.key4.when_pressed = self.key4_handler

        self.display_state = 1 # Default is key1   

    def key1_handler(self):

        self.display_state = 1

        print("Key 1 pressed: First connection")

        origin_id = self.config['connection1']['origin']
        destination_id = self.config['connection1']['destination']
        dep_arr_time = datetime.now().isoformat()

        arrival_times, departure_times = self.queryHandle.query_schedule(origin_id, destination_id, dep_arr_time)

        if arrival_times is not None and departure_times is not None:
            self.displayHandle.display_connection('connection1', arrival_times, departure_times)
        else:
            self.displayHandle.display_connection_not_found('connection1')

    def key2_handler(self):

        self.display_state = 2

        print("Key 2 pressed: Second connection")

        origin_id = self.config['connection2']['origin']
        destination_id = self.config['connection2']['destination']
        dep_arr_time = datetime.now().isoformat()

        arrival_times, departure_times = self.queryHandle.query_schedule(origin_id, destination_id, dep_arr_time)

        if arrival_times is not None and departure_times is not None:
            self.displayHandle.display_connection('connection2', arrival_times, departure_times)
        else:
            self.displayHandle.display_connection_not_found('connection2')
    
    def key3_handler(self):

        self.display_state = 3

        print("Key 3 pressed: Third connection")

        origin_id = self.config['connection3']['origin']
        destination_id = self.config['connection3']['destination']
        dep_arr_time = datetime.now().isoformat()

        arrival_times, departure_times = self.queryHandle.query_schedule(origin_id, destination_id, dep_arr_time)

        if arrival_times is not None and departure_times is not None:
            self.displayHandle.display_connection('connection3', arrival_times, departure_times)
        else:
            self.displayHandle.display_connection_not_found('connection3')

    def key4_handler(self):

        self.display_state = 4

        print("Key 4 pressed: Network status")

        network_status = self.networkHandle.check_network_status()
        ssid, signal_strength = self.networkHandle.check_wifi_details()

        self.displayHandle.display_network_status(network_status, ssid, signal_strength)

    def __del__(self):
        pass


class tramway_alert:
    def __init__(self):
        
        # Read configuration file (.yaml)
        with open('config.yaml', 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        
        # Initialize display
        self.displayHandle = displayHandler()

        # Initialize schedule handler
        self.scheduleHandle = scheduleHandler()

        # Initialize network handler
        self.networkHandle = networkHandler()

        # Initialize button handler
        self.buttonHandle = buttonHandler(self.displayHandle, self.scheduleHandle, self.networkHandle, self.config)
        
    def switch_case(self, display_state):
        switcher = {
            1: self.buttonHandle.key1_handler,
            2: self.buttonHandle.key2_handler,
            3: self.buttonHandle.key3_handler,
            4: self.buttonHandle.key4_handler
        }
        return switcher.get(display_state, self.displayHandle.unexpected_error)

    def main(self):

        # Upon startup, display welcome message for 5 seconds
        self.displayHandle.display_welcome()
        sleep(5)

        # Main loop
        while True:

            self.switch_case(self.buttonHandle.display_state)()

            # Do every 30 seconds
            sleep(self.config['update_interval'])

        # Clear the display
        self.displayHandle.clear_display()

if __name__ == "__main__":
    tramway_alert = tramway_alert()
    tramway_alert.main()
    pause()