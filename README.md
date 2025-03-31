# SystemAIR-API

A Python library for communicating with and controlling Systemair ventilation units through the Systemair Home Solutions API.

## Overview

SystemAIR-API allows you to connect to your Systemair ventilation units, retrieve status information, and control various functions such as ventilation modes, airflow levels, and temperature settings. The library provides a clean interface for interacting with your Systemair units programmatically, making it ideal for home automation systems, custom monitoring solutions, or integration with other smart home platforms.

### Package Structure

```
systemair_api/
├── __init__.py       # Main package exports
├── __main__.py       # Script for running as a module
├── api/              # API communication modules
│   ├── systemair_api.py     # Core API client
│   └── websocket_client.py  # WebSocket for real-time updates
├── auth/             # Authentication handling
│   └── authenticator.py     # OAuth2 authentication
├── models/           # Data models
│   ├── ventilation_data.py  # Mode/level definitions
│   └── ventilation_unit.py  # Main ventilation unit class
└── utils/            # Utilities
    ├── constants.py          # API endpoints and modes
    └── register_constants.py # Register IDs for device control
```

## Features

- Authentication with Systemair Home Solutions cloud
- Token management with automatic refresh
- Real-time monitoring via WebSocket connection
- Retrieve unit information and status
- Control ventilation modes and airflow levels
- Monitor temperatures, humidity, and air quality
- View and manage alarms
- Track active functions (heating, cooling, etc.)

## Installation

Install from source:

```bash
git clone https://github.com/henningbe/SystemAIR-API.git
cd SystemAIR-API
pip install -r requirements.txt
pip install -e .
```

You can run the module directly after installation:

```bash
# Run the example program
python -m systemair_api

# Import in your own projects
import systemair_api
```

## Requirements

- Python 3.7+
- requests
- websocket-client
- beautifulsoup4
- python-dotenv

All dependencies are listed in the `requirements.txt` file.

## Quick Start

```python
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
        print(f"Found device: {device['name']} (ID: {device['identifier']})")
        
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
        
        # Example: Change user mode to Away
        # from systemair_api.utils.constants import UserModes
        # api.write_data_item(device_id, 30, UserModes.AWAY + 1)
        
        # Keep connection alive for a while
        time.sleep(60)
        
        # Clean up
        ws_client.disconnect()
```

## Usage

### Authentication

First, authenticate with your Systemair account credentials:

```python
from systemair_api.auth.authenticator import SystemairAuthenticator

authenticator = SystemairAuthenticator('your.email@example.com', 'your_password')
access_token = authenticator.authenticate()

# The authenticator handles token expiry and refresh
if not authenticator.is_token_valid():
    access_token = authenticator.refresh_access_token()
```

### API Interaction

Use the SystemairAPI class to interact with the Systemair API:

```python
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
```

### Real-time Updates with WebSocket

Get real-time updates using the WebSocket client:

```python
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
```

### Using the VentilationUnit Class

The VentilationUnit class provides a convenient interface for managing units:

```python
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
```

## Constants and Enumerations

The library provides several constants and enumerations to make working with the API easier:

```python
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
```

## Security

To keep your credentials secure, use environment variables rather than hardcoding them:

```python
# .env file
EMAIL=your.email@example.com
PASSWORD=your_password
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
```

## Testing

The project includes a comprehensive test suite with over 85% code coverage. To run the tests:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage report
pytest --cov=systemair_api --cov-report=term --cov-report=html

# The coverage report will be available in htmlcov/index.html

# Run a specific test file
pytest tests/test_ventilation_unit.py

# Run tests with verbose output
pytest -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your new features or fixes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This library is not officially affiliated with, authorized, maintained, sponsored or endorsed by Systemair or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.