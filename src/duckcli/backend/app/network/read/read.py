import logging
from pyats_genie_command_parse import GenieCommandParse
from duckcli.backend.app.settings.settings import get_app_settings
from duckcli.backend.core.driver.ssh import NetmikoCli
from duckcli.backend.app.inventory.main import get_device
from duckcli.backend.core.utils import command_acl
from duckcli.backend.app.settings import settings

app_settings = get_app_settings()
# DONE: TODO: get the network device username and password from the os env # set docker build input params
USERNAME = app_settings.network_read_username
PASSWORD = app_settings.network_read_password
READ_CFG_TEMPLATE_BASE_DIR = app_settings.read_config_template_dir
SEND_READ_CMD_LIMIT = app_settings.max_read_command_set_limit
# TODO: config or oper data read func for SSH and netconf driver
# TODO: show run template examples
# TODO: add option - If genie parser is not avalable then try ttp template
logger = logging.getLogger(__name__)

PARSER_DEVICE_MAPPER = settings.GENIE_PARSER_DEVICE_MAPPER

# PARSER_DEVICE_MAPPER_ENUM = app_settings.ParserDeviceMapperEnum


def genie_cli_parser(cmd_obj):

    # time.sleep(360)
    """
    acl for command based on os type
    loop cmds list and get data
    store it as per the command as the results as list of dict [{hostname: host.xyz.com,cmd : show run , output: dict{}}]
    """
    results = []
    # print(cmd_obj)
    try:

        return _extracted_from_genie_cli_parser_14(cmd_obj, results)
    except Exception as error:
        # print(error)
        logger.error(error)
        results.append(
            {
                "error": str(error),
                "hostname": cmd_obj["hostname"],
                "commands": cmd_obj["commands"],
                "status": False,
            }
        )
        return {cmd_obj["hostname"]: results}


# TODO Rename this here and in `genie_cli_parser`
def _extracted_from_genie_cli_parser_14(cmd_obj, results):
    # print(cmd_obj["hostname"])
    device_data = get_device(hostname=cmd_obj["hostname"])
    # print(device_data)
    if len(device_data) == 0:
        log_message = {
            "hostname": cmd_obj["hostname"],
            "error": "device not in inventory DB",
        }
        logger.error(log_message)
        return log_message
    else:
        device = device_data[0]

    device_instance = NetmikoCli(
        device_type=device["osType"],
        host=device["hostname"],
        username=USERNAME,
        password=PASSWORD,
    )
    device_session = device_instance.connect()

    for cmd in cmd_obj["commands"]:

        validate_cmd = command_acl.read_command_acl(
            acl_pattern=settings.READ_COMMAND_ACL,
            command=str(cmd).strip(),
            hostname=cmd_obj["hostname"],
        )
        if not validate_cmd[0]:
            results.append(validate_cmd[1])
            continue
        cmd_response = device_instance.get_raw_command_output(
            device_session, command=str(cmd).strip()
        )
        # print(str(cmd).strip())
        if cmd_obj["rawFormat"]:
            results.append(
                {
                    "command": str(cmd).replace(" ", "_").strip(),
                    "response": cmd_response,
                    "hostname": cmd_obj["hostname"],
                    "status": True,
                }
            )
            continue
        # parser_device_type = PARSER_DEVICE_MAPPER[device["osType"]]
        os_type = device["osType"]
        parser_device_type = app_settings.parser_device_mapper[os_type].value
        # print(parser_device_type)
        parse_obj = GenieCommandParse(nos=parser_device_type)
        try:
            results.append(
                {
                    "command": str(cmd).replace(" ", "_").strip(),
                    "response": parse_obj.parse_string(
                        show_command=cmd, show_output_data=cmd_response
                    ),
                    "hostname": cmd_obj["hostname"],
                    "status": True,
                }
            )
        except Exception as cmd_err:
            log_message = {
                "command": str(cmd).replace(" ", "_"),
                "error": str(cmd_err),
                "hostname": cmd_obj["hostname"],
                "status": False,
            }

            results.append(log_message)
            logger.error(log_message)
    device_session.disconnect()
    return {cmd_obj["hostname"]: results}


def read_multithreading_wrapper(cmd_obj):
    # print(cmd_obj)
    return genie_cli_parser(cmd_obj=cmd_obj)
