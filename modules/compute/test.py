# -*- coding: utf-8 -*-

import unittest
import requests
import json
import time

#from cloudGate.common.define import *
#from cloudGate.config import *

#URL_BASE = "http://" + HOST + ":" + PORT + "/compute"
URL_BASE = "http://121.199.9.187:8083" + "/compute"
session = requests.session()

g_server_id = "i-627j4rnxa"


def print_ret(s, r):
    print "server_id:", s
    print "status:", r.status_code
    print "response:", r.text
    #print "wait 20 sencond....."
    #time.sleep(10)


class ComputeTest(unittest.TestCase):
    @staticmethod
    def print_json(s):
        print json.dumps(s, indent=4)

    def setUp(self):
        pass

    def tearDown(self):
        session.close()

    def server_create(self):
        global g_server_id
        print "-------- create server ---------"
        raw_input("press Enter to continue.")
        url = URL_BASE + "/v2.1/tenant_id/servers"
        session.headers.update({'X-Auth-Token': 'admintest:admintest'})
        image_id = "m-62xyxyqyv"
        body_js = {
            "server": {
                "name": "tmp-server-test",
                "imageRef": image_id,
                "flavorRef": "ecs.t1.small",
                "metadata": {
                    "My Server Name": "Apache1"
                }
            }
        }
        res = session.post(url, json=body_js)
        print_ret("", res)
        server = json.loads(res.text)
        g_server_id = server["server"]["id"]

    def test_server_action(self):
        self.server_create()

        print "server_id:", g_server_id
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % g_server_id
        session.headers.update({'X-Auth-Token': 'admintest:admintest'})

        print "-------- os-start ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"os-start": ""})
        print_ret(g_server_id, res)

        print "-------- os-getVNCConsole ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"os-getVNCConsole": {"type": "novnc"}})
        print_ret(g_server_id, res)

        print "-------- reboot ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"reboot": ""})
        print_ret(g_server_id, res)

        print "-------- os-stop ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"os-stop": ""})
        print_ret(g_server_id, res)

        print "-------- addSecurityGroup ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"addSecurityGroup": {"name": "sg-62oo4zakn"}})
        print_ret(g_server_id, res)

        print "-------- removeSecurityGroup ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"removeSecurityGroup": {"name": "sg-62oo4zakn"}})
        print_ret(g_server_id, res)

        print "-------- createImage ---------"
        raw_input("press Enter to continue.")
        snapshot_id = "s-62ev59pgw"
        res = session.post(url, json={"createImage": {"name": "compute_test", "snapshot_id": snapshot_id, "metadata": {"meta_var": "meta_val"}}})
        print_ret(g_server_id, res)


        print "-------- attach ---------"
        raw_input("press Enter to continue.")
        volume_id = "d-627mm61sa"
        res = session.post(url, json={
            "attach": {
                "volume_id": volume_id,
                "device": "/dev/vdb",
                "disk_bus": "ide",
                "device_type": "cdrom"
            }
        })
        print_ret(g_server_id, res)



        print "-------- forceDelete ---------"
        raw_input("press Enter to continue.")
        #res = session.post(url, json={"os-stop": ""})  
        #print_ret(g_server_id, res)
        res = session.post(url, json={"forceDelete": ""})
        print_ret(g_server_id, res)


        print "-------- addFloatingIp for Instance cw ---------"
        raw_input("press Enter to continue.")
        id = "i-62dstjiws"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % id
        res = session.post(url, json={"addFloatingIp": {"address": "47.89.8.89"}})
        print_ret(id, res)


        print "-------- removeFloatingIp for instance cw ---------"
        raw_input("press Enter to continue.")
        res = session.post(url, json={"removeFloatingIp": {"address": "47.89.8.89"}})
        print_ret(id, res)



if __name__ == '__main__':
    unittest.main()
