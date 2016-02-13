#www.aliyun.com/product/ram
from cloudGate.modules.identity.process_base import *

class AliyunIdentityProcessor(IdentityProcessorBase):
    def __init__(self, token):
        self.token = token

    def queryUsers(self, domian_id, name, enabled):
        print "call aliyun query users"
