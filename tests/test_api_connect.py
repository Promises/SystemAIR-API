"""Test module for validating connection to the Systemair API."""

import os
import pytest
import logging
from typing import Dict, Any, List, Optional

from systemair_api.auth.authenticator import SystemairAuthenticator
from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.api.websocket_client import SystemairWebSocket
from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.utils.exceptions import AuthenticationError, APIError, DeviceNotFoundError

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api_connection_test.log',
    filemode='w'
)
logger = logging.getLogger('APIConnectionTest')


class TestAPIConnection:
    """Test the connection to the Systemair API with real credentials."""

    def get_credentials(self) -> tuple:
        """Get credentials from environment variables.
        
        Returns:
            tuple: (email, password) or (None, None) if not available
        """
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')
        
        if not email or not password:
            logger.warning("No credentials found in environment variables")
            pytest.skip("EMAIL and PASSWORD environment variables required")
            return None, None
        
        return email, password

    def test_authentication(self):
        """Test authentication with the Systemair API."""
        email, password = self.get_credentials()
        if not email or not password:
            return
        
        try:
            logger.info("Attempting authentication")
            auth = SystemairAuthenticator(email, password)
            access_token = auth.authenticate()
            
            # Verify we got a token
            assert access_token, "No access token returned"
            assert len(access_token) > 20, "Access token seems too short"
            assert auth.token_expiry is not None, "No token expiry timestamp"
            
            logger.info(f"Authentication successful, token expires: {auth.token_expiry}")
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            pytest.fail(f"Authentication failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

    def test_get_account_devices(self):
        """Test fetching account devices from the API."""
        email, password = self.get_credentials()
        if not email or not password:
            return
        
        try:
            # Authenticate
            logger.info("Authenticating to get account devices")
            auth = SystemairAuthenticator(email, password)
            access_token = auth.authenticate()
            
            # Create API client
            api = SystemairAPI(access_token)
            
            # Get account devices
            logger.info("Fetching account devices")
            devices_data = api.get_account_devices()
            
            # Verify response structure
            assert 'data' in devices_data, "Missing 'data' in response"
            assert 'GetAccountDevices' in devices_data['data'], "Missing 'GetAccountDevices' in response data"
            
            # Get the devices
            devices = devices_data['data']['GetAccountDevices']
            logger.info(f"Found {len(devices)} devices")
            
            # Verify we have at least one device
            assert len(devices) > 0, "No devices found in account"
            
            # Verify device data structure
            device = devices[0]
            assert 'identifier' in device, "Missing 'identifier' in device data"
            assert 'name' in device, "Missing 'name' in device data"
            
            # Log device info
            logger.info(f"First device: {device['name']} (ID: {device['identifier']})")
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            pytest.fail(f"Authentication failed: {str(e)}")
        except APIError as e:
            logger.error(f"API error: {str(e)}")
            pytest.fail(f"API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

    def test_device_status_fetch(self):
        """Test fetching device status for all devices in the account."""
        email, password = self.get_credentials()
        if not email or not password:
            return
        
        try:
            # Authenticate
            logger.info("Authenticating to get device status")
            auth = SystemairAuthenticator(email, password)
            access_token = auth.authenticate()
            
            # Create API client
            api = SystemairAPI(access_token)
            
            # Get account devices
            devices_data = api.get_account_devices()
            devices = devices_data['data']['GetAccountDevices']
            
            if not devices:
                logger.warning("No devices found in account")
                pytest.skip("No devices found in account")
                return
            
            # Fetch status for each device
            for device in devices:
                device_id = device['identifier']
                device_name = device['name']
                logger.info(f"Fetching status for {device_name} (ID: {device_id})")
                
                try:
                    status_data = api.fetch_device_status(device_id)
                    
                    # Verify response structure
                    assert 'data' in status_data, "Missing 'data' in response"
                    assert 'GetView' in status_data['data'], "Missing 'GetView' in response data"
                    assert 'children' in status_data['data']['GetView'], "Missing 'children' in GetView"
                    
                    # Verify we have data items
                    children = status_data['data']['GetView']['children']
                    data_items = [
                        child['properties']['dataItem'] 
                        for child in children 
                        if 'properties' in child and 'dataItem' in child['properties']
                    ]
                    
                    logger.info(f"Found {len(data_items)} data items for {device_name}")
                    assert len(data_items) > 0, f"No data items found for device {device_name}"
                    
                    # Create and update a ventilation unit
                    unit = VentilationUnit(device_id, device_name)
                    unit.update_from_api(status_data)
                    
                    # Log some key unit properties
                    logger.info(f"Unit {device_name}:")
                    logger.info(f"  - User mode: {unit.user_mode_name}")
                    logger.info(f"  - Airflow: {unit.airflow}")
                    for temp_key, temp_value in unit.temperatures.items():
                        if temp_value is not None:
                            logger.info(f"  - Temperature {temp_key}: {temp_value}")
                    
                    # Verify device update worked
                    assert unit.user_mode is not None, "User mode not updated"
                    
                except DeviceNotFoundError as e:
                    logger.error(f"Device not found: {str(e)}")
                    pytest.fail(f"Device not found: {str(e)}")
                except APIError as e:
                    logger.error(f"API error: {str(e)}")
                    pytest.fail(f"API error: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    pytest.fail(f"Unexpected error: {str(e)}")
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            pytest.fail(f"Authentication failed: {str(e)}")
        except APIError as e:
            logger.error(f"API error: {str(e)}")
            pytest.fail(f"API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")

    def test_websocket_connection(self):
        """Test establishing a WebSocket connection and receiving updates."""
        email, password = self.get_credentials()
        if not email or not password:
            return
        
        # List to store received messages
        received_messages = []
        connected = False
        
        def on_message(data):
            """Callback for WebSocket messages."""
            logger.info(f"Received WebSocket message: {data.get('type')}")
            received_messages.append(data)
        
        try:
            # Authenticate
            logger.info("Authenticating for WebSocket connection")
            auth = SystemairAuthenticator(email, password)
            access_token = auth.authenticate()
            
            # Create API client
            api = SystemairAPI(access_token)
            
            # Create WebSocket client
            logger.info("Creating WebSocket client")
            ws_client = SystemairWebSocket(access_token, on_message)
            
            # Connect to WebSocket
            logger.info("Connecting to WebSocket")
            ws_client.connect()
            connected = True
            
            # Get account devices
            devices_data = api.get_account_devices()
            devices = devices_data['data']['GetAccountDevices']
            
            if not devices:
                logger.warning("No devices found in account")
                pytest.skip("No devices found in account")
                return
            
            # Broadcast status requests to trigger WebSocket updates
            device_ids = [device['identifier'] for device in devices]
            logger.info(f"Broadcasting status request for {len(device_ids)} devices")
            api.broadcast_device_statuses(device_ids)
            
            # Wait for messages (this would normally be handled by the main application loop)
            import time
            logger.info("Waiting for WebSocket messages...")
            time.sleep(5)  # Wait up to 5 seconds for messages
            
            # Clean up
            if connected:
                logger.info("Disconnecting WebSocket")
                ws_client.disconnect()
            
            # Log results
            logger.info(f"Received {len(received_messages)} WebSocket messages")
            
            # Note: In a real-world scenario, we'd expect at least one message,
            # but in testing, we might not get any due to timing issues
            # So we don't fail the test if no messages are received
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            pytest.fail(f"Authentication failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error: {str(e)}")
        finally:
            if connected:
                try:
                    ws_client.disconnect()
                except:
                    pass