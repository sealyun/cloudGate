from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import *

class LowVersionBlockStorageBaseHandler(HttpBaseHandler):   
    def get(self):
        pass

class BlockStorageBaseHandler(HttpBaseHandler):
    def __init__(self, *args, **kwargs):
        super(BlockStorageBaseHandler, self).__init__(args[0], args[1], **kwargs)
        token = self.request.headers["X-Auth-Token"]
        print ("--- WU JUN ---get token:", token)
        i = BlockStorageProcessorFac()
        self.p = i.create_processor(None, token)
        print ("--- WU JUN ---self.p:", self.p)
    """
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        print ("--- WU JUN ---get token:", token)
        i = BlockStorageProcessorFac()
        self.p = i.create_processor(None, token)
        print ("--- WU JUN ---self.p:", self.p)
        return self.p
    
    def get(self):
        #TODO
        pass
    """
    
class VolumesHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort = self.get_argument("sort", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)
        
        resp = self.p.queryVolumes(tenant_id, sort, limit, marker)
        print "VolumesHandler queryVolumes GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "==========================================" 
        self.send_json(resp)

    def post(self, tenant_id):
        volume = json.loads(self.request.body)["volume"]
        print "VolumesHandler createVolume Input Params is ", json.dumps(volume, indent=4)
        resp = self.p.createVolume(tenant_id, volume["size"],
                volume["availability_zone"],
                volume["source_volid"],
                volume["description"],
                volume["multiattach"],
                volume["snapshot_id"],
                volume["name"],
                volume["imageRef"],
                volume["volume_type"],
                volume["metadata"],
                volume["source_replica"],
                volume["consistencygroup_id"])
        if resp is None:
            print "===========  do create Volume Failed     =========="           
            self.set_status(403)
            return
        else:
            print "===========  do create Volume Successed  =========="
            print "VolumesHandler createVolume GET Resp Json: ========"
            ## print json.dumps(resp, indent=4)
            print "==========================================" 
            self.send_json(resp)

class VolumesDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        ## self.get_processor()
        sort = self.get_argument("sort",None)
        limit = self.get_argument("limit",None)
        marker = self.get_argument("marker",None)

        resp = self.p.queryVolumesDetails(tenant_id, sort, limit, marker)
        print "VolumesDetailHandler queryVolumesDetails GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "==========================================" 
        self.send_json(resp)

class VolumeHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_id):
        
        resp = self.p.queryVolume(tenant_id, volume_id)
        if resp is None:
            self.set_status(401)
            return
        else:
            self.set_status(200)            
            
        print "VolumeHandler queryVolume GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "==========================================" 
        self.send_json(resp)

    def put(self, tenant_id, volume_id):
        volume = json.loads(self.request.body)["volume"]

        volume = self.p.updateVolume(tenant_id, volume_id, 
                volume["name"],
                volume["description"])

        resp = {
            "volume":{
                "status":volume.status,
                "migration_status": volume.migration_status,
                "user_id": volume.user_id,
                "attachments": volume.attachments,
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
                "availability_zone": volume.availability_zone,
                "bootable": volume.bootable,
                "encrypted": volume.encrypted,
                "created_at": volume.create_at,
                "description": volume.description,
                "updated_at": volume.updated_at,
                "volume_type": volume.volume_type,
                "name": volume.name,
                "replication_status": volume.replication_status,
                "consistencygroup_id": volume.consistencygroup_id,
                "source_volid": volume.source_volid,
                "snapshot_id": volume.snapshot_id,
                "multiattach": volume.multiattach,
                "metadata": volume.metadata,
                "id": volume.id,
                "size": volume.size
            }
        }

        self.send_json(resp)

    def delete(self, tenant_id, volume_id):
        print "===========  do deleteVolume ==========  volume_id is ", volume_id
        if self.p.deleteVolume(tenant_id, volume_id):
            print "===========  do deleteVolume Success ==========" 
            self.set_status(202)
            pass
        else:
            print "===========  do deleteVolume Failed  =========="
            self.set_status(403)
            pass        

class VolumeMetadataHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_id):
        metadata = self.p.queryVolumeMetadata(tenant_id, volume_id)

        resp = {
            "metadata":metadata
        }

        self.send_json(resp)

    def put(self, tenant_id, volume_id):
        metadata = json.loads(self.request.body)["metadata"]

        metadata = self.p.updataVolumeMetadata(metadata["name"])

        resp = {
            "metadata":{
                "name":metadata.name
            }
        }

        self.send_json(resp)

class VolumeActionHandler(BlockStorageBaseHandler):
    def post(self, tenant_id, volume_id):
        ## print "AAAAAAAAAAAAAAAAA  VolumeActionHandler"
        action = json.loads(self.request.body)
        ## print "BBBBBBBBBBBBBBBBB  VolumeActionHandler"

        if self.p.volumeAction(tenant_id, volume_id, action):
            self.set_status(202)
            pass
        else:
            self.set_status(403)
            pass

class SnapshotsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort_key = self.get_argument("sort_key", None)
        sort_dir = self.get_argument("sort_dir", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        snapshots = self.p.querySnapshots(tenant_id, sort_key, sort_dir, limit, marker)

        resp = {
            "snapshots":[
                {
                    "status":s.status,
                    "metadata":s.metadata,
                    "name":s.name,
                    "volume_id":s.volume_id,
                    "create_at":s.create_at,
                    "size":s.size,
                    "id":s.id,
                    "description":s.description,
                }
                for s in snapshots
            ]
        }

    def post(self, tenant_id):
        snapshot = json.loads(self.request.body)["snapshot"]

        snapshot = self.p.createSnapshot(tenant_id, snapshot["name"],
                snapshot["description"],
                snapshot["volume_id"],
                snapshot["force"])

        resp = {
            "snapshot": {
                "status":snapshot.status,
                "description":snapshot.description,
                "create_at":snapshot.create_at,
                "metadata":snapshot.metadata,
                "volume_id":snapshot.volume_id,
                "size":snapshot.size,
                "id":snapshot.id,
                "name":snapshot.name,
            }
        }

        self.send_json(resp)

## "os-extended-snapshot-attributes:project_id" ???
## "metadata"
class SnapshotsDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.querySnapshotsDetails(tenant_id)
        print "SnapshotsDetailHandler querySnapshotsDetails GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)

class SnapshotHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, snapshot_id):
        resp = self.p.querySnapshot(tenant_id, snapshot_id)
        print "SnapshotHandler querySnapshot GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)

    def delete(self, tenant_id, snapshot_id):
        if self.p.deleteSnapshot(tenant_id, snapshot_id):
            self.set_status(202)
            pass
        else:
            self.set_status(403)
            pass

    def put(self, tenant_id, snapshot_id):
        snapshot = json.loads(self.request.body)["snapshot"]

        s = self.p.updateSnapshot(tenant_id, snapshot_id,
                snapshot["name"],
                snapshot["description"])

        resp = {
            "snapshot":{
                "create_at":s.create_at,
                "description":s.description,
                "name":s.name,
                "id":s.id,
                "size":s.size,
                "status":s.status,
                "volume_id":s.volume_id
            }
        }

        self.send_json(resp)

class SnapshotMetadataHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, snapshot_id):
        metadata = self.p.querySnapshotMetadata(tenant_id, snapshot_id)

        resp = {
            "metadata":{
                "name":metadata.name
            }
        }

        self.send_json(resp)

    def put(self, tenant_id, snapshot_id):
        metadata = json.loads(self.request.body)["metadata"]

        metadata = self.p.updataSnapshotMetadata(tenant_id, snapshot_id, metadata)

        resp = {
            "metadata":metadata
        }

        self.send_json(resp)


"""
class SnapshotsActionHandler(BlockStorageBaseHandler):
    def post(self, tenant_id, snapshot_id):
        action = json.loads(self.request.body)

        if self.p.snapshotsAction(tenant_id, volume_id, action):
            #HTTP 202
            pass
        else:
            pass
"""


class OsVolumeTransferDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.queryOsVolumeTransferDetail(tenant_id)
        print "OsVolumeTransferDetailHandler queryOsVolumeTransferDetail GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)        
        pass
    
    
class QosSpecsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort_key = self.get_argument("sort_key", None)
        sort_dir = self.get_argument("sort_dir", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)  
        
        resp = self.p.queryQosSpecs(tenant_id, sort_key, sort_dir, limit, marker)
        print "QosSpecsHandler queryQosSpecs GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)        
        pass    
    
class VolumeTypesHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort_key = self.get_argument("sort_key", None)
        sort_dir = self.get_argument("sort_dir", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)  
        
        resp = self.p.queryVolumeTypes(tenant_id, sort_key, sort_dir, limit, marker)
        print "TypesHandler queryTypes GET Resp Json: ========"
        print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)        
        pass
    
class VolumeTypeDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_type_id):
        resp = self.p.queryVolumeTypeDetail(tenant_id, volume_type_id)
        print "VolumeTypeDetailHandler queryVolumeTypeDetail GET Resp Json: ========"
        print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)          
        pass


class BlockStorageLimitsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.queryBlockStorageLimits(tenant_id)
        print "BlockStorageLimitsHandler queryBlockStorageLimits GET Resp Json: ========"
        print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)         
        pass
    

class BlockStorageExtensionsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.queryBlockStorageExtensions(tenant_id)
        print "BlockStorageExtensionsHandler queryBlockStorageExtensions GET Resp Json: ========"
        print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)           
        pass
    