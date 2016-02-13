from aliyun.processor import *

class IdentityProcessorFac():

    def __init__(self, type_ = None, token = None):
        if type_ == "aliyun" or not type_:
            return AliyunIdentityProcessor(token)
