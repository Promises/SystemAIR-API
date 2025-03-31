"""Ventilation unit model."""

from datetime import datetime

from systemair_api.models.ventilation_data import USER_MODES
from systemair_api.utils.constants import UserModes
from systemair_api.utils.register_constants import RegisterConstants


class VentilationUnit:
    """Model representing a Systemair ventilation unit."""
    
    def __init__(self, identifier, name):
        """Initialize a ventilation unit with a unique identifier and name."""
        self.identifier = identifier
        self.name = name
        self.model = None
        self.active_alarms = False
        self.airflow = None
        self.connectivity = []
        self.filter_expiration = None
        self.serial_number = None
        self.temperature = None
        self.user_mode = None
        self.air_quality = None
        self.humidity = None
        self.co2 = None
        self.update_in_progress = False
        self.configuration_wizard_active = False
        self.user_mode_remaining_time = None
        self.temperatures = {
            "oat": None,  # Outdoor Air Temperature
            "sat": None,  # Supply Air Temperature
            "setpoint": None
        }
        self.versions = []

        # Attributes from API data
        self.eco_mode = None
        self.locked_user = None
        self.alarm_type_a = None
        self.alarm_type_b = None
        self.alarm_type_c = None
        self.suw_required = None
        self.reheater_type = None
        self.active_functions = {
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

    def update_from_api(self, api_data):
        """Update the ventilation unit with data from the API."""
        if 'data' in api_data and 'GetView' in api_data['data']:
            children = api_data['data']['GetView']['children']
            for child in children:
                if 'properties' in child and 'dataItem' in child['properties']:
                    data_item = child['properties']['dataItem']
                    self._update_attribute(data_item)

    def _update_attribute(self, data_item):
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

    def update_from_websocket(self, ws_data):
        """Update the ventilation unit with data from a WebSocket message."""
        properties = ws_data.get("properties", {})

        # Update basic properties
        self.model = properties.get("model", self.model)
        self.active_alarms = properties.get("activeAlarms", self.active_alarms)
        self.airflow = properties.get("airflow", self.airflow)
        self.connectivity = properties.get("connectivity", self.connectivity)
        self.filter_expiration = properties.get("filterExpiration", self.filter_expiration)
        self.serial_number = properties.get("serialNumber", self.serial_number)
        self.temperature = properties.get("temperature", self.temperature)
        self.user_mode = properties.get("userMode", self.user_mode)
        self.air_quality = properties.get("airQuality", self.air_quality)
        self.humidity = properties.get("humidity", self.humidity)
        self.co2 = properties.get("co2", self.co2)

        # Update nested properties
        update_info = properties.get("update", {})
        self.update_in_progress = update_info.get("inProgress", self.update_in_progress)

        config_wizard = properties.get("configurationWizard", {})
        self.configuration_wizard_active = config_wizard.get("active", self.configuration_wizard_active)

        temperatures = properties.get("temperatures", {})
        self.temperatures.update(temperatures)

        versions = properties.get("versions", [])
        if versions:
            self.versions = versions

    def __str__(self):
        """String representation of the ventilation unit."""
        return f"VentilationUnit: {self.name} (ID: {self.identifier})"

    def get_status(self):
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
            "user_mode_remaining_time": self.user_mode_remaining_time
        }

    def print_status(self):
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

    def set_value(self, api, key: RegisterConstants, value, noprint = False):
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
        else:
            return result and result.get('data', {}).get('WriteDataItems')

    def set_user_mode(self, api, mode_value):
        """Set the user mode for the ventilation unit.
        
        Args:
            api: The SystemairAPI instance to use for communication
            mode_value: The mode value to set (use UserModes enum)
            
        Returns:
            None
        """
        if self.set_value(api, RegisterConstants.REG_MAINBOARD_USERMODE_HMI_CHANGE_REQUEST, mode_value + 1, True):
            # self.user_mode = mode_value
            print(f"User mode set to {USER_MODES.get(mode_value).get('name')} for {self.name}")
        else:
            print(f"Failed to set user mode for {self.name}")
