import json
import os
from django.forms import NullBooleanField
import requests
import docker
import time


class Zerotier_API(object):
    def __init__(self):

        self.network_api_key = "Basic YWdoaXg6SmFjZWtSemFzYQ=="
        self.zerotierd_start()
        self.zerotierd_start()
        self.local_api_key = str(
            open("/var/lib/zerotier-one/authtoken.secret", "r").read().split("\n", 1)[0]
        )
        self.local_api = "http://172.32.0.1:9993"
        self.device_list = {}
        if len(self.local_networks()) == 0:
            self.prod_network = self.create_default_network()["id"]
            self.join_default_network()
            self.configure_default_network()
        else:
            self.prod_network = self.local_networks()[0]

        self.reset_local_zerotier_interface()

    def request_local(self, path, data=None):
        if data is None:
            return requests.get(
                self.local_api + path, headers={"X-ZT1-Auth": self.local_api_key}
            )
        else:
            return requests.post(
                self.local_api + path,
                headers={"X-ZT1-Auth": self.local_api_key},
                data=data,
            )

    def status(self):
        return self.request_local("/status").json()

    def local_networks(self):
        return self.request_local("/controller/network").json()

    def get_interface_name(self):
        return self.request_local(f"/network/{self.prod_network}").json()[
            "portDeviceName"
        ]

    def peers(self):
        return self.request_local("/peer").json()

    def controller(self):
        return self.request_local("/controller").json()

    def get_local_network(self):
        return self.request_local(f"/controller/network/{self.prod_network}").json()

    def get_local_did(self):
        return self.status()["address"]

    def get_peer(self, ndid):
        return self.request_local(f"/peer/{ndid}").json()

    def list_controller_networks(self):
        return self.request_local("/controller/network").json()

    def get_controller_network(self):
        return self.request_local(f"/controller/network/{self.prod_network}").json()

    def get_controller_network_members(self):
        return self.request_local(
            f"/controller/network/{self.prod_network}/member"
        ).json()

    def get_controller_network_member(self, ndid):
        return self.request_local(
            f"/controller/network/{self.prod_network}/member/{ndid}"
        ).json()

    template = {
        "hidden": False,
        "name": "generic name",
        "noAutoAssignIps": False,
        "description": "generic description",
        "authorized": True,
        "config": {
            "activeBridge": False,
            "authorized": True,
            "capabilities": [0],
            "ipAssignments": [],
            "noAutoAssignIps": False,
            "tags": [["AGH-IX"]],
        },
    }

    def post_node_connect(self, ndid):
        template = self.template
        payload = json.dumps(template)
        return self.request_local(
            f"/controller/network/{self.prod_network}/member/{ndid}", data=payload
        ).json()

    def post_node(self, ndid, active_bridge, authorized, ip_address, no_auto_assign):
        template = self.template
        template["ipAssignments"] = [str(ip_address)]
        template["activeBridge"] = bool(active_bridge)
        template["authorized"] = bool(authorized)
        template["noAutoAssignIps"] = bool(no_auto_assign)

        payload = json.dumps(template)
        return self.request_local(
            f"/controller/network/{self.prod_network}/member/{ndid}", data=payload
        ).json()

    def reset_local_zerotier_interface(self):
        self.zerotierd_start()
        self.zerotier_join_leave_local_network("leave")
        self.zerotier_join_leave_local_network("join")
        time.sleep(3)
        self.ifname = self.get_interface_name()
        self.bridge_add_rm_interface("addif", "br2137", self.ifname)

    def join_default_network(self):
        self.zerotierd_start()
        self.zerotier_join_leave_local_network("join")
        time.sleep(3)
        self.ifname = self.get_interface_name()
        self.bridge_add("br2137")
        print(self.ifname)
        self.bridge_add_rm_interface("addif", "br2137", self.ifname)
        self.local_did = self.get_local_did()
        self.interface_on_off("br2137", "up")
        self.post_node(self.local_did, True, True, "10.44.0.1", True)

    def deauth(self, ndid):
        template = self.template
        template["authorized"] = False
        payload = json.dumps(template)
        return self.request_local(
            f"/controller/network/{self.prod_network}/member/{ndid}", data=payload
        ).json()

    def create_default_network(self):
        return requests.post(
            "http://172.32.0.1:9993/controller/network/"
            + str(self.get_local_did())
            + "______",
            headers={"X-ZT1-Auth": self.local_api_key},
            data="{}",
        ).json()

    def configure_default_network(self):
        requests.post(
            "http://172.32.0.1:9993/controller/network/" + str(self.prod_network),
            headers={"X-ZT1-Auth": self.local_api_key},
            data='{"ipAssignmentPools": [{"ipRangeStart": "10.44.128.1", "ipRangeEnd": "10.44.255.254"}], "routes": [{"target": "10.44.0.0/16", "via": null}], "v4AssignMode": "zt", "private": true }',
        ).json()

    def zerotierd_start(self):
        url = "http://172.32.0.1:5000/commands/zerotierone"
        payload = json.dumps({"force_unique_key": True})
        headers = {
            "Authorization": "Basic YWdoaXg6SmFjZWtSemFzYQ==",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def zerotier_join_leave_local_network(self, state):
        url = "http://172.32.0.1:5000/commands/zerotier"
        payload = json.dumps(
            {"args": [f"{state}", f"{self.prod_network}"], "force_unique_key": True}
        )
        headers = {
            "Authorization": "Basic YWdoaXg6SmFjZWtSemFzYQ==",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def interface_on_off(self, interface, state):
        url = "http://172.32.0.1:5000/commands/ifconfig"
        payload = json.dumps(
            {"args": [f"{interface}", f"{state}"], "force_unique_key": True}
        )
        headers = {
            "Authorization": "Basic YWdoaXg6SmFjZWtSemFzYQ==",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def bridge_add(self, name):
        url = "http://172.32.0.1:5000/commands/brctl"
        payload = json.dumps({"args": ["addbr", f"{name}"], "force_unique_key": True})
        headers = {
            "Authorization": "Basic YWdoaXg6SmFjZWtSemFzYQ==",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

    def bridge_add_rm_interface(self, command, brname, ifname):
        url = "http://172.32.0.1:5000/commands/brctl"
        payload = json.dumps(
            {"args": [f"{command}", f"{brname}", f"{ifname}"], "force_unique_key": True}
        )
        headers = {
            "Authorization": "Basic YWdoaXg6SmFjZWtSemFzYQ==",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
