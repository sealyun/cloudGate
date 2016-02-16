# -*- coding:utf-8 -*-

from cloudGate.modules.networking.process_base import *
from cloudGate.config import *

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526 import CreateVpcRequest
from aliyunsdkecs.request.v20140526 import DeleteVpcRequest
from aliyunsdkecs.request.v20140526 import ModifyVpcAttributeRequest

import json

class AliyunNetworkingProcessor(NetworkingProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryNetwotks(self, shared, tenantID):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        resp = json.loads(response)

        print resp
        return None
