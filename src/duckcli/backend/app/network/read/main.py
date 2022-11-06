import logging
from fastapi import APIRouter, Depends
from duckcli.backend.app.settings.settings import get_app_settings
from duckcli.backend.core.auth.main import verify_token
from duckcli.backend.core.auth.schemas import User
from duckcli.backend.app.network.read.schemas import NetworkRead
from duckcli.backend.app.network.read.read import read_multithreading_wrapper
from duckcli.backend.core.utils.multiprocessing import multi_processing

app_settings = get_app_settings()
logger = logging.getLogger(__name__)
SEND_READ_CMD_LIMIT = app_settings.max_read_command_set_limit
MULTIPROCESSING_THREADPOOL_LIMIT = app_settings.multiprocessing_threadpool_limit
network_read = APIRouter()


@network_read.post("/read/genie")
def network_get(network_read: NetworkRead, user: User = Depends(verify_token)):
    # print(network_read.dict(exclude_none=True))
    """
    create of func to run and add this to the MT que
    add multiprocessing

    """
    request_body = network_read.dict(exclude_none=True)
    if len(request_body.get("send_commands")) == 0:
        log_message = {
            "info": "no command to run, POST payload send_commands list is empty"
        }
        logger.info(log_message)
        return log_message
    elif len(request_body.get("send_commands")) > SEND_READ_CMD_LIMIT:
        log_message = {
            "info": f'Max send_command per request limit is set to {SEND_READ_CMD_LIMIT} and payload has {len(request_body.get("send_commands"))} command sets'
        }
        logger.info(log_message)
        return log_message

    return multi_processing(
        pool_limit=MULTIPROCESSING_THREADPOOL_LIMIT,
        wrapper_func=read_multithreading_wrapper,
        func_values=request_body["send_commands"],
    )
