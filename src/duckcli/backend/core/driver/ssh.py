#!/usr/bin/env python
from netmiko import ConnectHandler


class NetmikoCli:
    def __init__(
        self, device_type: str, host: str, username: str, password: str
    ) -> None:
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password

        self.device = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
        }

    def connect(self):
        return ConnectHandler(**self.device)

    def get_raw_command_output(self, session, command):
        return session.send_command(command)

    def get_ttp_parsed_output(self, session, command, ttp_template):
        return session.send_command(command, use_ttp=True, ttp_template=ttp_template)
