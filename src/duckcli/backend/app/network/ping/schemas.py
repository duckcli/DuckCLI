from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union
import ipaddress
import re

from duckcli.backend.app.settings.settings import get_app_settings

app_settings = get_app_settings()

hostname_pattern = app_settings.hostname_pattern


class TargetHosts(BaseModel):
    addresses: Optional[
        List[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]
    ]  # not in use
    hosts: List[str]
    count: Optional[int] = Field(1, gt=0, le=app_settings.max_ping_count_limit)
    interval: Optional[int] = Field(
        0.5, gt=0.0, le=app_settings.max_ping_interval_limit
    )
    timeout: Optional[int] = Field(0.5, gt=0.0, le=5)

    @validator("hosts", each_item=True)
    def valid_hostname(cls, v):
        assert re.match(hostname_pattern, v), "Must match the hostname pattern"
        return v

    @validator("addresses", each_item=True)
    def validate_ip_address(cls, v):
        version = int(ipaddress.ip_address(v).version)
        if version in {4, 6}:
            return str(v)
        else:
            raise ValueError("Does not appear to be an IPv4 or IPv6 address")
