from duckcli.frontend.app.ping.main import get_ping_responses
from duckcli.frontend.settings.settings import get_settings
import time
from duckcli.frontend.utils.auth import BackendAuth

start_time = time.perf_counter()
app_settings = get_settings()

TOKEN_ENDPOINT = app_settings.backend_token_url
USERNAME = app_settings.backend_username
PASSWORD = app_settings.backend_password
INVENTORY_URL = app_settings.backend_inventory_url

auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)
# ping_a_host = pinger(hostname="192.168.0.1", inventory=False)
# print(ping_a_host)
payload = {
    "hosts": ["cisco.com", "duckcli.com", "192.168.0.1", "8.8.8.8", "8.8.4.4"],
    "count": 10,
}

PING_URL = app_settings.backend_ping_check_url
resp = get_ping_responses(auth=auth, url=PING_URL, api_payload=payload)
elapsed = time.perf_counter() - start_time
print(elapsed)
print(resp)
