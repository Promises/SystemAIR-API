#!/usr/bin/env python
"""Main entry point for the systemair_api package."""

import os
import time
import threading
from dotenv import load_dotenv

from systemair_api.auth.authenticator import SystemairAuthenticator
from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.api.websocket_client import SystemairWebSocket
from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.utils.constants import UserModes

def on_message(message: dict) -> None:
    """Handle incoming WebSocket messages.
    
    Args:
        message: The message received from the WebSocket
    """
    print("Received WebSocket message:", message)

def main() -> None:
    """Run the example application demonstrating the SystemAIR API."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Get credentials from environment variables
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    if not email or not password:
        print("Please set EMAIL and PASSWORD environment variables")
        print("You can create a .env file with these variables")
        return
    
    # Authenticate
    authenticator = SystemairAuthenticator(email, password)
    access_token = authenticator.authenticate()
    
    if not access_token:
        print("Authentication failed")
        return
    
    print("Authentication successful, access token obtained")
    
    # Create API client
    api = SystemairAPI(access_token)
    
    # Get account devices
    devices_response = api.get_account_devices()
    if not devices_response or "data" not in devices_response:
        print("Failed to get devices")
        return
    
    devices = devices_response["data"]["GetAccountDevices"]
    if not devices:
        print("No devices found")
        return
    
    print(f"Found {len(devices)} devices:")
    ventilation_units = []
    
    for device in devices:
        print(f" - {device['name']} (ID: {device['identifier']})")
        ventilation_unit = VentilationUnit(device['identifier'], device['name'])
        ventilation_units.append(ventilation_unit)
    
    # Set up WebSocket client
    ws_client = SystemairWebSocket(access_token, on_message)
    ws_client.connect()
    
    try:
        # Get status for the first device
        if ventilation_units:
            unit = ventilation_units[0]
            
            # Get device status
            status_response = api.fetch_device_status(unit.identifier)
            if status_response:
                unit.update_from_api(status_response)
                print(f"\nCurrent Status for {unit.name}:")
                unit.print_status()
                
                # Broadcast to get updates via WebSocket
                api.broadcast_device_statuses([unit.identifier])
                
                # Example: Change user mode to Away
                print("\nChanging user mode to Away...")
                unit.set_user_mode(api, UserModes.AWAY)
                
                # Wait for a moment to receive WebSocket updates
                time.sleep(5)
                
                # Change user mode back to Auto
                print("\nChanging user mode back to Auto...")
                unit.set_user_mode(api, UserModes.AUTO)
                
                # Get updated status
                status_response = api.fetch_device_status(unit.identifier)
                if status_response:
                    unit.update_from_api(status_response)
                    print("\nUpdated Status:")
                    unit.print_status()
        
        # Keep the main thread alive for WebSocket messages
        print("\nListening for WebSocket messages. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Disconnect WebSocket
        ws_client.disconnect()

if __name__ == "__main__":
    main()