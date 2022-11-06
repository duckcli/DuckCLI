# DuckCLI  - Alpha release

It's main feature is to provide ✨ Network CLI interface ✨ in the Terminal**duck-cli**.


You can  locally build and  install **DuckCLI** uisng poerty, and run your program with the `duck-cli` command in your Terminal, and it will provide CLI interface to your network, system and inventory backends.

You can also use **DuckCLI** to generate  **duck-cli**  📝.

## Usage

### Install using Poetry

Install **DuckCLI**:

<div class="termy">

```console

git clone https://github.com/duckcli/DuckCLI.git
git checkout duckcli-v2-dev
cd DuckCLI
$ poerty build
$ poerty install 
---> 100%
Successfully installed DuckCLI
```

### Install using setup tools
python setup.py sdist

pip install dist/duckcli-*

### setup admin user 

```console
cd DuckCLI
Activate python venv :  poerty shell

 Usage: duck-cli-admin create-user [OPTIONS] USERNAME PASSWORD EMAIL --is-superuser

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *username      TEXT  [default: None] [required]                                                                      │
│*    password      TEXT  [default: None] [required]                                                                      │
│ *    email         TEXT  [default: None] [required]                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --is-superuser    --no-is-superuser      [default: no-is-superuser]                                                      │
│ --help                                   Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### Set Backend and frontend CLI ENV vars

```console
**set these env vars on your backend server**
export duckcli_app_network_read_username="xxxxx" # set your read-only network username
export duckcli_app_network_read_password="xxxxxxx"
export duckcli_jwt_secret_key="xxxxxxxxxxxxxxxxxxxxxxx"  # must be 64 chr/256bits

** on your CLI client machine set these env vars

export duckcli_backend_username="xxxxxx"
export duckcli_backend_password="xxxxx"

**if backend is running on a diffrent machine then set these env vars on your client Machine**
export duckcli_backend_inventory_url="https://<host-ip-address>:9999/inventory/device"
export duckcli_backend_token_url="https://<host-ip-address>:9999/auth/login"
export duckcli_backend_ping_check_url: str = "https://<host-ip-address>:9999/ping/start"
export duckcli_backend_status_check_url: str = "https://<host-ip-address>:9999/server/status"
export duckcli_backend_ping_check_url: str = "https://<host-ip-address>:9999/ping/start"

```

### Start the backend server 

```console

cd DuckCLI

Activate python venv :  poerty shell

python server.py

Note: icmplib requires Root privileges to create the socket; hence you may need to run the server as sudo user or give the correct permission for the logged-in user.
----
raise SocketPermissionError(privileged)
icmplib.exceptions.SocketPermissionError: Root privileges are required to create the socket
----

```
### Example CLI commands

```console
--
duck-cli inventory device-info --hostname "*cisco.com"
duck-cli inventory device-info --site-id sandbox
duck-cli inventory device-info --os-type cisco_xr
duck-cli inventory device-info --os-type cisco_xr --export
--
* duck-cli network  run-cmd --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version|show interfaces description|show inventory" 
* duck-cli network  run-cmd  --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version"  --raw-format
* duck-cli network  run-cmd --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version|show interfaces description|show inventory" --lookups "GigabitEthernet0/0/0/0"
* duck-cli network  run-cmd  --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version" --export

----
* duck-cli ping pinger --hostname "inetgw" --count 5
* duck-cli ping pinger --hostname "inetgw" --count 5 --live
* duck-cli ping pinger --hostnames "192.168.0.1|192.168.0.2" --count 5 --live --no-inventory
* duck-cli ping pinger --hostnames "192.168.0.1|192.168.0.2" --count 5 --no-inventory
---
```
