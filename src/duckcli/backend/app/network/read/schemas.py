from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, List, Union
import ipaddress
import re
from duckcli.backend.app.settings.settings import get_app_settings

app_settings = get_app_settings()


class DriverTypeEnum(str, Enum):
    SSH = "ssh"
    NETCONF = "netconf"
    TELENET = "telnet"
    CONSOLE = "console"


# r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"
hostname_pattern = app_settings.hostname_pattern
# r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"
alnum_dash_underscore_dot_pattern = app_settings.alnum_dash_underscore_dot_pattern
# r"[a-zA-Z0-9 ]*$"
command_pattern = app_settings.command_pattern

# TODO : add enum for all the ostypes & vendor, validator for commands


class Commands(BaseModel):
    hostname: str
    commands: List[str]
    osType: Optional[str] = None
    mgmtIp: Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]
    driverType: Optional[DriverTypeEnum]
    vendor: Optional[str] = None
    model: Optional[str] = None
    rawFormat: Optional[bool] = False

    @validator("mgmtIp")
    def validate_ip_address(cls, v):
        version = int(ipaddress.ip_address(v).version)
        if version in {4, 6}:
            return v
        else:
            raise ValueError("Does not appear to be an IPv4 or IPv6 address")

    @validator("hostname")
    def valid_hostname(cls, v):
        assert re.match(
            hostname_pattern, v
        ), "Must match the hostname str pattern in the schema."
        return v

    @validator("commands", each_item=True)
    def check_commands(cls, v):
        assert re.match(
            command_pattern, v
        ), "Must match the command pattern in the schema."
        return v

    # TODO: Not working
    """ @root_validator()
    @classmethod
    def validate_fields_at_the_same_time(cls, field_values):
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["model"]
        ), "Must match the model str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["vendor"]
        ), "Must match the vendor str pattern in the schema."
        assert re.match(
            alnum_dash_underscore_dot_pattern, field_values["osType"]
        ), "Must match the osType str pattern in the schema."

        return field_values"""


class NetworkRead(BaseModel):
    send_commands: List[Commands]
