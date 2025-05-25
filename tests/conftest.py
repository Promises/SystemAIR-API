import pytest
import os
import json
from unittest.mock import Mock, patch


@pytest.fixture
def mock_response():
    """Create a mock response with customizable status_code and json content"""
    class MockResponse:
        def __init__(self, json_data, status_code=200, content=None, headers=None, url=None):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content or b''
            self.text = content.decode('utf-8') if content else ''
            self.headers = headers or {}
            self.url = url or ''
            self.reason = 'OK' if status_code == 200 else 'Error'

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if 400 <= self.status_code < 600:
                raise Exception(f"HTTP Error: {self.status_code}")

    return MockResponse


@pytest.fixture
def mock_device_data():
    """Sample device data returned from the API"""
    return {
        "identifier": "IAM_123456789ABC",
        "name": "Test Ventilation Unit",
        "street": "Test Street 123",
        "zipcode": "12345",
        "city": "Test City",
        "country": "Test Country",
        "deviceType": {
            "entry": "entry1",
            "module": "module1",
            "scope": "scope1",
            "type": "type1"
        }
    }


@pytest.fixture
def mock_account_devices_response(mock_response, mock_device_data):
    """Sample response for get_account_devices"""
    return mock_response({
        "data": {
            "GetAccountDevices": [mock_device_data]
        }
    })


@pytest.fixture
def mock_device_status_response(mock_response):
    """Sample response for fetch_device_status"""
    return mock_response({
        "data": {
            "GetView": {
                "children": [
                    {
                        "type": "card",
                        "properties": {
                            "dataItem": {
                                "id": 29,  # REG_MAINBOARD_USERMODE_MODE_HMI
                                "value": 1  # MANUAL mode
                            }
                        }
                    },
                    {
                        "type": "card",
                        "properties": {
                            "dataItem": {
                                "id": 31,  # REG_MAINBOARD_SPEED_INDICATION_APP
                                "value": 3  # Normal airflow
                            }
                        }
                    },
                    {
                        "type": "card",
                        "properties": {
                            "dataItem": {
                                "id": 32,  # REG_MAINBOARD_TC_SP
                                "value": 210  # 21.0°C
                            }
                        }
                    },
                    {
                        "type": "card",
                        "properties": {
                            "dataItem": {
                                "id": 54,  # REG_MAINBOARD_SENSOR_OAT
                                "value": 150  # 15.0°C
                            }
                        }
                    }
                ]
            }
        }
    })


@pytest.fixture
def mock_write_data_response(mock_response):
    """Sample response for write_data_item"""
    return mock_response({
        "data": {
            "WriteDataItems": True
        }
    })


@pytest.fixture
def mock_broadcast_response(mock_response):
    """Sample response for broadcast_device_statuses"""
    return mock_response({
        "data": {
            "BroadcastDeviceStatuses": True
        }
    })


@pytest.fixture
def mock_websocket_data():
    """Sample websocket message data"""
    return {
        "type": "SYSTEM_EVENT",
        "action": "DEVICE_STATUS_UPDATE",
        "properties": {
            "id": "IAM_123456789ABC",
            "model": "Test Model",
            "activeAlarms": False,
            "airflow": 3,
            "connectivity": ["online", "cloud"],
            "filterExpiration": 2592000,
            "serialNumber": "SN12345",
            "temperature": 22.5,
            "userMode": 1,
            "airQuality": 90,
            "humidity": 45,
            "co2": 650,
            "update": {
                "inProgress": False
            },
            "configurationWizard": {
                "active": False
            },
            "temperatures": {
                "oat": 15.0,
                "sat": 19.5,
                "setpoint": 21.0
            },
            "versions": [
                {"type": "hardware", "version": "2.0"},
                {"type": "firmware", "version": "1.5.2"}
            ]
        }
    }


@pytest.fixture
def mock_auth_response(mock_response):
    """Mock authentication response with valid token"""
    return mock_response({
        "access_token": "mock_access_token_12345",
        "refresh_token": "mock_refresh_token_67890",
        "token_type": "Bearer",
        "expires_in": 3600
    })