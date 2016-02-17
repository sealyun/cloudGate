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
                    ],
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
        ## self.get_processor()
        sort = self.get_argument("sort",None)
        limit = self.get_argument("limit",None)
        marker = self.get_argument("marker",None)

        volumes = self.p.queryVolumesDetails(tenant_id, sort, limit, marker)
        """
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
        """
        
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
                        "readonly": "False",
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
                    "bootable": "False",
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
                    "bootable": "True",
                    "created_at": "2015-11-29T02:25:18.000000",
                    "volume_type": "lvmdriver-1"
                }
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

## "os-extended-snapshot-attributes:project_id" ???
## "metadata"
class SnapshotsDetailHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        ## self.get_processor()
        snapshots = self.p.querySnapshotsDetails(tenant_id)
        '''
        resp = {
            "snapshots":[
                {
                    "status":s["Status"],
                    "metadata":None,
                    "os-extended-snapshot-attributes:progress": s["Progress"],
                    "name": s["SnapshotName"],
                    "volume_id": s["SourceDiskId"],
                    "os-extended-snapshot-attributes:project_id":s["ProductCode"],
                    "created_at": s["CreationTime"],    
                    "size":s["SourceDiskSize"],
                    "id":s["SnapshotId"],
                    "description":s["Description"]
                }
                for s in snapshots
            ]
        }
        '''
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
        
        print "Final Resp Json is ", resp
        self.send_json(resp)

class SnapshotHandler(BlockStorageBaseHandler):
    def get(self, tenant_id, snapshot_id):
        s = self.p.querySnapshot(tenant_id, snapshot_id)

        resp = {
            "snapshot":{
                "status":s.status,
                "os-extended-snapshot-attributes:progress": s.os_extended_snapshot_attributes_progress,
                "description":s.description,
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



class OsVolumeTransferHandler(BlockStorageBaseHandler):
    def get(self, tenant_id):
        ## self.get_processor()
        self.p.queryOsVolumeTransfer(tenant_id)
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
        self.send_json(resp)        
        pass