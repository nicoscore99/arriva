#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image,ImageDraw,ImageFont, ImageOps
from transformations import invert_colors, png_to_bmp, on_raspi


font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

class MainFrame:
    def __init__(self):
        PIL_WIDTH = 264
        PIL_HEIGHT = 176

        # Define points globally
        self.P1 = (132, 0)
        self.P2 = (0, 44)
        self.P3 = (132+44, 0)
        self.P4 = (132+44+44, 0)
        self.P5 = (132, 44)
        self.P6 = (132+44, 44)
        self.P7 = (132+44+44, 44)
        self.P8 = (264, 44)

        # Text placement
        self.T1 = (8, 12)
        self.C1 = (8, 54)
        self.C2 = (40, 54)
        self.C3 = (242, 54)

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

        # Generate the image
        self.Limage = Image.new('1', (PIL_WIDTH, PIL_HEIGHT), 255)
        self.draw = ImageDraw.Draw(self.Limage)

        # Mainframe0],
        self.Limage.paste(self.icon_train, (self.P1[0], self.P1[1]))
        self.Limage.paste(self.icon_signal, (self.P3[0], self.P3[1]))
        self.Limage.paste(self.icon_error, (self.P4[0], self.P4[1]))

        self.draw.line(self.P2+self.P8, fill=0, width=2)

    def get(self, arg1, *args):
        return self.Limage

class ConnectionsFrame(MainFrame):
    def __init__(self):
        super().__init__()

        # Dummy content
        connection1 = ('S1', 'Wil, SG', "5'")
        connection2 = ('S2', 'Wattwil, SG', "6'")
        connection3 = ('S3', 'Zürich, ZH', "7'")
        self.dummy_connections = [connection1, connection2, connection3]

        # Invert the image of train
        icon_train = invert_colors(self.icon_train)
        self.Limage.paste(icon_train, (self.P1[0], self.P1[1]))

        # Draw title
        self.draw.text(self.T1, 'Departure', font=font24, fill=0, anchor="lt")
    
    def get(self, arg1, *args):
        # Get the image from the parent class
        image = super().get(arg1, *args)

        raspi = on_raspi()

        # Set current location
        self.Limage.paste(self.icon_location, (self.C1[0], self.C1[1]))
        self.draw.text(self.C2, arg1, font=font18, fill=0, anchor="lt")

        if raspi:
            if len(args) > 4: 
                raise ValueError("Too many arguments provided.")
            if len(args) > 0:
                for connection in args:
                    if not isinstance(connection, tuple) or len(connection) != 3:
                        raise ValueError("Each connection must be a tuple of three elements.")
                    
                for i, connection in enumerate(args):

                    # Move the coordinates down for the next connection
                    self.C1 = (self.C1[0], self.C1[1] + 24)
                    self.C2 = (self.C2[0], self.C2[1] + 24)
                    self.C3 = (self.C3[0], self.C3[1] + 24)

                    # Draw the connection text
                    self.draw.text(self.C1, connection[0], font=font18, fill=0, anchor="lt")
                    self.draw.text(self.C2, connection[1], font=font18, fill=0, anchor="lt")
                    self.draw.text(self.C3, connection[2], font=font18, fill=0, anchor="mt")

        else:
            # Draw the connections
            for i, connection in enumerate(self.dummy_connections):

                # Move the coordinates down for the next connection
                self.C1 = (self.C1[0], self.C1[1] + 24)
                self.C2 = (self.C2[0], self.C2[1] + 24)
                self.C3 = (self.C3[0], self.C3[1] + 24)

                # Draw the connection text
                self.draw.text(self.C1, connection[0], font=font18, fill=0, anchor="lt")
                self.draw.text(self.C2, connection[1], font=font18, fill=0, anchor="lt")
                self.draw.text(self.C3, connection[2], font=font18, fill=0, anchor="mt")

        return image
    
class SignalFrame(MainFrame):
    def __init__(self):
        super().__init__()

        # Invert the image of the signal
        icon_signal = invert_colors(self.icon_signal)
        self.Limage.paste(icon_signal, (self.P3[0], self.P3[1]))

        # Draw title
        self.draw.text(self.T1, 'Signal', font=font24, fill=0, anchor="lt")

    def get(self, arg1, *args):
        # Get the image from the parent class
        image = super().get(arg1, *args)

        return image
    
class ErrorFrame(MainFrame):
    def __init__(self):
        super().__init__()

        # Invert the image of the error
        icon_error = invert_colors(self.icon_error)
        self.Limage.paste(icon_error, (self.P4[0], self.P4[1]))

        # Draw title
        self.draw.text(self.T1, 'Error', font=font24, fill=0, anchor="lt")

    def get(self, arg1, *args):
        # Get the image from the parent class
        image = super().get(arg1, *args)

        return image