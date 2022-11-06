import schemathesis
from hypothesis import settings
import urllib3

from duckcli.frontend.settings.settings import get_settings
from duckcli.frontend.utils.auth import BackendAuth

urllib3.disable_warnings()


cli_settings = get_settings()
TOKEN_ENDPOINT = cli_settings.backend_token_url
USERNAME = cli_settings.backend_username
PASSWORD = cli_settings.backend_password
INVENTORY_URL = cli_settings.backend_inventory_url

auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)
schema = schemathesis.from_uri("https://localhost:9999/api", verify=False)

"""

schema = schemathesis.from_path(
    "./tests/openapi.json", base_url="https://localhost:9999"
)

schemathesis run --request-tls-verify false --max-response-time=100 -H "Authorization: Bearer xxxxxx" https://localhost:9999/api
"""

token = auth.access_token


@schema.parametrize()
@settings(max_examples=10)
def test_api(case):
    case.call_and_validate(verify=False, headers={"Authorization": f"Bearer {token}"})
