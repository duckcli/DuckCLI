from typing import Optional
import uvicorn
import urllib3
import typer
import requests
from duckcli.frontend.settings.settings import get_settings


urllib3.disable_warnings()


cli_settings = get_settings()

STATUS_CHECK_URL = cli_settings.backend_status_check_url


def get_server_status(url):
    response = requests.get(url=url, verify=cli_settings.verify_ssl_cert)
    return response.json()


app = typer.Typer()


@app.command()
def run_server(
    address: Optional[str] = "0.0.0.0",
    port: Optional[int] = 9999,
    verify: Optional[bool] = False,
):
    uvicorn.run(
        "server:app",
        host=address,
        reload=True,
        port=port,
        ssl_keyfile="key.key",
        ssl_certfile="cert.cer",
    )


if __name__ == "__main__":
    app()
