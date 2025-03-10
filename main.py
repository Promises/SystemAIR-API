import os
import time
from auth.authenticator import SystemairAuthenticator
from api.systemair_api import SystemairAPI
from api.websocket_client import SystemairWebSocket
from models.ventilation_unit import VentilationUnit
from utils.constants import USER_MODE_ENUM
from utils.register_constants import RegisterConstants

from dotenv import load_dotenv

# def on_websocket_message(data):
#     if data["type"] == "SYSTEM_EVENT" and data["action"] == "DEVICE_STATUS_UPDATE":
#         properties = data["properties"]
#         print(f"\n{datetime.now()} - WebSocket Update:")
#         print(f"User Mode: {USER_MODES.get(properties['userMode'], {}).get('name', 'Unknown')} ({properties['userMode']})")
#         print(f"Airflow: {AIRFLOW_LEVELS.get(properties['airflow'], 'Unknown')} ({properties['airflow']})")
#         print(f"Temperature: {properties['temperature']}°C")
#         print(f"Supply Air Temperature: {properties['temperatures']['sat']}°C")
#         print(f"Outdoor Air Temperature: {properties['temperatures']['oat']}°C")
#         print(f"Setpoint: {properties['temperatures']['setpoint']}°C")
#         print(f"Humidity: {properties['humidity']}%")
#         print(f"Air Quality: {properties['airQuality']}")
#         print(f"Filter Expiration: {properties['filterExpiration']} seconds")

load_dotenv()
ventilation_units = {}


def get_user_devices(api):
    response = api.get_account_devices()
    if response and 'data' in response:
        devices = response['data'].get('GetAccountDevices', [])
        for device in devices:
            unit = VentilationUnit(device["identifier"], device["name"])
            ventilation_units[unit.identifier] = unit
    else:
        print("Failed to fetch user devices")


def on_websocket_message(data):
    if data["type"] == "SYSTEM_EVENT" and data["action"] == "DEVICE_STATUS_UPDATE":
        device_id = data["properties"]["id"]
        if device_id in ventilation_units:
            ventilation_units[device_id].update_from_websocket(data)
            ventilation_units[device_id].print_status()


def main():
    # Replace with your actual email and password
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')


    if not email or not password:
        print("Error: Email or password not found in environment variables")
        return

    authenticator = SystemairAuthenticator(email, password)
    api = None
    websocket_client = None

    try:
        # Initial authentication
        print("Authenticating...")
        access_token = authenticator.authenticate()
        api = SystemairAPI(access_token)

        get_user_devices(api)
        if not ventilation_units:
            print("No devices found. Exiting.")
            return

        websocket_client = SystemairWebSocket(access_token, on_websocket_message)
        websocket_client.connect()
        device_ids = list(ventilation_units.keys())

        # Broadcast device statuses
        broadcast_result = api.broadcast_device_statuses(device_ids)
        # print(f"\n{datetime.now()} - Broadcast Device Statuses Result:")
        # print(broadcast_result)
        print("Fetching initial status for all devices...")
        for device_id, unit in ventilation_units.items():
            try:
                device_status = api.fetch_device_status(device_id)
                if device_status:
                    unit.update_from_api(device_status)
                    unit.print_status()
                else:
                    print(f"Failed to fetch device status for {unit.name}")
            except Exception as e:
                print(f"Error fetching device status for {unit.name}: {e}")
        loops = 0

        while True:
            print(f"\nCurrent token expiry: {authenticator.token_expiry}")

            # Check if token is still valid
            if not authenticator.is_token_valid():
                print("Token expired. Refreshing...")
                try:
                    access_token = authenticator.refresh_access_token()
                    print(f"Token refreshed. New expiry: {authenticator.token_expiry}")
                    api = SystemairAPI(access_token)
                    websocket_client.disconnect()
                    websocket_client = SystemairWebSocket(access_token, on_websocket_message)
                    websocket_client.connect()
                except Exception as e:
                    print(f"Failed to refresh token: {e}")
                    print("Re-authenticating...")
                    access_token = authenticator.authenticate()
                    api = SystemairAPI(access_token)
                    websocket_client.disconnect()
                    websocket_client = SystemairWebSocket(access_token, on_websocket_message)
                    websocket_client.connect()
                broadcast_result = api.broadcast_device_statuses(device_ids)

            # Fetch updated status for all devices
            print("\nRefreshing device statuses...")
            for device_id, unit in ventilation_units.items():
                try:
                    device_status = api.fetch_device_status(device_id)
                    if device_status:
                        unit.update_from_api(device_status)
                        unit.print_status()
                    else:
                        print(f"Failed to fetch device status for {unit.name}")
                except Exception as e:
                    print(f"Error fetching device status for {unit.name}: {e}")

            # Wait before next refresh
            print(f"\nWaiting 60 seconds before next refresh...")
            time.sleep(60)


    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if websocket_client:
            websocket_client.disconnect()


if __name__ == "__main__":
    main()
