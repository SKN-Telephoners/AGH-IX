import json
import os
import requests
import time
from daemon import runner


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



########################################################################################################################

    def status(self):
        return self.request_local("/status").json()

    def local_networks(self):
        return self.request_local("/network").json()

    def peers(self):
        return self.request_local("/peer").json()

    def controller(self):
        return self.request_local("/controller").json()

########################################################################################################################

    def get_local_network(self, nwid):
        return self.request_local("/network/" + nwid).json()

    def get_peer(self,ndid):
        return self.request_local("/peer" + ndid).json()

    def list_controller_networks(self):
        return self.request_local("/controller/network").json()

    def get_controller_network(self, nwid):
        return self.request_local("/controller/network/" + nwid).json()

    def get_controller_network_members(self, nwid):
        return self.request_local("/controller/network/" + nwid + "/member").json()

    def get_controller_network_member(self, nwid, ndid):
        return self.request_local("/controller/network/" + nwid + "/member/" + ndid).json()

########################################################################################################################

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
            "ipAssignments": ["192.168.2.2"],
            "noAutoAssignIps": False,
            "tags": [
                [
                    123,
                    456
                ]
            ]
        }
    }

    def post_node(self, nwid, ndid, active_bridge, authorized, ip_address, no_auto_assign):
        template = self.template
        template["ipAssignments"] = [str(ip_address)]
        template["activeBridge"] = bool(active_bridge)
        template["authorized"] = bool(authorized)
        template["noAutoAssignIps"] = bool(no_auto_assign)


        payload = json.dumps(template)
        return self.request_local("/controller/network/"+nwid+"/member/"+ndid, data=payload).json()


class Daemon():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            z = Zerotier_API()
            device_list = z.get_controller_network_members(z.prod_network).keys()
            if len(device_list) != z.device_count:
                new_clients = list(set(device_list) - set(z.device_list))
                z.device_list = device_list
                for i in new_clients:
                    z.post_node(z.prod_network, new_clients[i], "client"+str(int(z.device_count)+int(i)+1), "peering with client"+str(int(z.device_count)+int(i)+1), False, True, "10.21.37."+str(int(z.device_count)+int(i)+1), True)
                z.device_count = len(z.device_list)
                time.sleep(10)

app = Daemon()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
