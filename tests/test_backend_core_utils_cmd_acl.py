# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.


import duckcli.backend.core.utils.command_acl
from hypothesis import given, settings, strategies as st
import re


# TODO: replace st.nothing() with appropriate strategies
cmd_acl_pattern = [re.compile(r"^(show |display |admin display )")]
hostname_pattern = r"^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$"


@given(
    acl_pattern=st.sampled_from(cmd_acl_pattern),
    command=st.text(),
    hostname=st.from_regex(hostname_pattern),
)
@settings(max_examples=25)
def test_fuzz_read_command_acl(acl_pattern, command, hostname):
    duckcli.backend.core.utils.command_acl.read_command_acl(
        acl_pattern=acl_pattern, command=command, hostname=hostname
    )
