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

        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_accept_format('json')

        while True :
            response = self.clt.do_action(request)
            resp = json.loads(response)

            print resp

            if "Vpcs" not in resp.keys():
                break

            if resp["TotalCount"] <= 0:
                break

            for vpc in resp["Vpcs"]["Vpc"]:
                network = {}

                '''
                network["CidrBlock"] = vpc["CidrBlock"]
                network["CreationTime"] = vpc["CreationTime"]
                network["Description"] = vpc["Description"]
                network["RegionId"] = vpc["RegionId"]
                network["Status"] = vpc["Status"]
                network["VRouterId"] = vpc["VRouterId"]
                network["VSwitchIds"] = vpc["VSwitchIds"]
                network["VpcId"] = vpc["VpcId"]
                network["VpcName"] = vpc["VpcName"]
                '''

                if vpc["Status"] == "Available":
                    network["status"] = "ACTIVE"
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


        #test begin
        network = {}
        network["status"] = "ACTIVE"
        network["subnets"] = []
        network["name"] = "vpcname-qqqqqwwwwww"
        network["provider:physical_network"] = None
        network["admin_state_up"] = True
        network["tenant_id"] = tenantID
        network["provider:network_type"] = "local"
        network["router:external"] = False
        network["mtu"] = 0
        network["shared"] = False
        network["id"] = "vpcid-qqqqqwwwwww"
        network["provider:segmentation_id"] = None
        networks.append(network)
        #test end

        print networks
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

        print resp

        return None

    def createNetworks(self, inNetworks):
        #TODO
        pass

    def getAPIExtensions(self):
        return []