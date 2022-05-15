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

    def get_local_network(self):
        return self.request_local(f'/network/{self.prod_network}').json()
    
    def get_local_did(self):
        return self.status()["address"]

    def get_peer(self,ndid):
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
    
    def create_default_network(self):
        return requests.post("http://localhost:9993/controller/network/"+str(self.get_local_did())+"210645", headers={'X-ZT1-Auth':self.local_api_key}, data='{"ipAssignmentPools": [{"ipRangeStart": "10.21.37.10", "ipRangeEnd": "10.21.37.254"}], "routes": [{"target": "10.21.37.1/24", "via": null}], "v4AssignMode": "zt", "private": true }')

