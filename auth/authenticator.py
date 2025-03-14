import uuid
import requests
import json
import base64
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from utils.constants import AUTH_URL, TOKEN_URL, CLIENT_ID, REDIRECT_URI

class SystemairAuthenticator:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None

    def generate_state_parameter(self):
        return str(uuid.uuid4())

    def construct_auth_url(self, state):
        params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "state": state,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid"
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{AUTH_URL}?{query_string}"

    def simulate_login(self, auth_url):
        # print(f"Fetching login page from: {auth_url}")
        response = self.session.get(auth_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        form = soup.find('form')
        if not form:
            raise Exception('Login form not found')

        action_url = form['action']
        inputs = form.find_all('input')

        form_data = {}
        for input in inputs:
            if input['name'] == 'username':
                form_data[input['name']] = self.email
            elif input['name'] == 'password':
                form_data[input['name']] = self.password
            else:
                form_data[input['name']] = input.get('value', '')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        # print("Submitting login form...")
        response = self.session.post(action_url, data=form_data, headers=headers, allow_redirects=False)
        # print(f"Login form submission response status: {response.status_code} {response.reason}")

        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            # print("Redirect URL:", redirect_url)

            response = self.session.get(redirect_url, allow_redirects=True)
            # print(f"Redirect follow-up response status: {response.status_code} {response.reason}")

            if response.status_code == 200:
                if 'code=' in response.url:
                    auth_code = response.url.split('code=')[1].split('&')[0]
                    # print("Authorization Code:", auth_code)
                    print("Authentication success")
                    return auth_code
                else:
                    raise Exception('Authorization code not found in final URL')
            else:
                raise Exception('Failed to follow redirect URL')
        else:
            raise Exception('Login failed or redirect did not occur')

    def exchange_code_for_token(self, auth_code):
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

        response = requests.post(TOKEN_URL, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to exchange code for token:", response.content)
            response.raise_for_status()

    def authenticate(self):
        state = self.generate_state_parameter()
        auth_url = self.construct_auth_url(state)
        auth_code = self.simulate_login(auth_url)
        token_response = self.exchange_code_for_token(auth_code)
        self.access_token = token_response.get('access_token')
        self.refresh_token = token_response.get('refresh_token')
        self.token_expiry = self.get_token_expiry(self.access_token)
        return self.access_token

    def refresh_access_token(self):
        if not self.refresh_token:
            raise Exception("No refresh token available. Please authenticate first.")

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

        response = requests.post(TOKEN_URL, data=data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')  # Update refresh token if provided
            self.token_expiry = self.get_token_expiry(self.access_token)
            return self.access_token
        else:
            raise Exception(f"Failed to refresh token: {response.text}")

    def get_token_expiry(self, token):
        """Decode the JWT and extract the expiry time."""
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

    def is_token_valid(self):
        """Check if the current token is still valid."""
        if not self.token_expiry:
            return False

        # Consider the token invalid if it's about to expire in the next 30 seconds
        return datetime.now() + timedelta(seconds=30) < self.token_expiry
