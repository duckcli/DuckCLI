# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import duckcli.backend.core.auth.jwttoken
import urllib3
from duckcli.frontend.settings.settings import get_settings
from duckcli.frontend.utils.auth import BackendAuth
from hypothesis import given, strategies as st
from fastapi import HTTPException

urllib3.disable_warnings()

cli_settings = get_settings()
TOKEN_ENDPOINT = cli_settings.backend_token_url
USERNAME = cli_settings.backend_username
PASSWORD = cli_settings.backend_password
INVENTORY_URL = cli_settings.backend_inventory_url
auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)


# TODO: replace st.nothing() with an appropriate strategy


@given(
    username=st.one_of(st.none(), st.text()),
    email=st.one_of(st.none(), st.text()),
    is_superuser=st.one_of(st.none(), st.booleans()),
)
def test_fuzz_TokenData(username, email, is_superuser):
    duckcli.backend.core.auth.jwttoken.TokenData(
        username=username, email=email, is_superuser=is_superuser
    )


@given(data=st.builds(dict))
def test_fuzz_create_access_token(data):
    duckcli.backend.core.auth.jwttoken.create_access_token(data=data)


# TODO: Add option to get token for test_case_user
access_token = auth.access_token


@given(token=st.just(access_token), credentials_exception=st.just(HTTPException))
def test_fuzz_verify_token(token, credentials_exception):
    duckcli.backend.core.auth.jwttoken.verify_token(
        token=token, credentials_exception=credentials_exception
    )
