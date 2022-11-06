# add \n to acl
def read_command_acl(acl_pattern, command, hostname):
    if acl_pattern.search(command):
        return True, {}
    status = False
    return status, {
        "error": "invalid read command",
        "command": str(command).replace(" ", "_"),
        "hostname": hostname,
        "status": False,
    }
