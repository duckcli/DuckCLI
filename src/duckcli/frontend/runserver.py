import os
import sys
from typing import Optional
import uvicorn

BASE_DIR = os.getcwd()
# print(BASE_DIR)
sys.path.append(f"{BASE_DIR}")


def main(
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
