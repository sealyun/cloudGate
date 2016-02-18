# -*- coding:utf-8 -*-

from cloudGate.modules.networking.process_base import *
from cloudGate.config import *

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526 import CreateVpcRequest
from aliyunsdkecs.request.v20140526 import DeleteVpcRequest
from aliyunsdkecs.request.v20140526 import ModifyVpcAttributeRequest

import json

class AliyunNetworkingProcessor(NetworkingProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def getNetwotks(self, shared, tenantID, routerExternal):
        networks = []
        #Unsupport shared network and external network
        if shared == "True" or routerExternal == "True":
            print "Unsupport shared network and external network"
            return networks

        pagePos = 1
        pageSize = 50
        while True :
            request = DescribeVpcsRequest.DescribeVpcsRequest()
            request.set_PageNumber(pagePos)
            request.set_PageSize(pageSize)
            request.set_accept_format('json')
            response = self.clt.do_action(request)
            resp = json.loads(response)
            pagePos = pagePos + 1

            print "response: ", resp
            ''' response data
            {
              "PageNumber": 1,
              "PageSize": 10,
              "RequestId": "DA1DAE87-43FA-472F-98BB-4FDBAA4A688D",
              "TotalCount": 1,
              "Vpcs": {
                "Vpc":[
                  {
                    "CidrBlock": "172.16.0.0/16",
                    "CreationTime": "2014-10-29T13:30:19Z",
                    "Description": "",
                    "RegionId": "cn-beijing",
                    "Status": "Available",
                    "VRouterId": "vrt-25bezkd03",
                    "VSwitchIds": {
                      "VSwitchId": []
                    },
                    "VpcId": "vpc-257gq642n",
                    "VpcName": ""
                  }
                ]
              }
            }
            '''

            if "Vpcs" not in resp.keys():
                break

            if len(resp["Vpcs"]["Vpc"]) <= 0:
                break

            for vpc in resp["Vpcs"]["Vpc"]:
                network = {}

                if vpc["Status"] == "Available":
                    network["status"] = "ACTIVE"
                else:
                    network["status"] = vpc["Status"]
                network["subnets"] = []
                #network["subnets"].append(vpc["CidrBlock"])
                network["name"] = vpc["VpcName"]
                network["provider:physical_network"] = None
                network["admin_state_up"] = True
                network["tenant_id"] = tenantID
                network["provider:network_type"] = "local"
                network["router:external"] = False
                network["mtu"] = 0
                network["shared"] = False
                network["id"] = vpc["VpcId"]
                network["provider:segmentation_id"] = None

                networks.append(network)

        print "networks: ", networks
        return networks

    def createNetwork(self, inNetwork):
        print inNetwork
        name = inNetwork["name"]
        adminStateUp = inNetwork["admin_state_up"]
        shared = inNetwork["shared"]
        routerExternal = inNetwork["router:external"]
        tenantID = inNetwork["tenant_id"]

        #Unsupport shared network and external network
        if shared or routerExternal:
            print "Unsupport shared network and external network"
            return None

        request = CreateVpcRequest.CreateVpcRequest()
        request.set_VpcName(name)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp
        ''' response data
        {
          "RequestId": "461D0C42-D5D1-4009-9B6A-B3D5888A19A9",
          "RouteTableId": "vtb-25wm68mnh",
          "VRouterId": "vrt-25bezkd03",
          "VpcId": "vpc-257gq642n"
        }
        '''

        if "VpcId" not in resp.keys():
            return None

        outNetwork = {}
        outNetwork["status"] = "ACTIVE"
        outNetwork["subnets"] = []
        outNetwork["name"] = name
        outNetwork["admin_state_up"] = adminStateUp
        outNetwork["tenant_id"] = "ACTIVE"
        outNetwork["router:external"] = tenantID
        outNetwork["mtu"] = 0
        outNetwork["shared"] = shared
        outNetwork["id"] = resp["VpcId"]

        return outNetwork

    def createNetworks(self, inNetworks):
        outNetworks = []
        for inNetwork in inNetworks:
            outNetwork = self.createNetwork(inNetwork)
            outNetworks.append(outNetwork)
        return outNetworks

    def getAPIExtensions(self):
        return []

    def getNetwork(self, networkID):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Vpcs" not in resp.keys():
            return None

        if len(resp["Vpcs"]["Vpc"]) <= 0:
            return None

        networks = []
        for vpc in resp["Vpcs"]["Vpc"]:
            network = {}

            if vpc["Status"] == "Available":
                network["status"] = "ACTIVE"
            else:
                network["status"] = vpc["Status"]
            network["subnets"] = []
            network["name"] = vpc["VpcName"]
            network["router:external"] = False
            network["admin_state_up"] = True
            network["tenant_id"] = ""
            network["mtu"] = 0
            network["shared"] = False
            network["port_security_enabled"] = True
            network["id"] = vpc["VpcId"]

            if network["id"] == networkID:
                networks.append(network)

        if len(networks) > 0:
            return networks[0]
        else:
            return None

    def updateNetwork(self, networkID, inNetwork):
        networkName = inNetwork["name"]

        request = ModifyVpcAttributeRequest.ModifyVpcAttributeRequest()
        request.set_VpcName(networkName)
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        return self.getNetwork(networkID)

    def deleteNetwork(self, networkID):
        request = DeleteVpcRequest.DeleteVpcRequest()
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return False

        return True

    def getDHCPAgents(self, networkID):
        #TODO
        #Aliyun does not support
        return []

    def getSubsets(self, displayName, networkID, gatewayIP, ipVersion, cidr, id, enableDHCP, ipv6RaMode, ipv6AddressMode):
        #TODO
        #Aliyun does not support

        subnets = []

        subnet = {}
        subnet["name"] = ""
        subnet["enable_dhcp"] = ""
        subnet["network_id"] = ""
        subnet["tenant_id"] = ""
        subnet["dns_nameservers"] = ""
        subnet["allocation_pools"] = ""
        subnet["host_routes"] = ""
        subnet["ip_version"] = ""
        subnet["gateway_ip"] = ""
        subnet["cidr"] = ""
        subnet["id"] = ""

        subnets.append(subnet)
        return subnets

    def createSubnet(self, inSubnet):
        #TODO
        #Aliyun does not support

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        return outSubnet

    def createSubnets(self, inSubnets):
        #TODO
        #Aliyun does not support

        outSubnets = []

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        outSubnets.append(outSubnet)
        return outSubnets

    def getSubnet(self, subnetID):
        #TODO
        #Aliyun does not support

        subnet = {}
        subnet["name"] = ""
        subnet["enable_dhcp"] = ""
        subnet["network_id"] = ""
        subnet["tenant_id"] = ""
        subnet["dns_nameservers"] = ""
        subnet["allocation_pools"] = ""
        subnet["host_routes"] = ""
        subnet["ip_version"] = ""
        subnet["gateway_ip"] = ""
        subnet["cidr"] = ""
        subnet["id"] = ""

        return subnet

    def updateSubnet(self, subnetID, inSubnet):
        #TODO
        #Aliyun does not support

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        return outSubnet

    def deleteSubnet(self, subnetID):
        #TODO
        #Aliyun does not support

        return True

    def getPorts(self, status, displayName, adminState, networkID, tenantID, deviceOwner, macAddress, portID, securityGroups, deviceID):
        #TODO
        #Aliyun does not support

        outPorts = []

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        outPorts.append(outPort)
        return outPorts

    def createPort(self, inPort):
        #TODO
        #Aliyun does not support

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        return outPort

    def createPorts(self, inPorts):
        #TODO
        #Aliyun does not support

        outPorts = []

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        outPorts.append(outPort)
        return outPorts

    def getPort(self, portID):
        #TODO
        #Aliyun does not support

        port = {}
        port["status"] = ""
        port["name"] = ""
        port["allowed_address_pairs"] = ""
        port["admin_state_up"] = ""
        port["network_id"] = ""
        port["tenant_id"] = ""
        port["extra_dhcp_opts"] = ""
        port["device_owner"] = ""
        port["mac_address"] = ""
        port["fixed_ips"] = ""
        port["id"] = ""
        port["security_groups"] = ""
        port["device_id"] = ""

        return port

    def updatePort(self, portID, inPort):
        #TODO
        #Aliyun does not support

        outPort = {}
        outPort["status"] = ""
        outPort["binding:host_id"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["binding:profile"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""
        outPort["name"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["binding:vif_details"] = ""
        outPort["binding:vnic_type"] = ""
        outPort["binding:vif_type"] = ""
        outPort["mac_address"] = ""

        return outPort

    def deletePort(self, portID):
        #TODO
        #Aliyun does not support

        return True