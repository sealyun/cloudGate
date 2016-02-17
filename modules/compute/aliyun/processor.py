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
	request.set_accept_format('json')
	request.set_ImageId(image) if status else None
	request.set_Status(status) if status else None
	request.set_InstanceName(name) if name else None
	request.set_InstanceIds(host) if host else None
	request.set_PageSize(limit) if limit else None

        response = self.clt.do_action(request)

        resp = json.loads(response)
	print "resp :", json.dumps(resp, indent=4)
	if "Instances" in resp.keys():
	    return resp["Instances"]["Instance"]
        else:
            return []
	    	
    def createServer(self, tenant_id, name, imageRef, flavorRef, metadata):
	return []

    def queryServersDetails(self, tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker):
	request = DescribeInstancesRequest.DescribeInstancesRequest()
	request.set_accept_format('json')
	request.set_ImageId(image) if status else None
	request.set_Status(status) if status else None
	request.set_InstanceName(name) if name else None
	request.set_InstanceIds(host) if host else None
	request.set_PageSize(limit) if limit else None

        response = self.clt.do_action(request)

        resp = json.loads(response)
	print "resp :", json.dumps(resp, indent=4)
	if "Instances" in resp.keys():
	    return resp["Instances"]["Instance"]
        else:
            return []

    def queryServer(self, tenant_id, server_id):
	return []

    def updateServerName(self, tenant_id, server_id, name, imageRef, flavorRef, metadata):
	return []

    def updateServerIP(self, tenant_id, server_id, accessIPv4, accessIPv6):
	return []

    def updateServerOSDCFdiskConfig(self, tenant_id, server_id, OSDCFdiskConfig):
	return []

    def deleteServer(self, tenant_id, server_id):
	return []

    def ServerAction(self, tenat_id, server_id, action):
	return []

    def getExtensions(self):
        return []
