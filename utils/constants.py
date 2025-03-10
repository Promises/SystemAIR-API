CLIENT_ID = "iot-application"
REDIRECT_URI = "https://homesolutions.systemair.com"
AUTH_URL = "https://sso.systemair.com/auth/realms/iot/protocol/openid-connect/auth"
TOKEN_URL = "https://sso.systemair.com/auth/realms/iot/protocol/openid-connect/token"
GATEWAY_API_URL = "https://homesolutions.systemair.com/gateway/api"
REMOTE_API_URL = "https://homesolutions.systemair.com/remote-api/"



class USER_MODE_ENUM:
    AUTO = 0
    MANUAL = 1
    CROWDED = 2
    REFRESH = 3
    FIREPLACE = 4
    AWAY = 5
    HOLIDAY = 6
