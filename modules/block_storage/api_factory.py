# -*- encoding: utf-8 -*-

from aliyun.processor import *

class BlockStorageProcessorFac():

    def create_processor(self, type_ = None, token = None):
        if type_ == "aliyun" or not type_:
            return AliyunBlockStorageProcessor(token)