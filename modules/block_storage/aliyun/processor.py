# -*- coding: utf-8 -*-
from cloudGate.modules.block_storage.process_base import *
from cloudGate.config import *
from aliyunsdkcore import client
'''
from aliyunsdkecs.request.v20140526 import CreateDisk
from aliyunsdkecs.request.v20140526 import DescribeDisks
from aliyunsdkecs.request.v20140526 import AttachDisk
from aliyunsdkecs.request.v20140526 import DetachDisk
from aliyunsdkecs.request.v20140526 import ModifyDiskAttribute
from aliyunsdkecs.request.v20140526 import DeleteDisk
from aliyunsdkecs.request.v20140526 import ReInitDisk
from aliyunsdkecs.request.v20140526 import ResetDisk
from aliyunsdkecs.request.v20140526 import ReplaceSystemDisk
from aliyunsdkecs.request.v20140526 import ResizeDisk
from aliyunsdkecs.request.v20140526 import CreateSnapshot
from aliyunsdkecs.request.v20140526 import DeleteSnapshot
from aliyunsdkecs.request.v20140526 import DescribeSnapshots
from aliyunsdkecs.request.v20140526 import ModifyAutoSnapshotPolicy
from aliyunsdkecs.request.v20140526 import DescribeAutoSnapshotPolicy
'''
from aliyunsdkecs.request.v20140526 import CreateDiskRequest
from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
from aliyunsdkecs.request.v20140526 import AttachDiskRequest
from aliyunsdkecs.request.v20140526 import DetachDiskRequest
from aliyunsdkecs.request.v20140526 import ModifyDiskAttributeRequest
from aliyunsdkecs.request.v20140526 import DeleteDiskRequest
from aliyunsdkecs.request.v20140526 import ReInitDiskRequest
from aliyunsdkecs.request.v20140526 import ResetDiskRequest
from aliyunsdkecs.request.v20140526 import ReplaceSystemDiskRequest
from aliyunsdkecs.request.v20140526 import ResizeDiskRequest
from aliyunsdkecs.request.v20140526 import CreateSnapshotRequest
from aliyunsdkecs.request.v20140526 import DeleteSnapshotRequest
from aliyunsdkecs.request.v20140526 import DescribeSnapshotsRequest
from aliyunsdkecs.request.v20140526 import ModifyAutoSnapshotPolicyRequest
from aliyunsdkecs.request.v20140526 import DescribeAutoSnapshotPolicyRequest
from aliyunsdkecs.request.v20140526 import ModifySnapshotAttributeRequest


##NOTEST    no test 
##NOURLCALL no http url call this function
##NOMATCH:  aliyun openstack params not matched
TEST_FLAG = 0

import json

