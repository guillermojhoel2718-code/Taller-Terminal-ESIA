import os
import sys
import requests

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
ACCESS_TOKEN = env_vars.get('CANVA_ACCESS_TOKEN')

if not ACCESS_TOKEN:
    print("Error: CANVA_ACCESS_TOKEN missing.")
    sys.exit(1)

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# 1. Try to get the design details
print("Fetching design details for DAHEDbMITxc...")
design_id = "DAHEDbMITxc"
url_get = f"https://api.canva.com/rest/v1/designs/{design_id}"
resp = requests.get(url_get, headers=headers)
print(f"GET {url_get} -> {resp.status_code}")
print(resp.text)

# 2. Try to list templates (if it's a template)
url_templates = "https://api.canva.com/rest/v1/brand-templates"
resp_tpl = requests.get(url_templates, headers=headers)
print(f"\\nGET {url_templates} -> {resp_tpl.status_code}")
print(resp_tpl.text)

