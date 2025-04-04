import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7b_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

# def display_static_image(epd):
#     ### Display static image
#     logging.info("Displaying static image...")

#     epd.init_Fast()
#     Himage = Image.open(os.path.join(picdir, '2in7.bmp'))
#     epd.display_Fast(epd.getbuffer(Himage))
#     time.sleep(2)


try:
    logging.info("Initializing e-Paper display...")

    epd = epd2in7b_V2.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)

    logging.info("Drawing on display...")
    logging.info("Quick refresh demo")
    Himage = Image.open(os.path.join(picdir, '2in7.bmp'))
    epd.display_Fast(epd.getbuffer(Himage))
    time.sleep(2)
    
    logging.info("Finished displaying static image.")
    logging.info("Going to sleep...")
    epd.init()
    epd.Clear()
    epd.sleep()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7b_V2.epdconfig.module_exit(cleanup=True)
    exit()