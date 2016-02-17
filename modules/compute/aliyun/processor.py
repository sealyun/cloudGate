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

    def _convert_server_detail(self, s):
	return {
	    "addresses": {
		"private": [
		    {
			"addr": ip,
			"OS-EXT-IPS-MAC:mac_addr": "",
			"OS-EXT-IPS:type": "fixed",
			"version": 4
		    }
		    for ip in s["InnerIpAddress"]["IpAddress"]
		],
		"public": [
		    {
			"addr": ip,
			"OS-EXT-IPS-MAC:mac_addr": "",
			"OS-EXT-IPS:type": "fixed",
			"version": 4
		    }
		    for ip in s["PublicIpAddress"]["IpAddress"]
		]
	    },
	    "created": s["CreationTime"],
	    "flavor": {
		"id": "1", #todo
		"links": [
		    {
			"href": "http://openstack.example.com/openstack/flavors/1",
			"rel": "bookmark"
		    }
		]
	    },
	    "hostId": s["HostName"],
	    "id": s["InstanceId"],
	    "image": {
		"id": s["ImageId"],
		"links": [
		    {
			"href": "http://",
			"rel": "bookmark"
		    }
		]
	    },
	    "key_name": "",
	    "links": [
		{
		    "href": "http://",
		    "rel": "self"
		},
		{
		    "href": "http://",
		    "rel": "bookmark"
		}
	    ],
	    "metadata": {
		"My Server Name": s["InstanceName"]
	    },
	    "name": s["InstanceName"],
	    "accessIPv4": "",
	    "accessIPv6": "",
	    "config_drive": "",
	    "OS-DCF:diskConfig": "AUTO",
	    "OS-EXT-AZ:availability_zone": s["ZoneId"],
	    "OS-EXT-SRV-ATTR:host": s["HostName"],
	    "OS-EXT-SRV-ATTR:hypervisor_hostname": s["HostName"],
	    "OS-EXT-SRV-ATTR:instance_name": s["InstanceName"],
	    "OS-EXT-STS:power_state": 1 if s["DeviceAvailable"] else 0,
	    "OS-EXT-STS:task_state": "",
	    "OS-EXT-STS:vm_state": "active",
	    "os-extended-volumes:volumes_attached": [],
	    "OS-SRV-USG:launched_at": "",
	    "OS-SRV-USG:terminated_at": "",
	    "progress": 0,
	    "security_groups": [
		{
		    "name": name
		}
		for name in s["SecurityGroupIds"]["SecurityGroupId"]
	    ],
	    "status": s["Status"],
	    "host_status": "UP",
	    "tenant_id": "openstack",
	    "updated": s["ExpiredTime"],
	    "user_id": "fake"
	}

    def _convert_servers(self, servers):
	return {
	    "servers": [
		{
		    "id": s["InstanceId"],
		    "links": [
			{
			    "href": "http://",
			    "rel": "self"
			},
			{
			    "href": "http://",
			    "rel": "bookmark"
			}
		    ],
		    "name": s["InstanceName"]
		}
		for s in servers
	    ]
	}
	

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
	    return self._convert_servers(resp["Instances"]["Instance"])
        else:
            return {}
	    	
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
	    servers = []
	    for s in resp["Instances"]["Instance"]:
		servers.append(self._convert_server_detail(s))
	    return {"servers": servers}
        else:
            return {}

    def queryServer(self, tenant_id, server_id):
	request = DescribeInstancesRequest.DescribeInstancesRequest()
	request.set_accept_format('json')
	request.set_InstanceIds(json.dumps([server_id]))

        response = self.clt.do_action(request)

        resp = json.loads(response)
	print "resp :", json.dumps(resp, indent=4)
	if "Instances" in resp.keys():
	    return self._convert_server_detail(resp["Instances"]["Instance"][0])
        else:
            return {}

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
