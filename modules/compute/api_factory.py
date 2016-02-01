class ComputeProcessorFac():

    def __init__(self, type_ = None, tocken = None):
        if type_ == "aliyun" or !type_:
            return AliyunComputeProcessor(tocken)
