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
loadbalancer_id = ""

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
        if response.status_code == 201:
            global network_id
            network_id = json.loads(response.text)["network"]["id"]
            print "create network id: ", network_id

    def test_NetworkHandler_GET(self):
        print "\n----------test_NetworkHandler_GET----------"
        global network_id
        print "network id: ", network_id
        response = requests.get(host + network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        print response.text

    def test_NetworkHandler_PUT(self):
        print "\n----------test_NetworkHandler_PUT----------"
        global network_id
        print "network id: ", network_id
        data = '{"network":{"name": "vpc-2"}}'
        response = requests.put(host + network_url_base + '/v2.0/networks/' + network_id + '.json', data=data, headers=headers)
        print response.status_code
        print response.text

    def test_NetworkHandler_DELETE(self):
        print "\n----------test_NetworkHandler_DELETE----------"
        print "sleep 5 second, waiting for the network status change to be active"
        time.sleep(5)
        global network_id
        print "network id: ", network_id
        response = requests.delete(host + network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        print response.text

class LoadBalanceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LoadbalancersHandler_GET(self):
        print "\n----------test_LoadbalancersHandler_GET----------"
        response = requests.get(host + network_url_base + '/v2.0/lbaas/loadbalancers', headers=headers)
        print response.status_code
        print response.text

    def test_LoadbalancersHandler_POST(self):
        print "\n----------test_LoadbalancersHandler_POST----------"
        data = '{"loadbalancer": {"name": "loadbalancer1", \
                "description": "simple lb", \
                "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081", \
                "vip_subnet_id": "013d3059-87a4-45a5-91e9-d721068ae0b2", \
                "vip_address": "10.0.0.4", \
                "admin_state_up": true, \
                "provider": "sample_provider"}}'
        response = requests.post(host + network_url_base + '/v2.0/lbaas/loadbalancers', data=data, headers=headers)
        print response.status_code
        print response.text
        if response.status_code == 201:
            global loadbalancer_id
            loadbalancer_id = json.loads(response.text)["loadbalancer"]["id"]
            print "create loadbalancer id: ", loadbalancer_id

    def test_LoadbalancerHandler_GET(self):
        print "\n----------test_LoadbalancerHandler_GET----------"
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        response = requests.get(host + network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, headers=headers)
        print response.status_code
        print response.text

    def test_LoadbalancerHandler_PUT(self):
        print "\n----------test_LoadbalancerHandler_PUT----------"
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        data = '{"loadbalancer": {"admin_state_up": false,"description": "simple lb2","name": "loadbalancer2"}}'
        response = requests.put(host + network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, data=data, headers=headers)
        print response.status_code
        print response.text

    def test_LoadbalancerHandler_DELETE(self):
        print "\n----------test_LoadbalancerHandler_DELETE----------"
        print "sleep 5 second, waiting for the loadbalancer status change to be active"
        time.sleep(5)
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        response = requests.delete(host + network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, headers=headers)
        #response = requests.delete(host + network_url_base + '/v2.0/lbaas/loadbalancers/' + '1530d0d5cfe-cn-hongkong-am4-c04', headers=headers)
        print response.status_code
        print response.text

    def test_LoadbalancerStatusesHandler_GET(self):
        pass

    def test_LbaasListenersHandler_GET(self):
        pass

    def test_LbaasListenersHandler_PUT(self):
        pass

    def test_LbaasListenerHandler_GET(self):
        pass

    def test_LbaasListenerHandler_PUT(self):
        pass

    def test_LbaasListenerHandler_DELETE(self):
        pass

if __name__ == '__main__':
    unittest.main()
