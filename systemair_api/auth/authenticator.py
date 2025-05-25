"""SystemairAuthenticator - Authentication module for Systemair Home Solutions cloud."""

import uuid
import requests
import json
import base64
from typing import Dict, Optional, Any, Union, cast
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from systemair_api.utils.constants import APIEndpoints, CLIENT_ID, REDIRECT_URI
from systemair_api.utils.exceptions import AuthenticationError, TokenRefreshError

class SystemairAuthenticator:
    """Authentication handler for Systemair Home Solutions cloud.
    
    Manages the OAuth2 authentication flow, including:
    - Initial login with username/password
    - Token exchange
    - Token refresh
    - Token validation
    """
    
    def __init__(self, email: str, password: str) -> None:
        """Initialize the authenticator with user credentials.
        
        Args:
            email: User's email address
            password: User's password
        """
        self.email: str = email
        self.password: str = password
        self.session: requests.Session = requests.Session()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None

    def generate_state_parameter(self) -> str:
        """Generate a random state parameter for the OAuth flow.
        
        Returns:
            str: A random UUID as string
        """
        return str(uuid.uuid4())

    def construct_auth_url(self, state: str) -> str:
        """Construct the OAuth authorization URL.
        
        Args:
            state: State parameter to include in the URL
            
        Returns:
            str: Complete authorization URL
        """
        params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "state": state,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid"
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{APIEndpoints.AUTH}?{query_string}"

    def simulate_login(self, auth_url: str) -> str:
        """Simulate a browser login to obtain the authorization code.
        
        This method simulates the browser login process by:
        1. Fetching the login page
        2. Extracting the form and input fields
        3. Submitting the form with credentials
        4. Following redirects to obtain the authorization code
        
        Args:
            auth_url: The authorization URL to start the flow
            
        Returns:
            str: The authorization code if successful
            
        Raises:
            Exception: If login fails or authorization code cannot be obtained
        """
        # print(f"Fetching login page from: {auth_url}")
        response = self.session.get(auth_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        form = soup.find('form')
        if not form:
            raise AuthenticationError('Login form not found')

        # Cast to Tag to ensure proper type handling
        form_tag = cast(Tag, form)
        action_url = form_tag['action']
        inputs = form_tag.find_all('input')

        form_data = {}
        for input_tag in inputs:
            # Cast each input element to Tag
            input_tag = cast(Tag, input_tag)
            if input_tag.get('name') == 'username':
                form_data[input_tag['name']] = self.email
            elif input_tag.get('name') == 'password':
                form_data[input_tag['name']] = self.password
            elif input_tag.get('name'):
                form_data[input_tag['name']] = input_tag.get('value', '')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        # print("Submitting login form...")
        # Handle potential list type for action_url by ensuring it's a string
        if isinstance(action_url, list):
            action_url_str = action_url[0] if action_url else ''
        else:
            action_url_str = action_url
            
        response = self.session.post(action_url_str, data=form_data, headers=headers, allow_redirects=False)
        # print(f"Login form submission response status: {response.status_code} {response.reason}")

        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            # print("Redirect URL:", redirect_url)
            
            if redirect_url is None:
                raise AuthenticationError('Redirect URL not found in headers')

            response = self.session.get(redirect_url, allow_redirects=True)
            # print(f"Redirect follow-up response status: {response.status_code} {response.reason}")

            if response.status_code == 200:
                if 'code=' in response.url:
                    auth_code = response.url.split('code=')[1].split('&')[0]
                    # print("Authorization Code:", auth_code)
                    print("Authentication success")
                    return auth_code
                else:
                    raise AuthenticationError('Authorization code not found in final URL')
            else:
                raise AuthenticationError('Failed to follow redirect URL')
        else:
            raise AuthenticationError('Login failed or redirect did not occur')

    def exchange_code_for_token(self, auth_code: str) -> Dict[str, Any]:
        """Exchange an authorization code for access and refresh tokens.
        
        Args:
            auth_code: The authorization code obtained from login
            
        Returns:
            dict: Token response containing access_token, refresh_token, etc.
            
        Raises:
            requests.exceptions.HTTPError: If token exchange fails
        """
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://homesolutions.systemair.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers',
        }

        response = requests.post(APIEndpoints.TOKEN, data=data, headers=headers)
        if response.status_code == 200:
            return cast(Dict[str, Any], response.json())
        else:
            print("Failed to exchange code for token:", response.content)
            response.raise_for_status()
            # This line is never reached but needed for mypy
            return {}

    def authenticate(self) -> str:
        """Perform the full authentication flow.
        
        This method orchestrates the complete authentication process:
        1. Generate state parameter
        2. Construct auth URL
        3. Simulate login to get authorization code
        4. Exchange code for tokens
        5. Extract token expiry time
        
        Returns:
            str: The access token if successful
            
        Raises:
            AuthenticationError: If authentication fails for any reason
        """
        state = self.generate_state_parameter()
        auth_url = self.construct_auth_url(state)
        auth_code = self.simulate_login(auth_url)
        token_response = self.exchange_code_for_token(auth_code)
        self.access_token = token_response.get('access_token')
        self.refresh_token = token_response.get('refresh_token')
        
        if not self.access_token:
            raise AuthenticationError('No access token found in response')
            
        self.token_expiry = self.get_token_expiry(self.access_token)
        return str(self.access_token)

    def refresh_access_token(self) -> str:
        """Refresh the access token using the refresh token.
        
        Returns:
            str: The new access token if successful
            
        Raises:
            TokenRefreshError: If refresh fails or no refresh token is available
        """
        if not self.refresh_token:
            raise TokenRefreshError("No refresh token available. Please authenticate first.")

        data = {
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'refresh_token': self.refresh_token,
            'redirect_uri': REDIRECT_URI,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Origin': 'https://homesolutions.systemair.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }

        response = requests.post(APIEndpoints.TOKEN, data=data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')  # Update refresh token if provided
            
            if not self.access_token:
                raise TokenRefreshError('No access token found in refresh response')
                
            self.token_expiry = self.get_token_expiry(self.access_token)
            return str(self.access_token)
        else:
            raise TokenRefreshError(f"Failed to refresh token: {response.text}")

    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """Decode the JWT and extract the expiry time.
        
        Args:
            token: JWT token to decode
            
        Returns:
            datetime: Token expiry time as datetime object
            
        Raises:
            ValueError: If expiry time cannot be found in the token
        """
        try:
            # Split the token and get the payload part (second part)
            payload = token.split('.')[1]

            # Add padding if necessary
            payload += '=' * ((4 - len(payload) % 4) % 4)

            # Decode the Base64 string
            decoded_payload = base64.b64decode(payload)

            # Parse the JSON
            token_data = json.loads(decoded_payload)

            # Extract the expiry time
            exp_timestamp = token_data.get('exp')

            if exp_timestamp:
                return datetime.fromtimestamp(exp_timestamp)
            else:
                raise ValueError("No expiry time found in token")
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None

    def is_token_valid(self) -> bool:
        """Check if the current token is still valid.
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self.token_expiry:
            return False

        # Consider the token invalid if it's about to expire in the next 30 seconds
        return datetime.now() + timedelta(seconds=30) < self.token_expiry
