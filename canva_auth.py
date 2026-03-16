import os
import sys
import base64
import hashlib
import secrets
import threading
import webbrowser
import requests
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

env_path = 'config.env'

def read_env(path):
    env_vars = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        k, v = line.split('=', 1)
                        env_vars[k.strip()] = v.strip()
    return env_vars

env_vars = read_env(env_path)
CLIENT_ID = env_vars.get('CANVA_CLIENT_ID')
CLIENT_SECRET = env_vars.get('CANVA_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: CANVA_CLIENT_ID or CANVA_CLIENT_SECRET missing in config.env")
    sys.exit(1)

# Generate verifier and challenge
verifier = "".join([secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~") for i in range(64)])
digest = hashlib.sha256(verifier.encode('ascii')).digest()
challenge = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')

redirect_uri = 'http://127.0.0.1:3000'
scopes_encoded = 'design:content:read%20design:content:write%20design:meta:read%20asset:read%20asset:write%20profile:read'

auth_url = f"https://www.canva.com/api/oauth/authorize?code_challenge={challenge}&code_challenge_method=s256&scope={scopes_encoded}&response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(redirect_uri)}"

auth_code = None
server = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        
        if 'code' in qs:
            auth_code = qs['code'][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization successful!</h1><p>You can close this tab and return to the terminal.</p></body></html>")
            # Shutdown server in a new thread
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        elif 'error' in qs:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            error_msg = qs.get('error_description', ['Unknown error'])[0]
            error_code = qs.get('error', ['Unknown'])[0]
            print(f"\\nCanva returned an error: {error_code} - {error_msg}")
            self.wfile.write(f"<html><body><h1>Authorization Failed!</h1><p>Error: {error_msg}</p></body></html>".encode())
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

server = HTTPServer(('127.0.0.1', 3000), OAuthHandler)
print("Opening browser for authorization...")
print(f"URL: {auth_url}")
webbrowser.open(auth_url)

print("Waiting for authorization code on 127.0.0.1:3000 (Please login to Canva)...")
server.serve_forever()

if not auth_code:
    print("Failed to get authorization code.")
    sys.exit(1)

print("Authorization code received. Exchanging for access_token...")

token_url = "https://api.canva.com/rest/v1/oauth/token"
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth = base64.b64encode(auth_str.encode('ascii')).decode('ascii').replace('\n', '')

headers = {
    'Authorization': f'Basic {b64_auth}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'code_verifier': verifier,
    'redirect_uri': redirect_uri
}

response = requests.post(token_url, headers=headers, data=data)

if response.status_code != 200:
    print(f"Error getting token: {response.status_code}")
    print(response.text)
    sys.exit(1)

token_data = response.json()
access_token = token_data.get('access_token')
refresh_token = token_data.get('refresh_token')

if not access_token:
    print("No access token found in response.")
    sys.exit(1)

print("Access token retrieved. Updating config.env...")

env_lines = []
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        env_lines = f.readlines()

new_lines = []
for line in env_lines:
    if line.startswith('CANVA_ACCESS_TOKEN='):
        continue
    if line.startswith('CANVA_REFRESH_TOKEN='):
        continue
    new_lines.append(line)

if new_lines and not new_lines[-1].endswith('\n'):
    new_lines[-1] += '\n'

new_lines.append(f"CANVA_ACCESS_TOKEN={access_token}\n")
if refresh_token:
    new_lines.append(f"CANVA_REFRESH_TOKEN={refresh_token}\n")

with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fetching user info...")
user_url = "https://api.canva.com/rest/v1/users/me"
user_headers = {
    'Authorization': f'Bearer {access_token}'
}

user_resp = requests.get(user_url, headers=user_headers)
if user_resp.status_code == 200:
    user_info = user_resp.json()
    u = user_info.get('team_user', {})
    display_name = u.get('display_name', 'Unknown')
    print("=" * 40)
    print(f"Canva Login Successful: {display_name}")
    print(f"Full Response: {user_info}")
    print("=" * 40)
else:
    print(f"Error fetching user info: {user_resp.status_code}")
    print(user_resp.text)
    sys.exit(1)
