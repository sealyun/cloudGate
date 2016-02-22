# -*- coding: utf-8 -*-

import json
import os
import unittest

import requests

host = 'http://121.199.9.187:8082'
network_url_base = "/networking"

session = requests.session()
session.headers["X-Auth-Token"] = "admintest:admintest"

class NetworkTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_NetworksHandler_GET(self):
        print "\n----------test_NetworksHandler_GET----------"
        response = session.get(host + network_url_base + '/v2.0/networks.json')
        print(response.text)

    def test_NetworksHandler_POST(self):
        print "\n----------test_NetworksHandler_POST----------"
        data = '{"name": "vpc-1", "admin_state_up": false, "shared": false,"router:external": false,\
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869"}'
        response = session.post(host + network_url_base + '/v2.0/networks.json', data=data)
        print(response.text)

class LoadBalanceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
