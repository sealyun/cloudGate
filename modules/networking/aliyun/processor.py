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

    def queryNetwotks(self, shared, tenantID):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_accept_format('json')

        networks = []

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
                network["name"] = vpc["VpcName"]
                network["provider:physical_network"] = None
                network["admin_state_up"] = True
                network["tenant_id"] = tenantID
                network["provider:network_type"] = "local"
                network["router:external"] = True
                network["mtu"] = 0
                network["shared"] = shared
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
        network["router:external"] = True
        network["mtu"] = 0
        network["shared"] = shared
        network["id"] = "vpcid-qqqqqwwwwww"
        network["provider:segmentation_id"] = None
        networks.append(network)
        #test end

        print networks
        return networks

    def createNetwork(self, shared, tenantID, inNetwork):
        #TODO
        pass

    def createNetworks(self, shared, tenantID, inNetworks):
        #TODO
        pass