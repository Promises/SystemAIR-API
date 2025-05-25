"""Ventilation unit model."""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple, Set, cast

from systemair_api.models.ventilation_data import USER_MODES, VentilationData
from systemair_api.utils.constants import UserModes
from systemair_api.utils.register_constants import RegisterConstants
from systemair_api.api.systemair_api import SystemairAPI


class VentilationUnit:
    """Model representing a Systemair ventilation unit."""
    
    def __init__(self, identifier: str, name: str) -> None:
        """Initialize a ventilation unit with a unique identifier and name."""
        self.identifier: str = identifier
        self.name: str = name
        self.model: Optional[str] = None
        self.active_alarms: bool = False
        self.airflow: Optional[int] = None
        self.connectivity: List[str] = []
        self.filter_expiration: Optional[int] = None
        self.serial_number: Optional[str] = None
        self.temperature: Optional[float] = None
        self.user_mode: Optional[int] = None
        self.air_quality: Optional[int] = None
        self.humidity: Optional[int] = None
        self.co2: Optional[int] = None
        self.update_in_progress: bool = False
        self.configuration_wizard_active: bool = False
        self.user_mode_remaining_time: Optional[int] = None
        self.user_mode_times: Dict[str, Optional[int]] = {
            "holiday": None,  # REG_MAINBOARD_USERMODE_HOLIDAY_TIME
            "away": None,     # REG_MAINBOARD_USERMODE_AWAY_TIME
            "fireplace": None, # REG_MAINBOARD_USERMODE_FIREPLACE_TIME
            "refresh": None,  # REG_MAINBOARD_USERMODE_REFRESH_TIME
            "crowded": None,  # REG_MAINBOARD_USERMODE_CROWDED_TIME
        }
        self.temperatures: Dict[str, Optional[float]] = {
            "oat": None,  # Outdoor Air Temperature
            "sat": None,  # Supply Air Temperature
            "setpoint": None
        }
        self.versions: List[Dict[str, str]] = []

        # Attributes from API data
        self.eco_mode: Optional[int] = None
        self.locked_user: Optional[int] = None
        self.alarm_type_a: Optional[int] = None
        self.alarm_type_b: Optional[int] = None
        self.alarm_type_c: Optional[int] = None
        self.suw_required: Optional[int] = None
        self.reheater_type: Optional[int] = None
        self.active_functions: Dict[str, bool] = {
            'cooling': False,
            'free_cooling': False,
            'heating': False,
            'defrosting': False,
            'heat_recovery': False,
            'cooling_recovery': False,
            'moisture_transfer': False,
            'secondary_air': False,
            'vacuum_cleaner': False,
            'cooker_hood': False,
            'user_lock': False,
            'eco_mode': False,
            'heater_cool_down': False,
            'pressure_guard': False,
            'cdi_1': False,
            'cdi_2': False,
            'cdi_3': False
        }

    def update_from_api(self, api_data: Dict[str, Any]) -> None:
        """Update the ventilation unit with data from the API."""
        if 'data' in api_data and 'GetView' in api_data['data']:
            children = api_data['data']['GetView']['children']
            for child in children:
                if 'properties' in child and 'dataItem' in child['properties']:
                    data_item = child['properties']['dataItem']
                    self._update_attribute(data_item)

    def _update_attribute(self, data_item: Dict[str, Any]) -> None:
        """Update a specific attribute based on register data."""
        register_id = data_item['id']
        value = data_item['value']

        if register_id == RegisterConstants.REG_MAINBOARD_USERMODE_MODE_HMI:
            self.user_mode = value
        elif register_id == RegisterConstants.REG_MAINBOARD_SPEED_INDICATION_APP:
            self.airflow = value
        elif register_id == RegisterConstants.REG_MAINBOARD_TC_SP:
            self.temperatures['setpoint'] = value / 10.0
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_REMAINING_TIME_L:
            self.user_mode_remaining_time = value
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_HOLIDAY_TIME:
            self.user_mode_times['holiday'] = value
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_AWAY_TIME:
            self.user_mode_times['away'] = value
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_FIREPLACE_TIME:
            self.user_mode_times['fireplace'] = value
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_REFRESH_TIME:
            self.user_mode_times['refresh'] = value
        elif register_id == RegisterConstants.REG_MAINBOARD_USERMODE_CROWDED_TIME:
            self.user_mode_times['crowded'] = value
        elif register_id == RegisterConstants.REG_MAINBOARD_IAQ_LEVEL:
            self.air_quality = value
        elif register_id == RegisterConstants.REG_MAINBOARD_SENSOR_OAT:
            self.temperatures['oat'] = value / 10.0
        elif register_id == RegisterConstants.REG_MAINBOARD_ECO_MODE_ON_OFF:
            self.eco_mode = value
        elif register_id == RegisterConstants.REG_MAINBOARD_LOCKED_USER:
            self.locked_user = value
        elif register_id == RegisterConstants.REG_MAINBOARD_ALARM_TYPE_A:
            self.alarm_type_a = value
        elif register_id == RegisterConstants.REG_MAINBOARD_ALARM_TYPE_B:
            self.alarm_type_b = value
        elif register_id == RegisterConstants.REG_MAINBOARD_ALARM_TYPE_C:
            self.alarm_type_c = value
        elif register_id == RegisterConstants.REG_MAINBOARD_SUW_REQUIRED:
            self.suw_required = value
        elif register_id == RegisterConstants.REG_MAINBOARD_UNIT_CONFIG_REHEATER_TYPE:
            self.reheater_type = value
        elif register_id in range(RegisterConstants.REG_MAINBOARD_FUNCTION_ACTIVE_COOLING,
                                  RegisterConstants.REG_MAINBOARD_FUNCTION_ACTIVE_CDI_3 + 1):
            function_name = RegisterConstants.get_register_name(register_id).split('_')[-1].lower()
            self.active_functions[function_name] = value

    def update_from_websocket(self, ws_data: Dict[str, Any]) -> None:
        """Update the ventilation unit with data from a WebSocket message."""
        properties = ws_data

        # Extract property data if it's nested in 'properties'
        if "properties" in ws_data:
            properties = ws_data.get("properties", {})

        # Update basic properties
        if "model" in properties:
            self.model = properties.get("model")
        if "activeAlarms" in properties:
            self.active_alarms = properties.get("activeAlarms")
        if "airflow" in properties:
            self.airflow = properties.get("airflow")
        if "connectivity" in properties:
            self.connectivity = properties.get("connectivity")
        if "filterExpiration" in properties:
            self.filter_expiration = properties.get("filterExpiration")
        if "serialNumber" in properties:
            self.serial_number = properties.get("serialNumber")
        if "temperature" in properties:
            self.temperature = properties.get("temperature")
        if "userMode" in properties:
            self.user_mode = properties.get("userMode")
        if "airQuality" in properties:
            self.air_quality = properties.get("airQuality")
        if "humidity" in properties:
            self.humidity = properties.get("humidity")
        if "co2" in properties:
            self.co2 = properties.get("co2")

        # Update nested properties
        update_info = properties.get("update", {})
        if update_info and "inProgress" in update_info:
            self.update_in_progress = update_info.get("inProgress")

        config_wizard = properties.get("configurationWizard", {})
        if config_wizard and "active" in config_wizard:
            self.configuration_wizard_active = config_wizard.get("active")

        # Update temperature data
        temps = properties.get("temperatures", {})
        if temps:
            # Only update specific temperature keys that exist
            for key, value in temps.items():
                if key in self.temperatures:
                    self.temperatures[key] = value

        # Update version data
        versions = properties.get("versions", [])
        if versions:
            self.versions = versions

    def __str__(self) -> str:
        """String representation of the ventilation unit."""
        return f"VentilationUnit: {self.name} (ID: {self.identifier})"

    @property
    def user_mode_name(self) -> str:
        """Get the name of the current user mode."""
        if self.user_mode is None:
            return "Unknown"
        return VentilationData.get_user_mode_name(self.user_mode)
        
    def get_fan_speed(self) -> int:
        """Get the fan speed as a percentage (0-100)."""
        return self.airflow or 0
        
    def get_filter_alarm(self) -> bool:
        """Check if there's a filter alarm active."""
        # Placeholder implementation - will need to be updated based on how filter alarms are detected
        return self.active_alarms
        
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the ventilation unit as a dictionary."""
        return {
            "name": self.name,
            "model": self.model,
            "active_alarms": self.active_alarms,
            "airflow": self.airflow,
            "connectivity": self.connectivity,
            "filter_expiration": self.filter_expiration,
            "serial_number": self.serial_number,
            "temperature": self.temperature,
            "user_mode": self.user_mode,
            "user_mode_name": self.user_mode_name,
            "air_quality": self.air_quality,
            "humidity": self.humidity,
            "co2": self.co2,
            "update_in_progress": self.update_in_progress,
            "configuration_wizard_active": self.configuration_wizard_active,
            "temperatures": self.temperatures,
            "versions": self.versions,
            "eco_mode": self.eco_mode,
            "locked_user": self.locked_user,
            "alarm_type_a": self.alarm_type_a,
            "alarm_type_b": self.alarm_type_b,
            "alarm_type_c": self.alarm_type_c,
            "suw_required": self.suw_required,
            "reheater_type": self.reheater_type,
            "active_functions": self.active_functions,
            "user_mode_remaining_time": self.user_mode_remaining_time,
            "user_mode_times": self.user_mode_times
        }

    def print_status(self) -> None:
        """Print the current status of the ventilation unit."""
        print(f"\n{datetime.now()} - Status for {self.name}:")
        status = self.get_status()
        for key, value in status.items():
            if key not in ["active_functions", "versions", "connectivity"]:
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("Temperatures:")
        for temp_key, temp_value in status["temperatures"].items():
            print(f"  - {temp_key.upper()}: {temp_value}")

        print("Versions:")
        for version in status["versions"]:
            print(f"  - {version['type'].upper()}: {version['version']}")

        print("Connectivity:", status["connectivity"])

        print("Active Functions:")
        for function, is_active in status["active_functions"].items():
            if is_active:
                print(f"  - {function.replace('_', ' ').title()}")

    def set_value(self, api: SystemairAPI, key: int, value: Union[int, float, str], noprint: bool = False) -> Optional[bool]:
        """Set a register value for the ventilation unit.
        
        Args:
            api: The SystemairAPI instance to use for communication
            key: The register key to set
            value: The value to set
            noprint: Whether to suppress print output
            
        Returns:
            bool: True if successful, False otherwise
        """
        result = api.write_data_item(
            self.identifier,
            key,
            value
        )
        if not noprint:
            if result and result.get('data', {}).get('WriteDataItems'):
                print(f"Value for {RegisterConstants.get_register_name_by_number(key)} set to {value}")
            else:
                print(f"Failed to set user mode for {self.name}")
            return None
        else:
            return bool(result and result.get('data', {}).get('WriteDataItems'))

    def set_user_mode(self, api: SystemairAPI, mode_value: int, time_minutes: Optional[int] = None) -> None:
        """Set the user mode for the ventilation unit.
        
        Args:
            api: The SystemairAPI instance to use for communication
            mode_value: The mode value to set (use UserModes enum)
            time_minutes: Optional time duration in minutes for timed modes
                (Refresh, Crowded, Fireplace, Away, Holiday)
            
        Returns:
            None
        """
        # Map mode values to their time registers and determine if we need to set time
        mode_to_time_register = {
            UserModes.HOLIDAY: RegisterConstants.REG_MAINBOARD_USERMODE_HOLIDAY_TIME,
            UserModes.AWAY: RegisterConstants.REG_MAINBOARD_USERMODE_AWAY_TIME,
            UserModes.FIREPLACE: RegisterConstants.REG_MAINBOARD_USERMODE_FIREPLACE_TIME,
            UserModes.REFRESH: RegisterConstants.REG_MAINBOARD_USERMODE_REFRESH_TIME,
            UserModes.CROWDED: RegisterConstants.REG_MAINBOARD_USERMODE_CROWDED_TIME,
        }
        
        # Set the time value first if provided and this is a timed mode
        time_register = mode_to_time_register.get(mode_value)
        if time_minutes is not None and time_register is not None:
            # Convert minutes to the units expected by each specific register
            api_time_value = self._convert_minutes_to_api_units(mode_value, time_minutes)
            self.set_value(api, time_register, api_time_value, True)
            # Update local cache (keep in minutes for internal use)
            mode_key = self.get_mode_name_for_key(mode_value)
            if mode_key and hasattr(self, "user_mode_times") and mode_key in self.user_mode_times:
                self.user_mode_times[mode_key] = time_minutes
        
        # Then set the mode
        if self.set_value(api, RegisterConstants.REG_MAINBOARD_USERMODE_HMI_CHANGE_REQUEST, mode_value + 1, True):
            # self.user_mode = mode_value
            print(f"User mode set to {USER_MODES.get(mode_value, {}).get('name', 'Unknown')} for {self.name}")
        else:
            print(f"Failed to set user mode for {self.name}")

    def _convert_minutes_to_api_units(self, mode_value: int, time_minutes: int) -> int:
        """Convert time in minutes to the units expected by the API for each mode.
        
        API expects:
        - HOLIDAY: days (REG_MAINBOARD_USERMODE_HOLIDAY_TIME = 251)
        - AWAY: hours (REG_MAINBOARD_USERMODE_AWAY_TIME = 252) 
        - FIREPLACE: minutes (REG_MAINBOARD_USERMODE_FIREPLACE_TIME = 253)
        - REFRESH: minutes (REG_MAINBOARD_USERMODE_REFRESH_TIME = 254)
        - CROWDED: hours (REG_MAINBOARD_USERMODE_CROWDED_TIME = 255)
        """
        if mode_value == UserModes.HOLIDAY:
            return max(1, time_minutes // (24 * 60))  # Convert to days, minimum 1
        elif mode_value in [UserModes.AWAY, UserModes.CROWDED]:
            return max(1, time_minutes // 60)  # Convert to hours, minimum 1
        elif mode_value in [UserModes.FIREPLACE, UserModes.REFRESH]:
            return time_minutes  # Already in minutes
        else:
            return time_minutes  # Fallback
            
    def get_mode_name_for_key(self, mode_value: int) -> str:
        """Map numeric mode value to string mode key.
        
        Args:
            mode_value: The numeric mode value from UserModes enum
            
        Returns:
            str: The string key name (e.g., 'holiday', 'away', etc.)
        """
        mode_map = {
            UserModes.HOLIDAY: "holiday",
            UserModes.AWAY: "away",
            UserModes.FIREPLACE: "fireplace",
            UserModes.REFRESH: "refresh",
            UserModes.CROWDED: "crowded"
        }
        return mode_map.get(mode_value, "")
            
    def set_temperature(self, api: SystemairAPI, temperature: int) -> None:
        """Set the temperature setpoint for the ventilation unit.
        
        Args:
            api: The SystemairAPI instance to use for communication
            temperature: Temperature in tenths of degrees (e.g., 210 for 21.0°C)
            
        Returns:
            None
        """
        if self.set_value(api, RegisterConstants.REG_MAINBOARD_TC_SP, temperature, True):
            print(f"Temperature set to {temperature/10.0:.1f}°C for {self.name}")
        else:
            print(f"Failed to set temperature for {self.name}")
            
    def set_user_mode_time(self, api: SystemairAPI, mode: str, time_value: int) -> None:
        """Set the time duration for a specific user mode.
        
        Args:
            api: The SystemairAPI instance to use for communication
            mode: The mode to set time for ('holiday', 'away', 'fireplace', 'refresh', 'crowded')
            time_value: The time duration in minutes
            
        Returns:
            None
        """
        # Map mode names to their respective registers and mode values
        mode_info = {
            'holiday': (RegisterConstants.REG_MAINBOARD_USERMODE_HOLIDAY_TIME, UserModes.HOLIDAY),
            'away': (RegisterConstants.REG_MAINBOARD_USERMODE_AWAY_TIME, UserModes.AWAY),
            'fireplace': (RegisterConstants.REG_MAINBOARD_USERMODE_FIREPLACE_TIME, UserModes.FIREPLACE),
            'refresh': (RegisterConstants.REG_MAINBOARD_USERMODE_REFRESH_TIME, UserModes.REFRESH),
            'crowded': (RegisterConstants.REG_MAINBOARD_USERMODE_CROWDED_TIME, UserModes.CROWDED),
        }
        
        if mode not in mode_info:
            print(f"Invalid mode: {mode}. Must be one of {list(mode_info.keys())}")
            return
            
        register, mode_value = mode_info[mode]
        
        # Convert minutes to the units expected by the API for this specific mode
        api_time_value = self._convert_minutes_to_api_units(mode_value, time_value)
        
        if self.set_value(api, register, api_time_value, True):
            # Show the user-friendly units in the message
            unit_name = "days" if mode == 'holiday' else ("hours" if mode in ['away', 'crowded'] else "minutes")
            print(f"{mode.capitalize()} mode time set to {api_time_value} {unit_name} for {self.name}")
            # Update our local cache (keep in minutes for internal consistency)
            self.user_mode_times[mode] = time_value
        else:
            print(f"Failed to set {mode} mode time for {self.name}")
