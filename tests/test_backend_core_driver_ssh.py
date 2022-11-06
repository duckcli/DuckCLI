# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import duckcli.backend.core.driver.ssh
from hypothesis import given, strategies as st


@given(device_type=st.text(), host=st.text(), username=st.text(), password=st.text())
def test_fuzz_NetmikoCli(device_type, host, username, password):
    duckcli.backend.core.driver.ssh.NetmikoCli(
        device_type=device_type, host=host, username=username, password=password
    )
