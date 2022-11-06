from enum import Enum


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
