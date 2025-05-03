#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from datetime import datetime
from dateutil import parser
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
transformdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'display')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image, ImageDraw, ImageFont, ImageOps
from transformations import invert_colors, png_to_bmp, on_raspi, draw_multiline_text

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

class MainFrame:
    def __init__(self):
        PIL_WIDTH = 264
        PIL_HEIGHT = 176

        self.GRAY1  = 0xff #white
        self.GRAY2  = 0xC0
        self.GRAY3  = 0x80 #gray
        self.GRAY4  = 0x00 #Blackest

        # Define points globally
        self.P1 = (88, 0)
        self.P2 = (0, 44)
        self.P3 = (88+44, 0)
        self.P4 = (88+44+44, 0)
        self.P5 = (88, 44)
        self.P6 = (88+44, 44)
        self.P7 = (88+44+44, 44)
        self.P8 = (264, 44)
        self.P9 = (88+44+44+44, 0)

        # Text placement
        self.T1 = (8, 12)
        self.C1 = (8, 54)
        self.C2 = (50, 54)
        self.C3 = (242, 54)
        self.C4 = (80, 54)

        # Define edges
        self.E1 = (0, 0)
        self.E2 = (PIL_WIDTH, 0)
        self.E3 = (0, PIL_HEIGHT)
        self.E4 = (PIL_WIDTH, PIL_HEIGHT)

        # Load images as a binary image
        self.icon_error = png_to_bmp(picdir, 'error.png').resize((40, 40))
        self.icon_error = ImageOps.expand(self.icon_error, border=2, fill=255)  # Add a white border
        self.icon_signal = png_to_bmp(picdir, 'signal.png').resize((44, 44))
        self.icon_train = png_to_bmp(picdir, 'train.png').resize((40, 40))
        self.icon_train = ImageOps.expand(self.icon_train, border=2, fill=255)  # Add a white border
        self.icon_location = png_to_bmp(picdir, 'location.png').resize((20, 20))
        # self.icon_location = ImageOps.expand(self.icon_location, border=2, fill=255)
        self.icon_weather = png_to_bmp(picdir, 'weather.png').resize((40, 40))
        self.icon_weather = ImageOps.expand(self.icon_weather, border=2, fill=255)

        # Generate the image
        self.Limage = Image.new('L', (PIL_WIDTH, PIL_HEIGHT), 255)
        self.draw = ImageDraw.Draw(self.Limage)

        # Mainframe0],
        self.Limage.paste(self.icon_train, (self.P1[0], self.P1[1]))
        self.Limage.paste(self.icon_signal, (self.P3[0], self.P3[1]))
        self.Limage.paste(self.icon_weather, (self.P4[0], self.P4[1]))
        self.Limage.paste(self.icon_error, (self.P9[0], self.P9[1]))

        self.draw.line(self.P2+self.P8, fill=0, width=2)

    def reset(self):
        # Reset the image to white
        self.Limage = Image.new('L', (264, 176), 255)
        self.draw = ImageDraw.Draw(self.Limage)

        # Re-draw the main frame elements
        self.Limage.paste(self.icon_train, (self.P1[0], self.P1[1]))
        self.Limage.paste(self.icon_signal, (self.P3[0], self.P3[1]))
        self.Limage.paste(self.icon_weather, (self.P4[0], self.P4[1]))
        self.Limage.paste(self.icon_error, (self.P9[0], self.P9[1]))
        self.draw.line(self.P2+self.P8, fill=0, width=2)

    def get(self, *args):
        return self.Limage

class ConnectionsFrame(MainFrame):
    def __init__(self):
        super().__init__()

    def get(self, *args):
        # Get the image from the parent class
        image = super().get(*args)

        # Image reset
        self.reset()

        # Invert the image of train
        icon_train = invert_colors(self.icon_train)
        self.Limage.paste(icon_train, (self.P1[0], self.P1[1]))

        # Draw title
        self.draw.text(self.T1, 'Arrival', font=font24, fill=0, anchor="lt")

        # Set current location
        self.Limage.paste(self.icon_location, (self.C1[0], self.C1[1]))
        self.draw.text(self.C2, args[0], font=font18, fill=0, anchor="lt")
        
        C1_curr = self.C1
        C2_curr = self.C2
        C3_curr = self.C3

        if len(args) > 0:

            for connection in args[1]:
                if not isinstance(connection, tuple) or len(connection) != 3:
                    raise ValueError("Each connection must be a tuple of three elements.")
                
            for i, connection in enumerate(args[1]):

                # Move the coordinates down for the next connection
                C1_curr = (C1_curr[0], C1_curr[1] + 24)
                C2_curr = (C2_curr[0], C2_curr[1] + 24)
                C3_curr = (C3_curr[0], C3_curr[1] + 24)

                # Draw the connection text
                self.draw.text(C1_curr, connection[0], font=font18, fill=0, anchor="lt")
                self.draw.text(C2_curr, connection[1], font=font18, fill=0, anchor="lt")
                self.draw.text(C3_curr, connection[2], font=font18, fill=0, anchor="mt")

        return self.Limage
    
