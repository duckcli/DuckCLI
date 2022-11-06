import time
import re
import json
from enum import Enum
import typer
from typing import Optional

from rich.console import Console
from rich.text import Text

import requests

from duckcli.frontend.app.inventory.view import generate_inventory_table
from duckcli.frontend.utils.auth import BackendAuth
from duckcli.frontend.settings.settings import get_settings


cli_settings = get_settings()

start = time.time()


class ExportTypes(str, Enum):
    JSON = "json"
    YAML = "yaml"
    csv = "csv"


class SearchTypes(str, Enum):
    site_id = "site_id"
    os_type = "os_type"
    hostname = "hostname"


TOKEN_ENDPOINT = cli_settings.backend_token_url
USERNAME = cli_settings.backend_username
PASSWORD = cli_settings.backend_password
INVENTORY_URL = cli_settings.backend_inventory_url
auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)
# session.query(...).limit(page_size).offset(skip)


@auth.Decorators.refreshToken
def get_inventory_data(auth, url, wildcard_search=None):
    headers = {"Authorization": f"Bearer {auth.access_token}"}
    response = requests.get(
        url=url, headers=headers, verify=cli_settings.verify_ssl_cert
    )
    if wildcard_search:
        results = []
        for item in response.json():
            try:
                search_pattern = re.compile(r"{0}".format(wildcard_search))
                search_result = search_pattern.search(item["hostname"])
                if search_result:
                    # print(item)
                    results.append(item)
            except Exception as error:
                print(error)
        return results
    return response.json()


app = typer.Typer()


GET_STATUS_ERROR = Text()
console = Console()
# srch = re.compile(r'[*+]$')
# b = srch.search('sds**sd*')


@app.command()
def device_info(
    hostname: Optional[str] = typer.Option(None),
    os_type: Optional[str] = typer.Option(None),
    site_id: Optional[str] = typer.Option(None),
    export: Optional[bool] = typer.Option(False),
):
    data = {}
    wc_hostname = None
    whildcard_search_result = None
    if hostname:
        whildcard_search_pattern = re.compile(r"^[*]|[*]$")
        whildcard_search_result = whildcard_search_pattern.search(hostname)
    # print(whildcard_search_result)
    if whildcard_search_result and hostname:
        wc_hostname = str(hostname).replace("*", "")
        # print(wc_hostnames)
        data = get_inventory_data(
            auth=auth, url=f"{INVENTORY_URL}", wildcard_search=wc_hostname
        )
    elif site_id:
        data = get_inventory_data(
            auth=auth,
            url=f"{INVENTORY_URL}?site_id={site_id}",
            wildcard_search=wc_hostname,
        )
    elif os_type:
        data = get_inventory_data(
            auth=auth,
            url=f"{INVENTORY_URL}?os_type={os_type}",
            wildcard_search=wc_hostname,
        )
    elif hostname:
        data = get_inventory_data(
            auth=auth,
            url=f"{INVENTORY_URL}?hostname={hostname}",
            wildcard_search=wc_hostname,
        )
    else:
        # data = get_inventory_data(auth=auth,url=f"{INVENTORY_URL}",wildcard_search=wc_hostname)
        data = []
    if export:
        print(json.dumps(data))
        return data
    else:
        console = Console()
        with console.status("\n Gathering  inventory data") as inventory:
            console.print(generate_inventory_table(inventory=data))
            inventory.update()


# TDOD: Update search based on keys
@app.command()
def get_inventory(
    hostname: Optional[str] = None,
    export: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    console = Console()
    with console.status("\n Gathering inventory data") as inventory:
        data = get_inventory_data(auth=auth, url=INVENTORY_URL)
        console.print(generate_inventory_table(inventory=data))
        inventory.update()


if __name__ == "__main__":
    app()
