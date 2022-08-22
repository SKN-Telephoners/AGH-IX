#!/usr/bin/env python3
import sys, os

os.system(
    "ip netns exec session zerotier-cli -D/var/lib/zerotier-one leave "
    + f"{sys.argv[1]}"
)
os.system(
    "ip netns exec session zerotier-cli -D/var/lib/zerotier-one join "
    + f"{sys.argv[1]}"
)
os.system("ip netns exec session ovs-vsctl add-port lan " + f"{sys.argv[2]} " + "&")
