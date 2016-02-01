from handlers import * 
from cloudGate.common.define import BLOCK_STORAGE_BASE_URL

urls_low_version = [
    (BLOCK_STORAGE_BASE_URL, LowVersionBlockStorageBaseHandler),
]

url_v2 = [
    (BLOCK_STORAGE_BASE_URL + r"/v2", BlockStorageBaseHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/(.*)/volumes", VolumesHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/(.*)/volumes/detail", VolumesDetailHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/(.*)/volumes/(.*)", VolumeHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/(.*)/volumes/(.*)/metadata", VolumeMetadataHandler),
    (BLOCK_STORAGE_BASE_URL + r"/v2/(.*)/volumes/(.*)/action", VolumeActionHandler),

    (r"/v2/(.*)/snapshots", SnapshotsHandler),
    (r"/v2/(.*)/snapshots/detail", SnapshotsDetailHandler),
    (r"/v2/(.*)/snapshots/(.*)", SnapshotHandler),
    (r"/v2/(.*)/snapshots/(.*)/metadata", SnapshotMetadataHandler),
]

urls = urls_low_version + urls_v2
