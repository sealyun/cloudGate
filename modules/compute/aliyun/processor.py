#coding=utf-8
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

from cloudGate.config import *
from cloudGate.modules.compute.process_base import ComputeProcessorBase

import json


class AliyunComputeProcessor(ComputeProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryServers(self, tenant_id, changes_since,
            image, flavor, name, status, host, limit, marker):
	
	print "queryServers"
	request = DescribeInstancesRequest.DescribeInstancesRequest()

        response = self.clt.do_action(request)

        resp = json.loads(response)
	print "resp :", resp
	return resp["Instances"]["Instance"]
	    	
    def createServer(self, tenant_id, name, imageRef, flavorRef, metadata):
        pass

    def queryServersDetails(self, tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker):
        pass

    def queryServer(self, tenant_id, server_id):
        pass

    def updateServerName(self, tenant_id, server_id, name, imageRef, flavorRef, metadata):
        pass

    def updateServerIP(self, tenant_id, server_id, accessIPv4, accessIPv6):
        pass

    def updateServerOSDCFdiskConfig(self, tenant_id, server_id, OSDCFdiskConfig):
        pass

    def deleteServer(self, tenant_id, server_id):
        pass

    def ServerAction(self, tenat_id, server_id, action):
        #TODO a real action to aliyun server
        pass

    def getExtensions(self):
        return []
