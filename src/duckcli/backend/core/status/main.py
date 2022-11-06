from fastapi import APIRouter


server_status = APIRouter()


@server_status.get("/status")
def status_response():
    return {"status": "alive"}
