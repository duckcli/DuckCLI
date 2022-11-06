from fastapi import HTTPException
from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from duckcli.backend.core.auth.login_forms import LoginForm

# App modules
from duckcli.backend.core.driver.database import sqlite_db
from duckcli.backend.app.inventory.main import get_device
from duckcli.backend.core.settings.settings import get_core_settings

from duckcli.backend.core.auth.main import login
from duckcli.backend.core.auth.schemas import User

core_settings = get_core_settings()
db_connection = sqlite_db(url=core_settings.db_url)

BASE_DIR = core_settings.base_dir

ui_app = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=f"{BASE_DIR}/src/duckcli/backend/UI/templates")


@ui_app.get("/login/")
def login1(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@ui_app.post("/login2/")
def login2(request: Request, db: sqlite_db = Depends(User)):
    print(request)
    form = LoginForm(request)
    print(form)
    form.load_data()
    if form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("login.html", form.__dict__)
            login(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


# Test UI endpoint
@ui_app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@ui_app.get("/inventory/{hostname}", response_class=HTMLResponse)
async def read_inventory(request: Request, hostname: str):
    return templates.TemplateResponse(
        "base.html", {"request": request, "hostname": hostname}
    )


# Get Inventory UI endpoint
@ui_app.get("/inventory", response_class=HTMLResponse)
async def retrieve_all_devices(
    request: Request,
):  # current_user: User = Depends(verify_token)):
    # DONE: add fetch limit per qry - 500
    # devices_db = db_connection.execute(Devices.select()).fetchall()
    # convert response into Dict
    # [dict(row) for row in devices_db]
    devices = get_device()
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "devices": devices}
    )
