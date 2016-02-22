# -*- coding: utf-8 -*-

import json
import os
import unittest

import requests

host = 'http://121.199.9.187:8082'
network_url_base = "/networking"

headers = {}
headers["X-Auth-Token"] = "admintest:admintest"

class NetworkTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_NetworksHandler_GET(self):
        print "\n----------test_NetworksHandler_GET----------"
        response = requests.get(host + network_url_base + '/v2.0/networks.json', headers=headers)
        print(response.status_code)
        print(response.text)

    def test_NetworksHandler_POST(self):
        print "\n----------test_NetworksHandler_POST----------"
        data = '{"network":{"name": "vpc-1", "admin_state_up": false, "shared": false,"router:external": false,\
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869"}}'
        response = requests.post(host + network_url_base + '/v2.0/networks.json', data=data, headers=headers)
        print(response.status_code)
        print(response.text)

    def test_NetworkHandler_GET(self):
        print "\n----------test_NetworkHandler_GET----------"
        response = requests.get(host + network_url_base + '/v2.0/networks/vpc-62x5warir.json', headers=headers)
        print(response.status_code)
        print(response.text)

    def test_NetworkHandler_PUT(self):
        print "\n----------test_NetworkHandler_PUT----------"
        data = '{"network":{"name": "vpc-1"}}'
        response = requests.put(host + network_url_base + '/v2.0/networks/vpc-62x5warir.json', data=data, headers=headers)
        print(response.status_code)
        print(response.text)

    def test_NetworkHandler_DELETE(self):
        pass

class LoadBalanceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
