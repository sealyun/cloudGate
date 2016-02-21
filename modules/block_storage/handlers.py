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
        ## print "VolumesHandler createVolume Input Params is ", json.dumps(volume, indent=4)
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
        ##NOURLCALL NOTEST
        volume = json.loads(self.request.body)["volume"]
        print "VolumeHandler update Volume Input Params is ", json.dumps(volume, indent=4)
        resp = self.p.updateVolume(tenant_id, volume_id, 
                volume["name"],
                volume["description"])
                
        if resp is None:
            print "===========  do update volume Failed     =========="           
            self.set_status(403)
            return
        else:
            print "===========  do update volume Successed  =========="
            print "VolumeHandler update volume GET Resp Json: ========"
            print json.dumps(resp, indent=4)
            print "==========================================" 
            self.send_json(resp)

    def delete(self, tenant_id, volume_id):
        print "===========  do deleteVolume ==========  volume_id is ", volume_id
        if self.p.deleteVolume(tenant_id, volume_id):
            print "===========  do deleteVolume Success ==========" 
            self.set_status(202)
        else:
            print "===========  do deleteVolume Failed  =========="
            self.set_status(403)      

class VolumeMetadataHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_id):
        ##NOTEST NOIMPLEMENT
        resp = self.p.queryVolumeMetadata(tenant_id, volume_id)
        self.set_status(403)
        return
        self.send_json(resp)

    def put(self, tenant_id, volume_id):
        ##NOTEST NOIMPLEMENT
        metadata = json.loads(self.request.body)["metadata"]
        resp = self.p.updataVolumeMetadata(metadata["name"])
        self.set_status(403)
        return
        self.send_json(resp)


class VolumeActionHandler(BlockStorageBaseHandler):
    def post(self, tenant_id, volume_id):
        
        action = json.loads(self.request.body)
        print "VolumeActionHandler volume action Input Params is ", json.dumps(action, indent=4)

        if self.p.volumeAction(tenant_id, volume_id, action):
            print "Volume Action: Successed"
            self.set_status(202)
        else:
            print "Volume Action: Failed"
            self.set_status(403)

class SnapshotsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        ##NOURLCALL
        sort_key = self.get_argument("sort_key", None)
        sort_dir = self.get_argument("sort_dir", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        resp = self.p.querySnapshots(tenant_id, sort_key, sort_dir, limit, marker)
        
        print "SnapshotsHandler querySnapshots GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)

    def post(self, tenant_id):
        snapshot = json.loads(self.request.body)["snapshot"]
        print "SnapshotsHandler createSnapshot Input Params is ", json.dumps(snapshot, indent=4)
        resp = self.p.createSnapshot(tenant_id, snapshot["name"],
                snapshot["description"],
                snapshot["volume_id"],
                snapshot["force"])

        if resp is None:
            print "===========  do create snapshot Failed     =========="           
            self.set_status(403)
            return
        else:
            print "===========  do create snapshot Successed  =========="
            print "SnapshotsHandler createSnapshot GET Resp Json: ========"
            print json.dumps(resp, indent=4)
            print "==========================================" 
            self.send_json(resp)

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
        else:
            self.set_status(403)

    def put(self, tenant_id, snapshot_id):
        snapshot = json.loads(self.request.body)["snapshot"]
        print "SnapshotHandler update Snapshot Input Params is ", json.dumps(snapshot, indent=4)
        resp = self.p.updateSnapshot(tenant_id, snapshot_id,
                snapshot["name"],
                snapshot["description"])

        if resp is None:
            print "===========  do update snapshot Failed     =========="           
            self.set_status(403)
            return
        else:
            print "===========  do update snapshot Successed  =========="
            print "SnapshotsHandler update snapshot GET Resp Json: ========"
            ## print json.dumps(resp, indent=4)
            print "==========================================" 
            self.send_json(resp)

class SnapshotMetadataHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, snapshot_id):
        ##NOTEST NOIMPLEMENT
        resp = self.p.querySnapshotMetadata(tenant_id, snapshot_id)
        self.set_status(403)
        return
        self.send_json(resp)

    def put(self, tenant_id, snapshot_id):
        ##NOTEST NOIMPLEMENT
        metadata = json.loads(self.request.body)["metadata"]
        resp = self.p.updataSnapshotMetadata(tenant_id, snapshot_id, metadata)
        self.set_status(403)
        return
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
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)        
        pass
    
class VolumeTypeDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_type_id):
        resp = self.p.queryVolumeTypeDetail(tenant_id, volume_type_id)
        print "VolumeTypeDetailHandler queryVolumeTypeDetail GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)          
        pass


class BlockStorageLimitsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.queryBlockStorageLimits(tenant_id)
        print "BlockStorageLimitsHandler queryBlockStorageLimits GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)         
        pass
    

class BlockStorageExtensionsHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        resp = self.p.queryBlockStorageExtensions(tenant_id)
        print "BlockStorageExtensionsHandler queryBlockStorageExtensions GET Resp Json: ========"
        ## print json.dumps(resp, indent=4)
        print "=========================================="
        self.send_json(resp)           
        pass
    