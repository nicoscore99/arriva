import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from display.displays import ConnectionsFrame, SignalFrame, ErrorFrame, WeatherFrame
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

def test_WeatherFrame():

    test_dict = {
        "geolocation": {
            "geolocation_names": [
                {
                    "district": "St. Gallen",
                    "description_short": "St. Gallen, Sankt Gallen",
                    "description_long": "St. Gallen, Sankt Gallen, 672 m \u00fc.M.",
                    "id": "4bab2de25b121a135c35272ef5874f29",
                    "location_id": "417195520",
                    "type": "city",
                    "language": 0,
                    "translation_type": "orig",
                    "name": "Guggeien",
                    "country": "Schweiz",
                    "province": "Sankt Gallen",
                    "inhabitants": 10,
                    "height": 672,
                    "ch": 1
                }
            ],
            "id": "47.4467,9.4050",
            "lat": 47.4467,
            "lon": 9.405,
            "station_id": "S11683",
            "timezone": "Europe\/Zurich",
            "default_name": "Guggeien",
            "alarm_region_id": "9",
            "alarm_region_name": "Agglo St. Gallen",
            "district": "St. Gallen"
        },
        "forecast": {
            "day": [
                {
                    "local_date_time": "2025-05-03T00:00:00+02:00",
                    "TX_C": 22,
                    "TN_C": 16,
                    "PROBPCP_PERCENT": 71,
                    "RRR_MM": 0.8,
                    "FF_KMH": 7,
                    "FX_KMH": 41,
                    "DD_DEG": 270,
                    "SUNSET": 2035,
                    "SUNRISE": 602,
                    "SUN_H": 5,
                    "UVI": 6,
                    "SYMBOL_CODE": 4,
                    "SYMBOL24_CODE": 1,
                    "type": "day",
                    "min_color": {
                        "temperature": 16,
                        "background_color": "#e4e20c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 22,
                        "background_color": "#fcd804",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-04T00:00:00+02:00",
                    "TX_C": 15,
                    "TN_C": 12,
                    "PROBPCP_PERCENT": 93,
                    "RRR_MM": 14.0,
                    "FF_KMH": 6,
                    "FX_KMH": 28,
                    "DD_DEG": 290,
                    "SUNSET": 2037,
                    "SUNRISE": 600,
                    "SUN_H": 2,
                    "UVI": 6,
                    "SYMBOL_CODE": 25,
                    "SYMBOL24_CODE": 41,
                    "type": "day",
                    "min_color": {
                        "temperature": 12,
                        "background_color": "#bcd61c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 15,
                        "background_color": "#e4e20c",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-05T00:00:00+02:00",
                    "TX_C": 7,
                    "TN_C": 6,
                    "PROBPCP_PERCENT": 93,
                    "RRR_MM": 24.0,
                    "FF_KMH": 4,
                    "FX_KMH": 17,
                    "DD_DEG": 70,
                    "SUNSET": 2038,
                    "SUNRISE": 559,
                    "SUN_H": 0,
                    "UVI": 7,
                    "SYMBOL_CODE": 23,
                    "SYMBOL24_CODE": 47,
                    "type": "day",
                    "min_color": {
                        "temperature": 6,
                        "background_color": "#24865c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 7,
                        "background_color": "#3c9854",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-06T00:00:00+02:00",
                    "TX_C": 11,
                    "TN_C": 5,
                    "PROBPCP_PERCENT": 90,
                    "RRR_MM": 3.0,
                    "FF_KMH": 4,
                    "FX_KMH": 17,
                    "DD_DEG": 50,
                    "SUNSET": 2040,
                    "SUNRISE": 557,
                    "SUN_H": 2,
                    "UVI": 7,
                    "SYMBOL_CODE": 4,
                    "SYMBOL24_CODE": 21,
                    "type": "day",
                    "min_color": {
                        "temperature": 5,
                        "background_color": "#146d6c",
                        "text_color": "#ffffff"
                    },
                    "max_color": {
                        "temperature": 11,
                        "background_color": "#accf24",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-07T00:00:00+02:00",
                    "TX_C": 12,
                    "TN_C": 6,
                    "PROBPCP_PERCENT": 79,
                    "RRR_MM": 4.0,
                    "FF_KMH": 4,
                    "FX_KMH": 17,
                    "DD_DEG": 60,
                    "SUNSET": 2041,
                    "SUNRISE": 556,
                    "SUN_H": 2,
                    "UVI": 7,
                    "SYMBOL_CODE": 4,
                    "SYMBOL24_CODE": 47,
                    "type": "day",
                    "min_color": {
                        "temperature": 6,
                        "background_color": "#24865c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 12,
                        "background_color": "#bcd61c",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-08T00:00:00+02:00",
                    "TX_C": 12,
                    "TN_C": 6,
                    "PROBPCP_PERCENT": 78,
                    "RRR_MM": 3.0,
                    "FF_KMH": 4,
                    "FX_KMH": 15,
                    "DD_DEG": 60,
                    "SUNSET": 2042,
                    "SUNRISE": 554,
                    "SUN_H": 4,
                    "UVI": 7,
                    "SYMBOL_CODE": 4,
                    "SYMBOL24_CODE": 21,
                    "type": "day",
                    "min_color": {
                        "temperature": 6,
                        "background_color": "#24865c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 12,
                        "background_color": "#bcd61c",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-09T00:00:00+02:00",
                    "TX_C": 15,
                    "TN_C": 6,
                    "PROBPCP_PERCENT": 57,
                    "RRR_MM": 1.0,
                    "FF_KMH": 4,
                    "FX_KMH": 17,
                    "DD_DEG": 70,
                    "SUNSET": 2044,
                    "SUNRISE": 553,
                    "SUN_H": 7,
                    "UVI": 7,
                    "SYMBOL_CODE": 11,
                    "SYMBOL24_CODE": 21,
                    "type": "day",
                    "min_color": {
                        "temperature": 6,
                        "background_color": "#24865c",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 15,
                        "background_color": "#e4e20c",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-10T00:00:00+02:00",
                    "TX_C": 17,
                    "TN_C": 7,
                    "PROBPCP_PERCENT": 26,
                    "RRR_MM": 0.2,
                    "FF_KMH": 4,
                    "FX_KMH": 19,
                    "DD_DEG": 70,
                    "SUNSET": 2045,
                    "SUNRISE": 551,
                    "SUN_H": 8,
                    "UVI": 7,
                    "SYMBOL_CODE": 10,
                    "SYMBOL24_CODE": 1,
                    "type": "day",
                    "min_color": {
                        "temperature": 7,
                        "background_color": "#3c9854",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 17,
                        "background_color": "#f4e50b",
                        "text_color": "#000000"
                    }
                },
                {
                    "local_date_time": "2025-05-11T00:00:00+02:00",
                    "TX_C": 19,
                    "TN_C": 8,
                    "PROBPCP_PERCENT": 36,
                    "RRR_MM": 0.6,
                    "FF_KMH": 4,
                    "FX_KMH": 22,
                    "DD_DEG": 80,
                    "SUNSET": 2046,
                    "SUNRISE": 550,
                    "SUN_H": 9,
                    "UVI": 7,
                    "SYMBOL_CODE": 10,
                    "SYMBOL24_CODE": 2,
                    "type": "day",
                    "min_color": {
                        "temperature": 8,
                        "background_color": "#54a644",
                        "text_color": "#000000"
                    },
                    "max_color": {
                        "temperature": 19,
                        "background_color": "#fce404",
                        "text_color": "#000000"
                    }
                }
            ]
        }
    }




    weatherframe = WeatherFrame()
    image = weatherframe.get(test_dict['forecast']['day'])

    assert image is not None, "Image should not be None"
    assert isinstance(image, Image.Image), "Image should be of type PIL.Image.Image"
    assert image.size == (EPD_HEIGHT, EPD_WIDTH), f"Image size should be {(EPD_HEIGHT, EPD_WIDTH)}"
    assert image.mode == 'L', "Image mode should be 'L' (grayscale)"

def test_ErrorFrame():

    errorframe = ErrorFrame()
    image = errorframe.get("Error message")

    assert image is not None, "Image should not be None"
    assert isinstance(image, Image.Image), "Image should be of type PIL.Image.Image"
    assert image.size == (EPD_HEIGHT, EPD_WIDTH), f"Image size should be {(EPD_HEIGHT, EPD_WIDTH)}"
    assert image.mode == 'L', "Image mode should be 'L' (grayscale)"