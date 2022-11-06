# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.app.network.read.schemas
from duckcli.backend.app.network.read.schemas import Commands
from hypothesis import given, settings, example, strategies as st

hostname_pattern = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"

# Validate alanum, dash and underscore
alnum_dash_underscore_dot_pattern = r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"

alnum_pattern = r"[a-zA-Z0-9]*$"

cmd_pattern = r"[a-zA-Z0-9 ]*$"

# TODO: commands st.lists is not working
cmd_list = ["show int", "show arp", "show ip"]


@given(
    hostname=st.one_of(st.from_regex(hostname_pattern)),
    commands=st.sampled_from([cmd_list]),
    osType=st.one_of(st.text()),
    mgmtIp=st.ip_addresses(),
    driverType=st.one_of(
        st.none(),
        st.sampled_from(duckcli.backend.app.network.read.schemas.DriverTypeEnum),
    ),
    vendor=st.one_of(st.none(), st.text()),
    model=st.one_of(st.none(), st.text()),
)
@settings(max_examples=10)
def test_fuzz_Commands(hostname, commands, osType, mgmtIp, driverType, vendor, model):
    duckcli.backend.app.network.read.schemas.Commands(
        hostname=hostname,
        commands=commands,
        osType=osType,
        mgmtIp=mgmtIp,
        driverType=driverType,
        vendor=vendor,
        model=model,
    )


@given(v=st.ip_addresses())
@settings(max_examples=10)
def test_fuzz_Commands_validate_ip_address(v):
    duckcli.backend.app.network.read.schemas.Commands.validate_ip_address(v=v)


TEST_CMD_DATA = [
    {
        "hostname": "sandbox-iosxr-1.cisco.com",
        "commands": ["show interface summary", "show version"],
    }
]

# TODO: commands st input is not working so using sample data


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
            mgmtIp=st.one_of(st.ip_addresses()),
            model=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            osType=st.one_of(st.none(), st.one_of(st.none(), st.text())),
            vendor=st.one_of(st.none(), st.one_of(st.none(), st.text())),
        )
    )
)
@settings(max_examples=1)
@example(TEST_CMD_DATA)
def test_fuzz_NetworkRead(send_commands):
    duckcli.backend.app.network.read.schemas.NetworkRead(send_commands=send_commands)
