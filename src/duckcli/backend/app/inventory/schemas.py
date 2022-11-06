import ipaddress
import re
from pydantic import BaseModel, validator, root_validator
from enum import Enum
from typing import Optional, Union
from duckcli.backend.app.settings.settings import get_app_settings

app_settings = get_app_settings()


class DriverTypeEnum(str, Enum):
    SSH = "ssh"
    NETCONF = "netconf"
    TELENET = "telnet"
    CONSOLE = "console"


class OperatingEnvEnum(str, Enum):
    PROD = "prod"
    PREPROD = "preprod"
    TEST = "test"
    DEV = "dev"
    STAGE = "stage"


class DeviceFunctionEnum(str, Enum):
    ACCESS = "access"
    CORE = "core"
    BACKBONE = "backbone"
    FIREWALL = "firewall"
    LOADBALANCER = "loadbalancer"
    OTHER = "other"


# TODO : Change this to bool - not work with the DB model
class BoolEnum(str, Enum):
    TRUE = "True"
    FALSE = "False"


# r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"
hostname_pattern = app_settings.hostname_pattern
# r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"
alnum_dash_underscore_dot_pattern = app_settings.alnum_dash_underscore_dot_pattern
# r"[a-zA-Z0-9 ]*$"


class Device(BaseModel):
    hostname: str
    osType: str = "cisco_xr"
    mgmtIp: Union[ipaddress.IPv4Address, ipaddress.IPv6Address] = None
    driverType: DriverTypeEnum = DriverTypeEnum.SSH
    vendor: Optional[str] = "cisco"
    model: Optional[str] = "xrv"
    siteId: Optional[str] = "uxb"
    region: Optional[str] = "London"
    countryCode: Optional[str] = "UK"
    consoleServer: Optional[str] = "console1.server"
    consolePort: Optional[str] = "portxx"
    softwareVersion: Optional[str] = "unkown"
    deviceGroup: Optional[str] = "other"
    deviceFunction: DeviceFunctionEnum = DeviceFunctionEnum.OTHER
    automationEnabled: BoolEnum = BoolEnum.TRUE
    operatingEnv: OperatingEnvEnum = OperatingEnvEnum.TEST
    itsmStrictMode: BoolEnum = BoolEnum.FALSE
    changeControl: BoolEnum = BoolEnum.FALSE

    @validator("mgmtIp")
    def validate_ip_address(cls, v):
        version = int(ipaddress.ip_address(v).version)
        if version in {4, 6}:
            return str(v)
        else:
            raise ValueError("Does not appear to be an IPv4 or IPv6 address")

    @validator("hostname")
    def valid_hostname(cls, v):
        assert re.match(hostname_pattern, v), "Must match hostname pattern"
        return v

    @validator("consoleServer")
    def valid_console_server(cls, v):
        assert re.match(hostname_pattern, v), "Must match hostname pattern"
        return v

    @root_validator()
    @classmethod
    def validate_fields_at_the_same_time(cls, field_values):
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["model"]
        ), "Must match the model str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["siteId"]
        ), "Must match the siteId str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["vendor"]
        ), "Must match the vendor str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["region"]
        ), "Must match the region str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["deviceGroup"]
        ), "Must match the deviceGroup str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["osType"]
        ), "Must match the osType str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["countryCode"]
        ), "Must match the countryCode str pattern in the schema."
        """ assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["softwareVersion"]
        ), "Must match the softwareVersion str pattern in the schema."""
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["consolePort"]
        ), "Must match the consoleProt str pattern in the schema."
        return field_values
