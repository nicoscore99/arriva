import pytest

from display.displays import ConnectionsFrame, SignalFrame, WeatherFrame


def test_connections_frame_accepts_empty_list():
    frame = ConnectionsFrame()
    image = frame.get("Test Stop", [])
    assert image is not None


def test_signal_frame_rejects_invalid_types():
    frame = SignalFrame()
    with pytest.raises(ValueError):
        frame.get(123, "bad")


def test_weather_frame_handles_less_than_four_days():
    frame = WeatherFrame()
    forecasts = [
        {"local_date_time": "2025-05-03T00:00:00+02:00", "TX_C": 22, "TN_C": 16, "SYMBOL_CODE": 4},
        {"local_date_time": "2025-05-04T00:00:00+02:00", "TX_C": 15, "TN_C": 12, "SYMBOL_CODE": 25},
    ]
    image = frame.get(forecasts)
    assert image is not None
