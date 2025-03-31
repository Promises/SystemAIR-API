"""SystemairAPI - Core API communication module for Systemair ventilation units."""

import requests
from systemair_api.utils.constants import APIEndpoints

class SystemairAPI:
    """Core API interface for communicating with Systemair Home Solutions API.
    
    Provides methods for discovering devices, fetching device status,
    and sending control commands to ventilation units.
    """
    
    def __init__(self, access_token):
        """Initialize the SystemairAPI with an access token.
        
        Args:
            access_token: A valid JWT access token from authentication
        """
        self.access_token = access_token
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://homesolutions.systemair.com/device/home',
            'content-type': 'application/json',
            'x-access-token': self.access_token,
            'Origin': 'https://homesolutions.systemair.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

    def broadcast_device_statuses(self, device_ids):
        """Broadcast requests for device statuses to trigger WebSocket updates.
        
        Args:
            device_ids: List of device identifiers to request updates for
            
        Returns:
            dict: API response or None if error occurred
        """
        data = {
            "variables": {"deviceIds": device_ids},
            "query": """
            query ($deviceIds: [String]!) {
                BroadcastDeviceStatuses(deviceIds: $deviceIds)
            }
            """
        }

        try:
            response = requests.post(APIEndpoints.GATEWAY, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while broadcasting device statuses: {e}")
            return None

    def fetch_device_status(self, device_id):
        """Fetch detailed status for a specific device.
        
        Args:
            device_id: The unique identifier of the device
            
        Returns:
            dict: API response with detailed device status or None if error occurred
        """
        headers = self.headers.copy()
        headers['device-id'] = device_id
        headers['device-type'] = 'LEGACY'

        data = {
            "variables": {"input": {"route": "/home", "viewId": ""}},
            "query": """
            query ($input: GetViewInputType!) {
                GetView(input: $input) {
                    children {
                        type
                        properties
                    }
                }
            }
            """
        }

        try:
            response = requests.post(APIEndpoints.REMOTE, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching device status: {e}")
            return None

    def get_account_devices(self):
        """Get all devices associated with the current account.
        
        Returns:
            dict: API response with devices list or None if error occurred
        """
        data = {
            "operationName": "GetLoggedInAccount",
            "variables": {},
            "query": """
            query GetLoggedInAccount {
              GetAccountDevices {
                identifier
                name
                street
                zipcode
                city
                country
                deviceType {
                  entry
                  module
                  scope
                  type
                }
              }
            }
            """
        }

        try:
            response = requests.post(APIEndpoints.GATEWAY, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching account devices: {e}")
            return None


    def write_data_item(self, device_id, register_id, value):
        """Write a value to a specific register on a device.
        
        Args:
            device_id: The unique identifier of the device
            register_id: The register ID to write to
            value: The value to write
            
        Returns:
            dict: API response indicating success or None if error occurred
        """
        headers = self.headers.copy()
        headers['device-id'] = device_id
        headers['device-type'] = 'LEGACY'

        data = {
            "variables": {
                "input": {
                    "dataPoints": [{"id": register_id, "value": str(value)}]
                }
            },
            "query": """
            mutation ($input: WriteDataItemsInput!) {
                WriteDataItems(input: $input)
            }
            """
        }

        try:
            response = requests.post(APIEndpoints.REMOTE, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while writing data item: {e}")
            return None