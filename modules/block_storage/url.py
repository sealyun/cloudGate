from handlers import * 
from cloudGate.common.define import BLOCK_STORAGE_BASE_URL

urls_low_version = [
    (BLOCK_STORAGE_BASE_URL, LowVersionBlockStorageBaseHandler),
]

urls_v2 = [
    (BLOCK_STORAGE_BASE_URL + r"/v2", BlockStorageBaseHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/volumes", VolumesHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/volumes/detail", VolumesDetailHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/volumes/([^/]+)", VolumeHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/volumes/([^/]+)/metadata", VolumeMetadataHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/volumes/([^/]+)/action", VolumeActionHandler),

    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/snapshots", SnapshotsHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/snapshots/detail", SnapshotsDetailHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/snapshots/([^/]+)", SnapshotHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/snapshots/([^/]+)/metadata", SnapshotMetadataHandler),
    ## (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/snapshots/([^/]+)/action", SnapshotsActionHandler),
    
    ####### new Add handler ############
    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/os-volume-transfer/detail", OsVolumeTransferDetailHandler),

    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/qos-specs", QosSpecsHandler),

    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/types", VolumeTypesHandler),

    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/types/([^/]+)", VolumeTypeDetailHandler),

    (BLOCK_STORAGE_BASE_URL + r"/v2/([^/]+)/limits", BlockStorageLimitsHandler),
]

urls = urls_low_version + urls_v2
