import json
import requests
import time
from daemon import runner


class Zerotier_API(object):

    def __init__(self, local_api_key, central_api_key):
        self.local_api_key = str(local_api_key)
        self.central_api_key = str(central_api_key)
        self.local_api = "http://localhost:9993"
        self.central_api = "https://my.zerotier.com/api/v1/"
        self.device_list = {}
        self.prod_network = "b94f532ca08af24a"
        self.device_count = None


    def request_local(self, path, data=None):
        if data == None:
            return requests.get(self.local_api + path, headers={'X-ZT1-Auth':self.local_api_key})
        else:
            return requests.post(self.local_api + path, headers={'X-ZT1-Auth':self.local_api_key}, data=data)

    def request_central(self, path, data=None):
        if data == None:
            return requests.get(self.central_api + path, headers={'Authorization': 'Bearer ' + self.central_api_key})
        else:
            return requests.post(self.central_api + path, headers={'Authorization': 'Bearer ' + self.central_api_key}, data=data)



########################################################################################################################

    def status(self):
        return self.request_local("/status").json() #okej

    def local_networks(self):
        return self.request_local("/network").json() #okej

    def peers(self):
        return self.request_local("/peer").json() #okej

    def controller(self):
        return self.request_local("/controller").json() #okej

########################################################################################################################

    def get_local_network(self, nwid):
        return self.request_local("/network/" + nwid).json() #okej

    def get_peer(self,ndid):
        return self.request_local("/peer" + ndid).json() #okej

    def list_controller_networks(self):
        return self.request_local("/controller/network").json() #okej

    def get_controller_network(self, nwid):
        return self.request_local("/controller/network/" + nwid).json() #okej

    def get_controller_network_members(self, nwid):
        return self.request_local("/controller/network/" + nwid + "/member").json() #okej

    def get_controller_network_member(self, nwid, ndid):
        return self.request_local("/controller/network/" + nwid + "/member/" + ndid).json() #okej

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

    def post_node(self, nwid, ndid, name, description, active_bridge, authorized, ip_address, no_auto_assign):
        template = self.template
        template["name"] = str(name)
        template["description"] = str(description)
        template["config"]["ipAssignments"] = [str(ip_address)]
        template["config"]["activeBridge"] = bool(active_bridge)
        template["config"]["authorized"] = bool(authorized)
        template["config"]["noAutoAssignIps"] = bool(no_auto_assign)


        payload = json.dumps(template)
        return self.request_central("network/"+nwid+"/member/"+ndid, data=payload).json()


class Daemon():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            z = Zerotier_API(local_api_key="jmafk4t5l78b693flgwe94cm",
                             central_api_key="esfMOt8OjFHdTT928rK1iPzWxLV11Kp1")
            device_list = z.get_controller_network_members(z.prod_network).keys()
            if len(device_list) != z.device_count:
                new_clients = list(set(device_list) - set(z.device_list))
                z.device_list = device_list
                for i in new_clients:
                    z.post_node(z.prod_network, new_clients[i], "client"+str(int(z.device_count)+int(i)+1), "peering with client"+str(int(z.device_count)+int(i)+1), False, True, "10.21.37."+str(int(z.device_count)+int(i)+1), True)
                z.device_count = len(z.device_list)
                time.sleep(10)


    """
    z = Zerotier_API(local_api_key="jmafk4t5l78b693flgwe94cm", central_api_key="esfMOt8OjFHdTT928rK1iPzWxLV11Kp1")
    print(z.post_node("3efa5cb78a7d9141", "b3bf7fdcf9", "as210645", "peering with as210645", False, False, "192.168.4.1", False )) #example
    app = Daemon()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()
    print(z.device_list)
    """
