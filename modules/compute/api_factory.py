class ComputeProcessorFac():

    def __init__(self, type_ = None, tocken = None):
        if type_ == "aliyun" or not type_:
            return AliyunComputeProcessor(tocken)
