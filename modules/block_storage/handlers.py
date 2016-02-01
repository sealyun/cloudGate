from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler

class LowVersionBlockStorageBaseHandler(HttpBaseHandler):   
    def get(self):
        pass

class BlockStorageBaseHandler(HttpBaseHandler):
    #TODO init a processor
    def get(self):
        pass

class VolumesHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort = self.get_argument("sort", None)
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)

        volumes = self.p.queryVolumes(tenant_id, sort, limit, marker)

        resp = {
            "volumes":[
                {
                    "id":v.id,
                    "links":[
                        {
                            "href":"http://",
                            "rel":"self"
                        },
                        {
                            "href":"http://",
                            "rel":"bookmark"
                        }
                    ]
                    "name":v.name
                }
                for v in volumes
            ]
        }

        self.send_json(resp)

    def post(self, tenant_id):
        volume = json.loads(self.request.body)["volume"]

        volume = self.p.createVolume(tenant_id, volume["size"],
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

class VolumesDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        sort = self.get_argument("sort",None)
        limit = self.get_argument("limit",None)
        marker = self.get_argument("marker",None)

        volumes = self.p.queryVolumesDetails(tenant_id, sort, limit, marker)

        resp = {
            "volumes":[
                {
                    "migration_status": v.migration_status,
                    "attachments": v.attachments,
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
                    "availability_zone": v.availability_zone,
                    "os-vol-host-attr:host": v.os_vol_host_attr_host,
                    "encrypted": v.encrypted,
                    "os-volume-replication:extended_status": v.os_volume_replication_extended_status,
                    "replication_status": v.replication_status,
                    "snapshot_id": v.snapshot_id,
                    "id": v.id,
                    "size": v.size,
                    "user_id": v.user_id,
                    "os-vol-tenant-attr:tenant_id":v.os_vol_tenant_attr_tenant_id,
                    "os-vol-mig-status-attr:migstat": v.os_vol_mig_status_attr_migstat,
                    "metadata": v.metadata,
                    "status": v.status,
                    "description": v.description,
                    "multiattach": v.multiattach,
                    "os-volume-replication:driver_data": v.os_volume_replication_driver_data,
                    "source_volid": v.source_volid,
                    "consistencygroup_id": v.consistencygroup_id,
                    "os-vol-mig-status-attr:name_id": v.os_vol_mig_status_attr_name_id,
                    "name": v.name,
                    "bootable": v.bootable,
                    "created_at": v.create_at,
                    "volume_type": v.volume_type 
                }
                for v in volume
            ]
        }

        self.send_json(resp)

class VolumeHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, volume_id):

        volume = self.p.queryVolume(tenant_id, volume_id)

        resp = {
            "volume":{
                "status":volume.status,
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
                "os-vol-host-attr:host":volume.os_vol_host_attr_host,
                "source_volid": volume.source_volid,
                "snapshot_id": volume.snapshot_id,
                "id": volume.id,
                "description": volume.description,
                "name": volume.name,
                "created_at": volume.create_at,
                "volume_type": volume.volume_type,
                "os-vol-tenant-attr:tenant_id":volume.os_vol_tenant_attr_tenant_id,
                "size": volume.size,
                "os-volume-replication:driver_data": volume.os_volume_replication_driver_data,
                "os-volume-replication:extended_status": volume.os_volume_replication_extended_status,
                "metadata": volume.metadata,
            }
        }

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
        self.p.deleteVolume(tenant_id, volume_id)

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
        action = json.loads(self.request.body)

        if self.p.volumeAction(tenant_id, volume_id, action):
            #HTTP 202
            pass
        else:
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

class SnapshotsDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        snapshots = self.p.querySnapshotsDetails(tenant_id)

        resp = {
            "snapshots":[
                {
                    "status":s.status,
                    "metadata":s.metadata,
                    "os-extended-snapshot-attributes:progress": s.os_extended_snapshot_attributes_progress,
                    "name": s.name,
                    "volume_id": s.volume_id,
                    "os-extended-snapshot-attributes:project_id":s.os_extended_snapshot_attributes_project_id,
                    "created_at": s.create_at,    
                    "size":s.size,
                    "id":s.id,
                    "description":s.description
                }
                for s in snapshots
            ]
        }

        self.send_json(resp)

class SnapshotHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, snapshot_id):
        s = self.p.querySnapshot(tenant_id, snapshot_id)

        resp = {
            "snapshot":{
                "status":s.status,
                "os-extended-snapshot-attributes:progress": s.os_extended_snapshot_attributes_progress,
                "description":s.description
                "created_at": s.create_at,    
                "metadata":s.metadata,
                "volume_id": s.volume_id,
                "os-extended-snapshot-attributes:project_id":s.os_extended_snapshot_attributes_project_id,
                "size":s.size,
                "id":s.id,
                "name": s.name,
            }
        }

        self.send_json(resp)

    def delete(self, tenant_id, snapshot_id):
        if self.p.deleteSnapshot(tenant_id, snapshot_id):
            #http 202
            pass
        else:
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
        pass

    def put(self, tenant_id, snapshot_id):
        pass
