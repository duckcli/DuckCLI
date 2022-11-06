from fastapi import APIRouter, Depends
from duckcli.backend.core.auth.main import verify_token
from duckcli.backend.core.auth.schemas import User
from duckcli.backend.app.inventory.inventory import InventoryFactory
from duckcli.backend.app.inventory.schemas import Device
from typing import Optional
from duckcli.backend.core.settings.settings import get_core_settings


core_settings = get_core_settings()

inventory = InventoryFactory()

inventory_router = APIRouter()


@inventory_router.post("/device")
def add_device(device: Device, user: User = Depends(verify_token)):
    if not user.is_superuser:
        return [{"error": "Not enough permissions"}]
    inventory_instance = inventory.create_instance(
        inventory_type=core_settings.inventory_type
    )
    # print(device)
    if device.hostname is None or not str(device.hostname).replace(" ", ""):
        return [{"error": "hostname field is empty"}]
    # inventory_instance.add_device(data=device.dict())
    return inventory_instance.add_device(data=device)


# Add delete & PATCH
@inventory_router.delete("/device/{hostname}")
def delete_device(hostname: str, user: User = Depends(verify_token)):
    if user.is_superuser:
        inventory_instance = inventory.create_instance(
            inventory_type=core_settings.inventory_type
        )
        return inventory_instance.delete_device(hostname=hostname)

    else:
        return [{"error": "Not enough permissions"}]


@inventory_router.get("/device")
def get_device(
    hostname: Optional[str] = None,
    os_type: Optional[str] = None,
    site_id: Optional[str] = None,
    user: User = Depends(verify_token),
):
    inventory_instance = inventory.create_instance(
        inventory_type=core_settings.inventory_type
    )

    return inventory_instance.get_device_info(
        hostname=hostname, os_type=os_type, site_id=site_id
    )
