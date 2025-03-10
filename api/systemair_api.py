import requests
from utils.constants import REMOTE_API_URL, GATEWAY_API_URL

class SystemairAPI:
    def __init__(self, access_token):
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
        data = {
            "variables": {"deviceIds": device_ids},
            "query": """
            query ($deviceIds: [String]!) {
                BroadcastDeviceStatuses(deviceIds: $deviceIds)
            }
            """
        }

        try:
            response = requests.post(GATEWAY_API_URL, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while broadcasting device statuses: {e}")
            return None

    def fetch_device_status(self, device_id):
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
            response = requests.post(REMOTE_API_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching device status: {e}")
            return None

    def get_account_devices(self):
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
            response = requests.post(GATEWAY_API_URL, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching account devices: {e}")
            return None


    def write_data_item(self, device_id, register_id, value):
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
            response = requests.post(REMOTE_API_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while writing data item: {e}")
            return None