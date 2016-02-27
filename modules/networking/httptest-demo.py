# -*- coding: utf-8 -*-

import json
import unittest
import time

import requests

#from cloudGate.common.define import *
#from cloudGate.config import *

#host = 'http://121.199.9.187:8082'
#network_url_base = 'http://' + HOST + ':' + PORT + NETWORKING_BASE_URL
network_url_base = "http://121.199.9.187:8081/networking"

headers = {"X-Auth-Token": "admintest:admintest"}

network_id = ""
loadbalancer_id = ""
listener_id = ""
member_id = ""

#plese set loadbalancer id which created by aliyun dashboard for listener and member testing
loadbalancer_id_for_listener_member = "153214117f6-cn-hongkong-am4-c04"

class NetworkTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_NetworksHandler_GET(self):
        print "\n----------test_NetworksHandler_GET----------"
        raw_input("press enter to continue")
        response = requests.get(network_url_base + '/v2.0/networks.json', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_NetworksHandler_POST(self):
        print "\n----------test_NetworksHandler_POST----------"
        raw_input("press enter to continue")
        data = '{"network":{"name": "vpc-1", "admin_state_up": false, "shared": false,"router:external": false,\
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869"}}'
        response = requests.post(network_url_base + '/v2.0/networks.json', data=data, headers=headers)
        print response.status_code
        if response.status_code == 201:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)
        if response.status_code == 201:
            global network_id
            network_id = json.loads(response.text)["network"]["id"]
            print "create network id: ", network_id

    def test_NetworkHandler_GET(self):
        print "\n----------test_NetworkHandler_GET----------"
        raw_input("press enter to continue")
        global network_id
        print "network id: ", network_id
        response = requests.get(network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_NetworkHandler_PUT(self):
        print "\n----------test_NetworkHandler_PUT----------"
        raw_input("press enter to continue")
        global network_id
        print "network id: ", network_id
        data = '{"network":{"name": "vpc-2"}}'
        response = requests.put(network_url_base + '/v2.0/networks/' + network_id + '.json', data=data, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_NetworkHandler_DELETE(self):
        print "\n----------test_NetworkHandler_DELETE----------"
        raw_input("press enter to continue")
        print "sleep 3 second, waiting for the network status change to be active"
        time.sleep(3)
        global network_id
        print "network id: ", network_id
        response = requests.delete(network_url_base + '/v2.0/networks/' + network_id + '.json', headers=headers)
        print response.status_code
        print response.text

class LoadBalanceTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_LoadbalancersHandler_GET(self):
        print "\n----------test_LoadbalancersHandler_GET----------"
        raw_input("press enter to continue")
        response = requests.get(network_url_base + '/v2.0/lbaas/loadbalancers', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LoadbalancersHandler_POST(self):
        print "\n----------test_LoadbalancersHandler_POST----------"
        raw_input("press enter to continue")
        data = '{"loadbalancer": {"name": "loadbalancer1", \
                "description": "simple lb", \
                "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081", \
                "vip_subnet_id": "013d3059-87a4-45a5-91e9-d721068ae0b2", \
                "vip_address": "10.0.0.4", \
                "admin_state_up": true, \
                "provider": "sample_provider"}}'
        response = requests.post(network_url_base + '/v2.0/lbaas/loadbalancers', data=data, headers=headers)
        print response.status_code
        if response.status_code == 201:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)
        if response.status_code == 201:
            global loadbalancer_id
            loadbalancer_id = json.loads(response.text)["loadbalancer"]["id"]
            print "create loadbalancer id: ", loadbalancer_id

    def test_LoadbalancerHandler_GET(self):
        print "\n----------test_LoadbalancerHandler_GET----------"
        raw_input("press enter to continue")
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        response = requests.get(network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LoadbalancerStatusesHandler_GET(self):
        print "\n----------test_LoadbalancerStatusesHandler_GET----------"
        raw_input("press enter to continue")
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        response = requests.get(network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id + '/statuses', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LoadbalancerHandler_PUT(self):
        print "\n----------test_LoadbalancerHandler_PUT----------"
        raw_input("press enter to continue")
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        data = '{"loadbalancer": {"admin_state_up": false,"description": "simple lb2","name": "loadbalancer2"}}'
        response = requests.put(network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, data=data, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

     def test_LoadbalancerHandler_DELETE(self):
        print "\n----------test_LoadbalancerHandler_DELETE----------"
        raw_input("press enter to continue")
        print "sleep 3 second, waiting for the loadbalancer status change to be active"
        time.sleep(3)
        global loadbalancer_id
        print "loadbalancer id: ", loadbalancer_id
        response = requests.delete(network_url_base + '/v2.0/lbaas/loadbalancers/' + loadbalancer_id, headers=headers)
        print response.status_code
        print response.text

    def test_LbaasListenersHandler_GET(self):
        print "\n----------test_LbaasListenersHandler_GET----------"
        raw_input("press enter to continue")
        response = requests.get(network_url_base + '/v2.0/lbaas/listeners', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasListenersHandler_POST(self):
        print "\n----------test_LbaasListenersHandler_POST----------"
        raw_input("press enter to continue")
        global loadbalancer_id_for_listener_member

        jl = {}
        jl["admin_state_up"] = True
        jl["connection_limit"] = 100
        jl["description"] = "listener one"
        jl["loadbalancer_id"] = loadbalancer_id
        jl["name"] = "listener1"
        jl["protocol"] = "HTTP"
        jl["protocol_port"] = "80"
        jl["default_tls_container_ref"] = ""
        jl["sni_container_refs"] = []
        jd = {}
        jd["listener"] = jl

        data = json.dumps(jd)
        response = requests.post(network_url_base + '/v2.0/lbaas/listeners', data=data, headers=headers)
        print response.status_code
        if response.status_code == 201:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)
        if response.status_code == 201:
            global listener_id
            listener_id = json.loads(response.text)["listener"]["id"]
            print "create listener id: ", listener_id

    def test_LbaasListenerHandler_GET(self):
        print "\n----------test_LbaasListenerHandler_GET----------"
        raw_input("press enter to continue")
        global listener_id
        print "listener id: ", listener_id
        response = requests.get(network_url_base + '/v2.0/lbaas/listeners/' + listener_id, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasListenerHandler_PUT(self):
        print "\n----------test_LbaasListenerHandler_PUT----------"
        raw_input("press enter to continue")
        global listener_id
        print "listener id: ", listener_id
        data = '{"listener": {"admin_state_up": false, \
                "connection_limit": 200, \
                "description":"listener two", \
                "name": "listener2", \
                "default_tls_container_ref": "https://barbican.endpoint/containers/cc", \
                "sni_container_refs":["https://barbican.endpoint/containers/dd"]}}'
        response = requests.put(network_url_base + '/v2.0/lbaas/listeners/' + listener_id, data=data, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasListenerHandler_DELETE(self):
        print "\n----------test_LbaasListenerHandler_DELETE----------"
        raw_input("press enter to continue")
        print "sleep 3 second, waiting for the listener status change to be active"
        time.sleep(3)
        global listener_id
        print "listener id: ", listener_id
        response = requests.delete(network_url_base + '/v2.0/lbaas/listeners/' + listener_id, headers=headers)
        print response.status_code
        print response.text

    def test_LbaasPoolMembersHandler_GET(self):
        print "\n----------test_LbaasPoolMembersHandler_GET----------"
        raw_input("press enter to continue")
        response = requests.get(network_url_base + '/v2.0/lbaas/pools/' + loadbalancer_id_for_listener_member + '/members', headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasPoolMembersHandler_POST(self):
        print "\n----------test_LbaasPoolMembersHandler_POST----------"
        raw_input("press enter to continue")
        data = '{"member": \
                {"address": "10.47.44.13", \
                "admin_state_up": true, \
                "protocol_port": "80", \
                "subnet_id": "013d3059-87a4-45a5-91e9-d721068ae0b2", \
                "weight": "1"}}'
        response = requests.post(network_url_base + '/v2.0/lbaas/pools/' + loadbalancer_id_for_listener_member + '/members', data=data, headers=headers)
        print response.status_code
        if response.status_code == 201:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)
        if response.status_code == 201:
            global member_id
            member_id = json.loads(response.text)["member"]["id"]
            print "create member id: ", member_id

    def test_LbaasPoolMemberHandler_GET(self):
        print "\n----------test_LbaasPoolMemberHandler_GET----------"
        raw_input("press enter to continue")
        global member_id
        print "member id: ", member_id
        response = requests.get(network_url_base + '/v2.0/lbaas/pools/' + loadbalancer_id_for_listener_member + '/members/' + member_id, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasPoolMemberHandler_PUT(self):
        print "\n----------test_LbaasPoolMemberHandler_PUT----------"
        raw_input("press enter to continue")
        global member
        print "member id: ", member_id
        data = '{"member": {"admin_state_up": false,"weight": 5}}'
        response = requests.put(network_url_base + '/v2.0/lbaas/pools/' + loadbalancer_id_for_listener_member + '/members/' + member_id, data=data, headers=headers)
        print response.status_code
        if response.status_code == 200:
            j = json.loads(response.text)
            print json.dumps(j, indent=1)

    def test_LbaasPoolMemberHandler_DELETE(self):
        print "\n----------test_LbaasPoolMemberHandler_DELETE----------"
        raw_input("press enter to continue")
        print "sleep 3 second, waiting for the member status change to be active"
        time.sleep(3)
        global member_id
        print "member id: ", member_id
        response = requests.delete(network_url_base + '/v2.0/lbaas/pools/' + loadbalancer_id_for_listener_member + '/members/' + member_id, headers=headers)
        print response.status_code
        print response.text

if __name__ == '__main__':
    unittest.main()
