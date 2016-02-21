#coding=utf-8
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import ModifyInstanceAttributeRequest
from aliyunsdkecs.request.v20140526 import ModifyInstanceVpcAttributeRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
from aliyunsdkecs.request.v20140526 import JoinSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import LeaveSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest

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
                "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                "OS-EXT-IPS:type": "fixed",  #todo
                "version": 4
                }
                for ip in s["InnerIpAddress"]["IpAddress"]
            ],
            "public": [
                {
                "addr": ip,
                "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                "OS-EXT-IPS:type": "fixed",  #todo
                "version": 4
                }
                for ip in s["PublicIpAddress"]["IpAddress"]
            ]
            },
            "created": s["CreationTime"],
            "flavor": {  #todo
            "id": "1",  
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
            "links": [  #todo
                {
                "href": "http://",
                "rel": "bookmark"
                }
            ]
            },
            "key_name": "",  #todo
            "links": [  #todo
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
            "accessIPv4": "",  #todo
            "accessIPv6": "",  #todo
            "config_drive": "",  #todo
            "OS-DCF:diskConfig": "AUTO",  #todo
            "OS-EXT-AZ:availability_zone": s["ZoneId"],
            "OS-EXT-SRV-ATTR:host": s["HostName"],
            "OS-EXT-SRV-ATTR:hypervisor_hostname": s["HostName"],
            "OS-EXT-SRV-ATTR:instance_name": s["InstanceName"],
            "OS-EXT-STS:power_state": 1 if s["DeviceAvailable"] else 0,
            "OS-EXT-STS:task_state": "",  #todo
            "OS-EXT-STS:vm_state": "active",  #todo
            "os-extended-volumes:volumes_attached": [],  #todo
            "OS-SRV-USG:launched_at": "",  #todo
            "OS-SRV-USG:terminated_at": "",  #todo
            "progress": 0,  #todo
            "security_groups": [
            {
                "name": name
            }
            for name in s["SecurityGroupIds"]["SecurityGroupId"]
            ],
            "status": s["Status"],
            "host_status": "UP",  #todo
            "tenant_id": "openstack",  #todo
            "updated": s["ExpiredTime"],
            "user_id": "fake"  #todo
        }

    def queryServers(self, tenant_id, changes_since,
            image, flavor, name, status, host, limit, marker):
        headers, servers = self.query_ServersDetails(tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker)
        return {}, {
            "servers": [
                {
                    "id": s["id"],
                    "links": s["links"],
                    "name": s["name"]
                }
                for s in servers
            ]
        }
	    	
    def createServer(self, tenant_id, name, imageRef, flavorRef, metadata):
        request = CreateInstancesRequest.CreateInstancesRequest()
        request.set_accept_format('json')
        request.set_InstanceName(name)
        request.set_ImageId(imageRef)
        #todo set flavorRef
        #todo set metadata
        response = self.clt.do_action(request)

        resp = json.loads(response)
        #print "resp :", json.dumps(resp, indent=4)
        if "InstanceId" in resp:
            headers, s = self.query_server(tenant_id, resp["InstanceId"])
            return {}, {
                "server": {
                "OS-DCF:diskConfig": s["OS-DCF:diskConfig"],
                "adminPass": "zPnp2GseTqG4", #todo
                "id": s["id"],
                "links": s["links"],
                "security_groups": s["security_groups"]
                }
            }
        else:
            return {}, {}

    def queryServersDetails(self, tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        # not support query by "changes_since"
        request.set_ImageId(image) if image else None
        request.set_InstanceType(flavor) if flavor else None
        request.set_InstanceName(name) if name else None
        request.set_Status(status) if status else None
        # not support query by "host"
        request.set_PageSize(limit) if limit else None
        # not support query by "marker"

        response = self.clt.do_action(request)

        resp = json.loads(response)
        #print "resp :", json.dumps(resp, indent=4)

        if "Instances" not in resp.keys():
            return {}, {}

        headers = {}
        body = {
            "servers": [
                {
                    "addresses": {
                        "private": [
                            {
                            "addr": ip,
                            "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                            "OS-EXT-IPS:type": "fixed",  #todo
                            "version": 4
                            }
                            for ip in s["InnerIpAddress"]["IpAddress"]
                        ],
                        "public": [
                            {
                            "addr": ip,
                            "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                            "OS-EXT-IPS:type": "fixed",  #todo
                            "version": 4
                            }
                            for ip in s["PublicIpAddress"]["IpAddress"]
                        ]
                    },
                    "created": s["CreationTime"],
                    "flavor": {
                        "id": s["InstanceType"],  
                        "links": [  # todo
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
                        "links": [  #todo
                            {
                            "href": "http://",
                            "rel": "bookmark"
                            }
                        ]
                    },
                    "key_name": "",  #todo
                    "links": [  #todo
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
                    "accessIPv4": "",  #todo
                    "accessIPv6": "",  #todo
                    "config_drive": "",  #todo
                    "OS-DCF:diskConfig": "AUTO",  #todo
                    "OS-EXT-AZ:availability_zone": s["ZoneId"],
                    "OS-EXT-SRV-ATTR:host": s["HostName"],
                    "OS-EXT-SRV-ATTR:hypervisor_hostname": s["HostName"],
                    "OS-EXT-SRV-ATTR:instance_name": s["InstanceName"],
                    "OS-EXT-STS:power_state": 1 if s["DeviceAvailable"] else 0,
                    "OS-EXT-STS:task_state": "",  #todo
                    "OS-EXT-STS:vm_state": "active",  #todo
                    "os-extended-volumes:volumes_attached": [],  #todo
                    "OS-SRV-USG:launched_at": "",  #todo
                    "OS-SRV-USG:terminated_at": "",  #todo
                    "progress": 0,  #todo
                    "security_groups": [
                    {
                        "name": name
                    }
                    for name in s["SecurityGroupIds"]["SecurityGroupId"]
                    ],
                    #"status": s["Status"],
                    "status": "ACTIVE",
                    "host_status": "UP",  #todo
                    "tenant_id": "openstack",  #todo
                    "updated": s["ExpiredTime"],
                    "user_id": "fake"  #todo
                }
                for s in resp["Instances"]["Instance"]
            ]
        }

        return headers, body

    def queryServer(self, tenant_id, server_id):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_InstanceIds(json.dumps([server_id]))
        
        response = self.clt.do_action(request)
        
        resp = json.loads(response)
        #print "resp :", json.dumps(resp, indent=4)

        if "Instances" not in resp.keys() or len(resp["Instances"]["Instance"]) < 1:
            return {}, {}

        s = resp["Instances"]["Instance"][0]
        headers = {}
        body = {
            "server":
                {
                    "addresses": {
                        "private": [
                            {
                            "addr": ip,
                            "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                            "OS-EXT-IPS:type": "fixed",  #todo
                            "version": 4
                            }
                            for ip in s["InnerIpAddress"]["IpAddress"]
                        ],
                        "public": [
                            {
                            "addr": ip,
                            "OS-EXT-IPS-MAC:mac_addr": "",  #todo
                            "OS-EXT-IPS:type": "fixed",  #todo
                            "version": 4
                            }
                            for ip in s["PublicIpAddress"]["IpAddress"]
                        ]
                    },
                    "created": s["CreationTime"],
                    "flavor": {
                        "id": s["InstanceType"],  
                        "links": [  # todo
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
                        "links": [  #todo
                            {
                            "href": "http://",
                            "rel": "bookmark"
                            }
                        ]
                    },
                    "key_name": "",  #todo
                    "links": [  #todo
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
                    "accessIPv4": "",  #todo
                    "accessIPv6": "",  #todo
                    "config_drive": "",  #todo
                    "OS-DCF:diskConfig": "AUTO",  #todo
                    "OS-EXT-AZ:availability_zone": s["ZoneId"],
                    "OS-EXT-SRV-ATTR:host": s["HostName"],
                    "OS-EXT-SRV-ATTR:hypervisor_hostname": s["HostName"],
                    "OS-EXT-SRV-ATTR:instance_name": s["InstanceName"],
                    "OS-EXT-STS:power_state": 1 if s["DeviceAvailable"] else 0,
                    "OS-EXT-STS:task_state": "",  #todo
                    "OS-EXT-STS:vm_state": "active",  #todo
                    "os-extended-volumes:volumes_attached": [],  #todo
                    "OS-SRV-USG:launched_at": "",  #todo
                    "OS-SRV-USG:terminated_at": "",  #todo
                    "progress": 0,  #todo
                    "security_groups": [
                    {
                        "name": name
                    }
                    for name in s["SecurityGroupIds"]["SecurityGroupId"]
                    ],
                    #"status": s["Status"],
                    "status": "ACTIVE",
                    "host_status": "UP",  #todo
                    "tenant_id": "openstack",  #todo
                    "updated": s["ExpiredTime"],
                    "user_id": "fake"  #todo
                }
        }

        return headers, body

    def updateServerName(self, tenant_id, server_id, name, imageRef, flavorRef, metadata):
        request = ModifyInstanceAttributeRequest.ModifyInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_InstanceId(server_id)
        request.set_InstanceName(name)
        request.set_ImageId(imageRef)
        #todo set flavorRef
        request.set_HostName(metadata["My Server Name"])
	
        self.clt.do_action(request)
	
        return self.queryServer(tenant_id, server_id)

    def updateServerIP(self, tenant_id, server_id, accessIPv4, accessIPv6):
       	request = ModifyInstanceVpcAttributeRequest.ModifyInstanceVpcAttributeRequest()
        request.set_accept_format("json")
        request.set_InstanceId(server_id)
        request.set_PrivateIpAddress(accessIPv4)
        #todo set accessIPv6

        self.clt.do_action(request)

        return self.queryServer(tenant_id, server_id)

    def updateServerOSDCFdiskConfig(self, tenant_id, server_id, OSDCFdiskConfig):
	    #todo
        return self.queryServer(tenant_id, server_id)

    def deleteServer(self, tenant_id, server_id):
       	request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_accept_format("json")
        request.set_InstanceId(server_id)

        self.clt.do_action(request)

    def ServerAction(self, tenat_id, server_id, action):
        if "addFixedIp" in action:  # depend network 
            pass 
        if "addFloatingIp" in action:  # depend network
            pass
        if "attach" in action:  # depend volume
            pass
        if "confirmResize" in action:
            pass
        if "createImage" in action:  # depend image
            pass
        if "evacuate" in action:
            pass
        if "forceDelete" in action:
            pass
        if "lock" in action:
            pass
        if "pause" in action:
            pass
        if "reboot" in action:
            request = RebootInstanceRequest.RebootInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            self.clt.do_action(request)
        if "os-start" in action:
            request = StartInstanceRequest.StartInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            self.clt.do_action(request)
        if "os-stop" in action:
            request = StopInstanceRequest.StopInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            self.clt.do_action(request)
        if "unlock" in action:
            pass
        if "unpause" in action:
            pass
        if "unrescue" in action:
            pass
        if "addSecurityGroup" in action:
            request = JoinSecurityGroupRequest.JoinSecurityGroupRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            self.clt.do_action(request)
        if "removeSecurityGroup" in action:
            request = LeaveSecurityGroupRequest.LeaveSecurityGroupRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            self.clt.do_action(request)
    
    def serverAttachVolume(tenant_id, server_id, volumeAttachment, volumeId, device):
        headers = {}
        body = {}
        return headers, body

    def serverListVolumes(tenant_id, server_id):
        headers = {}
        body = {}
        return headers, body

    def volumeAttachmentDetail(tenant_id, server_id, attachment_id):
        headers = {}
        body = {}
        return headers, body
    
    def volumeAttachmentDetach(tenant_id, server_id):
        headers = {}
        body = {}
        return headers, body


    def queryFlavors(self, tenant_id):
        headers = {}
        headers["x-openstack-request-id"] = "default request id"
               
        body = {}
        """
        {
            "flavors":[
                {
                    "id": "1",
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2.1/openstack/flavors/1",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/openstack/flavors/1",
                            "rel": "bookmark"
                        }
                }
            ]
        }
        """
        return headers, body

    def createFlavor(self, tenant_id):
        pass

    def queryFlavor(self, tenant_id, flavor_id):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        request.set_accept_format("json")
        response = self.clt.do_action(request)
        resp = json.loads(response)
        """
        {
            "RequestId": "1651FBB6-4FBF-49FF-A9F5-DF5D696C7EC6",
            "InstanceTypes": 
            {
                "InstanceType": [
                    {
                        "InstanceTypeId": "ecs.t1.xsmall",
                        "CpuCoreCount": 1,
                        "MemorySize": 0.5
                    },
                    {
                        "InstanceTypeId": "ecs.t1.small",
                        "CpuCoreCount": 1,
                        "MemorySize": 1
                    }
                ]
            }
        }
        """
        headers = {}
        headers["x-openstack-request-id"] = resp["RequestId"]
        body = {
            "flavors": [
                {
                    "id": f["InstanceTypeId"],
                    "links": [
                        {
                            "href": "",
                            "rel": "self"
                        },
                        {
                            "href": "",
                            "rel": "bookmark"
                        }
                    ]        
                }
                for f in resp["InstanceTypes"]["InstanceType"]
            ]
        }
        return headers, body

    def deleteFlavor(self, tenant_id, flavor_id):
        pass

    def queryFlavorsDetail(self, tenant_id):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        request.set_accept_format("json")
        response = self.clt.do_action(request)
        resp = json.loads(response)
        """
        {
            "RequestId": "1651FBB6-4FBF-49FF-A9F5-DF5D696C7EC6",
            "InstanceTypes": 
            {
                "InstanceType": [
                    {
                        "InstanceTypeId": "ecs.t1.xsmall",
                        "CpuCoreCount": 1,
                        "MemorySize": 0.5
                    },
                    {
                        "InstanceTypeId": "ecs.t1.small",
                        "CpuCoreCount": 1,
                        "MemorySize": 1
                    }
                ]
            }
        }
        """
        headers = {}
        headers["x-openstack-request-id"] = resp["RequestId"]
        body = {
            "flavors": [
                {
                    "OS-FLV-DISABLED:disabled": False,  # todo
                    "disk": 1,  # todo
                    "OS-FLV-EXT-DATA:ephemeral": 0,  # todo
                    "os-flavor-access:is_public": True,  # todo
                    "id": f["InstanceTypeId"],
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2.1/openstack/flavors/1",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/openstack/flavors/1",
                            "rel": "bookmark"
                        }
                    ],
                    "name": f["InstanceTypeId"],
                    "ram": f["MemorySize"],
                    "swap": "",
                    "vcpus": f["CpuCoreCount"]
                }
                for f in resp["InstanceTypes"]["InstanceType"]
            ]
        }    
        return headers, body

    def getExtensions(self):
        return []