class SignalFrame(MainFrame):
    def __init__(self):
        super().__init__()

    def get(self, *args):
        # Get the image from the parent class
        image = super().get(*args)

        # Reset the image
        self.reset()

        # Invert the image of the signal
        icon_signal = invert_colors(self.icon_signal)
        self.Limage.paste(icon_signal, (self.P3[0], self.P3[1]))

        # Draw title
        self.draw.text(self.T1, 'Signal', font=font24, fill=0, anchor="lt")

        # First args is SSID, second args is signal strength
        if len(args) > 2: 
            raise ValueError("Too many arguments provided.")
        
        if len(args) > 0:
            if not isinstance(args[0], str):
                raise ValueError("SSID must be a string.")
            if not isinstance(args[1], int):
                raise ValueError("Signal strength must be an integer.")
            
            self.draw.text(self.C1, "SSID: ", font=font18, fill=0, anchor="lt")
            self.draw.text(self.C4, args[0], font=font18, fill=0, anchor="lt")

            C1_curr = (self.C1[0], self.C1[1] + 24)
            C4_curr = (self.C4[0], self.C4[1] + 24)

            self.draw.text(C1_curr, "Signal: ", font=font18, fill=0, anchor="lt")

            # Display the signal strength with square icons, always 5 squares, signal strength equals number of dark filles squares, the rest are grey
            for i in range(5):
                if i < args[1]:
                    self.draw.rectangle([(C4_curr[0], C4_curr[1]), (C4_curr[0] + 20, C4_curr[1] + 20)], fill=0)
                else:
                    self.draw.rectangle([(C4_curr[0], C4_curr[1]), (C4_curr[0] + 20, C4_curr[1] + 20)], fill=self.GRAY3)
                C4_curr = (C4_curr[0] + 24, C4_curr[1])

        return self.Limage
    
class WeatherFrame(MainFrame):
    def __init__(self):
        super().__init__()
        
        self.weather_positions =  [(39, 110), (101, 110), (163, 110), (225, 110)]

    def get(self, *args):
        # Directly pass the forcast array here

        # Get the image from the parent class
        image = super().get(*args)

        # Reset the image
        self.reset()

        # Invert the image of the weather
        icon_weather = invert_colors(self.icon_weather)
        self.Limage.paste(icon_weather, (self.P4[0], self.P4[1]))

        # Draw title
        self.draw.text(self.T1, 'Weather', font=font24, fill=0, anchor="lt")

        # Take the first 6 elements only
        forecasts = args[0][:4]

        for i, forecast in enumerate(forecasts):
            if not isinstance(forecast, dict):
                raise ValueError("Each forecast must be a dictionary.")

            # Get the image
            image_name = str(forecast['SYMBOL_CODE'])+'.png'
            icon_weather = png_to_bmp(picdir, image_name).resize((60, 60))
            icon_weather = ImageOps.expand(icon_weather, border=2, fill=255)

            self.Limage.paste(icon_weather, (self.weather_positions[i][0]-30, self.weather_positions[i][1]-30))

            # Get the weekday name 
            weekday = parser.parse(forecast['local_date_time']).strftime('%A')[0:3]
            self.draw.text((self.weather_positions[i][0], self.weather_positions[i][1]-25-15), weekday, font=font18, fill=0, anchor="mm")

            # Get the temperature
            temperature = (forecast['TX_C'] + forecast['TN_C']) / 2
            temperature = round(temperature, 1)
            temperature = str(temperature).replace('.', ',')

            self.draw.text((self.weather_positions[i][0], self.weather_positions[i][1]+25+25), temperature + '°', font=font18, fill=0, anchor="mm")      

        return self.Limage  
    
class ErrorFrame(MainFrame):
    def __init__(self):       
        super().__init__()

    def get(self, *args):
        # Get the image from the parent class
        image = super().get(*args)

        # Invert the image of the error
        icon_error = invert_colors(self.icon_error)
        self.Limage.paste(icon_error, (self.P9[0], self.P9[1]))

        # Draw title
        self.draw.text(self.T1, 'Error', font=font24, fill=0, anchor="lt")

        error_text = args[0]

        y_padding = 8
        x_padding = 8

        height = self.E3[1] - self.P2[1] - y_padding * 2
        width = self.E2[0] - self.P2[0] - x_padding * 2
       
        # Draw the error text
        error_image = draw_multiline_text(width, height, font18, error_text)

        # Paste the error image onto the main image
        self.Limage.paste(error_image, (self.P2[0] + x_padding, self.P2[1] + y_padding))

        return image