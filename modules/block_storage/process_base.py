# -*- encoding: utf-8 -*-

class BlockStorageProcessorBase():
    
    def queryVolumes(self, tenant_id, sort, limit, marker):
        pass
    
    def createVolume(self, tenant_id, size, availability_zone, source_volid,
                description, multiattach, snapshot_id, name, imageRef,
                volume_type, metadata, source_replica, consistencygroup_id):
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
    