# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.app.network.read.read
from hypothesis import given, strategies as st


# TODO: replace st.nothing() with appropriate strategies


TEST_DATA = [
    {
        "hostname": "sandbox-iosxr-1-dummy",
        "commands": ["show version"],
    }
]


@given(cmd_obj=st.sampled_from(TEST_DATA))
# @example(cmd_obj=TEST_DATA)
def test_fuzz_genie_cli_parser(cmd_obj):
    duckcli.backend.app.network.read.read.genie_cli_parser(cmd_obj=cmd_obj)
