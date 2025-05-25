import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from systemair_api.auth.authenticator import SystemairAuthenticator


class TestSystemairAuthenticator:
    @pytest.fixture
    def mock_authenticator(self):
        """Create an authenticator with test credentials"""
        auth = SystemairAuthenticator("test@example.com", "test_password")
        return auth

    @pytest.fixture
    def mock_auth_html_response(self, mock_response):
        """Mock the initial authentication page HTML response"""
        html_content = """
        <form action="https://sso.systemair.com/auth/login" method="post">
            <input type="hidden" name="csrf_token" value="test_csrf_token" />
            <input type="text" name="username" />
            <input type="password" name="password" />
            <input type="submit" name="login" value="Login" />
        </form>
        """
        return mock_response({}, content=html_content.encode(), 
                            headers={"Location": "https://callback?code=test_auth_code&state=test_state"})

    def test_generate_state_parameter(self, mock_authenticator):
        """Test that state parameter is generated and is a string"""
        state = mock_authenticator.generate_state_parameter()
        assert isinstance(state, str)
        assert len(state) > 0

    def test_construct_auth_url(self, mock_authenticator):
        """Test that auth URL is constructed correctly"""
        state = "test_state"
        auth_url = mock_authenticator.construct_auth_url(state)
        
        # Check that the URL contains required parameters
        assert "client_id=" in auth_url
        assert f"state={state}" in auth_url
        assert "redirect_uri=" in auth_url
        assert "response_type=code" in auth_url
        assert "scope=openid" in auth_url

    @patch('requests.Session.get')
    @patch('requests.Session.post')
    def test_simulate_login(self, mock_post, mock_get, mock_authenticator, mock_auth_html_response):
        """Test the login simulation process"""
        # Mock the initial get request that returns the login form
        mock_get.return_value = mock_auth_html_response
        
        # Mock the post request that submits the login form
        mock_post_response = MagicMock()
        mock_post_response.status_code = 302
        mock_post_response.headers = {"Location": "https://callback?code=test_auth_code&state=test_state"}
        mock_post.return_value = mock_post_response
        
        # Mock the follow-up get to the redirect URL
        mock_get_redirect = MagicMock()
        mock_get_redirect.status_code = 200
        mock_get_redirect.url = "https://homesolutions.systemair.com?code=test_auth_code&state=test_state"
        mock_get.side_effect = [mock_auth_html_response, mock_get_redirect]
        
        # Call the method
        auth_url = "https://test_auth_url"
        auth_code = mock_authenticator.simulate_login(auth_url)
        
        # Assertions
        assert auth_code == "test_auth_code"
        mock_get.assert_called()
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_exchange_code_for_token(self, mock_post, mock_authenticator, mock_auth_response):
        """Test the exchange of authorization code for access token"""
        mock_post.return_value = mock_auth_response
        
        result = mock_authenticator.exchange_code_for_token("test_auth_code")
        
        assert "access_token" in result
        assert result["access_token"] == "mock_access_token_12345"
        assert "refresh_token" in result
        mock_post.assert_called_once()

    @patch.object(SystemairAuthenticator, 'generate_state_parameter')
    @patch.object(SystemairAuthenticator, 'construct_auth_url')
    @patch.object(SystemairAuthenticator, 'simulate_login')
    @patch.object(SystemairAuthenticator, 'exchange_code_for_token')
    @patch.object(SystemairAuthenticator, 'get_token_expiry')
    def test_authenticate(self, mock_get_token_expiry, mock_exchange_code, mock_simulate_login, 
                         mock_construct_auth_url, mock_generate_state, mock_authenticator):
        """Test the full authentication flow"""
        # Setup mocks
        mock_generate_state.return_value = "test_state"
        mock_construct_auth_url.return_value = "https://test_auth_url"
        mock_simulate_login.return_value = "test_auth_code"
        mock_exchange_code.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token"
        }
        mock_get_token_expiry.return_value = datetime.now() + timedelta(hours=1)
        
        # Call authenticate
        token = mock_authenticator.authenticate()
        
        # Assertions
        assert token == "test_access_token"
        assert mock_authenticator.access_token == "test_access_token"
        assert mock_authenticator.refresh_token == "test_refresh_token"
        assert mock_authenticator.token_expiry is not None
        
        # Verify correct method calls
        mock_generate_state.assert_called_once()
        mock_construct_auth_url.assert_called_once_with("test_state")
        mock_simulate_login.assert_called_once_with("https://test_auth_url")
        mock_exchange_code.assert_called_once_with("test_auth_code")
        mock_get_token_expiry.assert_called_once_with("test_access_token")

    @patch('requests.post')
    def test_refresh_access_token(self, mock_post, mock_authenticator, mock_auth_response):
        """Test refreshing the access token"""
        # Setup
        mock_authenticator.refresh_token = "old_refresh_token"
        mock_post.return_value = mock_auth_response
        
        # Call refresh
        token = mock_authenticator.refresh_access_token()
        
        # Assertions
        assert token == "mock_access_token_12345"
        assert mock_authenticator.access_token == "mock_access_token_12345"
        assert mock_authenticator.refresh_token == "mock_refresh_token_67890"
        mock_post.assert_called_once()

    def test_is_token_valid(self, mock_authenticator):
        """Test checking if token is valid"""
        # Test with expired token
        mock_authenticator.token_expiry = datetime.now() - timedelta(seconds=60)
        assert not mock_authenticator.is_token_valid()
        
        # Test with valid token
        mock_authenticator.token_expiry = datetime.now() + timedelta(minutes=10)
        assert mock_authenticator.is_token_valid()
        
        # Test with no token
        mock_authenticator.token_expiry = None
        assert not mock_authenticator.is_token_valid()

    def test_get_token_expiry(self, mock_authenticator):
        """Test extracting expiry time from JWT token"""
        # Create a mock JWT token with a known expiry
        expiry_timestamp = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # The token parts have to be valid base64 to decode
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"  # {"alg":"HS256","typ":"JWT"}
        payload = f"e2V4cDoge2V4cGlyeV90aW1lc3RhbXB9fQ=="  # {"exp": {expiry_timestamp}}
        signature = "TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
        
        # Override the decode and load operations to return our test data
        with patch('base64.b64decode') as mock_decode:
            with patch('json.loads') as mock_loads:
                mock_decode.return_value = b'{"exp": 123456789}'
                mock_loads.return_value = {"exp": expiry_timestamp}
                
                # Call the method
                token = f"{header}.{payload}.{signature}"
                result = mock_authenticator.get_token_expiry(token)
                
                # Assertions
                assert isinstance(result, datetime)
                assert abs((result - datetime.fromtimestamp(expiry_timestamp)).total_seconds()) < 1