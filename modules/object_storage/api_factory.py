from aliyun.processor import *

class ObjectStorageProcessorFac():
    def create_processor(self, type_, token):
        if type_ == "aliyun" or not type_:
            return  AliyunObjectStorageProcessor(token) 
