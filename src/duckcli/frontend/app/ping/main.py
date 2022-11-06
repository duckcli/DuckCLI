import time
import json
import typer
from typing import Optional
from rich.live import Live
from rich.console import Console
import requests


from duckcli.frontend.app.inventory.main import get_inventory_data
from duckcli.frontend.utils.auth import BackendAuth
from duckcli.frontend.settings.settings import get_settings
from duckcli.frontend.app.ping.view import (
    generate_pingcheck_table,
    make_ping_check_layout,
    Header,
)


cli_settings = get_settings()
TOKEN_ENDPOINT = cli_settings.backend_token_url
USERNAME = cli_settings.backend_username
PASSWORD = cli_settings.backend_password
INVENTORY_URL = cli_settings.backend_inventory_url
auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)

app = typer.Typer()

layout = make_ping_check_layout()
layout["header"].update(Header())


@auth.Decorators.refreshToken
def get_ping_responses(auth, url, api_payload=None):
    if api_payload is None:
        api_payload = []
    try:
        headers = {"Authorization": f"Bearer {auth.access_token}"}
        response = requests.post(
            url=url, headers=headers, data=json.dumps(api_payload), verify=False
        )
        return response.json()
    except Exception as error:
        print(error)
        return []


PING_URL = cli_settings.backend_ping_check_url


# TODO: fix live table refresh delay issues - get inital data response
# TODO - enable ping for multiple hosts when using inventory DB
@app.command()
def pinger(
    hostname: str = None,
    site_id: Optional[str] = typer.Option(
        None, help="Use the site ID to get the list of devices from the inventory DB"
    ),
    live: bool = False,
    count: Optional[int] = 1,
    interval: Optional[int] = 1,
    inventory: bool = typer.Option(
        True, help="Use the inventory DB to get mgmt IPs of the hosts"
    ),
):
    ping_response = [
        {
            "address": "Collecting host info....please wait !!!",
            "is_alive": "Checking.....",
            "avg_rtt": 0,
            "min_rtt": 0,
            "max_rtt": 0,
            "packets_sent": 0,
            "packets_received": 0,
            "jitter": 0,
        }
    ]
    inventory_data = []
    hosts = []
    # Get the host mgmtIP to run the ping test

    if hostname and inventory:
        get_url = f"{INVENTORY_URL}?hostname={hostname}"
    elif site_id and inventory:
        get_url = f"{INVENTORY_URL}?site_id={site_id}"

    if inventory:
        inventory_data = get_inventory_data(auth=auth, url=get_url)
    else:
        hosts = hostname.split("|")
    # print(hosts)
    if len(inventory_data) == 0 and inventory:
        return {"error": "Host list is empty"}
    hosts.extend(
        device["mgmtIp"] for device in inventory_data if device["mgmtIp"] is not None
    )

    api_input_parms = {"hosts": hosts, "count": count, "interval": interval}
    console = Console()
    if live:

        layout["Ping"].update(generate_pingcheck_table(ping_response=ping_response))
        with Live(layout, refresh_per_second=10, screen=True):
            try:
                while True:
                    time.sleep(1)
                    layout["Ping"].update(
                        generate_pingcheck_table(ping_response=ping_response)
                    )
                    ping_response = get_ping_responses(
                        auth=auth, url=PING_URL, api_payload=api_input_parms
                    )
            except Exception as error:
                console.print(error, ping_response)

    else:

        with console.status("\n Running ping checks-----> \n") as ping_check:
            try:
                ping_response = get_ping_responses(
                    auth=auth, url=PING_URL, api_payload=api_input_parms
                )
                console.print(generate_pingcheck_table(ping_response=ping_response))
                print("\n")
                ping_check.update()
            except Exception as error:
                console.print(error, ping_response)
    return ping_response


if __name__ == "__main__":
    app()
