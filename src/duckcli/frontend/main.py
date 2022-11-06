from rich import print
import typer

# client side CLi tools
from duckcli.frontend.settings.settings import get_settings
from duckcli.frontend.utils.main import get_server_status

# Frontend CLI apps
from duckcli.frontend.app.inventory.main import app as inventory_app
from duckcli.frontend.app.command.main import app as command_app
from duckcli.frontend.app.ping.main import app as pinger_app


cli_settings = get_settings()
STATUS_CHECK_URL = cli_settings.backend_status_check_url
server_status = {"status": None}
try:
    server_status = get_server_status(STATUS_CHECK_URL)
except Exception as error:
    print("[red]Backend server is not reachable.....[/red]")
    print(f"[yellow]{error}[/yellow]")
    exit(0)
if server_status["status"] != "alive":
    print("Backend server is not reachable.....")
    exit(0)


# Backend server (create new user and start the server)


# Main cmd entrypoint

main_app = typer.Typer()

main_app.add_typer(inventory_app, name="inventory")
main_app.add_typer(command_app, name="network")
main_app.add_typer(pinger_app, name="ping")


def main():
    main_app()
