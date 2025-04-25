from display.displays import ConnectionsFrame, SignalFrame, ErrorFrame
from PIL import Image, ImageDraw
import pytest

EPD_WIDTH       = 176
EPD_HEIGHT      = 264

def test_ConnectionsFrame():

    connection1 = ('S1', 'Wil, SG', "5'")
    connection2 = ('S2', 'Wattwil, SG', "6'")
    connection3 = ('S3', 'Zürich, ZH', "7'")
    dummy_current_location = 'Mosnang, SG'
    dummy_connections = [connection1, connection2, connection3]

    connectionsframe = ConnectionsFrame()
    image = connectionsframe.get(dummy_current_location, dummy_connections)

    assert image is not None, "Image should not be None"
    assert isinstance(image, Image.Image), "Image should be of type PIL.Image.Image"
    assert image.size == (EPD_HEIGHT, EPD_WIDTH), f"Image size should be {(EPD_HEIGHT, EPD_WIDTH)}"
    assert image.mode == 'L', "Image mode should be 'L' (grayscale)"

def test_SignalFrame():

    signalframe = SignalFrame()
    image = signalframe.get("SSID", 2)

    assert image is not None, "Image should not be None"
    assert isinstance(image, Image.Image), "Image should be of type PIL.Image.Image"
    assert image.size == (EPD_HEIGHT, EPD_WIDTH), f"Image size should be {(EPD_HEIGHT, EPD_WIDTH)}"
    assert image.mode == 'L', "Image mode should be 'L' (grayscale)"
