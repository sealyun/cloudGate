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
        print "queryVolumes WUJUN begin ...."
        print "WUJUN tenant_id is ", tenant_id, "  limit is ", limit, "   marker is ", marker
        r = DescribeDisksRequest.DescribeDisksRequest()
        ##### r.set_ZoneId(self.regin)
        ## r.set_DiskIds()
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
        print "queryVolumes WUJUN response is ", response
        return response
        pass
    
    def createVolume(self, tenant_id, size, availability_zone, source_volid,
                description, multiattach, snapshot_id, name, imageRef,
                volume_type, metadata, source_replica, consistencygroup_id):
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
                    
        pass
    
    
    def queryVolumesDetails(self, tenant_id, sort, limit, marker):
        pass
    
    
    def queryVolume(self, tenant_id, volume_id):
        
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
        print "querySnapshotsDetails WUJUN begin ...."        
        r = DescribeSnapshotsRequest.DescribeSnapshotsRequest()
        
        r.set_accept_format('json')
        response = self.clt.do_action(r)
        print "querySnapshotsDetails WUJUN response is ", response
        return response        
        pass
    
    
    def querySnapshot(self, tenant_id, snapshot_id):
        pass
    
    def deleteSnapshot(self, tenant_id, snapshot_id):
        pass 
    
    def updateSnapshot(self, tenant_id, snapshot_id, name, description):
        pass
    
    
    def querySnapshotMetadata(self, tenant_id, snapshot_id):
        pass
    
    def updataSnapshotMetadata(self, tenant_id, snapshot_id, metadata):
        pass  