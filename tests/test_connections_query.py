import os
from pathlib import Path

import pytest
from unittest import mock

from backend.connections_query import ConnectionsQueryEngine


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


def test_get_connections_parses_response(credentials_file):
    xml_response = """\
<OJP xmlns:ojp="http://www.vdv.de/ojp" xmlns:siri="http://www.siri.org.uk/siri">
  <ojp:OJPResponse>
    <ojp:ServiceDelivery>
      <ojp:OJPStopEventDelivery>
        <ojp:StopEventResult>
          <ojp:StopEvent>
            <ojp:ThisCall>
              <ojp:CallAtStop>
                <siri:StopPointRef>8573984</siri:StopPointRef>
                <ojp:StopPointName><ojp:Text>Bern</ojp:Text></ojp:StopPointName>
                <ojp:PlannedQuay><ojp:Text>3</ojp:Text></ojp:PlannedQuay>
                <ojp:ServiceDeparture>
                  <ojp:TimetabledTime>2025-05-03T10:00:00Z</ojp:TimetabledTime>
                </ojp:ServiceDeparture>
              </ojp:CallAtStop>
            </ojp:ThisCall>
            <ojp:Service>
              <ojp:DestinationText><ojp:Text>Wil</ojp:Text></ojp:DestinationText>
              <ojp:TrainNumber>123</ojp:TrainNumber>
              <ojp:PublishedServiceName><ojp:Text>S1</ojp:Text></ojp:PublishedServiceName>
            </ojp:Service>
          </ojp:StopEvent>
        </ojp:StopEventResult>
      </ojp:OJPStopEventDelivery>
    </ojp:ServiceDelivery>
  </ojp:OJPResponse>
</OJP>
"""
    mock_response = mock.Mock()
    mock_response.content = xml_response.encode("utf-8")
    mock_response.raise_for_status = mock.Mock()

    with mock.patch("requests.post", return_value=mock_response) as mocked_post:
        engine = ConnectionsQueryEngine()
        result = engine.get_connections("8573984", "2025-05-03T09:55:00Z")
        mocked_post.assert_called_once()

    assert len(result) == 1
    assert result[0]["ServiceName"] == "S1"
    assert result[0]["Destination"] == "Wil"
    assert result[0]["DepartureTime"] == "2025-05-03T10:00:00Z"


def test_get_connections_raises_on_error(credentials_file):
    import requests
    with mock.patch("requests.post", side_effect=requests.RequestException("boom")):
        engine = ConnectionsQueryEngine()
        with pytest.raises(Exception, match="Connections API request failed"):
            engine.get_connections("8573984", "2025-05-03T09:55:00Z")
