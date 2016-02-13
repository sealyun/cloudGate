#www.aliyun.com/product/ram
class AliyunIdentityProcessor(IdentityProcessorBase):
    def __init__(self, token):
        self.token = token

    def queryUsers(self, domian_id, name, enabled):
        print "call aliyun query users"
