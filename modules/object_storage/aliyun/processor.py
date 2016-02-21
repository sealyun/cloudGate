from cloudGate.config import *
from cloudGate.modules.object_storage.process_base import *
import oss2

class AliyunObjectStorageProcessor(ObjectStorageBaseProcessor):
    def __init__(self, token):
        self.token = token
 
        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.end_point = IDENTITY["aliyun"]["oss_endpoint"]

        self.auth = oss2.Auth(self.access_key, self.access_secrect)

        self.service = oss2.Service(self.auth, self.end_point)

    def queryObjects(self, account, container, limit,
            marker, end_marker, prefix, format, delimiter, path):

        buckets = oss2.BucketIterator(self.service)

        print buckets

        return buckets

    def queryContainers(self):
        buckets = oss2.BucketIterator(self.service)

        return [b.name for b in buckets]

    def createContainer(self, account, container, x_container_read,
                x_container_write,
                x_container_sync_to,
                x_container_sync_key,
                x_versions_location,
                x_container_meta_name,
                content_type,
                x_detect_content_type,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra):

        bucket = oss2.Bucket(self.auth, self.end_point, container)
        bucket.create_bucket()

    def deleteContainer(self, account, container,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra):

        bucket = oss2.Bucket(self.auth, self.end_point, container)

        try:
            bucket.delete_bucket()
            return True
        except:
            return False

    def queryObjects(self, account, container, limit,
            marker, end_marker, prefix, format_, delimiter, path):

        bucket = oss2.Bucket(self.auth, self.end_point, container)

        objs = oss2.ObjectIterator(bucket)

        return objs

    def deleteObject(self, account, container, object_, multipart_manifest, x_trans_id_extra):
        bucket = oss2.Bucket(self.auth, self.end_point, container)

        bucket.delete_object(object_)
