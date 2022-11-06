import os
import sys
import logging


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import colorama


# from CRUD.authen import auth
# Core modules
from duckcli.backend.app.inventory.main import inventory_router
from duckcli.backend.core.auth.main import auth

from duckcli.backend.core.status.main import server_status
from duckcli.backend.core.settings.settings import get_core_settings


# UI modules
from duckcli.backend.UI.main import ui_app

# network read modules
from duckcli.backend.app.network.read.main import network_read

# network ping checks
from duckcli.backend.app.network.ping.main import ping_check

sys.dont_write_bytecode = True
core_settings = get_core_settings()
BASE_DIR = core_settings.base_dir
# print(BASE_DIR)

templates = Jinja2Templates(directory=f"{BASE_DIR}/src/duckcli/backend/UI/templates")

# logging.basicConfig(filename="server.log", level=logging.INFO)
logging.basicConfig(
    filename="server.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
cwd = os.getcwd()
logging.info(f"  os.getcwd() is {cwd}")
logger = logging.getLogger(__name__)
# print(cwd)
# print(constants.INVENTORY_FILE)
# print(constants.NETWORK_READ_USERNAME)
colorama.init()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI(docs_url="/api/docs", openapi_url="/api")
app.mount(
    "/static",
    StaticFiles(directory=f"{BASE_DIR}/src/duckcli/backend/UI/static"),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/auth")
app.include_router(inventory_router, prefix="/inventory")
app.include_router(network_read, prefix="/network")
app.include_router(ui_app, prefix="/ui")
app.include_router(server_status, prefix="/server")
app.include_router(ping_check, prefix="/ping")
logger.info("all api routers are loaded")


def main():
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        reload=True,
        port=9999,
        ssl_keyfile="key.key",
        ssl_certfile="cert.cer",
    )


if __name__ == "__main__":
    main()
