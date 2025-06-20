"""SystemAIR-API - Python library for controlling Systemair ventilation units."""

from systemair_api.api.systemair_api import SystemairAPI
from systemair_api.auth.authenticator import SystemairAuthenticator
from systemair_api.models.ventilation_unit import VentilationUnit
from systemair_api.api.websocket_client import SystemairWebSocket
from systemair_api.utils.exceptions import (
    SystemairError,
    AuthenticationError,
    TokenRefreshError,
    APIError,
    DeviceNotFoundError,
    WebSocketError,
    RateLimitError,
    ValidationError
)
from systemair_api.utils.constants import UserModes
from systemair_api.__version__ import __version__

__all__ = [
    'SystemairAPI',
    'SystemairAuthenticator', 
    'VentilationUnit',
    'SystemairWebSocket',
    'SystemairError',
    'AuthenticationError',
    'TokenRefreshError',
    'APIError',
    'DeviceNotFoundError',
    'WebSocketError',
    'RateLimitError',
    'ValidationError',
    'UserModes',
    '__version__'
]