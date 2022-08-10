import json
import os
from django.forms import NullBooleanField
import requests
import docker

class Zerotier_API(object):
    def __init__(self):

        self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
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
        if data == None:
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
        container = self.client.containers.get("zerotier-controller")
        container.exec_run("zerotier-cli leave " + str(self.prod_network))
        container.exec_run("zerotier-cli join " + str(self.prod_network))


    def join_default_network(self):
        self.local_did = self.get_local_did()
        container = self.client.containers.get("zerotier-controller")
        container.exec_run("zerotier-cli join " + str(self.prod_network))
        self.ifname = self.get_interface_name()
        container.exec_run("brctl addbr br2137")
        container.exec_run(f"brctl addif br2137 " + str(self.ifname))
        container.exec_run("ifconfig br2137 up")
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
