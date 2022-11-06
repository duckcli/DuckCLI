# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.app.network.read.main
from duckcli.backend.app.network.read.main import NetworkRead
from duckcli.backend.app.network.read.schemas import Commands
from duckcli.backend.core.auth.schemas import User
from hypothesis import given, settings, strategies as st


# TODO: replace st.nothing() with an appropriate strategy
hostname_pattern = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"

# Validate alanum, dash and underscore
alnum_dash_underscore_dot_pattern = r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"

alnum_pattern = r"[a-zA-Z0-9]*$"

# TODO does not work with examples more that 10 ( random issues ) - fix


@given(
    send_commands=st.lists(
        st.builds(
            Commands,
            driverType=st.one_of(
                st.none(),
                st.one_of(
                    st.none(),
                    st.sampled_from(
                        duckcli.backend.app.network.read.schemas.DriverTypeEnum
                    ),
                ),
            ),
            hostname=st.from_regex(hostname_pattern),
            mgmtIp=st.one_of(st.ip_addresses(v=4), st.ip_addresses(v=6)),
            model=st.from_regex(alnum_dash_underscore_dot_pattern),
            osType=st.from_regex(alnum_dash_underscore_dot_pattern),
            rawFormat=st.one_of(st.just(False), st.one_of(st.none(), st.booleans())),
            vendor=st.from_regex(alnum_dash_underscore_dot_pattern),
        )
    )
)
@settings(max_examples=1)
def test_fuzz_NetworkRead(send_commands):
    duckcli.backend.app.network.read.main.NetworkRead(send_commands=send_commands)


TEST_DATA = [
    {
        "send_commands": [
            {
                "hostname": "sandbox-iosxr-2.cisco.com",
                "commands": ["show version"],
            }
        ]
    }
]

TEST_USER_DATA = [
    {
        "username": "prathapshetty",
        "email": "demo@duckcli.com",
        "is_superuser": True,
        "password": "sdsadasED!23",
    }
]
# TODO: This test will try to connect to a network device and run command -- Change this to mock or dummy device


@given(
    network_read=st.sampled_from(TEST_DATA),
    user=st.sampled_from(TEST_USER_DATA),
)
@settings(max_examples=10)
def test_fuzz_network_get(network_read, user):
    user_test_data = User(**user)
    network_read_instance = NetworkRead(**network_read)
    duckcli.backend.app.network.read.main.network_get(
        network_read=network_read_instance, user=user_test_data
    )
