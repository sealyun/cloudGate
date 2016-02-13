#www.aliyun.com/product/ram
from cloudGate.modules.identity.process_base import *
from cloudGate.config import *
from aliyunsdkcore import client

from aliyunsdkram.request.v20150501 import ListUsersRequest

class AliyunIdentityProcessor(IdentityProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryUsers(self, domian_id, name, enabled):
        request = ListUsersRequest.ListUsersRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        print response

        return response["Users"]["User"]
