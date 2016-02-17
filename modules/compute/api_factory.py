from aliyun.processor import *

class ComputeProcessorFac():

    def create_processor(self, type_ = None, tocken = None):
        if type_ == "aliyun" or not type_:
            return AliyunComputeProcessor(tocken)
