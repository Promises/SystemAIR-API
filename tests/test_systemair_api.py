import pytest
from unittest.mock import patch, Mock
import requests

from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.utils.constants import APIEndpoints


class TestSystemairAPI:
    @pytest.fixture
    def api_client(self):
        """Create an API client with test access token"""
        return SystemairAPI("test_access_token")

    def test_initialization(self, api_client):
        """Test that the API client is initialized correctly"""
        assert api_client.access_token == "test_access_token"
        assert api_client.headers["x-access-token"] == "test_access_token"
        assert "User-Agent" in api_client.headers
        assert "content-type" in api_client.headers

    @patch('requests.post')
    def test_get_account_devices(self, mock_post, api_client, mock_account_devices_response):
        """Test getting account devices"""
        # Setup
        mock_post.return_value = mock_account_devices_response
        
        # Call the method
        result = api_client.get_account_devices()
        
        # Assertions
        assert result["data"]["GetAccountDevices"][0]["identifier"] == "IAM_123456789ABC"
        assert result["data"]["GetAccountDevices"][0]["name"] == "Test Ventilation Unit"
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_account_devices_error(self, mock_post, api_client):
        """Test handling error when getting account devices"""
        # Setup - simulate a request exception
        mock_post.side_effect = requests.exceptions.RequestException("Test error")
        
        # Call the method
        result = api_client.get_account_devices()
        
        # Assertions
        assert result is None
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_fetch_device_status(self, mock_post, api_client, mock_device_status_response):
        """Test fetching device status"""
        # Setup
        mock_post.return_value = mock_device_status_response
        device_id = "IAM_123456789ABC"
        
        # Call the method
        result = api_client.fetch_device_status(device_id)
        
        # Assertions
        assert "data" in result
        assert "GetView" in result["data"]
        assert len(result["data"]["GetView"]["children"]) > 0
        
        # Verify headers were set correctly
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["headers"]["device-id"] == device_id
        assert call_kwargs["headers"]["device-type"] == "LEGACY"
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_fetch_device_status_error(self, mock_post, api_client):
        """Test handling error when fetching device status"""
        # Setup - simulate a request exception
        mock_post.side_effect = requests.exceptions.RequestException("Test error")
        device_id = "IAM_123456789ABC"
        
        # Call the method
        result = api_client.fetch_device_status(device_id)
        
        # Assertions
        assert result is None
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_broadcast_device_statuses(self, mock_post, api_client, mock_broadcast_response):
        """Test broadcasting device statuses"""
        # Setup
        mock_post.return_value = mock_broadcast_response
        device_ids = ["IAM_123456789ABC", "IAM_987654321XYZ"]
        
        # Call the method
        result = api_client.broadcast_device_statuses(device_ids)
        
        # Assertions
        assert result["data"]["BroadcastDeviceStatuses"] is True
        
        # Check that the device IDs were passed correctly
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["json"]["variables"]["deviceIds"] == device_ids
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_broadcast_device_statuses_error(self, mock_post, api_client):
        """Test handling error when broadcasting device statuses"""
        # Setup - simulate a request exception
        mock_post.side_effect = requests.exceptions.RequestException("Test error")
        device_ids = ["IAM_123456789ABC"]
        
        # Call the method
        result = api_client.broadcast_device_statuses(device_ids)
        
        # Assertions
        assert result is None
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_write_data_item(self, mock_post, api_client, mock_write_data_response):
        """Test writing data item to a device"""
        # Setup
        mock_post.return_value = mock_write_data_response
        device_id = "IAM_123456789ABC"
        register_id = 30  # REG_MAINBOARD_USERMODE_HMI_CHANGE_REQUEST
        value = 2  # CROWDED mode
        
        # Call the method
        result = api_client.write_data_item(device_id, register_id, value)
        
        # Assertions
        assert result["data"]["WriteDataItems"] is True
        
        # Verify headers and parameters
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["headers"]["device-id"] == device_id
        assert call_kwargs["headers"]["device-type"] == "LEGACY"
        assert call_kwargs["json"]["variables"]["input"]["dataPoints"][0]["id"] == register_id
        assert call_kwargs["json"]["variables"]["input"]["dataPoints"][0]["value"] == str(value)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_write_data_item_error(self, mock_post, api_client):
        """Test handling error when writing data item"""
        # Setup - simulate a request exception
        mock_post.side_effect = requests.exceptions.RequestException("Test error")
        device_id = "IAM_123456789ABC"
        register_id = 30
        value = 2
        
        # Call the method
        result = api_client.write_data_item(device_id, register_id, value)
        
        # Assertions
        assert result is None
        mock_post.assert_called_once()