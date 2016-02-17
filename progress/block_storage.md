Block Storage 
Volume：对应ECS的磁盘API
POST
/v2/​{tenant_id}​/volumes
Create volume
Creates a volume.
 
detail
GET
/v2/​{tenant_id}​/volumes
List volumes
Lists summary information for all Block Storage volumes that the tenant can access.
 
detail
GET
/v2/​{tenant_id}​/volumes/detail
List volumes with details
Lists all Block Storage volumes, with details, that the tenant can access.
 
detail
GET
/v2/​{tenant_id}​/volumes/​{volume_id}​
Show volume details
Shows details for a volume.
 
detail
PUT
/v2/​{tenant_id}​/volumes/​{volume_id}​
Update volume
Updates a volume.
 
detail
DELETE
/v2/​{tenant_id}​/volumes/​{volume_id}​
Delete volume
Deletes a volume.
 
detail
GET
/v2/​{tenant_id}​/volumes/​{volume_id}​/metadata
Show volume metadata
Shows metadata for a volume.
 
detail
PUT
/v2/​{tenant_id}​/volumes/​{volume_id}​/metadata
Update volume metadata
Updates metadata for a volume.
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Extend volume size
Extends the size of a volume to a requested size, in gibibytes (GiB). Specify the os-extend action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Reset volume statuses
Resets the status, attach status, and migration status for a volume. Specify the os-reset_statusaction in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Set image metadata for volume
Sets the image metadata for a volume. Specify theos-set_image_metadata action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Remove image metadata from volume
Removes image metadata, by key, from a volume. Specify the os-unset_image_metadata action in the request body and the key for the metadata key and value pair that you want to remove.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Attach volume to server
Attaches a volume to a server. Specify theos- attach action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Unmanage volume
Removes a volume from Block Storage management without removing the back-end storage object that is associated with it. Specify the os-unmanage action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Force detach volume
Forces a volume to detach. Specify theos-force_detach action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Promote replicated volume
Promotes a replicated volume. Specify theos-promote-replica action in the request body.
 
detail
POST
/v2/​{tenant_id}​/volumes/​{volume_id}​/action
Reenable volume replication
Re-enables replication of a volume. Specify thevolume-replica-reenable- action in the request body.

Snapshot
对应ECS的快照
POST
/v2/​{tenant_id}​/snapshots
Create snapshot
Creates a volume snapshot, which is a point-in-time, complete copy of a volume. You can create a volume from a snapshot.
 
detail
GET
/v2/​{tenant_id}​/snapshots
List snapshots
Lists all Block Storage snapshots, with summary information, that the tenant can access.
 
detail
GET
/v2/​{tenant_id}​/snapshots/detail
List snapshots with details
Lists all Block Storage snapshots, with details, that the tenant can access.
 
detail
GET
/v2/​{tenant_id}​/snapshots/​{snapshot_id}​
Show snapshot details
Shows details for a snapshot.
 
detail
PUT
/v2/​{tenant_id}​/snapshots/​{snapshot_id}​
Update snapshot
Updates a snapshot.
 
detail
DELETE
/v2/​{tenant_id}​/snapshots/​{snapshot_id}​
Delete snapshot
Deletes a snapshot.
 
detail
GET
/v2/​{tenant_id}​/snapshots/​{snapshot_id}​/metadata
Show snapshot metadata
Shows metadata for a snapshot.
 
detail
PUT
/v2/​{tenant_id}​/snapshots/​{snapshot_id}​/metadata
Update snapshot metadata
Updates metadata for a snapshot.

