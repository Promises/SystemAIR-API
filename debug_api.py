#!/usr/bin/env python3
"""
Debug script for testing SystemAIR-API connection and data retrieval.

This standalone script helps diagnose connection issues by:
- Authenticating with the Systemair Home Solutions API
- Retrieving account devices
- Fetching device status data
- Creating VentilationUnit objects and printing their status

Usage:
    python debug_api.py

The script requires credentials in environment variables:
- EMAIL: Your Systemair account email
- PASSWORD: Your Systemair account password

Or you can use a .env file in the same directory.
"""

import os
import sys
import logging
import json
import traceback
from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
script_dir = Path(__file__).parent.absolute()
log_file = script_dir / "systemair_debug.log"
print(f"Attempting to write log file to: {log_file}")
print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")

# Check if we can write to the directory
try:
    test_file = script_dir / "test_write_permission.tmp"
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print(f"Directory is writable: {script_dir}")
except Exception as e:
    print(f"Directory is NOT writable: {script_dir}, Error: {str(e)}")

try:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(log_file), mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    print(f"Log file created successfully at: {log_file}")
except Exception as e:
    print(f"ERROR creating log file: {str(e)}")
    # Fallback to console-only logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger('SystemairDebug')

# Import the SystemAIR-API modules
from systemair_api.auth.authenticator import SystemairAuthenticator
from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.utils.exceptions import AuthenticationError, APIError, DeviceNotFoundError

def main():
    """Main function to test API connection and data retrieval."""
    # Direct output to both stdout and file
    log_file = open("debug_api.log", "w")
    
    def log(message):
        """Log to both stdout and file."""
        print(message)
        log_file.write(message + "\n")
        log_file.flush()  # Force writing to file
    
    log("Starting SystemAIR API debug script...")
    logger.info("Starting debug script")
    
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get credentials
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')
        
        if not email or not password:
            log("ERROR: Email or password not found in environment variables.")
            log("Please create a .env file with EMAIL and PASSWORD variables.")
            logger.error("Missing EMAIL or PASSWORD environment variables")
            return False
        
        log("Using email: " + email)
        
        try:
            # Step 1: Authenticate
            log("\n--- AUTHENTICATION ---")
            logger.info("Authenticating with Systemair API")
            auth = SystemairAuthenticator(email, password)
            access_token = auth.authenticate()
            logger.info(f"Authentication successful, token expires: {auth.token_expiry}")
            log("Authentication successful!")
            log(f"Token expires: {auth.token_expiry}")
            
            # Step 2: Create API client
            log("\n--- API CLIENT ---")
            logger.info("Creating API client")
            api = SystemairAPI(access_token)
            
            # Step 3: Get account devices
            log("\n--- FETCHING DEVICES ---")
            logger.info("Fetching account devices")
            devices_data = api.get_account_devices()
            
            # Log raw API response
            logger.debug(f"Raw API response: {json.dumps(devices_data, indent=2)}")
            
            # Check response structure
            if 'data' not in devices_data or 'GetAccountDevices' not in devices_data['data']:
                log("ERROR: Unexpected API response structure")
                logger.error("Unexpected API response structure")
                log(f"Response: {devices_data}")
                return False
            
            # Get devices
            devices = devices_data['data']['GetAccountDevices']
            device_count = len(devices)
            logger.info(f"Found {device_count} devices")
            log(f"Found {device_count} devices")
            
            if device_count == 0:
                log("WARNING: No devices found in account")
                logger.warning("No devices found in account")
                return False
            
            # Step 4: Process each device
            for i, device in enumerate(devices, 1):
                device_id = device['identifier']
                device_name = device['name']
                
                log(f"\n--- DEVICE {i}/{device_count}: {device_name} (ID: {device_id}) ---")
                logger.info(f"Processing device: {device_name} (ID: {device_id})")
                
                try:
                    # Fetch device status
                    log("Fetching device status...")
                    logger.info(f"Fetching status for device: {device_id}")
                    status_data = api.fetch_device_status(device_id)
                    
                    # Log raw status data
                    logger.debug(f"Raw device status: {json.dumps(status_data, indent=2)}")
                    
                    # Check response structure
                    if 'data' not in status_data or 'GetView' not in status_data['data']:
                        log(f"ERROR: Unexpected status response structure for device {device_id}")
                        logger.error(f"Unexpected status response structure for device {device_id}")
                        continue
                    
                    # Count data items
                    children = status_data['data']['GetView']['children']
                    data_items = [
                        child['properties']['dataItem'] 
                        for child in children 
                        if 'properties' in child and 'dataItem' in child['properties']
                    ]
                    logger.info(f"Found {len(data_items)} data items for device {device_id}")
                    log(f"Found {len(data_items)} data registers in device response")
                    
                    # Sample of data items (first 5)
                    if data_items:
                        logger.info("Sample data items:")
                        log("\nSample data registers:")
                        for item in data_items[:5]:
                            register_id = item['id']
                            value = item['value']
                            logger.info(f"  Register ID: {register_id}, Value: {value}")
                            log(f"  Register ID: {register_id}, Value: {value}")
                    
                    # Create ventilation unit
                    unit = VentilationUnit(device_id, device_name)
                    unit.update_from_api(status_data)
                    
                    # Print unit status
                    log("\nVentilation Unit Status:")
                    unit.print_status()
                    
                    logger.info(f"Successfully processed device {device_id}")
                    
                except DeviceNotFoundError as e:
                    log(f"ERROR: Device not found: {str(e)}")
                    logger.error(f"Device not found: {str(e)}")
                except APIError as e:
                    log(f"ERROR: API error: {str(e)}")
                    logger.error(f"API error: {str(e)}")
                except Exception as e:
                    log(f"ERROR: Unexpected error: {str(e)}")
                    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                    traceback.print_exc(file=log_file)
            
            # Test broadcasting device statuses
            log("\n--- BROADCASTING DEVICE STATUSES ---")
            logger.info("Testing broadcast device statuses")
            device_ids = [device['identifier'] for device in devices]
            log(f"Broadcasting status request for {len(device_ids)} devices...")
            broadcast_result = api.broadcast_device_statuses(device_ids)
            logger.debug(f"Broadcast result: {broadcast_result}")
            
            if broadcast_result and broadcast_result.get('data', {}).get('BroadcastDeviceStatuses') is True:
                log("Broadcast successful!")
            else:
                log("Broadcast response: " + str(broadcast_result))
            
            log("\nTest completed successfully!")
            logger.info("Debug script completed successfully")
            return True
            
        except AuthenticationError as e:
            log(f"ERROR: Authentication failed: {str(e)}")
            logger.error(f"Authentication failed: {str(e)}")
        except APIError as e:
            log(f"ERROR: API error: {str(e)}")
            logger.error(f"API error: {str(e)}")
        except Exception as e:
            log(f"ERROR: Unexpected error: {str(e)}")
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            traceback.print_exc(file=log_file)
    
    except Exception as e:
        log(f"CRITICAL ERROR: {str(e)}")
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        traceback.print_exc(file=log_file)
    
    finally:
        log_file.close()
        log("Log files written to debug_api.log and systemair_debug.log")
        
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)