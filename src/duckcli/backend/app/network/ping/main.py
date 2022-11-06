import time
import asyncio
import logging
from fastapi import APIRouter, Depends
from duckcli.backend.app.settings.settings import get_app_settings
from duckcli.backend.core.auth.main import verify_token
from duckcli.backend.core.auth.schemas import User
from duckcli.backend.app.network.ping.schemas import TargetHosts
from duckcli.backend.app.network.ping.ping_check import are_alive

app_settings = get_app_settings()

logger = logging.getLogger(__name__)

ping_check = APIRouter()


@ping_check.post("/start")
def run_ping_checks(target_hosts: TargetHosts, user: User = Depends(verify_token)):
    start_time = time.perf_counter()
    if len(target_hosts.hosts) == 0:
        return []
    if len(target_hosts.hosts) > app_settings.max_ping_check_host_limit:
        return {
            "error": f"Lenght of the host address list is larger than the max limit of {app_settings.max_ping_check_host_limit}"
        }
    results = asyncio.run(
        are_alive(
            addresses=target_hosts.hosts,
            count=target_hosts.count,
            interval=target_hosts.interval,
            timeout=target_hosts.timeout,
        )
    )
    elapsed = time.perf_counter() - start_time
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    # print(results)
    return results
