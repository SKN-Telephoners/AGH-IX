import json

import requests


class Zerotier_API(object):

    def __init__(self):
        self.local_api_key = str(open("/var/lib/zerotier-one/authtoken.secret", "r").read().split('\n', 1)[0])
        self.local_api = "http://zerotier:9993"
        self.device_list = {}
        if len(self.local_networks()) == 0:
            self.prod_network = self.create_default_network()["id"]
        else:
            self.prod_network = self.local_networks()[0]
        self.device_count = None

    def request_local(self, path, data=None):
        if data is None:
            return requests.get(self.local_api + path, headers={'X-ZT1-Auth': self.local_api_key})
        else:
            return requests.post(self.local_api + path, headers={'X-ZT1-Auth': self.local_api_key}, data=data)

    def status(self):
        return self.request_local("/status").json()

    def local_networks(self):
        return self.request_local("/controller/network").json()

    def peers(self):
        return self.request_local("/peer").json()

    def controller(self):
        return self.request_local("/controller").json()

    def get_local_network(self):
        return self.request_local(f'/controller/network/{self.prod_network}').json()

    def get_local_did(self):
        return self.status()["address"]

    def get_peer(self, ndid):
        return self.request_local(f'/peer/{ndid}').json()

    def list_controller_networks(self):
        return self.request_local("/controller/network").json()

    def get_controller_network(self):
        return self.request_local(f'/controller/network/{self.prod_network}').json()

    def get_controller_network_members(self):
        return self.request_local(f'/controller/network/{self.prod_network}/member').json()

    def get_controller_network_member(self, ndid):
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}').json()

    template = {
        "hidden": False,
        "name": "generic name",
        "noAutoAssignIps": False,
        "description": "generic description",
        "authorized": True,
        "config": {
            "activeBridge": False,
            "authorized": True,
            "capabilities": [
                0
            ],
            "ipAssignments": [],
            "noAutoAssignIps": False,
            "tags": [
                [
                    "AGH-IX"
                ]
            ]
        }
    }

    def post_node_connect(self, ndid):
        template = self.template
        payload = json.dumps(template)
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}', data=payload).json()

    def post_node(self, ndid, active_bridge, authorized, ip_address, no_auto_assign):
        template = self.template
        template["ipAssignments"] = [str(ip_address)]
        template["activeBridge"] = bool(active_bridge)
        template["authorized"] = bool(authorized)
        template["noAutoAssignIps"] = bool(no_auto_assign)

        payload = json.dumps(template)
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}', data=payload).json()

    def deauth(self, ndid):
        template = self.template
        template["authorized"] = False
        payload = json.dumps(template)
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}', data=payload).json()

    def create_default_network(self):
        return requests.post("http://zerotier:9993/controller/network/" + str(self.get_local_did()) + "______",
                             headers={'X-ZT1-Auth': self.local_api_key},
                             data='{"ipAssignmentPools": [{"ipRangeStart": "10.21.37.1", "ipRangeEnd": "10.21.29.254"}], "routes": [{"target": "10.21.36.0/22", "via": null}], "v4AssignMode": "zt", "private": true }').json()
