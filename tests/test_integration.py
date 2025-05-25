import pytest
from unittest.mock import patch, Mock, MagicMock
import os

from systemair_api.auth.authenticator import SystemairAuthenticator
from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.api.websocket_client import SystemairWebSocket
from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.utils.constants import UserModes
from systemair_api.utils.register_constants import RegisterConstants


class TestIntegration:
    """
    Integration tests that verify the interaction between components.
    These tests mock external API calls but test real interactions between classes.
    """
    
    @pytest.fixture
    def mock_env_variables(self):
        """Mock environment variables"""
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "test_password"}):
            yield
    
    @patch.object(SystemairAuthenticator, 'authenticate')
    @patch.object(SystemairAPI, 'get_account_devices')
    @patch.object(SystemairAPI, 'fetch_device_status')
    def test_device_discovery_and_status(self, mock_fetch_status, mock_get_devices, 
                                        mock_authenticate, mock_env_variables, 
                                        mock_account_devices_response,
                                        mock_device_status_response):
        """Test the flow from authentication to device discovery and status fetching"""
        # Setup mocks
        mock_authenticate.return_value = "test_access_token"
        mock_get_devices.return_value = mock_account_devices_response.json()
        mock_fetch_status.return_value = mock_device_status_response.json()
        
        # Create authenticator and authenticate
        authenticator = SystemairAuthenticator("test@example.com", "test_password")
        access_token = authenticator.authenticate()
        
        # Create API client and discover devices
        api = SystemairAPI(access_token)
        devices_response = api.get_account_devices()
        
        # Process device data
        device_data = devices_response["data"]["GetAccountDevices"][0]
        unit = VentilationUnit(device_data["identifier"], device_data["name"])
        
        # Fetch device status
        status_response = api.fetch_device_status(unit.identifier)
        unit.update_from_api(status_response)
        
        # Assertions
        assert mock_authenticate.called
        assert mock_get_devices.called
        assert mock_fetch_status.called
        assert unit.identifier == "IAM_123456789ABC"
        assert unit.name == "Test Ventilation Unit"
        assert unit.user_mode == 1  # MANUAL mode
        assert unit.airflow == 3  # NORMAL airflow
        assert unit.temperatures["setpoint"] == 21.0
    
    @patch.object(SystemairAuthenticator, 'authenticate')
    @patch.object(SystemairAPI, 'write_data_item')
    def test_writing_device_data(self, mock_write_data, mock_authenticate, mock_write_data_response):
        """Test writing data to a device"""
        # Setup mocks
        mock_authenticate.return_value = "test_access_token"
        mock_write_data.return_value = mock_write_data_response.json()
        
        # Create authenticator and API client
        authenticator = SystemairAuthenticator("test@example.com", "test_password")
        access_token = authenticator.authenticate()
        api = SystemairAPI(access_token)
        
        # Create a unit and set a value
        unit = VentilationUnit("IAM_123456789ABC", "Test Unit")
        
        # Change user mode
        result = unit.set_user_mode(api, UserModes.AWAY)
        
        # Assertions
        assert mock_authenticate.called
        assert mock_write_data.called
        # The set_user_mode method calls set_value which returns the result of the API call
        mock_write_data.assert_called_once()
    
    @patch.object(SystemairAuthenticator, 'is_token_valid')
    @patch.object(SystemairAuthenticator, 'refresh_access_token')
    @patch.object(SystemairAPI, 'broadcast_device_statuses')
    def test_token_refresh_flow(self, mock_broadcast, mock_refresh_token, 
                               mock_is_valid, mock_auth_response,
                               mock_broadcast_response):
        """Test the token refresh flow"""
        # Setup mocks
        mock_is_valid.side_effect = [False, True]  # First invalid, then valid
        mock_refresh_token.return_value = "new_test_access_token"
        mock_broadcast.return_value = mock_broadcast_response.json()
        
        # Create authenticator with pre-configured tokens
        authenticator = SystemairAuthenticator("test@example.com", "test_password")
        authenticator.access_token = "old_test_access_token"
        authenticator.refresh_token = "test_refresh_token"
        
        # Check if token is valid (it's not)
        if not authenticator.is_token_valid():
            # Refresh the token
            access_token = authenticator.refresh_access_token()
            # Create a new API client with the new token
            api = SystemairAPI(access_token)
            
            # Make an API call
            device_ids = ["IAM_123456789ABC"]
            result = api.broadcast_device_statuses(device_ids)
        
        # Assertions
        assert mock_is_valid.call_count == 1
        assert mock_refresh_token.called
        assert mock_broadcast.called
        assert result["data"]["BroadcastDeviceStatuses"] is True
    
    @patch.object(SystemairWebSocket, 'connect')
    @patch.object(SystemairWebSocket, 'disconnect')
    def test_websocket_lifecycle(self, mock_disconnect, mock_connect):
        """Test WebSocket lifecycle with ventilation unit updates"""
        # Setup callback for WebSocket messages
        received_data = []
        
        def on_message(data):
            received_data.append(data)
            
            # Update a unit if it's a device status update
            if data["type"] == "SYSTEM_EVENT" and data["action"] == "DEVICE_STATUS_UPDATE":
                unit.update_from_websocket(data)
        
        # Create a WebSocket client and unit
        ws_client = SystemairWebSocket("test_access_token", on_message)
        unit = VentilationUnit("IAM_123456789ABC", "Test Unit")
        
        # Connect the WebSocket
        ws_client.connect()
        
        # Simulate receiving a message
        ws_client.on_message(None, '{"type":"SYSTEM_EVENT","action":"DEVICE_STATUS_UPDATE","properties":{"id":"IAM_123456789ABC","temperature":23.5,"userMode":2,"airflow":4}}')
        
        # Disconnect the WebSocket
        ws_client.disconnect()
        
        # Assertions
        assert mock_connect.called
        assert mock_disconnect.called
        assert len(received_data) == 1
        assert received_data[0]["type"] == "SYSTEM_EVENT"
        assert unit.temperature == 23.5
        assert unit.user_mode == 2
        assert unit.airflow == 4