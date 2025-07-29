"""Tests for the weather.py module."""
import json
from typing import Any, Dict
import pytest
from unittest.mock import AsyncMock, patch

import httpx
import pytest_asyncio

import weather


@pytest.fixture
def alert_data_full() -> Dict[str, Any]:
    """Return a sample alert data with features."""
    return {
        "features": [
            {
                "properties": {
                    "event": "Flood Warning",
                    "areaDesc": "Miami County",
                    "severity": "Moderate",
                    "description": "A flood warning is in effect for this area.",
                    "instruction": "Move to higher ground. Avoid flood waters."
                }
            },
            {
                "properties": {
                    "event": "Heat Advisory",
                    "areaDesc": "Dade County",
                    "severity": "Minor",
                    "description": "A heat advisory is in effect for this area.",
                    "instruction": "Stay hydrated and avoid prolonged sun exposure."
                }
            }
        ]
    }


@pytest.fixture
def alert_data_empty() -> Dict[str, Any]:
    """Return a sample alert data with no features."""
    return {
        "features": []
    }


@pytest.fixture
def forecast_points_data() -> Dict[str, Any]:
    """Return a sample forecast points data."""
    return {
        "properties": {
            "forecast": "https://api.weather.gov/gridpoints/MIA/50,50/forecast"
        }
    }


@pytest.fixture
def forecast_data() -> Dict[str, Any]:
    """Return a sample forecast data."""
    return {
        "properties": {
            "periods": [
                {
                    "name": "Today",
                    "temperature": 75,
                    "temperatureUnit": "F",
                    "windSpeed": "10 mph",
                    "windDirection": "NE",
                    "detailedForecast": "Sunny with a high near 75. Northeast wind around 10 mph."
                },
                {
                    "name": "Tonight",
                    "temperature": 60,
                    "temperatureUnit": "F",
                    "windSpeed": "5 mph",
                    "windDirection": "N",
                    "detailedForecast": "Clear with a low around 60. North wind around 5 mph."
                },
                {
                    "name": "Tomorrow",
                    "temperature": 78,
                    "temperatureUnit": "F",
                    "windSpeed": "8 mph",
                    "windDirection": "E",
                    "detailedForecast": "Mostly sunny with a high near 78. East wind around 8 mph."
                },
                {
                    "name": "Tomorrow Night",
                    "temperature": 62,
                    "temperatureUnit": "F",
                    "windSpeed": "5 mph",
                    "windDirection": "NE",
                    "detailedForecast": "Partly cloudy with a low around 62. Northeast wind around 5 mph."
                },
                {
                    "name": "Monday",
                    "temperature": 80,
                    "temperatureUnit": "F",
                    "windSpeed": "10 mph",
                    "windDirection": "SE",
                    "detailedForecast": "Partly sunny with a high near 80. Southeast wind around 10 mph."
                },
                {
                    "name": "Monday Night",
                    "temperature": 65,
                    "temperatureUnit": "F",
                    "windSpeed": "5 mph",
                    "windDirection": "S",
                    "detailedForecast": "Mostly cloudy with a low around 65. South wind around 5 mph."
                }
            ]
        }
    }


@pytest_asyncio.fixture
async def mock_client(
    monkeypatch, alert_data_full, alert_data_empty, forecast_points_data, forecast_data
) -> None:
    """Mock the httpx.AsyncClient for testing."""
    
    # Create a proper mock class that supports async context manager
    class MockResponse:
        def __init__(self, url, **kwargs):
            self.url = url
            self.kwargs = kwargs
            self.status_code = 200
        
        async def json(self):
            """Return mock data based on URL."""
            if "alerts/active/area/FL" in self.url:
                return alert_data_full
            elif "alerts/active/area/XX" in self.url:
                return {}
            elif "alerts/active/area/CA" in self.url:
                return alert_data_empty
            elif "points/25.0,-80.0" in self.url:
                return forecast_points_data
            elif "gridpoints/MIA/50,50/forecast" in self.url:
                return forecast_data
            return {}
        
        async def raise_for_status(self):
            """Raise an exception for certain URLs."""
            if "points/999.0,999.0" in self.url:
                raise httpx.HTTPStatusError(
                    "404 Not Found", request=None, response=self
                )
            # Otherwise, do nothing
            return
    
    class MockAsyncClient:
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
        async def get(self, url, **kwargs):
            """Return mock response based on URL."""
            return MockResponse(url, **kwargs)

    # Create a new AsyncClient factory that returns our mock client
    def mock_async_client(*args, **kwargs):
        return MockAsyncClient()

    # Patch httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient", mock_async_client)


