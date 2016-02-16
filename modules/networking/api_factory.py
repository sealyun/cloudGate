# -*- coding:utf-8 -*-

from cloudGate.modules.networking.aliyun.processor import *
from cloudGate.modules.networking.amazon.processor import *


class NetworkingProcessorFactory(object):
    def __init__(self):
        pass

    def getProcessor(self, type, token):
        if type == "aliyun":
            return AliyunNetworkingProcessor(token)
        elif type == "amazon":
            return AmazonNetworkingProcessor(token)

    def getAliyunProcessor(self, token):
        return AliyunNetworkingProcessor(token)

    def getAmazonProcessor(self, token):
        return AmazonNetworkingProcessor(token)
