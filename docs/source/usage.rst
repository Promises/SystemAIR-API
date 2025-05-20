Usage
=====

Quick Start
-----------

.. code-block:: python

    import os
    import time
    from dotenv import load_dotenv
    from systemair_api.auth.authenticator import SystemairAuthenticator
    from systemair_api.api.systemair_api import SystemairAPI
    from systemair_api.api.websocket_client import SystemairWebSocket

    # Load environment variables
    load_dotenv()

    # Authentication
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    authenticator = SystemairAuthenticator(email, password)
    access_token = authenticator.authenticate()

    # API connection
    api = SystemairAPI(access_token)

    # Get user devices
    devices = api.get_account_devices()
    if devices and 'data' in devices:
        for device in devices['data'].get('GetAccountDevices', []):
            print(f"Found device: {device['name']} (ID: {device['identifier']}")
            
            # Fetch device status
            device_id = device['identifier']
            status = api.fetch_device_status(device_id)
            
            # Set up WebSocket for real-time updates
            def on_websocket_message(data):
                if data["type"] == "SYSTEM_EVENT" and data["action"] == "DEVICE_STATUS_UPDATE":
                    props = data["properties"]
                    print(f"Update from {props['id']}: Mode={props['userMode']}, Temperature={props['temperature']}°C")
                    
            ws_client = SystemairWebSocket(access_token, on_websocket_message)
            ws_client.connect()
            
            # Broadcast for status updates
            api.broadcast_device_statuses([device_id])
            
            # Keep connection alive for a while
            time.sleep(60)
            
            # Clean up
            ws_client.disconnect()

Authentication
-------------

First, authenticate with your Systemair account credentials:

.. code-block:: python

    from systemair_api.auth.authenticator import SystemairAuthenticator

    authenticator = SystemairAuthenticator('your.email@example.com', 'your_password')
    access_token = authenticator.authenticate()

    # The authenticator handles token expiry and refresh
    if not authenticator.is_token_valid():
        access_token = authenticator.refresh_access_token()

API Interaction
--------------

Use the SystemairAPI class to interact with the Systemair API:

.. code-block:: python

    from systemair_api.api.systemair_api import SystemairAPI

    api = SystemairAPI(access_token)

    # Get all registered devices
    devices = api.get_account_devices()

    # Get detailed status for a specific device
    device_id = "IAM_123456789ABC"
    status = api.fetch_device_status(device_id)

    # Control your device
    api.write_data_item(device_id, 30, 6)  # Set user mode to Away
    api.write_data_item(device_id, 32, 210)  # Set temperature setpoint to 21.0°C

Real-time Updates with WebSocket
-------------------------------

Get real-time updates using the WebSocket client:

.. code-block:: python

    from systemair_api.api.websocket_client import SystemairWebSocket

    def on_message(data):
        if data["type"] == "SYSTEM_EVENT" and data["action"] == "DEVICE_STATUS_UPDATE":
            props = data["properties"]
            print(f"Temperature: {props['temperature']}°C")
            print(f"Humidity: {props['humidity']}%")
            print(f"Air Quality: {props['airQuality']}")

    ws_client = SystemairWebSocket(access_token, on_message)
    ws_client.connect()

    # Request status updates
    api.broadcast_device_statuses([device_id])

    # When done
    ws_client.disconnect()

Using the VentilationUnit Class
------------------------------

The VentilationUnit class provides a convenient interface for managing units:

.. code-block:: python

    from systemair_api.models.ventilation_unit import VentilationUnit

    # Create and configure a unit
    unit = VentilationUnit("IAM_123456789ABC", "Living Room Ventilation")

    # Update the unit from API data
    status_data = api.fetch_device_status(unit.identifier)
    unit.update_from_api(status_data)

    # Check unit status
    print(unit.temperatures["oat"])  # Outdoor air temperature
    print(unit.user_mode)  # Current user mode
    print(unit.airflow)  # Current airflow level

    # Set user mode
    from systemair_api.utils.constants import UserModes
    unit.set_user_mode(api, UserModes.REFRESH)  # Set to Refresh mode

    # Print full status
    unit.print_status()

Constants and Enumerations
-------------------------

The library provides several constants and enumerations to make working with the API easier:

.. code-block:: python

    from systemair_api.utils.constants import UserModes

    # User modes
    UserModes.AUTO      # 0
    UserModes.MANUAL    # 1
    UserModes.CROWDED   # 2
    UserModes.REFRESH   # 3
    UserModes.FIREPLACE # 4
    UserModes.AWAY      # 5
    UserModes.HOLIDAY   # 6

    # Access register constants directly
    from systemair_api.utils.register_constants import RegisterConstants

    # Example registers
    RegisterConstants.REG_MAINBOARD_USERMODE_MODE_HMI  # 29
    RegisterConstants.REG_MAINBOARD_TC_SP  # 32 (Temperature setpoint)
    RegisterConstants.REG_MAINBOARD_ECO_MODE_ON_OFF  # 34

Error Handling
-------------

The library provides custom exceptions for handling different error types:

.. code-block:: python

    from systemair_api.utils.exceptions import (
        SystemairError, AuthenticationError, APIError, DeviceNotFoundError, WebSocketError
    )

    try:
        # Attempt operations
        access_token = authenticator.authenticate()
        api = SystemairAPI(access_token)
        devices = api.get_account_devices()
    except AuthenticationError as e:
        print(f"Authentication failed: {e.message}")
    except APIError as e:
        print(f"API Error (status {e.status_code}): {e.message}")
    except DeviceNotFoundError as e:
        print(f"Device not found: {e.device_id}")
    except WebSocketError as e:
        print(f"WebSocket error: {e.message}")
    except SystemairError as e:
        print(f"General error: {e.message}")

Security
-------

To keep your credentials secure, use environment variables rather than hardcoding them:

.. code-block:: python

    import os
    from dotenv import load_dotenv

    load_dotenv()
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')