def test_format_alert():
    """Test the format_alert function."""
    feature = {
        "properties": {
            "event": "Flood Warning",
            "areaDesc": "Miami County",
            "severity": "Moderate",
            "description": "A flood warning is in effect for this area.",
            "instruction": "Move to higher ground. Avoid flood waters."
        }
    }

    formatted = weather.format_alert(feature)
    
    assert "Event: Flood Warning" in formatted
    assert "Area: Miami County" in formatted
    assert "Severity: Moderate" in formatted
    assert "Description: A flood warning is in effect for this area." in formatted
    assert "Instructions: Move to higher ground. Avoid flood waters." in formatted


@pytest.mark.asyncio
async def test_get_alerts_success(mock_client):
    """Test successful retrieval of alerts."""
    result = await weather.get_alerts("FL")
    
    assert "Event: Flood Warning" in result
    assert "Area: Miami County" in result
    assert "Event: Heat Advisory" in result
    assert "Area: Dade County" in result


@pytest.mark.asyncio
async def test_get_alerts_no_alerts(mock_client):
    """Test when there are no alerts for a state."""
    result = await weather.get_alerts("CA")
    
    assert result == "No active alerts for this state."


@pytest.mark.asyncio
async def test_get_alerts_api_failure(mock_client):
    """Test handling of API failure in get_alerts."""
    result = await weather.get_alerts("XX")
    
    assert result == "Unable to fetch alerts or no alerts found."


@pytest.mark.asyncio
async def test_get_forecast_success(mock_client):
    """Test successful retrieval of forecast."""
    result = await weather.get_forecast(25.0, -80.0)
    
    assert "Today" in result
    assert "Temperature: 75°F" in result
    assert "Tonight" in result
    assert "Temperature: 60°F" in result
    assert "Tomorrow" in result
    assert "Forecast: Mostly sunny with a high near 78. East wind around 8 mph." in result


@pytest.mark.asyncio
async def test_get_forecast_points_api_failure(mock_client):
    """Test handling of Points API failure in get_forecast."""
    result = await weather.get_forecast(999.0, 999.0)
    
    assert result == "Unable to fetch forecast data for this location."
@pytest.mark.asyncio
async def test_get_forecast_forecast_api_failure(monkeypatch, mock_client, forecast_points_data):
    """Test handling of Forecast API failure in get_forecast."""
    
    # Direct patching of the make_nws_request function 
    async def mock_make_nws_request(url):
        if "gridpoints" in url:
            return None
        elif "points" in url:
            return forecast_points_data
        return None
    
    monkeypatch.setattr(weather, "make_nws_request", mock_make_nws_request)
    
    result = await weather.get_forecast(26.0, -81.0)
    
    assert result == "Unable to fetch detailed forecast."
@pytest.mark.asyncio
async def test_make_nws_request_exception(monkeypatch):
    """Test that make_nws_request handles exceptions gracefully."""
    
    # Create a mock class that raises an exception on get
    class ExceptionMockClient:
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
        async def get(self, *args, **kwargs):
            raise Exception("Test exception")
    
    # Create a constructor that returns our mock client
    def mock_exception_client(*args, **kwargs):
        return ExceptionMockClient()
    
    # Apply the monkeypatch
    monkeypatch.setattr(httpx, "AsyncClient", mock_exception_client)
    
    result = await weather.make_nws_request("https://api.weather.gov/test")
    
    assert result is None

