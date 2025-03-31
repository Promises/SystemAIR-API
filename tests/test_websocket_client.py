import pytest
from unittest.mock import patch, Mock, MagicMock
import json
import threading

from systemair_api.api.websocket_client import SystemairWebSocket


class TestSystemairWebSocket:
    @pytest.fixture
    def callback_mock(self):
        """Create a mock callback function"""
        return Mock()
    
    @pytest.fixture
    def websocket_client(self, callback_mock):
        """Create a websocket client with test access token and mock callback"""
        return SystemairWebSocket("test_access_token", callback_mock)

    def test_initialization(self, websocket_client, callback_mock):
        """Test that the WebSocket client is initialized correctly"""
        assert websocket_client.access_token == "test_access_token"
        assert websocket_client.on_message_callback == callback_mock
        assert websocket_client.ws is None
        assert websocket_client.thread is None

    def test_on_message(self, websocket_client, callback_mock, mock_websocket_data):
        """Test handling of a received message"""
        # Setup
        ws_mock = Mock()
        message = json.dumps(mock_websocket_data)
        
        # Call the method
        websocket_client.on_message(ws_mock, message)
        
        # Assertions
        callback_mock.assert_called_once_with(mock_websocket_data)

    def test_on_error(self, websocket_client):
        """Test handling of an error"""
        # Setup
        ws_mock = Mock()
        error = Exception("Test error")
        
        # Call the method
        websocket_client.on_error(ws_mock, error)
        
        # No assertion needed, just checking it doesn't raise an exception

    def test_on_close(self, websocket_client):
        """Test handling of connection close"""
        # Setup
        ws_mock = Mock()
        close_status_code = 1000
        close_msg = "Normal closure"
        
        # Call the method
        websocket_client.on_close(ws_mock, close_status_code, close_msg)
        
        # No assertion needed, just checking it doesn't raise an exception

    def test_on_open(self, websocket_client):
        """Test handling of connection open"""
        # Setup
        ws_mock = Mock()
        
        # Call the method
        websocket_client.on_open(ws_mock)
        
        # No assertion needed, just checking it doesn't raise an exception

    @patch('websocket.WebSocketApp')
    @patch('websocket.enableTrace')
    @patch('threading.Thread')
    def test_connect(self, mock_thread, mock_enable_trace, mock_websocket_app, websocket_client):
        """Test connecting to the WebSocket server"""
        # Setup
        mock_ws = Mock()
        mock_websocket_app.return_value = mock_ws
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        # Call the method
        websocket_client.connect()
        
        # Assertions
        mock_enable_trace.assert_called_once_with(True)
        mock_websocket_app.assert_called_once()
        
        # Check that WebSocketApp was created with correct parameters
        ws_args = mock_websocket_app.call_args[0]
        ws_kwargs = mock_websocket_app.call_args[1]
        assert "wss://homesolutions.systemair.com/streaming/" in ws_args[0]
        assert "accessToken" in ws_kwargs["header"][0]
        assert "test_access_token" in ws_kwargs["header"][0]
        
        # Check the callback handlers were set
        assert ws_kwargs["on_open"] == websocket_client.on_open
        assert ws_kwargs["on_message"] == websocket_client.on_message
        assert ws_kwargs["on_error"] == websocket_client.on_error
        assert ws_kwargs["on_close"] == websocket_client.on_close
        
        # Check that thread was created and started
        assert websocket_client.ws == mock_ws
        assert websocket_client.thread == mock_thread_instance
        assert mock_thread.call_args[1]["target"] == mock_ws.run_forever
        assert "sslopt" in mock_thread.call_args[1]["kwargs"]
        mock_thread_instance.start.assert_called_once()

    def test_disconnect(self, websocket_client):
        """Test disconnecting from the WebSocket server"""
        # Setup
        websocket_client.ws = Mock()
        websocket_client.thread = Mock()
        
        # Call the method
        websocket_client.disconnect()
        
        # Assertions
        websocket_client.ws.close.assert_called_once()
        websocket_client.thread.join.assert_called_once()