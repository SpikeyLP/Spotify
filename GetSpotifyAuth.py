import requests
import webbrowser
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Spotify App Credentials
CLIENT_ID = '' #Your Client ID
CLIENT_SECRET = '' #Your Client Secret
# Redirect URI must match the one set in your Spotify Developer Dashboard
REDIRECT_URI = 'http://127.0.0.1:8080'
SCOPE = 'user-read-playback-state'

# Global variable to store token
_token_data = {}

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _token_data
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if 'code' in query:
            code = query['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'You may now close this window.')

            token_data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET
            }

            token_response = requests.post('https://accounts.spotify.com/api/token', data=token_data)
            _token_data = token_response.json()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing code parameter in callback.')

def get_spotify_token():
    global _token_data
    # Step 1: Open browser to authorize
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    full_auth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    webbrowser.open(full_auth_url)

    # Step 2: Wait for redirect and handle it
    server = HTTPServer(('localhost', 8080), AuthHandler)
    server.handle_request()

    # Step 3: Return access token
    return _token_data["access_token"]
