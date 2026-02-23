from pathlib import Path
import time
from unittest import mock

import pytest
import requests

from backend.weather_query import WeatherQueryEngine


def _write_credentials(tmp_path: Path) -> Path:
    credentials = tmp_path / "credentials.yaml"
    credentials.write_text(
        "\n".join(
            [
                "OpenTransportData:",
                "  api_key: test_key",
                "  url: https://example.com/ojp",
                "MeteoMeteoProductFreemium:",
                "  client_id: test_client",
                "  client_secret: test_secret",
                "  auth_url: https://example.com/oauth",
                "  forecast_url: https://example.com/forecast",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return credentials


@pytest.fixture()
def credentials_file(tmp_path, monkeypatch):
    credentials = _write_credentials(tmp_path)
    monkeypatch.setenv("ARRIVA_CREDENTIALS_PATH", str(credentials))
    yield credentials


def test_get_weather_forecast_success(credentials_file):
    def _mock_get(url, *args, **kwargs):
        mock_response = mock.Mock()
        if url == "https://example.com/oauth":
            mock_response.json.return_value = {"access_token": "token123"}
        elif url == "https://example.com/forecast/47.4467,9.4050":
            mock_response.json.return_value = {"forecast": {"day": []}}
        else:
            raise AssertionError("Unexpected URL")
        mock_response.raise_for_status = mock.Mock()
        return mock_response

    with mock.patch("requests.get", side_effect=_mock_get):
        engine = WeatherQueryEngine()
        result = engine.get_weather_forecast(47.4467, 9.4050)

    assert "forecast" in result
    assert result["forecast"]["day"] == []


def test_get_weather_forecast_returns_cache_on_failure(credentials_file, monkeypatch):
    engine = WeatherQueryEngine()
    engine.forecast = {"cached": True}
    engine.forecast_timer = time.time() - 2000
    engine.access_token = "token123"
    engine.access_token_timer = time.time()

    def _fail(*args, **kwargs):
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", _fail)

    result = engine.get_weather_forecast(47.4467, 9.4050)
    assert result == {"cached": True}
