#!/usr/bin/env python3
import os

os.system("ip netns exec session rc-update add ovs-modules")
os.system("ip netns exec session rc-update add ovsdb-server")
os.system("ip netns exec session rc-update add ovs-vswitchd")
os.system("ip netns exec session rc-service ovs-modules start")
os.system("ip netns exec session rc-service ovs-vswitchd start")
os.system("/usr/share/openvswitch/scripts/ovs-ctl start")
