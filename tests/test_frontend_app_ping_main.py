# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import duckcli.frontend.app.ping.main
from hypothesis import given, settings, strategies as st

# TODO hostname validation does not work   -- Fix


@given(
    hostname=st.sampled_from(["duckcli.com"]),
    site_id=st.one_of(st.text()),
    live=st.sampled_from([False]),
    count=st.sampled_from([1]),
    interval=st.sampled_from([1]),
    inventory=st.sampled_from([False]),
)
@settings(max_examples=1)
def test_fuzz_pinger(hostname, site_id, live, count, interval, inventory):
    duckcli.frontend.app.ping.main.pinger(
        hostname=hostname,
        site_id=site_id,
        live=live,
        count=count,
        interval=interval,
        inventory=inventory,
    )
