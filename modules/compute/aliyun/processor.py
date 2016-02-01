class AliyunComputeProcessor(ComputeProcessorBase):
    #we can get accessKey and accessSecret from tocken
    def __init__(self, tocken):
        #TODO we can init aliyun request in ComputeProcessorBase
        self.tocken == tocken

    def ServerAction(self, tenat_id, server_id, action):
        #TODO a real action to aliyun server
        pass
