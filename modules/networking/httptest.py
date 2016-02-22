# -*- coding: utf-8 -*-

import json
import unittest
import time

import requests

host = 'http://121.199.9.187:8082'
network_url_base = "/networking"

headers = {}
headers["X-Auth-Token"] = "admintest:admintest"

network_id = ""

class NetworkTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_NetworksHandler_GET(self):
        print "\n----------test_NetworksHandler_GET----------"
        response = requests.get(host + network_url_base + '/v2.0/networks.json', headers=headers)
        print response.status_code
        print response.text

    def test_NetworksHandler_POST(self):
        print "\n----------test_NetworksHandler_POST----------"
        data = '{"network":{"name": "vpc-1", "admin_state_up": false, "shared": false,"router:external": false,\
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869"}}'
        response = requests.post(host + network_url_base + '/v2.0/networks.json', data=data, headers=headers)
        print response.status_code
        print response.text
        global network_id
        network_id = json.loads(response.text)["network"]["id"]

    def test_NetworkHandler_GET(self):
        print "\n----------test_NetworkHandler_GET----------"
        global network_id
        response = requests.get(host + network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        print response.text

    def test_NetworkHandler_PUT(self):
        print "\n----------test_NetworkHandler_PUT----------"
        global network_id
        data = '{"network":{"name": "vpc-2"}}'
        response = requests.put(host + network_url_base + '/v2.0/networks/' + network_id + '.json', data=data, headers=headers)
        print response.status_code
        print response.text

    def test_NetworkHandler_DELETE(self):
        print "\n----------test_NetworkHandler_DELETE----------"
        print "sleep 5 second, waiting for the network status change to be active"
        time.sleep(5)
        global network_id
        response = requests.delete(host + network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        print response.text

class LoadBalanceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