class AliyunBlockStorageProcessor(BlockStorageProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]
        
        print "WUJUN token is ", self.token
        print "WUJUN regin is ", self.regin
        
        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)
    
    def _convertDiskStatus2VolumeStatus(self, disk_status):
        ## Aliyun       In_use | Available | Attaching | Detaching | Creating | ReIniting | All
        ## Openstack    creating | available | attaching | in-use | deleting | error | error_deleting
        ##              backing-up | restoring-backup | error_restoring | error_extending
        #### PARAM NOMATCH
        """
        volume_status = "available"
        if disk_status == "In_use":
            volume_status = "in-use"
        elif disk_status == "Available":
            volume_status = "available"
        elif disk_status == "Attaching":
            volume_status = "attaching"
        elif disk_status == "Detaching":
            volume_status = "available"
        elif disk_status == "Creating":
            volume_status = "creating"
        elif disk_status == "ReIniting":
            volume_status = "available"
        elif disk_status == "All":
            volume_status = "available"
        print "disk_status is ", disk_status, "   convert volume_status is  ", volume_status
        return volume_status
        """
        """
        volume_status = None
        if disk_status == "In_use":
            volume_status = "in-use"
        else:
            volume_status = "available"
        return volume_status
        """
        ### for test
        return "available"
        ## if in-use status not allowed delete
        ## return "in-use"
    
    def _convertVolumeStatus2DiskStatus(self, volume_status):
        """
        disk_status = "Available"
        if volume_status == "available":
            disk_status = "Available"
        elif volume_status == "in-use":
            disk_status = "In_use"
        elif volume_status == "attaching":
            disk_status = "Attaching"
        elif volume_status == "deleting":
            disk_status = "Detaching"
        elif volume_status == "creating":
            disk_status = "Creating"
        print "volume_status is ", volume_status, "   convert disk_status is  ", disk_status
        return disk_status
        """
        """
        if volume_status == "in-use":
            disk_status = "In_use"
        else:
            disk_status = "Available"
        return disk_status
        """
        ### for test
        ## return "Available"
        return "In_use"
        
    def _convertSnapshotStatusAliyun2Openstack(self, aliyun_snapshot_status):
        ## aliyun: progressing | accomplished | failed | all
        ## openstack: creating | available | deleting | error | error_deleting
        return "available"
    
    def _convertSnapshotStatusOpenstack2Aliyun(self, openstack_snapshot_status):
        ## aliyun: progressing | accomplished | failed | all
        ## openstack: creating | available | deleting | error | error_deleting        
        return "accomplished"
    
    def queryVolumes(self, tenant_id, sort, limit, marker):
        print "queryVolumes WUJUN Begin ...... , tenant_id is ", tenant_id, "  sort is ", sort, "  limit is ", limit, "   marker is ", marker
        if TEST_FLAG:
            resp = {
                "volumes": [
                    {
                        "id": "45baf976-c20a-4894-a7c3-c94b7376bf55",
                        "links": [
                            {
                                "href": "http://localhost:8776/v2/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/45baf976-c20a-4894-a7c3-c94b7376bf55",
                                "rel": "self"
                            },
                            {
                                "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/45baf976-c20a-4894-a7c3-c94b7376bf55",
                                "rel": "bookmark"
                            }
                        ],
                        "name": "vol-004"
                    },
                    {
                        "id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
                        "links": [
                            {
                                "href": "http://localhost:8776/v2/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                                "rel": "self"
                            },
                            {
                                "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                                "rel": "bookmark"
                            }
                        ],
                        "name": "vol-003"
                    }
                ]
            }
        else:
            r = DescribeDisksRequest.DescribeDisksRequest()
            '''
            r.set_InstanceId()
            r.set_DiskType()
            r.set_Category()
            r.set_Status()
            r.set_SnapshotId()
            r.set_Portable()
            r.set_PageNumber()
            r.set_PageSize()
            r.set_DiskName()
            '''
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "queryVolumes WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]
            resp = {
                "volumes":[
                    {
                        "id":v["DiskId"],
                        "links":[
                            {
                                "href":"http://",
                                "rel":"self"
                            },
                            {
                                "href":"http://",
                                "rel":"bookmark"
                            }
                        ],
                        "name":v["DiskName"]
                    }
                    for v in volumesdetail
                ]
            }
        return resp
    
    def createVolume(self, tenant_id, size, availability_zone, source_volid,
                description, multiattach, snapshot_id, name, imageRef,
                volume_type, metadata, source_replica, consistencygroup_id):
        print "createVolume WUJUN Begin ...... "
        if TEST_FLAG:
            resp = {
                "volume": {
                    "status": "creating",
                    "migration_status": None,
                    "user_id": "0eea4eabcf184061a3b6db1e0daaf010",
                    "attachments": [],
                    "links": [
                        {
                            "href": "http://23.253.248.171:8776/v2/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                            "rel": "self"
                        },
                        {
                            "href": "http://23.253.248.171:8776/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                            "rel": "bookmark"
                        }
                    ],
                    "availability_zone": "nova",
                    "bootable": "false",
                    "encrypted": False,
                    "created_at": "2015-11-29T03:01:44.000000",
                    "description": None,
                    "updated_at": None,
                    "volume_type": "lvmdriver-1",
                    "name": "test-volume-attachments",
                    "replication_status": "disabled",
                    "consistencygroup_id": None,
                    "source_volid": None,
                    "snapshot_id": None,
                    "multiattach": False,
                    "metadata": {},
                    "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                    "size": 2
                }
            }
        else:
            print "source_volid is ", source_volid, "  snapshot_id is ", snapshot_id
            if source_volid:
                print "Not Supported create disk used by source volid. Error!!! Error!!! Error!!!"
                return None
            disk_category = volume_type.split(" ")[1]
            min_size = 0
            max_size = 0
            if disk_category == "cloud":
                min_size = 5
                max_size = 2000
            elif disk_category == "cloud_efficiency":
                min_size = 20
                max_size = 2048
            elif disk_category == "cloud_ssd":
                min_size = 20
                max_size = 1024
            else:
                print "Disk Category is Error Error Error !!!!!!!"
                return None
            
            r = CreateDiskRequest.CreateDiskRequest()
            r.set_ZoneId("cn-hongkong-b")
            r.set_DiskName(name)

            if size < min_size:
                size = min_size
            if size > max_size:
                size = max_size
            r.set_Size(size)   
            r.set_Description(description)
            if not(snapshot_id is None):
                r.set_SnapshotId(snapshot_id)                                     
            r.set_DiskCategory(disk_category)

            ### r.set_ClientToken(self.token)      
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            print "createVolume WUJUN response is ", json.dumps(resp, indent=4)
            ### if not resp.has_key("DiskId"):
            if resp.has_key("Code"):
                print "Aliyun Create Disk Operation have Error!!!!!!"
                return None
            
            disk_id = resp["DiskId"]
            
            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            print "when createVolume, queryVolume WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]  
            resp = { "volume": {} }
            for v in volumesdetail:
                if v["DiskId"]==disk_id:
                    resp = {
                        "volume": {
                            "status": self._convertDiskStatus2VolumeStatus(v["Status"]),##"creating",
                            "migration_status": None,
                            "user_id": "0eea4eabcf184061a3b6db1e0daaf010",
                            "attachments": [],
                            "links": [
                                {
                                    "href":"http://",
                                    "rel": "self"
                                },
                                {
                                    "href":"http://",
                                    "rel": "bookmark"
                                }
                            ],
                            "availability_zone": v["ZoneId"], ##"nova",
                            "bootable": "false",
                            "encrypted": False,
                            "created_at": v["CreationTime"],
                            "description": v["Description"],
                            "updated_at": None,
                            "volume_type": v["Type"],##"lvmdriver-1",
                            "name": v["DiskName"],
                            "replication_status": "disabled",
                            "consistencygroup_id": None,
                            "source_volid": None,
                            "snapshot_id": v["SourceSnapshotId"],
                            "multiattach": False,
                            "metadata": {},
                            "id": v["DiskId"],
                            "size": v["Size"]
                        }
                    }            
        return resp
    
    
    def queryVolumesDetails(self, tenant_id, sort, limit, marker):
        print "queryVolumesDetails WUJUN Begin ...... , tenant_id is ", tenant_id, "  sort is ", sort, "  limit is ", limit, "   marker is ", marker
        if TEST_FLAG:
            resp = {
                "volumes": [
                    {
                        "migration_status": None,
                        "attachments": [
                        ],
                        "links": [ 
                            {
                                "href": "http://",
                                "rel": "self"
                            },
                            {
                                "href": "http://",
                                "rel": "bookmark"
                            },
                        ],
                        "availability_zone": "nova",
                        "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1", ##None,
                        "encrypted": False,
                        "os-volume-replication:extended_status": None,
                        "replication_status": "disabled",
                        "snapshot_id": None,
                        "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                        "size": 2,
                        "user_id": "32779452fcd34ae1a53a797ac8a1e064",
                        "os-vol-tenant-attr:tenant_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",
                        "os-vol-mig-status-attr:migstat": None,
                        "metadata": {
                        },
                        "status": "in-use",
                        "description": None,
                        "multiattach": True,
                        "os-volume-replication:driver_data": None,
                        "source_volid": None,
                        "consistencygroup_id": None,
                        "os-vol-mig-status-attr:name_id": None,
                        "name": "test-volume-attachments",
                        "bootable": "false",
                        "created_at": "2015-11-29T03:01:44.000000",
                        "volume_type": "system"##"lvmdriver-1"
                    }
                ]
            }
        else:    
            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "queryVolumesDetails WUJUN Origin Data *********####### response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]             
            
            resp = {
                "volumes":[
                    {
                        "migration_status": None,
                        "attachments": [                        
                        ],
                        "links": [ 
                            {
                                "href": "http://",
                                "rel": "self"
                            },
                            {
                                "href": "http://",
                                "rel": "bookmark"
                            },
                        ],
                        "availability_zone": v["ZoneId"], ##"nova"
                        "os-vol-host-attr:host": None, ##"difleming@lvmdriver-1#lvmdriver-1",
                        "encrypted": False,
                        "os-volume-replication:extended_status": None,
                        "replication_status": "disabled",
                        "snapshot_id": v["SourceSnapshotId"],
                        "id": v["DiskId"],
                        "size": v["Size"],
                        "user_id": None, ##"32779452fcd34ae1a53a797ac8a1e064",
                        "os-vol-tenant-attr:tenant_id": None, ##"bab7d5c60cd041a0a36f7c4b6e1dd978",
                        "os-vol-mig-status-attr:migstat": None,
                        "metadata": {},
                        "status": self._convertDiskStatus2VolumeStatus(v["Status"]), ###"in-use", ###v["Status"],
                        "description": v["Description"],
                        "multiattach": False,
                        "os-volume-replication:driver_data": None,
                        "source_volid": None,
                        "consistencygroup_id": None,
                        "os-vol-mig-status-attr:name_id": None,
                        "name": v["DiskName"],
                        "bootable": "true",
                        "created_at": v["CreationTime"], 
                        "volume_type": v["Type"]
                    }
                    for v in volumesdetail
                ]
            }
            pass
        return resp
    
    
    def queryVolume(self, tenant_id, volume_id):
        if TEST_FLAG:
            resp = {
                "volume": {
                    "status": "available",
                    "attachments": [],
                    "links": [
                        {
                            "href": "http://localhost:8776/v2/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                            "rel": "self"
                        },
                        {
                            "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                            "rel": "bookmark"
                        }
                    ],
                    "availability_zone": "nova",
                    "bootable": "true",
                    "os-vol-host-attr:host": "ip-10-168-107-25",
                    "source_volid": None,
                    "snapshot_id": None,
                    "id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "description": "Super volume.",
                    "name": "vol-002",
                    "created_at": "2013-02-25T02:40:21.000000",
                    "volume_type": "None",
                    "os-vol-tenant-attr:tenant_id": "0c2eba2c5af04d3f9e9d0d410b371fde",
                    "size": 1,
                    "os-volume-replication:driver_data": None,
                    "os-volume-replication:extended_status": None,
                    "metadata": {
                        "contents": "not junk"
                    }
                }
            }            
            pass
        else:
            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "queryVolume WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]  
            resp = { "volume": {} }
            for v in volumesdetail:
                if v["DiskId"]==volume_id:
                    resp = {
                        "volume": {
                            "status": self._convertDiskStatus2VolumeStatus(v["Status"]), ###v["Status"],
                            "attachments": [],
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
                            "availability_zone": v["ZoneId"], ##"nova", 
                            "bootable": "true",
                            "os-vol-host-attr:host": None, ##"ip-10-168-107-25", 
                            "source_volid": None,
                            "snapshot_id": v["SourceSnapshotId"],
                            "id":  v["DiskId"],
                            "description": v["Description"],
                            "name": v["DiskName"],
                            "created_at": v["CreationTime"],
                            "volume_type": v["Type"],
                            "os-vol-tenant-attr:tenant_id": None, ##"0c2eba2c5af04d3f9e9d0d410b371fde", #None
                            "size": v["Size"],
                            "os-volume-replication:driver_data": None,
                            "os-volume-replication:extended_status": None,
                            "metadata": {}
                        }  
                    }
        return resp
        pass
    
    def updateVolume(self, tenant_id, volume_id, name, description):
        ### NOCALL
        print "there is no called"    
        print "updateVolume WUJUN Begin ...... "
        if TEST_FLAG:
            resp = {
                "volume": {
                    "status": "available",
                    "migration_status": None,
                    "user_id": "0eea4eabcf184061a3b6db1e0daaf010",
                    "attachments": [],
                    "links": [
                        {
                            "href": "http://localhost:8776/v2/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                            "rel": "self"
                        },
                        {
                            "href": "http://localhost:8776/0c2eba2c5af04d3f9e9d0d410b371fde/volumes/5aa119a8-d25b-45a7-8d1b-88e127885635",
                            "rel": "bookmark"
                        }
                    ],
                    "availability_zone": "nova",
                    "bootable": "false",
                    "encrypted": False,
                    "created_at": "2015-11-29T03:01:44.000000",
                    "description": "This is yet, another volume.",
                    "updated_at": None,
                    "volume_type": "lvmdriver-1",
                    "name": "vol-003",
                    "replication_status": "disabled",
                    "consistencygroup_id": None,
                    "source_volid": None,
                    "snapshot_id": None,
                    "multiattach": None,
                    "metadata": {
                        "contents": "not junk"
                    },
                    "id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "size": 1
                }
            }            
        else:
            print "updateVolume WUJUN begin ...."        
            r = ModifyDiskAttributeRequest.ModifyDiskAttributeRequest()
            r.set_accept_format('json')
            r.set_DiskId(volume_id);
            r.set_DiskName(name);
            r.set_Description(description);
            response = self.clt.do_action(r)
            resp = json.loads(response) 
            print "updateVolume WUJUN response:", json.dumps(resp, indent=4)    
            if resp.has_key("Code"):
                print "Aliyun Modify Disk Attribute Operation Failed, Have Error"
                return False

            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "when update volume, queryVolume WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]  
            resp = { "volume": {} }
            for v in volumesdetail:
                if v["DiskId"]==volume_id:
                    resp = {
                        "volume": {
                            "status": self._convertDiskStatus2VolumeStatus(v["Status"]), ###v["Status"],
                            "migration_status": None,
                            "user_id": "0eea4eabcf184061a3b6db1e0daaf010",
                            "attachments": [],
                            "links": [
                                {
                                    "href":"http://",
                                    "rel": "self"
                                },
                                {
                                    "href":"http://",
                                    "rel": "bookmark"
                                }
                            ],
                            "availability_zone": v["ZoneId"],##"nova",
                            "bootable": "false",
                            "encrypted": False,
                            "created_at": v["CreationTime"],
                            "description": v["Description"],
                            "updated_at": None,
                            "volume_type": v["Type"], ##"lvmdriver-1",
                            "name": v["DiskName"],
                            "replication_status": "disabled",
                            "consistencygroup_id": None,
                            "source_volid": None,
                            "snapshot_id": v["SourceSnapshotId"],
                            "multiattach": False,
                            "metadata": {},
                            "id": v["DiskId"],
                            "size": v["Size"]
                        }
                    }                
        return resp
    
    def deleteVolume(self, tenant_id, volume_id):
        print "deleteVolume WUJUN begin .... tenant_id is ", tenant_id, "  volume_id is ", volume_id     
        r = DeleteDiskRequest.DeleteDiskRequest()
        r.set_DiskId(volume_id)
        r.set_accept_format('json')
        response = self.clt.do_action(r)
        resp = json.loads(response)
        print "deleteVolume WUJUN response:", json.dumps(resp, indent=4) 
        if resp.has_key("Code"):
            print "Aliyun Delete Disk Operation Failed, Have Error"
            return False
        return True   
    
    
    def queryVolumeMetadata(self, tenant_id, volume_id):
        pass
    
    def updataVolumeMetadata(self, name):
        pass
    
    
    def volumeAction(self, tenant_id, volume_id, action):
        print "$$$$$$$$$$$  Volume Action is ", json.dumps(action, indent=4)
        if action.has_key("os-reset_status"):
            ##aliyun NOSUPPORT
            print "aliyun not support os-reset_status volume status. Warn!!! Warn!!!"
            return False
            """
            {
                "os-reset_status": {
                    "status": "available",
                    "attach_status": "detached",
                    "migration_status": "migrating"
                }
            }            
            """
            print "volumeAction os-reset_status WUJUN begin ...."        
            r = ModifyDiskAttributeRequest.ModifyDiskAttributeRequest()
            r.set_accept_format('json')
            r.set_DiskId(volume_id);
            ## r.set_DiskName("");
            r.set_Description("ModifyDescription ... test ...");
            response = self.clt.do_action(r)
            resp = json.loads(response) 
            print "volumeAction os-reset_status WUJUN response:", json.dumps(resp, indent=4)
            if resp.has_key("Code"):
                print "volumeAction os-reset_status Failed!!! Have Error!!!"
                return False
                pass
            pass
        elif action.has_key("os-attach"):
            ### NOTEST  NOURLCALL
            """
            {
                "os-attach": {
                    "instance_uuid": "95D9EF50-507D-11E5-B970-0800200C9A66",
                    "mountpoint": "/dev/vdc"
                }
            } 
            """
            r = AttachDiskRequest.AttachDiskRequest()
            r.set_InstanceId(action["os-attach"]["instance_uuid"])
            r.set_DiskId(volume_id)
            r.set_Device(action["os-attach"]["mountpoint"])
            r.set_DeleteWithInstance(True)  ## or False
            response = self.clt.do_action(r)
            resp = json.loads(response) 
            print "volumeAction os-attach WUJUN response:", json.dumps(resp, indent=4)
            if resp.has_key("Code"):
                print "volumeAction os-attach Failed!!! Have Error!!!"
                return False
        elif action.has_key("os-force_detach"):
            ### NOTEST NOURLCALL
            ### aliyun need instanceID and diskID but opengstack is attachment_id
            ### solve the way attachment_id real value is instanceID
            """
            {
                "os-force_detach": {
                    "attachment_id": "d8777f54-84cf-4809-a679-468ffed56cf1",
                    "connector": {
                        "initiator": "iqn.2012-07.org.fake:01"
                    }
                }
            }            
            """
            
            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "when os-force_detach, queryVolumesList WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]  
            instance_id = None
            for v in volumesdetail:            
                if v["DiskId"]==volume_id:
                    instance_id = v["InstanceId"]
            if not instance_id:
                print "Disk ID is ", volume_id, " not attached, so no find related instance_id ", instance_id 
                return False
            r = DetachDiskRequest.DetachDiskRequest()
            r.set_InstanceId(instance_id)
            r.set_DiskId(volume_id)
            response = self.clt.do_action(r)
            resp = json.loads(response) 
            print "volumeAction os-force_detach WUJUN response:", json.dumps(resp, indent=4)
            if resp.has_key("Code"):
                print "volumeAction os-force_detach Failed!!! Have Error!!!"
                return False
        elif action.has_key("os-extend"):
            ##aliyun NOSUPPORT
            print "aliyun not support os-extend dynamic change volume size. Warn!!! Warn!!!"
            return False
        elif action.has_key("os-set_image_metadata"):
            ##aliyun NOSUPPORT
            print "aliyun not support os-set_image_metadata"
            return False
        elif action.has_key("os-unmanage"):
            ##aliyun NOSUPPORT
            print "aliyun not support os-unmanage"
            return False
        elif action.has_key("os-promote-replica"):
            print "aliyun not support os-promote-replica"
            ##aliyun NOSUPPORT
            return False
        elif action.has_key("volume-replica-reenable"):
            ##aliyun NOSUPPORT
            print "aliyun not support volume-replica-reenable"
            return False
            pass        
        else:
            print "Unknown Error!!! Unknown Error!!! Unknown Error!!!"
            return False
        return True

    
    def querySnapshots(self, tenant_id, sort_key, sort_dir, limit, marker):
        ##TODO NOURLCALL
        print "querySnapshots WUJUN Begin ...... "
        if TEST_FLAG:
            resp = {
                "snapshots": [
                    {
                        "status": "available",
                        "metadata": {
                            "name": "test"
                        },
                        "name": "test-volume-snapshot",
                        "volume_id": "173f7b48-c4c1-4e70-9acc-086b39073506",
                        "created_at": "2015-11-29T02:25:51.000000",
                        "size": 1,
                        "id": "b1323cda-8e4b-41c1-afc5-2fc791809c8c",
                        "description": "volume snapshot"
                    }
                ]
            }
        else:
            print "querySnapshots WUJUN begin ...."        
            r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
            
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ##print "querySnapshots WUJUN response:", json.dumps(resp, indent=4)
            snapshots = resp["Snapshots"]["Snapshot"] 
            
            resp = {
                "snapshots":[
                    {
                        "status":self._convertSnapshotStatusAliyun2Openstack(s["Status"]), ##s["Status"],
                        "metadata":{},
                        "name": s["SnapshotName"],
                        "volume_id": s["SourceDiskId"],
                        "created_at": s["CreationTime"],    
                        "size":s["SourceDiskSize"],
                        "id":s["SnapshotId"],
                        "description":s["Description"]
                    }
                    for s in snapshots
                ]
            }
        return resp 
    
    def createSnapshot(self, tenant_id, name, description, volume_id, force):
        print "createSnapshot WUJUN Begin ...... "
        if TEST_FLAG:
            resp = {
                "snapshot": {
                    "status": "creating",
                    "description": "Daily backup",
                    "created_at": "2013-02-25T03:56:53.081642",
                    "metadata": {},
                    "volume_id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "size": 1,
                    "id": "ffa9bc5e-1172-4021-acaf-cdcd78a9584d",
                    "name": "snap-001"
                }
            } 
        else:
            r = CreateSnapshotRequest.CreateSnapshotRequest()
            r.set_DiskId(volume_id)
            r.set_SnapshotName(name)
            r.set_Description(description)     
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            print "createSnapshot WUJUN response is ", json.dumps(resp, indent=4)
            ### if not resp.has_key("SnapshotId"):
            if resp.has_key("Code"):
                print "Aliyun Create Snapshot Operation have Error!!!!!!"
                return None

            snapshot_id = resp["SnapshotId"]
            
            r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            print "when create Snapshot, query snapshots list WUJUN response:", json.dumps(resp, indent=4)
            snapshots = resp["Snapshots"]["Snapshot"]
            resp = { "snapshot": {} }
            for s in snapshots:
                if s["SnapshotId"]==snapshot_id:
                    resp = {
                        "snapshot": {
                            "status": self._convertSnapshotStatusAliyun2Openstack(s["Status"]),##s["Status"],
                            "description": s["Description"],
                            "created_at": s["CreationTime"],
                            "metadata": {},
                            "volume_id": s["SourceDiskId"],
                            "size": s["SourceDiskSize"],
                            "id": s["SnapshotId"],
                            "name": s["SnapshotName"]
                        }
                    }
        return resp
    
    
    def querySnapshotsDetails(self, tenant_id):
        if TEST_FLAG:
            ## faked data for test
            resp = {
                "snapshots": [
                    {
                        "status": "available",
                        "metadata": {
                            "name": "test"
                        },
                        "os-extended-snapshot-attributes:progress": "100%",
                        "name": "test-volume-snapshot",
                        "volume_id": "173f7b48-c4c1-4e70-9acc-086b39073506",
                        "os-extended-snapshot-attributes:project_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",
                        "created_at": "2015-11-29T02:25:51.000000",
                        "size": 1,
                        "id": "b1323cda-8e4b-41c1-afc5-2fc791809c8c",
                        "description": "volume snapshot"
                    }
                ]
            }
        else:
            print "querySnapshotsDetails WUJUN begin ...."        
            r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
            
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ##print "querySnapshotsDetails WUJUN response:", json.dumps(resp, indent=4)
            snapshots = resp["Snapshots"]["Snapshot"] 
            
            resp = {
                "snapshots":[
                    {
                        "status":self._convertSnapshotStatusAliyun2Openstack(s["Status"]), ##s["Status"],
                        "metadata":{},
                        "os-extended-snapshot-attributes:progress": s["Progress"],
                        "name": s["SnapshotName"],
                        "volume_id": s["SourceDiskId"],
                        "os-extended-snapshot-attributes:project_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",##None ##s["ProductCode"],
                        "created_at": s["CreationTime"],    
                        "size":s["SourceDiskSize"],
                        "id":s["SnapshotId"],
                        "description":s["Description"]
                    }
                    for s in snapshots
                ]
            }
        return resp
    
    
    def querySnapshot(self, tenant_id, snapshot_id):
        if TEST_FLAG:
            ## faked data for test
            resp = {
                "snapshot": {
                    "status": "available",
                    "os-extended-snapshot-attributes:progress": "100%",
                    "description": "Daily backup",
                    "created_at": "2013-02-25T04:13:17.000000",
                    "metadata": {},
                    "volume_id": "5aa119a8-d25b-45a7-8d1b-88e127885635",
                    "os-extended-snapshot-attributes:project_id": "0c2eba2c5af04d3f9e9d0d410b371fde",
                    "size": 1,
                    "id": "2bb856e1-b3d8-4432-a858-09e4ce939389",
                    "name": "snap-001"
                }
            }              
            pass
        else:
            print "querySnapshot WUJUN begin ...."        
            r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
            
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ##print "querySnapshotsDetails WUJUN response:", json.dumps(resp, indent=4)
            snapshots = resp["Snapshots"]["Snapshot"]

            resp = { "snapshot": {} }
            for s in snapshots:
                if s["SnapshotId"]==snapshot_id:                        
                    resp = {
                        "snapshot": {
                            "status": self._convertSnapshotStatusAliyun2Openstack(s["Status"]), ## s["Status"],
                            "os-extended-snapshot-attributes:progress": s["Progress"],
                            "description": s["Description"],
                            "created_at": s["CreationTime"],
                            "metadata": {},
                            "volume_id": s["SourceDiskId"],
                            "os-extended-snapshot-attributes:project_id": None, ##"0c2eba2c5af04d3f9e9d0d410b371fde",
                            "size": s["SourceDiskSize"],
                            "id": s["SnapshotId"],
                            "name": s["SnapshotName"]
                        }
                    }
        return resp
        pass
    
    def deleteSnapshot(self, tenant_id, snapshot_id):
        print "deleteSnapshot WUJUN begin .... snapshot_id is ", snapshot_id        
        r = DeleteSnapshotRequest.DeleteSnapshotRequest()
        r.set_SnapshotId(snapshot_id)
        r.set_accept_format('json')
        response = self.clt.do_action(r)
        resp = json.loads(response)
        print "deleteSnapshot WUJUN response:", json.dumps(resp, indent=4)  
        if resp.has_key("Code"):
            print "Delete Snapshot Failed"
            pass
        return True
        pass 
    
    def updateSnapshot(self, tenant_id, snapshot_id, name, description):
        print "updateSnapshot WUJUN Begin ...... "
        if TEST_FLAG:
            resp = {
                "snapshot": {
                    "created_at": "2013-02-20T08:11:34.000000",
                    "description": "This is yet, another snapshot",
                    "name": "snap-002",
                    "id": "4b502fcb-1f26-45f8-9fe5-3b9a0a52eaf2",
                    "size": 1,
                    "status": "available",
                    "volume_id": "2402b902-0b7a-458c-9c07-7435a826f794"
                }
            }
        else:
            r = ModifySnapshotAttributeRequest.ModifySnapshotAttributeRequest()
            r.set_SnapshotId(snapshot_id)
            r.set_SnapshotName(name)
            r.set_Description(description)     
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            print "updateSnapshot WUJUN response is ", json.dumps(resp, indent=4)
            ### if not resp.has_key("SnapshotId"):
            if resp.has_key("Code"):
                print "Aliyun Update Snapshot Operation have Error!!!!!!"
                return None            
            r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ### print "when updateSnapshot, query snapshot list WUJUN response:", json.dumps(resp, indent=4)
            snapshots = resp["Snapshots"]["Snapshot"]
            resp = { "snapshot": {} }
            for s in snapshots:
                if s["SnapshotId"]==snapshot_id:
                    resp = {
                        "snapshot": {
                            "created_at": s["CreationTime"],
                            "description": s["Description"],
                            "name": s["SnapshotName"],
                            "id": s["SnapshotId"],
                            "size": s["SourceDiskSize"],
                            "status": self._convertSnapshotStatusAliyun2Openstack(s["Status"]), ### s["Status"],
                            "volume_id": s["SourceDiskId"]
                        }
                    }
        return resp
    
    
    def querySnapshotMetadata(self, tenant_id, snapshot_id):
        pass
    
    def updataSnapshotMetadata(self, tenant_id, snapshot_id, metadata):
        pass
    
    
    def queryOsVolumeTransferDetail(self, tenant_id):
        print "queryOsVolumeTransferDetail WUJUN Do Nothing, tenant_id is ", tenant_id        
        ## if TEST_FLAG:
        if 1:
            ## faked data
            resp = {
                "transfers": [
                    {
                        "id": "cac5c677-73a9-4288-bb9c-b2ebfb547377",
                        "created_at": "2015-02-25T03:56:53.081642",
                        "name": "first volume transfer",
                        "volume_id": "894623a6-e901-4312-aa06-4275e6321cce",
                        "links": [
                            {
                                "href": "http://localhost/v2/firstproject/volumes/1",
                                "rel": "self"
                            },
                            {
                                "href": "http://localhost/firstproject/volumes/1",
                                "rel": "bookmark"
                            }
                        ]
                    },
                    {
                        "id": "f26c0dee-d20d-4e80-8dee-a8d91b9742a1",
                        "created_at": "2015-03-25T03:56:53.081642",
                        "name": "second volume transfer",
                        "volume_id": "673db275-379f-41af-8371-e1652132b4c1",
                        "links": [
                            {
                                "href": "http://localhost/v2/firstproject/volumes/2",
                                "rel": "self"
                            },
                            {
                                "href": "http://localhost/firstproject/volumes/2",
                                "rel": "bookmark"
                            }
                        ]
                    }
                ]
            }
        return resp
        
        
    def queryQosSpecs(self, tenant_id, sort_key, sort_dir, limit, marker):
        print "queryQosSpecs WUJUN Do Nothing, tenant_id is ", tenant_id, "  sort_key is ", sort_key, "  sort_dir is ", sort_dir, "  limit is ", limit, "   marker is ", marker         
        ## if TEST_FLAG:
        if 1:
            resp = {
                "qos_specs": [
                    {
                        "specs": {
                            "availability": "100",
                            "numberOfFailures": "0"
                        },
                        "consumer": "back-end",
                        "name": "reliability-spec",
                        "id": "0388d6c6-d5d4-42a3-b289-95205c50dd15"
                    },
                    {
                        "specs": {
                            "delay": "0",
                            "throughput": "100"
                        },
                        "consumer": "back-end",
                        "name": "performance-spec",
                        "id": "ecfc6e2e-7117-44a4-8eec-f84d04f531a8"
                    }
                ]
            }            
            pass
        return resp
        pass
    
    
    def queryVolumeTypes(self, tenant_id, sort_key, sort_dir, limit, marker):
        print "queryTypes WUJUN Do Nothing, tenant_id is ", tenant_id, "  sort_key is ", sort_key, "  sort_dir is ", sort_dir, "  limit is ", limit, "   marker is ", marker        
        ## aliyun disk_type        all | system | data
        ## aliyun disk_category    all | cloud | cloud_efficiency | cloud_ssd | ephemeral | ephemeral_ssd
        ## if TEST_FLAG:
        if 1:
            resp = {
                "volume_types": [
                    {
                        "extra_specs": { },
                        "id": "6685584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "data cloud_efficiency"
                    },
                    {
                        "extra_specs": { },
                        "id": "1185584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "data cloud_ssd"
                    },
                    {
                        "extra_specs": { },
                        "id": "2285584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "data cloud"
                    },
                    {
                        "extra_specs": { },
                        "id": "3385584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "data ephemeral"
                    },
                    {
                        "extra_specs": { },
                        "id": "4485584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "data ephemeral_ssd"
                    }                    
                ]
            }
        return resp


    def queryVolumeTypeDetail(self, tenant_id, volume_type_id):
        print "queryVolumeTypeDetail WUJUN Do Nothing, tenant_id is ", tenant_id, "  volume_type_id is ", volume_type_id       
        ## if TEST_FLAG:
        if 1:
            if volume_type_id == "6685584b-1eac-4da6-b5c3-555430cf68ff":
                resp = {
                    "volume_type": {
                        "id": "6685584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "vol-type-001",
                        "description": "volume type 001",
                        "is_public": "true",
                        "extra_specs": {
                        }
                    }
                }
            elif volume_type_id == "default":
                print "enter default volume type"
                resp = {
                    "volume_type": {
                        "id": "6685584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "vol-type-001",
                        "description": "volume type 001",
                        "is_public": "true",
                        "extra_specs": {
                        }
                    }
                }                
                pass
        return resp        
        pass
    
    
    def queryBlockStorageLimits(self, tenant_id):
        print "queryBlockStorageLimits WUJUN Do Nothing, tenant_id is ", tenant_id      
        ## if TEST_FLAG:
        if 1:
            resp = {
                "limits": {
                    "rate": [],
                    "absolute": {
                        "totalSnapshotsUsed": 0,
                        "maxTotalBackups": 10,
                        "maxTotalVolumeGigabytes": 1000,
                        "maxTotalSnapshots": 10,
                        "maxTotalBackupGigabytes": 1000,
                        "totalBackupGigabytesUsed": 0,
                        "maxTotalVolumes": 10,
                        "totalVolumesUsed": 0,
                        "totalBackupsUsed": 0,
                        "totalGigabytesUsed": 0
                    }
                }
            }
        return resp         
        pass
    
    
    def queryBlockStorageExtensions(self, tenant_id):
        print "queryBlockStorageExtensions WUJUN Do Nothing, tenant_id is ", tenant_id      
        ## if TEST_FLAG:
        if 1:
            resp = {
                "extensions": [
                    {
                        "updated": "2013-04-18T00:00:00+00:00",
                        "name": "SchedulerHints",
                        "links": [],
                        "namespace": "http://docs.openstack.org/block-service/ext/scheduler-hints/api/v2",
                        "alias": "OS-SCH-HNT",
                        "description": "Pass arbitrary key/value pairs to the scheduler."
                    },
                    {
                        "updated": "2011-06-29T00:00:00+00:00",
                        "name": "Hosts",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/hosts/api/v1.1",
                        "alias": "os-hosts",
                        "description": "Admin-only host administration."
                    },
                    {
                        "updated": "2011-11-03T00:00:00+00:00",
                        "name": "VolumeTenantAttribute",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume_tenant_attribute/api/v1",
                        "alias": "os-vol-tenant-attr",
                        "description": "Expose the internal project_id as an attribute of a volume."
                    },
                    {
                        "updated": "2011-08-08T00:00:00+00:00",
                        "name": "Quotas",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/quotas-sets/api/v1.1",
                        "alias": "os-quota-sets",
                        "description": "Quota management support."
                    },
                    {
                        "updated": "2011-08-24T00:00:00+00:00",
                        "name": "TypesManage",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/types-manage/api/v1",
                        "alias": "os-types-manage",
                        "description": "Types manage support."
                    },
                    {
                        "updated": "2013-07-10T00:00:00+00:00",
                        "name": "VolumeEncryptionMetadata",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/os-volume-encryption-metadata/api/v1",
                        "alias": "os-volume-encryption-metadata",
                        "description": "Volume encryption metadata retrieval support."
                    },
                    {
                        "updated": "2012-12-12T00:00:00+00:00",
                        "name": "Backups",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/backups/api/v1",
                        "alias": "backups",
                        "description": "Backups support."
                    },
                    {
                        "updated": "2013-07-16T00:00:00+00:00",
                        "name": "SnapshotActions",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/snapshot-actions/api/v1.1",
                        "alias": "os-snapshot-actions",
                        "description": "Enable snapshot manager actions."
                    },
                    {
                        "updated": "2012-05-31T00:00:00+00:00",
                        "name": "VolumeActions",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume-actions/api/v1.1",
                        "alias": "os-volume-actions",
                        "description": "Enable volume actions\n    "
                    },
                    {
                        "updated": "2013-10-03T00:00:00+00:00",
                        "name": "UsedLimits",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/used-limits/api/v1.1",
                        "alias": "os-used-limits",
                        "description": "Provide data on limited resources that are being used."
                    },
                    {
                        "updated": "2012-05-31T00:00:00+00:00",
                        "name": "VolumeUnmanage",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume-unmanage/api/v1.1",
                        "alias": "os-volume-unmanage",
                        "description": "Enable volume unmanage operation."
                    },
                    {
                        "updated": "2011-11-03T00:00:00+00:00",
                        "name": "VolumeHostAttribute",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume_host_attribute/api/v1",
                        "alias": "os-vol-host-attr",
                        "description": "Expose host as an attribute of a volume."
                    },
                    {
                        "updated": "2013-07-01T00:00:00+00:00",
                        "name": "VolumeTypeEncryption",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume-type-encryption/api/v1",
                        "alias": "encryption",
                        "description": "Encryption support for volume types."
                    },
                    {
                        "updated": "2013-06-27T00:00:00+00:00",
                        "name": "AvailabilityZones",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/os-availability-zone/api/v1",
                        "alias": "os-availability-zone",
                        "description": "Describe Availability Zones."
                    },
                    {
                        "updated": "2013-08-02T00:00:00+00:00",
                        "name": "Qos_specs_manage",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/qos-specs/api/v1",
                        "alias": "qos-specs",
                        "description": "QoS specs support."
                    },
                    {
                        "updated": "2011-08-24T00:00:00+00:00",
                        "name": "TypesExtraSpecs",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/types-extra-specs/api/v1",
                        "alias": "os-types-extra-specs",
                        "description": "Type extra specs support."
                    },
                    {
                        "updated": "2013-08-08T00:00:00+00:00",
                        "name": "VolumeMigStatusAttribute",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume_mig_status_attribute/api/v1",
                        "alias": "os-vol-mig-status-attr",
                        "description": "Expose migration_status as an attribute of a volume."
                    },
                    {
                        "updated": "2012-08-13T00:00:00+00:00",
                        "name": "CreateVolumeExtension",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/image-create/api/v1",
                        "alias": "os-image-create",
                        "description": "Allow creating a volume from an image in the Create Volume v1 API."
                    },
                    {
                        "updated": "2014-01-10T00:00:00-00:00",
                        "name": "ExtendedServices",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/extended_services/api/v2",
                        "alias": "os-extended-services",
                        "description": "Extended services support."
                    },
                    {
                        "updated": "2012-06-19T00:00:00+00:00",
                        "name": "ExtendedSnapshotAttributes",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/extended_snapshot_attributes/api/v1",
                        "alias": "os-extended-snapshot-attributes",
                        "description": "Extended SnapshotAttributes support."
                    },
                    {
                        "updated": "2012-12-07T00:00:00+00:00",
                        "name": "VolumeImageMetadata",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume_image_metadata/api/v1",
                        "alias": "os-vol-image-meta",
                        "description": "Show image metadata associated with the volume."
                    },
                    {
                        "updated": "2012-03-12T00:00:00+00:00",
                        "name": "QuotaClasses",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/quota-classes-sets/api/v1.1",
                        "alias": "os-quota-class-sets",
                        "description": "Quota classes management support."
                    },
                    {
                        "updated": "2013-05-29T00:00:00+00:00",
                        "name": "VolumeTransfer",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/volume-transfer/api/v1.1",
                        "alias": "os-volume-transfer",
                        "description": "Volume transfer management support."
                    },
                    {
                        "updated": "2014-02-10T00:00:00+00:00",
                        "name": "VolumeManage",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/os-volume-manage/api/v1",
                        "alias": "os-volume-manage",
                        "description": "Allows existing backend storage to be 'managed' by Cinder."
                    },
                    {
                        "updated": "2012-08-25T00:00:00+00:00",
                        "name": "AdminActions",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/admin-actions/api/v1.1",
                        "alias": "os-admin-actions",
                        "description": "Enable admin actions."
                    },
                    {
                        "updated": "2012-10-28T00:00:00-00:00",
                        "name": "Services",
                        "links": [],
                        "namespace": "http://docs.openstack.org/volume/ext/services/api/v2",
                        "alias": "os-services",
                        "description": "Services support."
                    }
                ]
            }
        return resp

        