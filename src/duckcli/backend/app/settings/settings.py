import os
import re
from enum import Enum
from functools import lru_cache
from pydantic import BaseSettings, Field


BASE_DIR = os.getcwd()

# convert this to enum
GENIE_PARSER_DEVICE_MAPPER = {
    "cisco_xr": "iosxr",
    "cisco_xe": "iosxe",
    "ios": "ios",
    "cisco_ios": "ios",
    "cisco_nxos": "nxos",
}


class ParserDeviceMapperEnum(str, Enum):
    cisco_xr = "iosxr"
    cisco_xe = "iosxe"
    ios = "ios"
    cisco_ios = "ios"
    cisco_nxos = "nxos"
    cisco_asa = "asa"
    juniper_junos = "junos"
    linux = "linux"
    f5_ltm = "bigip"
    f5_linux = "bigip"
    f5_tmsh = "bigip"
    nokia_sros = "sros"
    arista_eos = "aireos"


"""netmiko: juniper
juniper_junos
linux
nokia_sros
f5_linux
f5_ltm
f5_tmsh
cisco_asa
arista_eos"""

"""pysts parser:
supported_nos = {'aireos',
                  'apic',
                  'asa',
                  'bigip',
                  'cheetah',
                  'comware',
                  'dnac',
                  'gaia',
                  'ios',
                  'iosxe',
                  'iosxr',
                  'ironware',
                  'junos',
                  'linux',
                  'nxos',
                  'sros',
                  'viptela'}
"""
# TODO: add \n to cmd acl
READ_COMMAND_ACL = re.compile(r"^(show |display |admin display )")
# Vendor/ostype and template path prefix mapper
TEMPLATE_FOLDER_PREFIX_MAPPER = {"cisco_xr": "/cisco/iosxr"}


class Settings(BaseSettings):
    network_read_username: str = Field(
        "admin"  # change me ! for testing sandbox-iosxr-1.cisco.com username
    )
    network_read_password: str = Field(
        "C1sco12345"  # change me ! for testing sandbox-iosxr-1.cisco.com password
    )
    network_write_username: str = None
    network_write_password: str = None
    max_read_command_set_limit: int = 10
    multiprocessing_threadpool_limit: int = 10
    read_state_template_dir: str = Field(
        f"{BASE_DIR}/src/duckcli/backend/templates/read_state"
    )
    read_config_template_dir: str = Field(
        f"{BASE_DIR}/src/duckcli/backend/templates/read_config"
    )
    write_config_template_dir: str = Field(
        f"{BASE_DIR}/src/duckcli/backend/templates/write_config"
    )
    delete_config_template_dir: str = Field(
        f"{BASE_DIR}/src/duckcli/backend/templates/delete_config"
    )
    parser_device_mapper = ParserDeviceMapperEnum
    hostname_pattern: str = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"
    alnum_dash_underscore_dot_pattern: str = r"^[.A-Za-z_-][.A-Za-z0-9_-]*$"
    command_pattern: str = r"[a-zA-Z0-9 ]*$"
    max_ping_check_host_limit: int = 100
    max_ping_count_limit: int = 100
    max_ping_interval_limit: int = 10

    class Config:
        env_prefix = "duckcli_app"


settings = Settings()


@lru_cache()
def get_app_settings():
    return Settings()
