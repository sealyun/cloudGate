from aliyun.processor import *

class ImageServiceProcessorFac():

    def create_processor(self, type_ = None, token = None):
        if type_ == "aliyun" or not type_:
            return AliyunImageServiceProcessor(token)
