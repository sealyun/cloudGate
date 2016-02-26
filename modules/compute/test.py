# -*- coding: utf-8 -*-

import unittest
import requests
import json
import time

URL_BASE = "http://121.199.9.187:8083/compute"
session = requests.session()


def print_ret(s, r):
    print "server_id:", s
    print "status:", r.status_code
    print "response:", r.text
    print "wait 20 sencond....."
    time.sleep(20)


class ComputeTest(unittest.TestCase):
    @staticmethod
    def print_json(s):
        print json.dumps(s, indent=4)

    def setUp(self):
        pass

    def tearDown(self):
        session.close()

    def test_server_create(self):
        url = URL_BASE + "/v2.1/tenant_id/servers"
        session.headers.update({'X-Auth-Token': 'admintest:admintest'})
        image_id = "m-62xyxyqyv"
        body_js = {
            "server": {
                "name": "new-server-test",
                "imageRef": image_id,
                "flavorRef": "ecs.t1.small",
                "metadata": {
                    "My Server Name": "Apache1"
                }
            }
        }
        res = session.post(url, json=body_js)
        print_ret("", res)

    def test_server_action(self):
        server_id = "i-22mcbn9tk"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        session.headers.update({'X-Auth-Token': 'admintest:admintest'})

        res = session.post(url, json={"os-stop": ""})
        print "-------- os-sto ---------"
        print_ret(server_id, res)

        res = session.post(url, json={"os-start": ""})
        print "-------- os-start ---------"
        print_ret(server_id, res)

        res = session.post(url, json={"reboot": ""})
        print "-------- reboot ---------"
        print_ret(server_id, res)

        res = session.post(url, json={"addSecurityGroup": {"name": "sg-22kwj1104"}})
        print "-------- addSecurityGroup ---------"
        print_ret(server_id, res)

        res = session.post(url, json={"removeSecurityGroup": {"name": "sg-22kwj1104"}})
        print "-------- removeSecurityGroup ---------"
        print_ret(server_id, res)

        server_id = "i-22yuah2hm"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        res = session.post(url, json={"addFloatingIp": {"address": "47.88.169.249"}})
        print "-------- addFloatingIp ---------"
        print_ret(server_id, res)

        server_id = "i-22yuah2hm"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        res = session.post(url, json={"removeFloatingIp": {"address": "47.88.169.249"}})
        print "-------- removeFloatingIp ---------"
        print_ret(server_id, res)


        server_id = "i-229hwebbw"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        res = session.post(url, json={"os-stop": ""})   # 先停止主机才能进行删除
        print_ret(server_id, res)
        res = session.post(url, json={"forceDelete": ""})
        print "-------- forceDelete ---------"
        print_ret(server_id, res)


        server_id = "i-229hwebbw"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        snapshot_id = "s-62ev59pgw"
        res = session.post(url, json={"createImage": {"name": "cw1", "snapshot_id": snapshot_id, "metadata": {"meta_var": "meta_val"}}})
        print "-------- createImage ---------"
        print_ret(server_id, res)


        server_id = "i-62wqo7iy2"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        volume_id = "d-62oesjamu"
        res = session.post(url, json={
            "attach": {
                "volume_id": volume_id,
                "device": "/dev/vdb",
                "disk_bus": "ide",
                "device_type": "cdrom"
            }
        })
        print "-------- attach ---------"
        print_ret(server_id, res)


        server_id = "i-62wqo7iy2"
        url = URL_BASE + "/v2.1/tenant_id/servers/%s/action" % server_id
        res = session.post(url, json={"os-getVNCConsole": {"type": "novnc"}})
        print "-------- os-getVNCConsole ---------"
        print_ret(server_id, res)











if __name__ == '__main__':
    unittest.main()
