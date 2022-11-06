# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.core.auth.main
from duckcli.backend.core.auth.main import User
from hypothesis import given, settings, strategies as st


hostname_pattern = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"

# Validate alnum, dash, dot and underscore
alnum_dash_underscore_dot_pattern = r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"

alnum_pattern = r"[a-zA-Z0-9]+$"

password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

username_min_len_pattern = r"^[A-Za-z0-9]+.{4,}$"


@given(
    username=st.from_regex(username_min_len_pattern),
    email=st.emails(),
    is_superuser=st.booleans(),
    password=st.from_regex(password_pattern),
)
@settings(max_examples=1)
def test_fuzz_User(username, email, is_superuser, password):
    duckcli.backend.core.auth.main.User(
        username=username, email=email, is_superuser=is_superuser, password=password
    )


TEST_USER_DATA = [
    {
        "username": "pshetty233",
        "email": "demo@duckcli.com",
        "is_superuser": True,
        "password": "Dadswod123!",
    }
]

TEST_USER_DATA2 = [
    {
        "username": "pshettywew",
        "email": "demo@duckcli.com",
        "is_superuser": True,
        "password": "Sassrerd153!",
    }
]


@given(
    username=st.sampled_from(["admin"]),
    enable=st.booleans(),
    user=st.sampled_from(TEST_USER_DATA),
)
@settings(max_examples=1)
def test_fuzz_change_superuser(username, enable, user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.change_superuser(
        username=username, enable=enable, user=user_test_data
    )


@given(data=st.builds(dict))
@settings(max_examples=1)
def test_fuzz_create_access_token(data):
    duckcli.backend.core.auth.main.create_access_token(data=data)


@given(
    username=st.from_regex(username_min_len_pattern),
    user=st.sampled_from(TEST_USER_DATA),
)
@settings(max_examples=1)
def test_fuzz_delete_user_data(username, user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.delete_user_data(
        username=username, user=user_test_data
    )


@given(user=st.sampled_from(TEST_USER_DATA))
@settings(max_examples=1)
def test_fuzz_retrieve_all_user(user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.retrieve_all_user(user=user_test_data)


# TODO These tests are not working - fix
"""@given(
    username=st.sampled_from(["admin"]),
)
@example(TEST_USER_DATA)
def test_fuzz_retrieve_one_user(username, user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.retrieve_one_user(
        username=username, user=user_test_data
    )
"""

"""@example(TEST_USER_DATA)
def test_fuzz_update_user_data(username, req, user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.update_user_data(
        username=username, req=req, user=user_test_data
    )


@example(TEST_USER_DATA)
def test_fuzz_create_user(req, user):
    user_test_data = User(**user)
    duckcli.backend.core.auth.main.create_user(req=req, user=user_test_data)"""
