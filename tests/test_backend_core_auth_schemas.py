# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.core.auth.schemas
from hypothesis import given, settings, strategies as st


alnum_pattern = r"[a-zA-Z0-9]+$"
password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


@given(username=st.from_regex(alnum_pattern), password=st.from_regex(password_pattern))
@settings(max_examples=20)
def test_fuzz_Login(username, password):
    duckcli.backend.core.auth.schemas.Login(username=username, password=password)


@given(access_token=st.text(), token_type=st.text())
@settings(max_examples=20)
def test_fuzz_Token(access_token, token_type):
    duckcli.backend.core.auth.schemas.Token(
        access_token=access_token, token_type=token_type
    )


@given(
    username=st.from_regex(alnum_pattern),
    email=st.emails(),
    is_superuser=st.one_of(st.none(), st.booleans()),
)
@settings(max_examples=20)
def test_fuzz_TokenData(username, email, is_superuser):
    duckcli.backend.core.auth.schemas.TokenData(
        username=username, email=email, is_superuser=is_superuser
    )


@given(
    username=st.sampled_from(["admin1233"]),
    email=st.sampled_from(["admin1233@duckcli.com"]),
    is_superuser=st.booleans(),
    password=st.sampled_from(["Pdfer345343!"]),
)
@settings(max_examples=5)
def test_fuzz_User(username, email, is_superuser, password):
    duckcli.backend.core.auth.schemas.User(
        username=username, email=email, is_superuser=is_superuser, password=password
    )
