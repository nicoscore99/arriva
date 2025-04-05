#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

# # Display resolution
# EPD_WIDTH       = 176
# EPD_HEIGHT      = 264

P1 = (74, 88)
P2 = (-132, 30)
P3 = (74, 30)
P4 = (132, 30)
P5 = (74, -28)
P6 = (132, -28)
P7 = (74, -88)

E1 = (-132, 88)
E2 = (132, 88)
E3 = (-132, -88)
E4 = (132, -88)

try:
    logging.info("epd2in7 Demo")   
    epd = epd2in7_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

    # Quick refresh
    logging.info("Display Connections Page")

    # White image
    Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)

    # Side bar
    draw.line(P1 + P7, fill = 0)
    draw.line(P2 + P4, fill = 0)
    draw.line(P5 + P6, fill = 0)

    # Rotate the image by 90 degrees clockwise and translate the origin to (-epd.width/2, epd.height/2)
    Limage = Limage.transform(Limage.size, Image.AFFINE, (0, 1, -epd.width/2, -1, 0, epd.height/2))

    epd.display_Fast(epd.getbuffer(Limage))
    time.sleep(2)

    logging.info("Clear...")
    epd.init()   
    epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    exit()