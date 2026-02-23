import importlib
import sys
import types
from datetime import datetime, timezone

def _import_arriva():
    if "gpiozero" not in sys.modules:
        gpiozero = types.ModuleType("gpiozero")

        class DummyGPIO:
            def __init__(self, *args, **kwargs):
                pass

            def close(self):
                pass

        gpiozero.Button = DummyGPIO
        gpiozero.LED = DummyGPIO
        sys.modules["gpiozero"] = gpiozero

    if "waveshare_epd" not in sys.modules:
        waveshare_epd = types.ModuleType("waveshare_epd")
        epd2in7_V2 = types.ModuleType("waveshare_epd.epd2in7_V2")

        class DummyEPD:
            def init(self):
                pass

            def Clear(self):
                pass

            def display(self, *args, **kwargs):
                pass

            def getbuffer(self, *args, **kwargs):
                return None

        epd2in7_V2.EPD = DummyEPD
        waveshare_epd.epd2in7_V2 = epd2in7_V2
        sys.modules["waveshare_epd"] = waveshare_epd
        sys.modules["waveshare_epd.epd2in7_V2"] = epd2in7_V2

    return importlib.import_module("arriva").Arriva


def test_connections_formatting_handles_timezones():
    Arriva = _import_arriva()
    arriva = Arriva.__new__(Arriva)
    arriva_module = importlib.import_module("arriva")

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2025, 5, 3, 9, 55, 0, tzinfo=timezone.utc)

    original_datetime = arriva_module.datetime
    try:
        setattr(arriva_module, "datetime", FixedDateTime)
        connections = [
            {"ServiceName": "S1", "Destination": "Wil", "DepartureTime": "2025-05-03T10:00:00Z"},
            {"ServiceName": "S2", "Destination": "St. Gallen", "DepartureTime": "2025-05-03T12:00:00+02:00"},
            {"ServiceName": "S3", "Destination": "Bern", "DepartureTime": "bad-time"},
        ]

        formatted = Arriva.connections_formatting(arriva, connections)
    finally:
        setattr(arriva_module, "datetime", original_datetime)

    assert formatted[0][2] == "5"
    assert formatted[1][2] == "5"
    assert formatted[2][2] == "?"


def test_button4_does_not_change_status(monkeypatch):
    Arriva = _import_arriva()
    arriva = Arriva.__new__(Arriva)
    arriva.status = 2
    arriva.timer_interval = 60
    arriva.update_screen = lambda: None

    monkeypatch.setattr("time.time", lambda: 1000)

    Arriva.button4_callback(arriva)
    assert arriva.status == 2
