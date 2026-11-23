import pytest
from unittest.mock import patch, Mock

from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.utils.constants import UserModes
from systemair_api.utils.register_constants import RegisterConstants


class TestVentilationUnit:
    @pytest.fixture
    def ventilation_unit(self):
        """Create a test ventilation unit"""
        return VentilationUnit("IAM_123456789ABC", "Test Unit")

    def test_initialization(self, ventilation_unit):
        """Test that ventilation unit is initialized correctly"""
        assert ventilation_unit.identifier == "IAM_123456789ABC"
        assert ventilation_unit.name == "Test Unit"
        assert ventilation_unit.model is None
        assert ventilation_unit.active_alarms is False
        assert ventilation_unit.airflow is None
        assert ventilation_unit.temperature is None
        assert ventilation_unit.user_mode is None
        assert ventilation_unit.temperatures == {"oat": None, "sat": None, "eat": None, "setpoint": None}
        assert len(ventilation_unit.active_functions) > 0
        for function, state in ventilation_unit.active_functions.items():
            assert state is False

    def test_update_from_api(self, ventilation_unit, mock_device_status_response):
        """Test updating unit from API response"""
        # Call the method
        ventilation_unit.update_from_api(mock_device_status_response.json())
        
        # Assertions
        assert ventilation_unit.user_mode == 1  # MANUAL mode
        assert ventilation_unit.airflow == 3  # Normal airflow
        assert ventilation_unit.temperatures["setpoint"] == 21.0  # 21.0°C
        assert ventilation_unit.temperatures["oat"] == 15.0  # 15.0°C

    def test_update_from_websocket(self, ventilation_unit, mock_websocket_data):
        """Test updating unit from WebSocket message"""
        # Call the method
        ventilation_unit.update_from_websocket(mock_websocket_data)
        
        # Assertions
        assert ventilation_unit.model == "Test Model"
        assert ventilation_unit.active_alarms is False
        assert ventilation_unit.airflow == 3
        assert ventilation_unit.connectivity == ["online", "cloud"]
        assert ventilation_unit.filter_expiration == 2592000
        assert ventilation_unit.serial_number == "SN12345"
        assert ventilation_unit.temperature == 22.5
        assert ventilation_unit.user_mode == 1
        assert ventilation_unit.air_quality == 90
        assert ventilation_unit.humidity == 45
        assert ventilation_unit.co2 == 650
        assert ventilation_unit.update_in_progress is False
        assert ventilation_unit.configuration_wizard_active is False
        assert ventilation_unit.temperatures["oat"] == 15.0
        assert ventilation_unit.temperatures["sat"] == 19.5
        assert ventilation_unit.temperatures["setpoint"] == 21.0
        assert len(ventilation_unit.versions) == 2
        assert ventilation_unit.versions[0]["type"] == "hardware"
        assert ventilation_unit.versions[0]["version"] == "2.0"

    def test_get_status(self, ventilation_unit):
        """Test getting unit status as dictionary"""
        # Setup - add some test data to the unit
        ventilation_unit.user_mode = 1
        ventilation_unit.airflow = 3
        ventilation_unit.temperature = 22.5
        ventilation_unit.temperatures["setpoint"] = 21.0
        
        # Call the method
        status = ventilation_unit.get_status()
        
        # Assertions
        assert status["name"] == "Test Unit"
        assert status["user_mode"] == 1
        assert status["airflow"] == 3
        assert status["temperature"] == 22.5
        assert status["temperatures"]["setpoint"] == 21.0
        assert "active_functions" in status
        assert "versions" in status

    @patch('builtins.print')
    def test_print_status(self, mock_print, ventilation_unit):
        """Test printing unit status"""
        # Setup - add some test data to the unit
        ventilation_unit.user_mode = 1
        ventilation_unit.airflow = 3
        ventilation_unit.temperature = 22.5
        ventilation_unit.temperatures["setpoint"] = 21.0
        ventilation_unit.temperatures["oat"] = 15.0
        ventilation_unit.active_functions["heating"] = True
        ventilation_unit.versions = [
            {"type": "hardware", "version": "2.0"},
            {"type": "firmware", "version": "1.5.2"}
        ]
        
        # Call the method
        ventilation_unit.print_status()
        
        # Assertions - verify print was called multiple times
        assert mock_print.call_count > 5

    @patch('systemair_api.api.systemair_api.SystemairAPI.write_data_item')
    def test_set_value(self, mock_write_data_item, ventilation_unit):
        """Test setting a register value"""
        # Setup
        mock_api = Mock()
        mock_write_data_item.return_value = {"data": {"WriteDataItems": True}}
        mock_api.write_data_item = mock_write_data_item
        
        # Call the method
        register_id = RegisterConstants.REG_MAINBOARD_TC_SP
        value = 220  # 22.0°C
        result = ventilation_unit.set_value(mock_api, register_id, value, True)
        
        # Assertions
        assert result is True
        mock_write_data_item.assert_called_once_with(
            ventilation_unit.identifier, register_id, value
        )

    @patch('systemair_api.api.systemair_api.SystemairAPI.write_data_item')
    def test_set_value_failure(self, mock_write_data_item, ventilation_unit):
        """Test handling failure when setting a register value"""
        # Setup
        mock_api = Mock()
        mock_write_data_item.return_value = {"data": {"WriteDataItems": False}}
        mock_api.write_data_item = mock_write_data_item
        
        # Call the method
        register_id = RegisterConstants.REG_MAINBOARD_TC_SP
        value = 220  # 22.0°C
        result = ventilation_unit.set_value(mock_api, register_id, value, True)
        
        # Assertions
        assert result is False
        mock_write_data_item.assert_called_once()

    @patch.object(VentilationUnit, 'set_value')
    def test_set_user_mode(self, mock_set_value, ventilation_unit):
        """Test setting user mode"""
        # Setup
        mock_api = Mock()
        mock_set_value.return_value = True
        
        # Call the method
        mode_value = UserModes.AWAY
        ventilation_unit.set_user_mode(mock_api, mode_value)
        
        # Assertions
        mock_set_value.assert_called_once_with(
            mock_api, 
            RegisterConstants.REG_MAINBOARD_USERMODE_HMI_CHANGE_REQUEST, 
            mode_value + 1,  # Note the +1 for API compatibility
            True
        )

    def test_update_attribute(self, ventilation_unit):
        """Test updating a specific attribute from a data item"""
        # Test user mode update
        ventilation_unit._update_attribute({"id": RegisterConstants.REG_MAINBOARD_USERMODE_MODE_HMI, "value": 2})
        assert ventilation_unit.user_mode == 2
        
        # Test airflow update
        ventilation_unit._update_attribute({"id": RegisterConstants.REG_MAINBOARD_SPEED_INDICATION_APP, "value": 4})
        assert ventilation_unit.airflow == 4
        
        # Test temperature setpoint update
        ventilation_unit._update_attribute({"id": RegisterConstants.REG_MAINBOARD_TC_SP, "value": 230})
        assert ventilation_unit.temperatures["setpoint"] == 23.0
        
        # Test outdoor temperature update
        ventilation_unit._update_attribute({"id": RegisterConstants.REG_MAINBOARD_SENSOR_OAT, "value": 100})
        assert ventilation_unit.temperatures["oat"] == 10.0
        
        # Test active function update
        ventilation_unit._update_attribute({"id": RegisterConstants.REG_MAINBOARD_FUNCTION_ACTIVE_HEATING, "value": 1})
        assert ventilation_unit.active_functions["heating"] == 1

    @staticmethod
    def _data_items(*items):
        """A fetch_data_items response, including the temperature-unit register
        (id 28) the cloud adds alongside temperature registers."""
        unit_register = {"id": 28, "type": 3, "value": 0}
        return {"data": {"GetDataItems": [unit_register, *[{"id": i, "type": 2, "value": v} for i, v in items]]}}

    def test_extract_temperature_from_humidity_board(self, ventilation_unit):
        """With the humidity sensor board fitted, its value wins over the unused sensor register"""
        ventilation_unit.update_from_data_items(self._data_items(
            (RegisterConstants.REG_MAINBOARD_SENSOR_EAT, 0),
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_CONFIGURED, True),
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_VALUE, 179),
        ))
        assert ventilation_unit.temperatures["eat"] == 17.9

    def test_extract_temperature_from_dedicated_sensor(self, ventilation_unit):
        """Without the humidity sensor board, the dedicated extract air sensor is used"""
        ventilation_unit.update_from_data_items(self._data_items(
            (RegisterConstants.REG_MAINBOARD_SENSOR_EAT, 238),
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_CONFIGURED, False),
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_VALUE, 0),
        ))
        assert ventilation_unit.temperatures["eat"] == 23.8

    def test_extract_temperature_independent_of_register_order(self, ventilation_unit):
        """The source choice holds whichever order the registers arrive in"""
        ventilation_unit.update_from_data_items(self._data_items(
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_VALUE, 179),
            (RegisterConstants.REG_MAINBOARD_SENSOR_EAT, 0),
            (RegisterConstants.REG_MAINBOARD_SENSOR_PDM_EAT_CONFIGURED, True),
        ))
        assert ventilation_unit.temperatures["eat"] == 17.9

    def test_extract_temperature_unknown_until_source_known(self, ventilation_unit):
        """A bare sensor reading is not reported until it is known which sensor is fitted"""
        ventilation_unit.update_from_data_items(self._data_items(
            (RegisterConstants.REG_MAINBOARD_SENSOR_EAT, 0),
        ))
        assert ventilation_unit.temperatures["eat"] is None

    def test_update_from_data_items_ignores_malformed_response(self, ventilation_unit):
        """An empty or error-shaped response changes nothing"""
        ventilation_unit.update_from_data_items({})
        ventilation_unit.update_from_data_items({"data": {"GetDataItems": None}})
        assert ventilation_unit.temperatures["eat"] is None

    def test_extract_air_registers(self):
        """The registers callers must fetch for the extract air temperature"""
        assert VentilationUnit.EXTRACT_AIR_REGISTERS == [57, 88, 89]
