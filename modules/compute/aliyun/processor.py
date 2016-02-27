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
from aliyunsdkecs.request.v20140526 import AllocateEipAddressRequest
from aliyunsdkecs.request.v20140526 import AssociateEipAddressRequest
from aliyunsdkecs.request.v20140526 import DescribeEipAddressesRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import ReleaseEipAddressRequest
from aliyunsdkecs.request.v20140526 import UnassociateEipAddressRequest
from aliyunsdkecs.request.v20140526 import DescribeZonesRequest
from aliyunsdkecs.request.v20140526 import CreateImageRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceVncUrlRequest

from aliyunsdkecs.request.v20140526 import AttachDiskRequest
from aliyunsdkecs.request.v20140526 import DetachDiskRequest

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
                "href": "",
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
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceName(name)
        request.set_ImageId(imageRef)
        request.set_InstanceType(flavorRef)
        request.set_SecurityGroupId("sg-62m1xgqht")
        #request.set_VSwitchId("vsw-62b7n1bsk") #for test
        #request.add_query_param("RegionId", "cn-hongkong")
        response = self.clt.do_action(request)
        resp = json.loads(response)
        print "resp :", json.dumps(resp, indent=4)

        return {}, {
                "server": {
                "OS-DCF:diskConfig": "AUTO",
                "adminPass": "", #todo
                "id": resp["InstanceId"],
                "links": [],
                "security_groups": []
                }
            }
        if "InstanceId" in resp:
            headers, server = self.queryServer(tenant_id, resp["InstanceId"])
            s = server["server"]
            return {}, {
                "server": {
                "OS-DCF:diskConfig": "AUTO",
                "adminPass": "", #todo
                "id": resp["InstanceId"],
                "links": [],
                "security_groups": []
                }
            }
        else:
            return {}, {}
    
    def queryServersDetails(self, tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker):
        regions = self._queryRegions()
        #print "---regions:"
        #print json.dumps(regions, indent=4)
        servers = []
        for region in regions["Regions"]["Region"]:
            id = region["RegionId"]
            servers += self._queryServersDetails(tenant_id, changes_since, image, flavor, name, status, host, limit, marker, id)
        #print "------servers:"
        #print json.dumps(servers, indent=4)
        return {}, {"servers": servers}

    def _queryServersDetails(self, tenant_id, changes_since, image,
            flavor, name, status, host, limit, marker, region):

        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')

        request.add_query_param('RegionId', region)
        # not support query by "changes_since"
        request.set_ImageId(image) if image else None
        request.set_InstanceType(flavor) if flavor else None
        request.set_InstanceName(name) if name else None
        #request.set_Status(status) if status else None
        # not support query by "host"
        #request.set_PageSize(limit) if limit else None
        # not support query by "marker"

        response = self.clt.do_action(request)

        resp = json.loads(response)
        #print "---query serversdetail resp :", json.dumps(resp, indent=4)

        if "Instances" not in resp.keys():
            return []

        return [
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
                            "href": "",
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
                    "status": "ACTIVE" if s["Status"] != "Stopped" else "Stopped",
                    "host_status": "DOWN" if s["Status"] == "Stopped" else "UP",  #todo
                    "tenant_id": "openstack",  #todo
                    "updated": s["ExpiredTime"],
                    "user_id": "fake"  #todo
                }
                for s in resp["Instances"]["Instance"]
            ]

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
                            "href": "",
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

        rep = self.clt.do_action(request)
        print "---rep:", rep
    
    def createFloatingIp(tenant_id, pool):
        request = AllocateEipAddressRequest.AllocateEipAddressRequest()
        request.set_accept_format("json")

        request.add_query_param('RegionId', pool)

        response = self.clt.do_action(request)

        resp = json.loads(response)
        """
        {
          "AllocationId": "eip-25877c70x", 
          "EipAddress": "123.56.0.206", 
          "RequestId": "B6B9F518-60F8-4D81-9242-1207B356754D"
        }
        """
        
        return {}, {
            "floating_ip": {
                "instance_id": "",
                "ip": resp["EipAddress"],
                "fixed_ip": "",
                "id": resp["AllocationId"],
                "pool": pool
            }
        }

    def queryFloatingIps(tenant_id):
        request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
        request.set_accept_format("json")
        
        ips = []
        regions = self._queryRegions()
        for region in regions["Regions"]["Region"]:
            request.add_query_param('RegionId', region["RegionId"])

            response = self.clt.do_action(request)

            resp = json.loads(response)
            """
            {
              "EipAddresses": {
                "EipAddress": [
                  {
                    "AllocationId": "eip-2578g5v5a",
                    "AllocationTime": "2014-05-28T03:03:16Z ",
                    "Bandwidth": "1",
                    "InstanceId": "",
                    "InternetChargeType": " PayByBandwidth ",
                    "IpAddress": "123.56.0.36",
                    "OperationLocks": {
                      "LockReason": []
                    },
                    "RegionId": "cn-beijing",
                    "Status": "Available"
                  }
                ]
              },
              "PageNumber": 1,
              "PageSize": 10,
              "RequestId": "51BE7822-4121-428A-88F3-262AE4FD868D",
              "TotalCount": 1
            } 
            """
            ips += resp["EipAddresses"]["EipAddress"]
        return {}, {
                "floatingips": [
                    {
                        "router_id": "",
                        "tenant_id": tenant_id,
                        "floating_network_id": "",
                        "fixed_ip_address": "",
                        "floating_ip_address": ip["IpAddress"],
                        "port_id": "",
                        "id": ip["AllocationId"],
                        "status": "ACTIVE"
                    }
                    for ip in ips
                ]
            }

    def queryFloatingIpDetail(tenant_id, floating_ip_id):
        request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
        request.set_accept_format("json")
        
        request.set_AllocationId(floating_ip_id)

        response = self.clt.do_action(request)

        resp = json.loads(response)
        """
        {
          "EipAddresses": {
            "EipAddress": [
              {
                "AllocationId": "eip-2578g5v5a",
                "AllocationTime": "2014-05-28T03:03:16Z ",
                "Bandwidth": "1",
                "InstanceId": "",
                "InternetChargeType": " PayByBandwidth ",
                "IpAddress": "123.56.0.36",
                "OperationLocks": {
                  "LockReason": []
                },
                "RegionId": "cn-beijing",
                "Status": "Available"
              }
            ]
          },
          "PageNumber": 1,
          "PageSize": 10,
          "RequestId": "51BE7822-4121-428A-88F3-262AE4FD868D",
          "TotalCount": 1
        } 
        """
        ip = resp["EipAddresses"][EipAddress][0]
        return {}, {
                "floating_ip": {
                    "instance_id": "",
                    "ip": ip["IpAddress"],
                    "fixed_ip": "",
                    "id": ip["AllocationId"],
                    "pool": ip["RegionId"]
                }
            }

    def deleteFloatingIp(self, tenant_id, floating_ip_id):
        request = ReleaseEipAddressRequest.ReleaseEipAddressRequest
        request.set_accept_format("json")
        
        request.set_AllocationId(floating_ip_id)

        response = self.clt.do_action(request)

    
    def _queryRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format("json")

        response = self.clt.do_action(request)
        resp = json.loads(response)
        """ 
        {
            "RequestId": "611CB80C-B6A9-43DB-9E38-0B0AC3D9B58F",
            "Regions": {
                "Region": [{
                    "RegionId": "cn-hangzhou"
                },
                {
                    "RegionId": "cn-qingdao"
                }]
            }
        }
        """
        
        return resp

    def _queryFloatingIpAllocationId(self, ip):
        regions = self._queryRegions()
        for region in regions["Regions"]["Region"]:
            request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
            request.set_accept_format("json")
            request.add_query_param("RegionId", region['RegionId'])
            response = self.clt.do_action(request)
            resp = json.loads(response)
            print "---resp:", resp
            for eip in resp["EipAddresses"]["EipAddress"]:
                if ip == eip["IpAddress"]:
                    return eip["AllocationId"]
        return ""

    def serverAction(self, tenant_id, server_id, action):
        if "addFixedIp" in action:  # depend network 
            pass 
        if "removeFixedIp" in action:  # depend network 
            pass 
        elif "addFloatingIp" in action:  # depend network
            id = self._queryFloatingIpAllocationId(action["addFloatingIp"]["address"])    
            if not id:
                return
            request = AssociateEipAddressRequest.AssociateEipAddressRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            request.set_AllocationId(id)
            self.clt.do_action(request)

        elif "removeFloatingIp" in action:
            id = self._queryFloatingIpAllocationId(action["removeFloatingIp"]["address"])    
            if not id:
                return 

            request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            request.set_AllocationId(id)
            self.clt.do_action(request)

        elif "attach" in action:  # depend volume
            '''
            action
            {
                "attach": {
                    "volume_id": "15e59938-07d5-11e1-90e3-e3dffe0c5983",
                    "device": "/dev/vdb",
                    "disk_bus": "ide",
                    "device_type": "cdrom"
                }
            }
            '''
            self.serverAttachVolume(tenant_id, server_id, action["attach"]["volume_id"], None)
        elif "createImage" in action:  # depend image
            print "---createImage"
            request = CreateImageRequest.CreateImageRequest()
            request.set_accept_format('json')
            request.set_SnapshotId(action["createImage"]["snapshot_id"])
            request.set_ImageName(action["createImage"]["name"])

            response = self.clt.do_action(request)
            resp = json.loads(response)
            print "---resp:", resp
        elif "forceDelete" in action:
            print "----forceDelete"
            self.deleteServer(tenant_id, server_id)

        elif "lock" in action:
            pass
        elif "unlock" in action:
            pass
        elif "os-getVNCConsole" in action:
            request = DescribeInstanceVncUrlRequest.DescribeInstanceVncUrlRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            response = self.clt.do_action(request)
            res = json.loads(response)
            return {}, {
                 "console": {
                 "type": "",
                 "url": res["VncUrl"]
                 }
            }
        elif "reboot" in action:
            print "----reboot"
            print "server_id:", server_id
            request = RebootInstanceRequest.RebootInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            s = self.clt.do_action(request)
            print 'rep:', s
        elif "os-start" in action:
            print "----start"
            print "server_id:", server_id
            request = StartInstanceRequest.StartInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            s = self.clt.do_action(request)
            print 'rep:', s
        elif "os-stop" in action:
            print "----stop"
            print "server_id:", server_id
            request = StopInstanceRequest.StopInstanceRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            s = self.clt.do_action(request)
            print 'rep:', s
        elif "addSecurityGroup" in action:
            print "------addSecurityGroup"
            security_group_id = action["addSecurityGroup"]["name"] #todo
            print "server_id:", server_id
            print "security_group_id:", security_group_id
            request = JoinSecurityGroupRequest.JoinSecurityGroupRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            request.set_SecurityGroupId(security_group_id)

            s = self.clt.do_action(request)
            print 'rep:', s
        elif "removeSecurityGroup" in action:
            print "------removeSecurityGroup"
            security_group_id = action["removeSecurityGroup"]["name"] #todo
            print "server_id:", server_id
            print "security_group_id:", security_group_id
            request = LeaveSecurityGroupRequest.LeaveSecurityGroupRequest()
            request.set_accept_format("json")
            request.set_InstanceId(server_id)
            request.set_SecurityGroupId(security_group_id)
            s = self.clt.do_action(request)
            print 'rep:', s
        return {}, {}
    
    def serverAttachVolume(self, tenant_id, instance_id, volume_id, device):
        headers = {}
        body = {}
        r = AttachDiskRequest.AttachDiskRequest()
        r.set_accept_format('json')
        r.set_InstanceId(instance_id)
        r.set_DiskId(volume_id)
        if device:
            r.set_Device(device)
        ## r.set_DeleteWithInstance(True)  ## or False        
        response = self.clt.do_action(r)
        resp = json.loads(response) 
        print "serverAttachVolume WUJUN response:", json.dumps(resp, indent=4)
        if resp.has_key("Code"):
            print "volumeAction os-attach Failed!!! Have Error!!!"
            return headers, None
        body = {
            "volumeAttachment": {
                "device": device,
                "id": "a26887c6-c47b-4654-abb5-dfadf7d3f803",
                "serverId": instance_id,
                "volumeId": volume_id
            }
        }        
        return headers, body

    def serverListVolumes(self, tenant_id, server_id):
        headers = {}
        body = {}
        return headers, body

    def volumeAttachmentDetail(self, tenant_id, server_id, attachment_id):
        headers = {}
        body = {}
        return headers, body
    
    def volumeAttachmentDetach(self, tenant_id, server_id, attachment_id):
        headers = {}
        body = {}
        
        return headers, body
    
    def getQuotaSets(self, admin_tenant_id, tenant_id):
        return {}, {
                "quota_set": {
                "injected_file_content_bytes": 10240,
                "metadata_items": 128,
                "server_group_members": 10,
                "server_groups": 10,
                "ram": 51200,
                "floating_ips": 10,
                "key_pairs": 100,
                "id": "91a3c6da787643c78f2a7c7428fa54f2",
                "instances": 10,
                "security_group_rules": 20,
                "injected_files": 5,
                "cores": 20,
                "fixed_ips": -1,
                "injected_file_path_bytes": 255,
                "security_groups": 10
            }
        } 

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
                            "href": "",
                            "rel": "self"
                        },
                        {
                            "href": "",
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
                            "href": "",
                            "rel": "self"
                        },
                        {
                            "href": "",
                            "rel": "bookmark"
                        }
                    ],
                    "name": f["InstanceTypeId"],
                    "ram": 1024 * f["MemorySize"],
                    "swap": "",
                    "vcpus": f["CpuCoreCount"]
                }
                for f in resp["InstanceTypes"]["InstanceType"]
            ]
        }    
        print "---queryFlavorsDeatil, body:"
        #print body
        return headers, body
    
    def getAvailabilityZone(self, tenant_id):
        regions = self._queryRegions()
        zones = []
        for region in regions["Regions"]["Region"]:
            request = DescribeZonesRequest.DescribeZonesRequest()
            request.set_accept_format("json")
            request.add_query_param('RegionId', region["RegionId"])
            response = self.clt.do_action(request)
            resp = json.loads(response)
            for z in resp["Zones"]["Zone"]:
                available = "Instance" in z["AvailableResourceCreation"]["ResourceTypes"]
                zones.append({"zoneState":{"available": available}, "hosts": "", "zoneName": z["ZoneId"]})
        return {}, {
           "availabilityZoneInfo": zones
        }   

    def getExtensions(self):
        return {}, {
            "extensions": [
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Multinic",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "NMN",
                    "description": "Multiple network support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "DiskConfig",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-DCF",
                    "description": "Disk Management Extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedAvailabilityZone",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-AZ",
                    "description": "Extended Availability Zone support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ImageSize",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-IMG-SIZE",
                    "description": "Adds image size to image listings."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedIps",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-IPS",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedIpsMac",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-IPS-MAC",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedServerAttributes",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-SRV-ATTR",
                    "description": "Extended Server Attributes support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedStatus",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-EXT-STS",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorDisabled",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-FLV-DISABLED",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorExtraData",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-FLV-EXT-DATA",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "SchedulerHints",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-SCH-HNT",
                    "description": "Pass arbitrary key/value pairs to the scheduler."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerUsage",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "OS-SRV-USG",
                    "description": "Adds launched_at and terminated_at on Servers."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AccessIPs",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-access-ips",
                    "description": "Access IPs support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AdminActions",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-admin-actions",
                    "description": "Enable admin-only server actions\n\n    Actions include: resetNetwork, injectNetworkInfo, os-resetState\n    "
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AdminPassword",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-admin-password",
                    "description": "Admin password management support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Agents",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-agents",
                    "description": "Agents support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Aggregates",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-aggregates",
                    "description": "Admin-only aggregate administration."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AssistedVolumeSnapshots",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-assisted-volume-snapshots",
                    "description": "Assisted volume snapshots."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AttachInterfaces",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-attach-interfaces",
                    "description": "Attach interface support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "AvailabilityZone",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-availability-zone",
                    "description": "1. Add availability_zone to the Create Server API.\n       2. Add availability zones describing.\n    "
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "BareMetalExtStatus",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-baremetal-ext-status",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "BareMetalNodes",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-baremetal-nodes",
                    "description": "Admin-only bare-metal node administration."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "BlockDeviceMapping",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-block-device-mapping",
                    "description": "Block device mapping boot support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "BlockDeviceMappingV2Boot",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-block-device-mapping-v2-boot",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "CellCapacities",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-cell-capacities",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Cells",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-cells",
                    "description": "Enables cells-related functionality such as adding neighbor cells,\n    listing neighbor cells, and getting the capabilities of the local cell.\n    "
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Certificates",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-certificates",
                    "description": "Certificates support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Cloudpipe",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-cloudpipe",
                    "description": "Adds actions to create cloudpipe instances.\n\n    When running with the Vlan network mode, you need a mechanism to route\n    from the public Internet to your vlans.  This mechanism is known as a\n    cloudpipe.\n\n    At the time of creating this class, only OpenVPN is supported.  Support for\n    a SSH Bastion host is forthcoming.\n    "
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "CloudpipeUpdate",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-cloudpipe-update",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ConfigDrive",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-config-drive",
                    "description": "Config Drive Extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ConsoleAuthTokens",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-console-auth-tokens",
                    "description": "Console token authentication support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ConsoleOutput",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-console-output",
                    "description": "Console log output support, with tailing ability."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Consoles",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-consoles",
                    "description": "Interactive Console support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "CreateBackup",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-create-backup",
                    "description": "Create a backup of a server."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Createserverext",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-create-server-ext",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "DeferredDelete",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-deferred-delete",
                    "description": "Instance deferred delete."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Evacuate",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-evacuate",
                    "description": "Enables server evacuation."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedEvacuateFindHost",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-evacuate-find-host",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedFloatingIps",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-floating-ips",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedHypervisors",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-hypervisors",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedNetworks",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-networks",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedQuotas",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-quotas",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedRescueWithImage",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-rescue-with-image",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedServices",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-services",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedServicesDelete",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-services-delete",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedStatus",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-status",
                    "description": "Extended Status support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ExtendedVolumes",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-extended-volumes",
                    "description": "Extended Volumes support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FixedIPs",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-fixed-ips",
                    "description": "Fixed IPs support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorAccess",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-flavor-access",
                    "description": "Flavor access support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorExtraSpecs",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-flavor-extra-specs",
                    "description": "Flavors extra specs support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorManage",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-flavor-manage",
                    "description": "Flavor create/delete API support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorRxtx",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-flavor-rxtx",
                    "description": "Support to show the rxtx status of a flavor."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FlavorSwap",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-flavor-swap",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FloatingIpDns",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-floating-ip-dns",
                    "description": "Floating IP DNS support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FloatingIpPools",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-floating-ip-pools",
                    "description": "Floating IPs support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FloatingIps",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-floating-ips",
                    "description": "Floating IPs support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "FloatingIpsBulk",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-floating-ips-bulk",
                    "description": "Bulk handling of Floating IPs."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Fping",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-fping",
                    "description": "Fping Management Extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "HideServerAddresses",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-hide-server-addresses",
                    "description": "Support hiding server addresses in certain states."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Hosts",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-hosts",
                    "description": "Admin-only host administration."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "HypervisorStatus",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-hypervisor-status",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Hypervisors",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-hypervisors",
                    "description": "Admin-only hypervisor administration."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "InstanceActions",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-instance-actions",
                    "description": "View a log of actions and events taken on an instance."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "OSInstanceUsageAuditLog",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-instance_usage_audit_log",
                    "description": "Admin-only Task Log Monitoring."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Keypairs",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-keypairs",
                    "description": "Keypair Support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "LockServer",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-lock-server",
                    "description": "Enable lock/unlock server actions."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "MigrateServer",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-migrate-server",
                    "description": "Enable migrate and live-migrate server actions."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Migrations",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-migrations",
                    "description": "Provide data on migrations."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "MultipleCreate",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-multiple-create",
                    "description": "Allow multiple create in the Create Server v2.1 API."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Networks",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-networks",
                    "description": "Admin-only Network Management Extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "NetworkAssociationSupport",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-networks-associate",
                    "description": "Network association support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "PauseServer",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-pause-server",
                    "description": "Enable pause/unpause server actions."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Personality",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-personality",
                    "description": "Personality support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "PreserveEphemeralOnRebuild",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-preserve-ephemeral-rebuild",
                    "description": "Allow preservation of the ephemeral partition on rebuild."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "QuotaClasses",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-quota-class-sets",
                    "description": "Quota classes management support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Quotas",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-quota-sets",
                    "description": "Quotas management support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Rescue",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-rescue",
                    "description": "Instance rescue mode."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "SecurityGroupDefaultRules",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-security-group-default-rules",
                    "description": "Default rules for security group support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "SecurityGroups",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-security-groups",
                    "description": "Security group support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerDiagnostics",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-diagnostics",
                    "description": "Allow Admins to view server diagnostics through server action."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerExternalEvents",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-external-events",
                    "description": "Server External Event Triggers."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerGroupQuotas",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-group-quotas",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerGroups",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-groups",
                    "description": "Server group support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerListMultiStatus",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-list-multi-status",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerPassword",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-password",
                    "description": "Server password support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerSortKeys",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-sort-keys",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "ServerStartStop",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-server-start-stop",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Services",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-services",
                    "description": "Services support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Shelve",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-shelve",
                    "description": "Instance shelve mode."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "SimpleTenantUsage",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-simple-tenant-usage",
                    "description": "Simple tenant usage extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "SuspendServer",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-suspend-server",
                    "description": "Enable suspend/resume server actions."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "OSTenantNetworks",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-tenant-networks",
                    "description": "Tenant-based Network Management Extension."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "UsedLimits",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-used-limits",
                    "description": "Provide data on limited resources that are being used."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "UsedLimitsForAdmin",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-used-limits-for-admin",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "UserData",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-user-data",
                    "description": "Add user_data to the Create Server API."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "UserQuotas",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-user-quotas",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "VirtualInterfaces",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-virtual-interfaces",
                    "description": "Virtual interface support."
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "VolumeAttachmentUpdate",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-volume-attachment-update",
                    "description": ""
                },
                {
                    "updated": "2014-12-03T00:00:00Z",
                    "name": "Volumes",
                    "links": [],
                    "namespace": "http://docs.openstack.org/compute/ext/fake_xml",
                    "alias": "os-volumes",
                    "description": "Volumes support."
                }
            ]
        }

    def getLimits(self):
        return {}, {
            "limits": {
                "rate": [],
                "absolute": {
                    "maxServerMeta": 128,
                    "maxPersonality": 5,
                    "totalServerGroupsUsed": 0,
                    "maxImageMeta": 128,
                    "maxPersonalitySize": 10240,
                    "maxTotalKeypairs": 100,
                    "maxSecurityGroupRules": 20,
                    "maxServerGroups": 10,
                    "totalCoresUsed": 1,
                    "totalRAMUsed": 2048,
                    "totalInstancesUsed": 1,
                    "maxSecurityGroups": 10,
                    "totalFloatingIpsUsed": 0,
                    "maxTotalCores": 20,
                    "maxServerGroupMembers": 10,
                    "maxTotalFloatingIps": 10,
                    "totalSecurityGroupsUsed": 1,
                    "maxTotalInstances": 10,
                    "maxTotalRAMSize": 51200
                }
            }
        }
