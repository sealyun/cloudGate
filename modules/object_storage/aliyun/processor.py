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
        print ([b for b in buckets])

        return None
