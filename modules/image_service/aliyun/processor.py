import json

from cloudGate.modules.image_service.process_base import ImageServiceProcessorBase
from cloudGate.config import *
from aliyunsdkcore import client


from aliyunsdkram.request.v20150501 import ListVirtualMFADevicesRequest

class AliyunImageServiceProcessor(ImageServiceProcessorBase):

    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryImages(self, limit, marker, name, visibility, member_status, owner, status,
                    size_min, size_max, sort_key, sort_dir, sort, tag):
        request = ListVirtualMFADevicesRequest.ListVirtualMFADevicesRequest()
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        images = []
        print('resp', resp)
        return images
