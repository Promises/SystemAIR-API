"""Register constants for Systemair ventilation units."""

class RegisterConstants:
    """Register constants used for reading and writing data to ventilation units."""
    REG_IAM_HEARTBEAT = 0
    REG_IAM_UPTIME = 1
    REG_IAM_ACCESS_TOKEN = 2
    REG_IAM_CPU_IDENTIFIER = 3
    REG_IAM_PU_UPDATE_SOURCE = 4
    REG_IAM_UPDATE_PROCESS_STATE = 5
    REG_IAM_UPDATE_PROCESS_CURRENT_FILE_TRANSFER_PERCENTAGE = 6
    REG_IAM_UPDATE_PROCESS_CURRENT_FILE = 7
    REG_IAM_CFG_STORAGE_FILENAME_1 = 8
    REG_IAM_CFG_STORAGE_STATUS = 9
    REG_IAM_CFG_STORAGE_TRANSFER_STATE = 10
    REG_IAM_CFG_STORAGE_TRANSFER_PROGRESS = 11
    REG_IAM_CFG_STORAGE_TRANSFER_ERROR_CODE = 12
    REG_IAM_CFG_STORAGE_CTRL = 13
    REG_MAINBOARD_PASSWD_PC_UNLOCKED = 14
    REG_MAINBOARD_PASSWD_PC_SETTINGS = 15
    REG_MAINBOARD_FACTORY_RESET = 16
    REG_MAINBOARD_SET_USER_SAFE_CONFIG = 17
    REG_MAINBOARD_ACTIVATE_USER_SAFE_CONFIG = 18
    REG_MAINBOARD_USER_SAFE_CONFIG_VALID = 19
    REG_MAINBOARD_FILTER_PERIOD = 20
    REG_MAINBOARD_FILTER_PERIOD_SET = 21
    REG_MAINBOARD_FILTER_REMAINING_TIME_L = 22
    REG_MAINBOARD_FILTER_KIT_INDEX = 23
    REG_MAINBOARD_TIME_YEAR = 24
    REG_MAINBOARD_TIME_AUTO_SUM_WIN = 25
    REG_MAINBOARD_HOUR_FORMAT = 26
    REG_MAINBOARD_SYSTEM_UNIT_MODEL_TYPE = 27
    REG_MAINBOARD_SYSTEM_UNIT_TEMPERATURE = 28
    REG_MAINBOARD_USERMODE_MODE_HMI = 29 # Ventilation mode
    REG_MAINBOARD_USERMODE_HMI_CHANGE_REQUEST = 30 # Set ventilation mode ACTION
    REG_MAINBOARD_SPEED_INDICATION_APP = 31 # Air speed
    REG_MAINBOARD_TC_SP = 32 # Target setpoint supply air temp
    REG_MAINBOARD_IAQ_LEVEL = 33
    REG_MAINBOARD_ECO_MODE_ON_OFF = 34
    REG_MAINBOARD_LOCKED_USER = 35
    REG_MAINBOARD_LOCKED_FILTER = 36
    REG_MAINBOARD_LOCKED_WEEK_SCHEDULE = 37
    REG_MAINBOARD_USERMODE_MANUAL_AIRFLOW_LEVEL_SAF = 38
    REG_MAINBOARD_USERMODE_MANUAL_AIRFLOW_LEVEL_EAF = 39
    REG_MAINBOARD_FAN_MANUAL_STOP_ALLOWED = 40
    REG_MAINBOARD_SYSTEM_UNIT_MODEL1 = 41
    REG_MAINBOARD_SYSTEM_SERIAL_NUMBER1 = 42
    REG_MAINBOARD_SUW_REQUIRED = 43
    REG_MAINBOARD_FAN_REGULATION_UNIT = 44
    REG_MAINBOARD_SYSTEM_UNIT_FLOW = 45
    REG_MAINBOARD_SYSTEM_UNIT_PRESSURE = 46
    REG_MAINBOARD_FAN_REGULATION_PBAND = 47
    REG_MAINBOARD_FAN_REGULATION_ITIME = 48
    REG_MAINBOARD_K_FACTOR_SAF = 49
    REG_MAINBOARD_K_FACTOR_EAF = 50
    REG_MAINBOARD_WS_FAN_LEVEL_SCHEDULED = 51
    REG_MAINBOARD_WS_FAN_LEVEL_UNSCHEDULED = 52
    REG_MAINBOARD_SENSOR_SAT = 53
    REG_MAINBOARD_SENSOR_OAT = 54 # Sensor Outside air temp (Celsius * 10)
    REG_MAINBOARD_SENSOR_FPT = 55
    REG_MAINBOARD_SENSOR_RAT = 56
    REG_MAINBOARD_SENSOR_EAT = 57
    REG_MAINBOARD_SENSOR_ECT = 58
    REG_MAINBOARD_SENSOR_EFT = 59
    REG_MAINBOARD_SENSOR_OHT = 60
    REG_MAINBOARD_SENSOR_RHS = 61
    REG_MAINBOARD_SENSOR_BYS = 62
    REG_MAINBOARD_SENSOR_EMT = 63
    REG_MAINBOARD_SENSOR_RGS = 64
    REG_MAINBOARD_SENSOR_CO2S_1 = 65
    REG_MAINBOARD_SENSOR_CO2S_2 = 66
    REG_MAINBOARD_SENSOR_CO2S_3 = 67
    REG_MAINBOARD_SENSOR_CO2S_4 = 68
    REG_MAINBOARD_SENSOR_CO2S_5 = 69
    REG_MAINBOARD_SENSOR_CO2S_6 = 70
    REG_MAINBOARD_SENSOR_RHS_1 = 71
    REG_MAINBOARD_SENSOR_RHS_2 = 72
    REG_MAINBOARD_SENSOR_RHS_3 = 73
    REG_MAINBOARD_SENSOR_RHS_4 = 74
    REG_MAINBOARD_SENSOR_RHS_5 = 75
    REG_MAINBOARD_SENSOR_RHS_6 = 76
    REG_MAINBOARD_SENSOR_CO2S = 77
    REG_MAINBOARD_SENSOR_RHS_PDM = 78
    REG_MAINBOARD_SENSOR_P_SAF = 79
    REG_MAINBOARD_SENSOR_P_EAF = 80
    REG_MAINBOARD_SENSOR_FLOW_SAF = 81
    REG_MAINBOARD_SENSOR_FLOW_EAF = 82
    REG_MAINBOARD_SENSOR_RPM_SAF = 83
    REG_MAINBOARD_SENSOR_RPM_EAF = 84
    REG_MAINBOARD_SENSOR_FLOW_PIGGYBACK_SAF = 85
    REG_MAINBOARD_SENSOR_FLOW_PIGGYBACK_EAF = 86
    REG_MAINBOARD_SENSOR_DI_BYF = 87
    REG_MAINBOARD_SENSOR_PDM_EAT_CONFIGURED = 88
    REG_MAINBOARD_SENSOR_PDM_EAT_VALUE = 89
    REG_MAINBOARD_INPUT_EXTERNAL_CTRL_SAF = 90
    REG_MAINBOARD_INPUT_EXTERNAL_CTRL_EAF = 91
    REG_MAINBOARD_PDM_CONNECTED_RH = 92
    REG_MAINBOARD_PDM_CONNECTED_T = 93
    REG_MAINBOARD_PDM_CORRECTION_RH = 94
    REG_MAINBOARD_PDM_CORRECTION_T = 95
    REG_MAINBOARD_PIGGYBACK_1_PRESSURE_SAF = 96
    REG_MAINBOARD_PIGGYBACK_1_PRESSURE_EAF = 97
    REG_MAINBOARD_PIGGYBACK_1_SAF_COMPENSATION = 98
    REG_MAINBOARD_PIGGYBACK_1_EAF_COMPENSATION = 99
    REG_MAINBOARD_PIGGYBACK_1_MODE = 100
    REG_MAINBOARD_PIGGYBACK_2_MODE = 101
    REG_MAINBOARD_FUNCTION_ACTIVE_COOLING = 102
    REG_MAINBOARD_FUNCTION_ACTIVE_FREE_COOLING = 103
    REG_MAINBOARD_FUNCTION_ACTIVE_HEATING = 104
    REG_MAINBOARD_FUNCTION_ACTIVE_DEFROSTING = 105
    REG_MAINBOARD_FUNCTION_ACTIVE_HEAT_RECOVERY = 106
    REG_MAINBOARD_FUNCTION_ACTIVE_COOLING_RECOVERY = 107
    REG_MAINBOARD_FUNCTION_ACTIVE_MOISTURE_TRANSFER = 108
    REG_MAINBOARD_FUNCTION_ACTIVE_SECONDARY_AIR = 109
    REG_MAINBOARD_FUNCTION_ACTIVE_VACUUM_CLEANER = 110
    REG_MAINBOARD_FUNCTION_ACTIVE_COOKER_HOOD = 111
    REG_MAINBOARD_FUNCTION_ACTIVE_USER_LOCK = 112
    REG_MAINBOARD_FUNCTION_ACTIVE_ECO_MODE = 113
    REG_MAINBOARD_FUNCTION_ACTIVE_HEATER_COOL_DOWN = 114
    REG_MAINBOARD_FUNCTION_ACTIVE_PRESSURE_GUARD = 115
    REG_MAINBOARD_FUNCTION_ACTIVE_CDI_1 = 116
    REG_MAINBOARD_FUNCTION_ACTIVE_CDI_2 = 117
    REG_MAINBOARD_FUNCTION_ACTIVE_CDI_3 = 118
    REG_MAINBOARD_ALARM_TYPE_A = 119
    REG_MAINBOARD_ALARM_TYPE_B = 120
    REG_MAINBOARD_ALARM_TYPE_C = 121
    REG_MAINBOARD_ALARM_SAF_CTRL_ERROR = 122
    REG_MAINBOARD_ALARM_SAF_CTRL_ALARM = 123
    REG_MAINBOARD_ALARM_SAF_CTRL_CLEAR_ALARM = 124
    REG_MAINBOARD_ALARM_EAF_CTRL_ERROR = 125
    REG_MAINBOARD_ALARM_EAF_CTRL_ALARM = 126
    REG_MAINBOARD_ALARM_EAF_CTRL_CLEAR_ALARM = 127
    REG_MAINBOARD_ALARM_FROST_PROT_ERROR = 128
    REG_MAINBOARD_ALARM_FROST_PROT_ALARM = 129
    REG_MAINBOARD_ALARM_FROST_PROT_CLEAR_ALARM = 130
    REG_MAINBOARD_ALARM_DEFROSTING_ERROR = 131
    REG_MAINBOARD_ALARM_DEFROSTING_ALARM = 132
    REG_MAINBOARD_ALARM_DEFROSTING_CLEAR_ALARM = 133
    REG_MAINBOARD_ALARM_SAF_RPM_ERROR = 134
    REG_MAINBOARD_ALARM_SAF_RPM_ALARM = 135
    REG_MAINBOARD_ALARM_SAF_RPM_CLEAR_ALARM = 136
    REG_MAINBOARD_ALARM_EAF_RPM_ERROR = 137
    REG_MAINBOARD_ALARM_EAF_RPM_ALARM = 138
    REG_MAINBOARD_ALARM_EAF_RPM_CLEAR_ALARM = 139
    REG_MAINBOARD_ALARM_FPT_ERROR = 140
    REG_MAINBOARD_ALARM_FPT_ALARM = 141
    REG_MAINBOARD_ALARM_FPT_CLEAR_ALARM = 142
    REG_MAINBOARD_ALARM_OAT_ERROR = 143
    REG_MAINBOARD_ALARM_OAT_ALARM = 144
    REG_MAINBOARD_ALARM_OAT_CLEAR_ALARM = 145
    REG_MAINBOARD_ALARM_SAT_ERROR = 146
    REG_MAINBOARD_ALARM_SAT_ALARM = 147
    REG_MAINBOARD_ALARM_SAT_CLEAR_ALARM = 148
    REG_MAINBOARD_ALARM_RAT_ERROR = 149
    REG_MAINBOARD_ALARM_RAT_ALARM = 150
    REG_MAINBOARD_ALARM_RAT_CLEAR_ALARM = 151
    REG_MAINBOARD_ALARM_EAT_ERROR = 152
    REG_MAINBOARD_ALARM_EAT_ALARM = 153
    REG_MAINBOARD_ALARM_EAT_CLEAR_ALARM = 154
    REG_MAINBOARD_ALARM_ECT_ERROR = 155
    REG_MAINBOARD_ALARM_ECT_ALARM = 156
    REG_MAINBOARD_ALARM_ECT_CLEAR_ALARM = 157
    REG_MAINBOARD_ALARM_EFT_ERROR = 158
    REG_MAINBOARD_ALARM_EFT_ALARM = 159
    REG_MAINBOARD_ALARM_EFT_CLEAR_ALARM = 160
    REG_MAINBOARD_ALARM_OHT_ERROR = 161
    REG_MAINBOARD_ALARM_OHT_ALARM = 162
    REG_MAINBOARD_ALARM_OHT_CLEAR_ALARM = 163
    REG_MAINBOARD_ALARM_EMT_ERROR = 164
    REG_MAINBOARD_ALARM_EMT_ALARM = 165
    REG_MAINBOARD_ALARM_EMT_CLEAR_ALARM = 166
    REG_MAINBOARD_ALARM_RGS_ERROR = 167
    REG_MAINBOARD_ALARM_RGS_ALARM = 168
    REG_MAINBOARD_ALARM_RGS_CLEAR_ALARM = 169
    REG_MAINBOARD_ALARM_BYS_ERROR = 170
    REG_MAINBOARD_ALARM_BYS_ALARM = 171
    REG_MAINBOARD_ALARM_BYS_CLEAR_ALARM = 172
    REG_MAINBOARD_ALARM_SECONDARY_AIR_ERROR = 173
    REG_MAINBOARD_ALARM_SECONDARY_AIR_ALARM = 174
    REG_MAINBOARD_ALARM_SECONDARY_AIR_CLEAR_ALARM = 175
    REG_MAINBOARD_ALARM_FILTER_ERROR = 176
    REG_MAINBOARD_ALARM_FILTER_ALARM = 177
    REG_MAINBOARD_ALARM_FILTER_CLEAR_ALARM = 178
    REG_MAINBOARD_ALARM_EXTRA_CONTROLLER_ERROR = 179
    REG_MAINBOARD_ALARM_EXTRA_CONTROLLER_ALARM = 180
    REG_MAINBOARD_ALARM_EXTRA_CONTROLLER_CLEAR_ALARM = 181
    REG_MAINBOARD_ALARM_EXTERNAL_STOP_ERROR = 182
    REG_MAINBOARD_ALARM_EXTERNAL_STOP_ALARM = 183
    REG_MAINBOARD_ALARM_EXTERNAL_STOP_CLEAR_ALARM = 184
    REG_MAINBOARD_ALARM_MANUAL_OVERRIDE_OUTPUTS_ERROR = 185
    REG_MAINBOARD_ALARM_MANUAL_OVERRIDE_OUTPUTS_ALARM = 186
    REG_MAINBOARD_ALARM_MANUAL_OVERRIDE_OUTPUTS_CLEAR_ALARM = 187
    REG_MAINBOARD_ALARM_RH_ERROR = 188
    REG_MAINBOARD_ALARM_RH_ALARM = 189
    REG_MAINBOARD_ALARM_RH_CLEAR_ALARM = 190
    REG_MAINBOARD_ALARM_CO2_ERROR = 191
    REG_MAINBOARD_ALARM_CO2_ALARM = 192
    REG_MAINBOARD_ALARM_CO2_CLEAR_ALARM = 193
    REG_MAINBOARD_ALARM_LOW_SAT_ERROR = 194
    REG_MAINBOARD_ALARM_LOW_SAT_ALARM = 195
    REG_MAINBOARD_ALARM_LOW_SAT_CLEAR_ALARM = 196
    REG_MAINBOARD_ALARM_BYF_ERROR = 197
    REG_MAINBOARD_ALARM_BYF_ALARM = 198
    REG_MAINBOARD_ALARM_BYF_CLEAR_ALARM = 199
    REG_MAINBOARD_ALARM_PDM_RHS_ERROR = 200
    REG_MAINBOARD_ALARM_PDM_RHS_ALARM = 201
    REG_MAINBOARD_ALARM_PDM_RHS_CLEAR_ALARM = 202
    REG_MAINBOARD_ALARM_PDM_EAT_ERROR = 203
    REG_MAINBOARD_ALARM_PDM_EAT_ALARM = 204
    REG_MAINBOARD_ALARM_PDM_EAT_CLEAR_ALARM = 205
    REG_MAINBOARD_ALARM_MANUAL_FAN_STOP_ERROR = 206
    REG_MAINBOARD_ALARM_MANUAL_FAN_STOP_ALARM = 207
    REG_MAINBOARD_ALARM_MANUAL_FAN_STOP_CLEAR_ALARM = 208
    REG_MAINBOARD_ALARM_OVERHEAT_TEMPERATURE_ERROR = 209
    REG_MAINBOARD_ALARM_OVERHEAT_TEMPERATURE_ALARM = 210
    REG_MAINBOARD_ALARM_OVERHEAT_TEMPERATURE_CLEAR_ALARM = 211
    REG_MAINBOARD_ALARM_FIRE_ALARM_ERROR = 212
    REG_MAINBOARD_ALARM_FIRE_ALARM_ALARM = 213
    REG_MAINBOARD_ALARM_FIRE_ALARM_CLEAR_ALARM = 214
    REG_MAINBOARD_ALARM_FILTER_WARNING_ERROR = 215
    REG_MAINBOARD_ALARM_FILTER_WARNING_ALARM = 216
    REG_MAINBOARD_ALARM_FILTER_WARNING_CLEAR_ALARM = 217
    REG_MAINBOARD_ALARM_SAF_CTRL_TIMESTAMP_L = 218
    REG_MAINBOARD_ALARM_EAF_CTRL_TIMESTAMP_L = 219
    REG_MAINBOARD_ALARM_FROST_PROT_TIMESTAMP_L = 220
    REG_MAINBOARD_ALARM_DEFROSTING_TIMESTAMP_L = 221
    REG_MAINBOARD_ALARM_SAF_RPM_TIMESTAMP_L = 222
    REG_MAINBOARD_ALARM_EAF_RPM_TIMESTAMP_L = 223
    REG_MAINBOARD_ALARM_FPT_TIMESTAMP_L = 224
    REG_MAINBOARD_ALARM_OAT_TIMESTAMP_L = 225
    REG_MAINBOARD_ALARM_SAT_TIMESTAMP_L = 226
    REG_MAINBOARD_ALARM_RAT_TIMESTAMP_L = 227
    REG_MAINBOARD_ALARM_EAT_TIMESTAMP_L = 228
    REG_MAINBOARD_ALARM_ECT_TIMESTAMP_L = 229
    REG_MAINBOARD_ALARM_EFT_TIMESTAMP_L = 230
    REG_MAINBOARD_ALARM_OHT_TIMESTAMP_L = 231
    REG_MAINBOARD_ALARM_EMT_TIMESTAMP_L = 232
    REG_MAINBOARD_ALARM_RGS_TIMESTAMP_L = 233
    REG_MAINBOARD_ALARM_BYS_TIMESTAMP_L = 234
    REG_MAINBOARD_ALARM_SECONDARY_AIR_TIMESTAMP_L = 235
    REG_MAINBOARD_ALARM_FILTER_TIMESTAMP_L = 236
    REG_MAINBOARD_ALARM_EXTRA_CONTROLLER_TIMESTAMP_L = 237
    REG_MAINBOARD_ALARM_EXTERNAL_STOP_TIMESTAMP_L = 238
    REG_MAINBOARD_ALARM_RH_TIMESTAMP_L = 239
    REG_MAINBOARD_ALARM_CO2_TIMESTAMP_L = 240
    REG_MAINBOARD_ALARM_LOW_SAT_TIMESTAMP_L = 241
    REG_MAINBOARD_ALARM_BYF_TIMESTAMP_L = 242
    REG_MAINBOARD_ALARM_PDM_RHS_TIMESTAMP_L = 243
    REG_MAINBOARD_ALARM_PDM_EAT_TIMESTAMP_L = 244
    REG_MAINBOARD_ALARM_MANUAL_OVERRIDE_OUTPUTS_TIMESTAMP_L = 245
    REG_MAINBOARD_ALARM_MANUAL_FAN_STOP_TIMESTAMP_L = 246
    REG_MAINBOARD_ALARM_OVERHEAT_TEMPERATURE_TIMESTAMP_L = 247
    REG_MAINBOARD_ALARM_FIRE_ALARM_TIMESTAMP_L = 248
    REG_MAINBOARD_ALARM_FILTER_WARNING_TIMESTAMP_L = 249
    REG_MAINBOARD_USERMODE_REMAINING_TIME_L = 250
    REG_MAINBOARD_USERMODE_HOLIDAY_TIME = 251
    REG_MAINBOARD_USERMODE_AWAY_TIME = 252
    REG_MAINBOARD_USERMODE_FIREPLACE_TIME = 253
    REG_MAINBOARD_USERMODE_REFRESH_TIME = 254
    REG_MAINBOARD_USERMODE_CROWDED_TIME = 255
    REG_MAINBOARD_DEMC_CO2_SETTINGS_ON_OFF = 256
    REG_MAINBOARD_DEMC_RH_SETTINGS_ON_OFF = 257
    REG_MAINBOARD_WS_ANY_DEFINED = 258
    REG_MAINBOARD_HEAT_EXCHANGER_TYPE = 259
    REG_MAINBOARD_UNIT_CONFIG_REHEATER_TYPE = 260
    REG_MAINBOARD_UNIT_CONFIG_BYPASS_LOCATION = 261
    REG_MAINBOARD_DEFROSTING_DISABLE = 262
    REG_MAINBOARD_CFG_HEAT_EXCHANGER_ACTUATOR_TYPE = 263
    REG_MAINBOARD_PASSIVE_HOUSE_ACTIVATION = 264
    REG_MAINBOARD_PASSIVE_HOUSE_CERTIFICATION = 265
    REG_MAINBOARD_PASSIVE_HOUSE_MAX_LIMIT = 266
    REG_MAINBOARD_CFG_HEATER_ACTUATOR_TYPE = 267
    REG_MAINBOARD_CFG_CHANGE_OVER_ACTUATOR_TYPE = 268
    REG_MAINBOARD_HEATER_CIRC_PUMP_START_T = 269
    REG_MAINBOARD_HEATER_CIRC_PUMP_STOP_DELAY = 270
    REG_MAINBOARD_CHANGE_OVER_CIRC_PUMP_START_T = 271
    REG_MAINBOARD_CHANGE_OVER_CIRC_PUMP_STOP_DELAY = 272
    REG_MAINBOARD_UNIT_CONFIG_COOLER = 273
    REG_MAINBOARD_CFG_COOLER_ACTUATOR_TYPE = 274
    REG_MAINBOARD_COOLER_OAT_INTERLOCK_T = 275
    REG_MAINBOARD_COOLER_CIRC_PUMP_STOP_DELAY = 276
    REG_MAINBOARD_UNIT_CONFIG_EXTRA_CONTROLLER = 277
    REG_MAINBOARD_EXTRA_CONTROLLER_PREHEATER_SETPOINT_TYPE = 278
    REG_MAINBOARD_EXTRA_CONTROLLER_SET_PI_SETPOINT = 279
    REG_MAINBOARD_EXTRA_CONTROLLER_SET_PI_PBAND = 280
    REG_MAINBOARD_EXTRA_CONTROLLER_SET_PI_ITIME = 281
    REG_MAINBOARD_CFG_EXTRA_ACTUATOR_TYPE = 282
    REG_MAINBOARD_EXTRA_CONTROLLER_CIRC_PUMP_START_T = 283
    REG_MAINBOARD_EXTRA_CONTROLLER_CIRC_PUMP_STOP_DELAY = 284
    REG_MAINBOARD_EXTRA_CONTROLLER_GEO_PRECOOLER_SP = 285
    REG_MAINBOARD_EXTRA_CONTROLLER_GEO_PRECOOLER_ACTIVATION_T = 286
    REG_MAINBOARD_EXTRA_CONTROLLER_GEO_PREHEATER_SP = 287
    REG_MAINBOARD_EXTRA_CONTROLLER_GEO_PREHEATER_ACTIVATION_T = 288
    REG_MAINBOARD_PASSWD_ADMIN = 289
    REG_MAINBOARD_PU_UPDATE_SOURCE = 290
    REG_MAINBOARD_PU_RUNNING_VERSION_MAJOR = 291
    REG_MAINBOARD_PU_RUNNING_VERSION_MINOR = 292
    REG_MAINBOARD_PU_RUNNING_VERSION_BUILD = 293

    # Add more constants here as needed

    @classmethod
    def get_register_name(cls, register_number: int) -> str:
        """Get the register name for a given register number."""
        for attr, value in cls.__dict__.items():
            if not attr.startswith("__") and value == register_number:
                return attr
        return f"UNKNOWN_REGISTER_{register_number}"


    @classmethod
    def get_register_name_by_number(cls, register_number: int) -> str:
        """Get the register name for a given register number."""
        for attr, value in cls.__dict__.items():
            if not attr.startswith("__") and value == register_number:
                return attr
        return f"UNKNOWN_REGISTER_{register_number}"


    @classmethod
    def get_register_name_without_prefix(cls, register_number: int) -> str:
        """Get the register name without the REG_MAINBOARD_ prefix."""
        full_name = cls.get_register_name_by_number(register_number)
        return full_name.replace("REG_MAINBOARD_", "")
