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

            if resp["TotalCount"] <= 0:
                break

            for vpc in resp["Vpcs"]["Vpc"]:
                network = {}

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
        '''
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
        '''
        #test end

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
        #TODO
        pass

    def getAPIExtensions(self):
        return []