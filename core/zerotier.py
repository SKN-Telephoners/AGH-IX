import json
import os
import requests

class Zerotier_API(object):

    def __init__(self):
        self.local_api_key = os.getenv('ZEROTIER_API_KEY')
        self.local_api = "http://localhost:9993"
        self.device_list = {}
        self.prod_network = os.getenv('ZEROTIER_NETWORK')
        self.device_count = None


    def request_local(self, path, data=None):
        if data == None:
            return requests.get(self.local_api + path, headers={'X-ZT1-Auth':self.local_api_key})
        else:
            return requests.post(self.local_api + path, headers={'X-ZT1-Auth':self.local_api_key}, data=data)

    def status(self):
        return self.request_local("/status").json()

    def local_networks(self):
        return self.request_local("/network").json()

    def peers(self):
        return self.request_local("/peer").json()

    def controller(self):
        return self.request_local("/controller").json()

    def get_local_network(self, nwid):
        return self.request_local(f'/network/{nwid}').json()

    def get_peer(self,ndid):
        return self.request_local(f'/peer/{ndid}').json()

    def list_controller_networks(self):
        return self.request_local("/controller/network").json()

    def get_controller_network(self, nwid):
        return self.request_local(f'/controller/network/{nwid}').json()

    def get_controller_network_members(self, nwid):
        return self.request_local(f'/controller/network/{nwid}/member').json()

    def get_controller_network_member(self, nwid, ndid):
        return self.request_local(f'/controller/network/{nwid}/member/{ndid}').json()

    template = {
        "hidden": False,
        "name": "generic name",
        "description": "generic description",
        "config": {
            "activeBridge": False,
            "authorized": True,
            "capabilities": [
                0
            ],
            "ipAssignments": ["0.0.0.0"],
            "noAutoAssignIps": False,
            "tags": [
                [
                    "AGH-IX"
                ]
            ]
        }
    }

    def post_node(self, ndid):
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}', data=json.dumps(self.template)).json()

    def post_node(self, ndid, active_bridge, authorized, ip_address, no_auto_assign):
        template = self.template
        template["ipAssignments"] = [str(ip_address)]
        template["activeBridge"] = bool(active_bridge)
        template["authorized"] = bool(authorized)
        template["noAutoAssignIps"] = bool(no_auto_assign)

        payload = json.dumps(template)
        return self.request_local(f'/controller/network/{self.prod_network}/member/{ndid}', data=payload).json()
