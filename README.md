# DuckCLI  - Alpha release

Its main feature is to provide a CLI interface to run ✨ Network CLI commands ✨ on multiple remote devices via a DuckCLI API backend server.


You can  locally build and  install **DuckCLI** uisng Poerty, and run your cli commands with the `duck-cli` command in your Terminal, and it will provide CLI interface to your network, system and inventory backends.

## Usage

### Install using Poetry

Install **DuckCLI**:

note: You need to install Poetry on your build machine

<https://python-poetry.org/docs/#installation>


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

### Install using setup tools [!! not tested but this should work !!]
python setup.py sdist

pip install dist/duckcli-*

### setup admin user 

```console
cd DuckCLI
Activate python venv :  poerty shell


Example: 

duck-cli-admin create-user admin Password123! dem123@duckcli.com --is-superuser


-----
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
# DuckCLI/src/duckcli/backend/app/settings/settings.py
export duckcli_app_network_read_username="xxxxx" # set your read-only network username. default is - admin
export duckcli_app_network_read_password="xxxxxxx" # default is C1sco12345
#DuckCLI/src/duckcli/backend/core/settings/settings.py
export duckcli_jwt_secret_key="xxxxxxxxxxxxxxxxxxxxxxx"  # must be 64 chr/256bits. 
Note:  For testing & dev jwt secret key  is randomly generated inside settings.py file ---> comment out the generate function and set the key as env var

** on your CLI client machine set these env vars

export duckcli_backend_username="xxxxxx"
export duckcli_backend_password="xxxxx"

**if backend is running on a diffrent machine then set these env vars on your client Machine**
export duckcli_backend_inventory_url="https://<host-ip-address>:9999/inventory/device"
export duckcli_backend_token_url="https://<host-ip-address>:9999/auth/login"
export duckcli_backend_ping_check_url="https://<host-ip-address>:9999/ping/start"
export duckcli_backend_status_check_url= "https://<host-ip-address>:9999/server/status"
export duckcli_backend_network_read_url="https://host-ip-address>9999/network/read/genie"


```

### Start the backend server 

```console

cd DuckCLI

Activate python venv :  poerty shell

Add ssl cert and key path in server.py -
        ssl_keyfile="key.key"
        ssl_certfile="cert.cer"

--Creating a self-signed cert ----
openssl req -x509 -nodes -days 1000 -newkey rsa:2048 -keyout  key.key -out cert.cer
--------------------
-- Run server
python server.py

Note: icmplib requires Root privileges to create the socket; hence you may need to run the server as sudo user or give the correct permission for the logged-in user.
----
raise SocketPermissionError(privileged)
icmplib.exceptions.SocketPermissionError: Root privileges are required to create the socket
----

```

### Add your network device to the inventory DB

```console
Open Postman or any API dev tool
# Get auth token 
POST https://localhost:9999/auth/login
Set these body parms
-----
x-www-from-urlencoded 
Key :username
value: admin 
key: password
vlaue : Password123!  
--

# Create a new device 

POST https://localhost:9999/inventory/device

authorization: Bearer Token  [copy-paste the token from the auth response]

Body type:  raw / JSON

{
        "hostname": "sandbox-iosxr-1.cisco.com",
        "vendor": "Cisco",
        "model": "xrv",
        "osType": "cisco_xr",
        "mgmtIp": "131.226.217.150",
        "driverType": "ssh",
        "siteId": "sandbox"
    }

# Check if the device is added to the DB 

GET https://localhost:9999/inventory/device

```

### Example CLI commands

```console
Open a new terminal
cd DuckCLI

Activate python venv :  poerty shell
Set client machine env vars

Example: 
export duckcli_backend_username="admin"
export duckcli_backend_password="Password123!"

--
* duck-cli inventory device-info --hostname "*cisco.com"
* duck-cli inventory device-info --site-id sandbox
* duck-cli inventory device-info --os-type cisco_xr
* duck-cli inventory device-info --os-type cisco_xr --export
--
* duck-cli network  run-cmd --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version|show interfaces description|show inventory" 
* duck-cli network  run-cmd  --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version"  --raw-format
* duck-cli network  run-cmd --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version|show interfaces description|show inventory" --lookups "GigabitEthernet0/0/0/0"
* duck-cli network  run-cmd  --hostnames "sandbox-iosxr-1.cisco.com|sandbox-iosxr-2.cisco.com" --commands "show version" --export

----
* duck-cli ping pinger --hostname "inetgw" --count 5
* duck-cli ping pinger --hostname "inetgw" --count 5 --live
* duck-cli ping pinger --hostname "192.168.0.1|192.168.0.2" --count 5 --live --no-inventory
* duck-cli ping pinger --hostname "192.168.0.1|192.168.0.2" --count 5 --no-inventory
---
```
