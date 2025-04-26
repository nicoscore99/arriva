#!/usr/bin/python
# -*- coding:utf-8 -*-
import traceback
import logging
import time
from transformations import on_raspi

logging.basicConfig(level=logging.DEBUG)

# import the static image class
from displays import ConnectionsFrame, SignalFrame, ErrorFrame

def main():

    # Create an instance of the StaticImage class
    static_image = SignalFrame()
    # Get the image
    image = static_image.get("MyWifi", 2)

    # Check if the current device is Raspberry Pi
    raspberry_pi = on_raspi()

    if raspberry_pi:
        try:
            # import waveshare_epd library for Raspberry Pi
            from waveshare_epd import epd2in7_V2

            # Initialize the display
            epd = epd2in7_V2.EPD()
            epd.init()

            # Reset the display
            epd.reset()

            epd.Clear()
            
            # Display the image
            epd.display(epd.getbuffer(image))

            time.sleep(5)
            # Clear the display
            epd.init()
            epd.Clear()

            # Sleep to save power
            epd.sleep()
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd2in7_V2.epdconfig.module_exit(cleanup=True)
            exit()
        except Exception as e:
            logging.error("An error occurred: %s", e)
            traceback.print_exc()
        finally:
            # Cleanup the display instance
            if 'epd' in locals():
                epd2in7_V2.epdconfig.module_exit(cleanup=True)
    else:
        try:
            # Dispay the image on screen

            # Rotate image by 90 degrees
            image.show()
            time.sleep(5)
            # Close the image window
            image.close()
        except Exception as e:
            logging.error("An error occurred: %s", e)
            traceback.print_exc()
        finally:
            # Cleanup the image instance
            if 'image' in locals():
                image.close()

if __name__ == '__main__':
    main()