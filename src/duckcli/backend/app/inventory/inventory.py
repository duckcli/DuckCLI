from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
import sys
from duckcli.backend.core.driver.database import sqlite_db
from duckcli.backend.app.inventory.schemas import Device
from duckcli.backend.app.inventory.models import Devices

from duckcli.backend.core.settings.settings import get_core_settings


core_settings = get_core_settings()
db_connection = sqlite_db(url=core_settings.db_url)


class InventoryFileTypes(Enum):
    YAML = "YAML"
    JSON = "JSON"


class InventoryTypes(Enum):
    LOCAL_FILE = "LOCAL_FILE"
    LOCAL_DB = "LOCAL_DB"
    NETBOX = "NETBOX"


class InventoryABC(ABC):
    @abstractmethod
    def add_device():
        pass

    @abstractmethod
    def delete_device():
        pass

    @abstractmethod
    def update_device():
        pass

    @abstractmethod
    def get_device_info():
        pass


class LocalFile(InventoryABC):
    db = []

    def __init__(self, file_type, file_location):
        self.file_tpye = file_type
        self.file_location = file_location

        if str(self.file_tpye).upper() == InventoryFileTypes.YAML.value:
            print("loading YAML inventory file ")
            # TODO: Open YAML file and load the data - one time activity
            self.db = [
                {
                    "hostname": "router1",
                    "os_tpye": "cisco_xr",
                    "mgmt_ip": "192.168.20.5",
                }
            ]

    def add_device(self, device: Device):
        return NotImplementedError

    def get_device_info(self, hostname=None):

        return self.db


class LocalDb(InventoryABC):
    def add_device(self, data):
        if db_connection.execute(
            Devices.select().where(Devices.c.hostname == data.hostname)
        ).fetchall():
            return db_connection.execute(
                Devices.select().where(Devices.c.hostname == data.hostname)
            ).fetchall()

        try:
            db_connection.execute(
                Devices.insert().values(
                    hostname=data.hostname,
                    vendor=data.vendor,
                    model=data.model,
                    osType=data.osType,
                    mgmtIp=str(data.mgmtIp),
                    driverType=data.driverType,
                    deviceFunction=data.deviceFunction,
                    automationEnabled=data.automationEnabled,
                    operatingEnv=data.operatingEnv,
                    siteId=data.siteId,
                    region=data.region,
                    countryCode=data.countryCode,
                    consoleServer=data.consoleServer,
                    consolePort=data.consolePort,
                    softwareVersion=data.softwareVersion,
                    deviceGroup=data.deviceGroup,
                    itsmStrictMode=data.itsmStrictMode,
                    changeControl=data.changeControl,
                )
            )
            return db_connection.execute(
                Devices.select().where(Devices.c.hostname == data.hostname)
            ).fetchall()
            # return db_connection.execute(Devices.select()).fetchall()

        except Exception as error:

            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print(error, filename, line_number)

    def delete_device(self, hostname: Optional[str]):

        if db_connection.execute(
            Devices.select().where(Devices.c.hostname == hostname)
        ).fetchall():
            db_connection.execute(
                Devices.delete().where(Devices.c.hostname == hostname)
            )
            return [{"message": f"{hostname} got deleted"}]

    def update_device(self, device: Device):
        return NotImplementedError

    def get_device_info(
        self,
        hostname: Optional[str] = None,
        os_type: Optional[str] = None,
        site_id: Optional[str] = None,
    ):
        # return {}
        result = []
        try:
            if hostname:
                device_data = db_connection.execute(
                    Devices.select().where(Devices.c.hostname == hostname)
                ).fetchall()
            elif os_type:
                device_data = db_connection.execute(
                    Devices.select().where(Devices.c.osType == os_type)
                ).fetchall()
            elif site_id:
                device_data = db_connection.execute(
                    Devices.select().where(Devices.c.siteId == site_id)
                ).fetchall()
            else:
                # fetch limit is set to: 250
                # device_data = db_connection.execute(Devices.select()).fetchall()
                device_data = db_connection.execute(Devices.select()).fetchmany(
                    core_settings.inventory_fetch_limit
                )
            result = [dict(row) for row in device_data]
            # print(result)
            return result
        except Exception as d_err:
            print(d_err)
            return result.append([{"hostname": hostname, "error": d_err}])


class NetBox(InventoryABC):
    def add_device(self, device: Device):
        return NotImplementedError

    def get_device_info(self):
        return NotImplementedError


class InventoryFactory:
    def create_instance(
        self,
        inventory_type,
        file_type=None,
        file_location=None,
        url=None,
        username=None,
        password=None,
        token=None,
    ):
        if str(inventory_type).upper() == InventoryTypes.LOCAL_FILE.value:
            return LocalFile(file_type=file_type, file_location=file_location)
        elif str(inventory_type).upper() == InventoryTypes.LOCAL_DB.value:
            return LocalDb()
        elif str(inventory_type).upper() == InventoryTypes.NETBOX.value:
            return NetBox()
