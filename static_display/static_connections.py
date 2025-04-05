#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image,ImageDraw,ImageFont
from transformations import invert_colors, png_to_bmp


font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

class StaticImage:
    def __init__(self):
        PIL_WIDTH = 264
        PIL_HEIGHT = 176

        # Define points
        P1 = (PIL_WIDTH-58, 0)
        P2 = (0, 58)
        P3 = (PIL_WIDTH-58, 58)
        P4 = (PIL_WIDTH, 58)
        P5 = (PIL_WIDTH-58, 2*58)
        P6 = (PIL_WIDTH, 2*58)
        P7 = (PIL_WIDTH-58, PIL_HEIGHT)

        # Define edges
        E1 = (0, 0)
        E2 = (PIL_WIDTH, 0)
        E3 = (0, PIL_HEIGHT)
        E4 = (PIL_WIDTH, PIL_HEIGHT)

        # Title placement
        T1 = (58, 17)

        EPD_WIDTH = 176
        EPD_HEIGHT = 264

        # Load images as a binary image
        # Convert images to 1-bit black and white (1) mode
        icon_error = Image.open(os.path.join(picdir, 'error.bmp')).resize((58, 58))
        icon_signal = Image.open(os.path.join(picdir, 'signal.bmp')).resize((58, 58))
        # icon_location = Image.open(os.path.join(picdir, 'location.bmp')).resize((58, 58))
        icon_train = Image.open(os.path.join(picdir, 'train.bmp')).resize((58, 58))

        icon_location = png_to_bmp(picdir, 'location_check.png').resize((58, 58))

        self.Limage = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)

        # Draw the image
        self.draw = ImageDraw.Draw(self.Limage)

        # Invert the image of train
        icon_train = icon_train.convert('1')
        icon_train = icon_train.point(lambda x: 255-x)
        icon_train = icon_train.convert('1')

        self.Limage.paste(icon_location, (E1[0], E1[1]))
        self.Limage.paste(icon_train, (P1[0], P1[1]))
        self.Limage.paste(icon_signal, (P3[0], P3[1]))
        self.Limage.paste(icon_error, (P5[0], P5[1]))

        self.draw.line(P1 + P7, fill=0)
        self.draw.line(P2 + P4, fill=0)
        self.draw.line(P5 + P6, fill=0)

        # Title
        self.draw.text(T1, 'Connections', font=font24, ll=0)
        

    def get(self):
        return self.Limage