# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import duckcli.backend.app.inventory.main
from duckcli.backend.core.auth.schemas import User
from hypothesis import settings, given, strategies as st


hostname_pattern = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"

# Validate alanum, dash and underscore
alnum_dash_underscore_dot_pattern = r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"

alnum_pattern = r"[a-zA-Z0-9]*$"


@given(
    hostname=st.one_of(st.from_regex(hostname_pattern)),
    osType=st.from_regex(alnum_dash_underscore_dot_pattern),
    mgmtIp=st.ip_addresses(),
    driverType=st.sampled_from(duckcli.backend.app.inventory.schemas.DriverTypeEnum),
    vendor=st.from_regex(alnum_dash_underscore_dot_pattern),
    model=st.from_regex(alnum_dash_underscore_dot_pattern),
    siteId=st.from_regex(alnum_dash_underscore_dot_pattern),
    region=st.from_regex(alnum_dash_underscore_dot_pattern),
    countryCode=st.from_regex(alnum_dash_underscore_dot_pattern),
    consoleServer=st.from_regex(alnum_dash_underscore_dot_pattern),
    consolePort=st.from_regex(alnum_dash_underscore_dot_pattern),
    softwareVersion=st.from_regex(alnum_dash_underscore_dot_pattern),
    deviceGroup=st.from_regex(alnum_dash_underscore_dot_pattern),
    deviceFunction=st.sampled_from(
        duckcli.backend.app.inventory.schemas.DeviceFunctionEnum
    ),
    automationEnabled=st.sampled_from(duckcli.backend.app.inventory.schemas.BoolEnum),
    operatingEnv=st.sampled_from(
        duckcli.backend.app.inventory.schemas.OperatingEnvEnum
    ),
    itsmStrictMode=st.sampled_from(duckcli.backend.app.inventory.schemas.BoolEnum),
    changeControl=st.sampled_from(duckcli.backend.app.inventory.schemas.BoolEnum),
)
@settings(max_examples=10)
def test_fuzz_Device(
    hostname,
    osType,
    mgmtIp,
    driverType,
    vendor,
    model,
    siteId,
    region,
    countryCode,
    consoleServer,
    consolePort,
    softwareVersion,
    deviceGroup,
    deviceFunction,
    automationEnabled,
    operatingEnv,
    itsmStrictMode,
    changeControl,
):
    duckcli.backend.app.inventory.main.Device(
        hostname=hostname,
        osType=osType,
        mgmtIp=mgmtIp,
        driverType=driverType,
        vendor=vendor,
        model=model,
        siteId=siteId,
        region=region,
        countryCode=countryCode,
        consoleServer=consoleServer,
        consolePort=consolePort,
        softwareVersion=softwareVersion,
        deviceGroup=deviceGroup,
        deviceFunction=deviceFunction,
        automationEnabled=automationEnabled,
        operatingEnv=operatingEnv,
        itsmStrictMode=itsmStrictMode,
        changeControl=changeControl,
    )


@given(v=st.ip_addresses())
def test_fuzz_Device_validate_ip_address(v):
    duckcli.backend.app.inventory.main.Device.validate_ip_address(v=v)


@given(
    hostname=st.one_of(st.from_regex(hostname_pattern)),
    os_type=st.none(),
    site_id=st.none(),
)
@settings(max_examples=25)
def test_fuzz_get_device(hostname, os_type, site_id):
    duckcli.backend.app.inventory.main.get_device(
        hostname=hostname, os_type=os_type, site_id=site_id
    )


TEST_USER_DATA = [
    {
        "username": "prathapshetty",
        "email": "demo@duckcli.com",
        "is_superuser": True,
        "password": "sdsadasED!23",
    }
]
TEST_ADD_DEVICE = [
    {
        "hostname": "sandbox-iosxr-1.cisco.com",
        "vendor": "cisco",
        "model": "xrv",
        "osType": "cisco_xr",
        "mgmtIp": "131.226.217.151",
        "driverType": "ssh",
        "siteId": "uxb",
        "region": "London",
        "countryCode": "UK",
        "consoleServer": "console1.server",
        "consolePort": "portxx",
        "softwareVersion": "712KLK",
        "automationEnabled": "True",
        "deviceFunction": "core",
        "deviceGroup": "ma01",
        "operatingEnv": "test",
        "itsmStrictMode": "False",
        "changeControl": "False",
    }
]


@given(
    device_data=st.sampled_from(TEST_ADD_DEVICE),
    user=st.sampled_from(TEST_USER_DATA),
)
@settings(max_examples=25)
def test_fuzz_add_device(device_data, user):
    # print(device)
    user_test_data = User(**user)
    device_instance = duckcli.backend.app.inventory.main.Device(**device_data)
    # print(device_instance)
    duckcli.backend.app.inventory.main.add_device(
        device=device_instance, user=user_test_data
    )
