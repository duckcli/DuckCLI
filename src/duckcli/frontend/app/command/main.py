import time

import json


import requests
from typing import Optional
import typer
from rich.live import Live
from rich.console import Console
from rich.text import Text
from rich import print, print_json
from nested_lookup import nested_lookup

from duckcli.frontend.utils.auth import BackendAuth
from duckcli.frontend.settings.settings import get_settings


start = time.time()
cli_settings = get_settings()

TOKEN_ENDPOINT = cli_settings.backend_token_url
USERNAME = cli_settings.backend_username
PASSWORD = cli_settings.backend_password
CMD_URL = cli_settings.backend_network_read_url
auth = BackendAuth(token_url=TOKEN_ENDPOINT, username=USERNAME, password=PASSWORD)


def display_live_data(get_data_func):
    with Live(refresh_per_second=60) as live_data:
        while False:
            try:
                live_response = get_data_func()
                time.sleep(2)
                live_data.update(live_response)
            except Exception as error:
                print(error)


@auth.Decorators.refreshToken
def get_command_data(auth, data, url):
    # print(auth.access_token)
    headers = {"Authorization": f"Bearer {auth.access_token}"}
    response = requests.post(
        url=url, headers=headers, data=json.dumps(data), verify=False
    )
    return response.json()


app = typer.Typer()


GET_JOB_STATUS_ERROR = Text()
console = Console()


def raw_cmd_response(hostnames, data):
    for cmd_resp in data:
        for host in hostnames:
            if per_cmd_resp := cmd_resp.get(host):
                for cmd in per_cmd_resp:
                    # print(cmd)
                    if cmd["status"]:
                        console.print(
                            "----------------------------------------------------------"
                        )
                        console.print(
                            f"Command [bold magenta]{cmd['command']}[/bold magenta] response from device : [bold yellow]{cmd['hostname']}[/bold yellow] \n"
                        )
                        console.print(cmd["response"])
                    else:
                        console.print(
                            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        )
                        console.print(
                            f"Commands [bold magenta]{cmd['commands']}[/bold magenta] response from device : [bold red]{cmd['hostname']}[/bold red] \n"
                        )
                        console.print(cmd["error"])


def key_lookups(lookups, data):
    lookup_strs = lookups.split("|")
    for lookup_str in lookup_strs:
        lookup_value = nested_lookup(lookup_str, data)
        console.print(lookup_value)


@app.command()
def run_cmd(
    hostnames: str = typer.Option(...),
    commands: str = typer.Option(...),
    lookups: Optional[str] = typer.Option(None),
    raw_format: Optional[bool] = typer.Option(False),
    export: Optional[bool] = typer.Option(False),
):  # sourcery skip: low-code-quality
    start = time.time()
    commands = commands.split("|")
    hostnames = hostnames.split("|")
    command_set = [
        {"hostname": hostname, "commands": commands, "rawFormat": raw_format}
        for hostname in hostnames
    ]

    cmd_payload = {"send_commands": command_set}

    console = Console()
    # print(lookups)
    with console.status(
        "Gathering command output from the device.....\n\n"
    ) as cmd_response:
        data = get_command_data(auth=auth, data=cmd_payload, url=CMD_URL)
        # print(data)
        if raw_format:
            raw_cmd_response(hostnames=hostnames, data=data)
        elif lookups:
            key_lookups(lookups=lookups, data=data)
        else:
            print_json(json.dumps(data))
    cmd_response.update()
    end = time.time()

    if not export:
        console.print(
            "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        )
        console.print(
            f"All the above commands took a total of [bold yellow]{round(end - start)} seconds[/bold yellow] to run."
        )
        console.print(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        )


if __name__ == "__main__":
    app()
