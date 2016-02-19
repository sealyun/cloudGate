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
        if 1:
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
            r = CreateDiskRequest.CreateDiskRequest()
            ## r.set_OwnerId(owner_id)
            ## r.set_ResourceOwnerAccount(resource_owner_account)
            ## r.set_ResourceOwnerId(resource_owner_id)
            ##### r.set_ZoneId(self.regin)
            ## r.set_SnapshotId(snapshot_id)
            r.set_DiskName(name)
            r.set_Size(size)
            ## r.set_DiskCategory(disk_category)
            r.set_Description(description)
            ### r.set_ClientToken(self.token)
            ### r.set_OwnerAccount("wj")  ## wj or admin       
            r.set_accept_format('json')
            ### response = self.clt.do_action(r)
            print "createVolume WUJUN response is ", response
            return True
        return resp
    
    
    def queryVolumesDetails(self, tenant_id, sort, limit, marker):
        print "queryVolumesDetails WUJUN Begin ...... , tenant_id is ", tenant_id, "  sort is ", sort, "  limit is ", limit, "   marker is ", marker
        if TEST_FLAG:
            resp = {
                "volumes": [
                    {
                        "migration_status": None,
                        "attachments": [
                            {
                                "server_id": "f4fda93b-06e0-4743-8117-bc8bcecd651b",
                                "attachment_id": "3b4db356-253d-4fab-bfa0-e3626c0b8405",
                                "host_name": None,
                                "volume_id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38",
                                "device": "/dev/vdb",
                                "id": "6edbc2f4-1507-44f8-ac0d-eed1d2608d38"
                            }
                        ],
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
                        "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1",
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
                            "readonly": "false",
                            "attached_mode": "rw"
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
                        "volume_type": "lvmdriver-1"
                    },
                    {
                        "migration_status": None,
                        "attachments": [],
                        "links": [
                            {
                                "href": "http://23.253.248.171:8776/v2/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/173f7b48-c4c1-4e70-9acc-086b39073506",
                                "rel": "self"
                            },
                            {
                                "href": "http://23.253.248.171:8776/bab7d5c60cd041a0a36f7c4b6e1dd978/volumes/173f7b48-c4c1-4e70-9acc-086b39073506",
                                "rel": "bookmark"
                            }
                        ],
                        "availability_zone": "nova",
                        "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1",
                        "encrypted": False,
                        "os-volume-replication:extended_status": None,
                        "replication_status": "disabled",
                        "snapshot_id": None,
                        "id": "173f7b48-c4c1-4e70-9acc-086b39073506",
                        "size": 1,
                        "user_id": "32779452fcd34ae1a53a797ac8a1e064",
                        "os-vol-tenant-attr:tenant_id": "bab7d5c60cd041a0a36f7c4b6e1dd978",
                        "os-vol-mig-status-attr:migstat": None,
                        "metadata": {},
                        "status": "available",
                        "volume_image_metadata": {
                            "kernel_id": "8a55f5f1-78f7-4477-8168-977d8519342c",
                            "checksum": "eb9139e4942121f22bbc2afc0400b2a4",
                            "min_ram": "0",
                            "ramdisk_id": "5f6bdf8a-92db-4988-865b-60bdd808d9ef",
                            "disk_format": "ami",
                            "image_name": "cirros-0.3.4-x86_64-uec",
                            "image_id": "b48c53e1-9a96-4a5a-a630-2e74ec54ddcc",
                            "container_format": "ami",
                            "min_disk": "0",
                            "size": "25165824"
                        },
                        "description": "",
                        "multiattach": False,
                        "os-volume-replication:driver_data": None,
                        "source_volid": None,
                        "consistencygroup_id": None,
                        "os-vol-mig-status-attr:name_id": None,
                        "name": "test-volume",
                        "bootable": "true",
                        "created_at": "2015-11-29T02:25:18.000000",
                        "volume_type": "lvmdriver-1"
                    }
                ]
            }
        else:    
            r = DescribeDisksRequest.DescribeDisksRequest()
            r.set_accept_format('json')
            response = self.clt.do_action(r)
            resp = json.loads(response)
            ## print "queryVolumesDetails WUJUN response:", json.dumps(resp, indent=4)
            volumesdetail = resp["Disks"]["Disk"]             
            
            resp = {
                "volumes":[
                    {
                        "migration_status": None,
                        "attachments": [],
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
                        "availability_zone": v["ZoneId"],
                        "os-vol-host-attr:host": "difleming@lvmdriver-1#lvmdriver-1",
                        "encrypted": False,
                        "os-volume-replication:extended_status": None,
                        "replication_status": "disabled",
                        "snapshot_id": v["SourceSnapshotId"],
                        "id": v["DiskId"],
                        "size": v["Size"],
                        "user_id": "32779452fcd34ae1a53a797ac8a1e064",
                        "os-vol-tenant-attr:tenant_id":"bab7d5c60cd041a0a36f7c4b6e1dd978",
                        "os-vol-mig-status-attr:migstat": None,
                        "metadata": {},
                        "status": v["Status"],
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
                            "status": v["Status"],
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
                            "availability_zone": v["ZoneId"],
                            "bootable": "true",
                            "os-vol-host-attr:host": "ip-10-168-107-25",
                            "source_volid": None,
                            "snapshot_id": v["SourceSnapshotId"],
                            "id":  v["DiskId"],
                            "description": v["Description"],
                            "name": v["DiskName"],
                            "created_at": v["CreationTime"],
                            "volume_type": v["Type"],
                            "os-vol-tenant-attr:tenant_id": "0c2eba2c5af04d3f9e9d0d410b371fde",
                            "size": v["Size"],
                            "os-volume-replication:driver_data": None,
                            "os-volume-replication:extended_status": None,
                            "metadata": {
                                "contents": "not junk"
                            }
                        }  
                    }
        return resp
        pass
    
    def updateVolume(self, tenant_id, volume_id, name, description):
        pass
    
    def deleteVolume(self, tenant_id, volume_id):
        pass    
    
    
    def queryVolumeMetadata(self, tenant_id, volume_id):
        pass
    
    def updataVolumeMetadata(self, name):
        pass
    
    
    def volumeAction(self, tenant_id, volume_id, action):
        pass

    
    def querySnapshots(self, tenant_id, sort_key, sort_dir, limit, marker):
        pass 
    
    def createSnapshot(self, tenant_id, name, description, volume_id, force):
        pass
    
    
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
                        "status":s["Status"],
                        "metadata":{},
                        "os-extended-snapshot-attributes:progress": s["Progress"],
                        "name": s["SnapshotName"],
                        "volume_id": s["SourceDiskId"],
                        "os-extended-snapshot-attributes:project_id": None, ##s["ProductCode"],
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
                    "status": s["Status"],
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
                            "status": "available",
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
        pass 
    
    def updateSnapshot(self, tenant_id, snapshot_id, name, description):
        pass
    
    
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
    
    
    def queryTypes(self, tenant_id, sort_key, sort_dir, limit, marker):
        print "queryTypes WUJUN Do Nothing, tenant_id is ", tenant_id, "  sort_key is ", sort_key, "  sort_dir is ", sort_dir, "  limit is ", limit, "   marker is ", marker        
        ## if TEST_FLAG:
        if 1:
            {
                "volume_types": [
                    {
                        "extra_specs": {
                            "capabilities": "gpu"
                        },
                        "id": "6685584b-1eac-4da6-b5c3-555430cf68ff",
                        "name": "SSD"
                    },
                    {
                        "extra_specs": {},
                        "id": "8eb69a46-df97-4e41-9586-9a40a7533803",
                        "name": "SATA"
                    }
                ]
            }            
            pass
        pass          