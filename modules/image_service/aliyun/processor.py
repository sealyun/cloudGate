import json

from cloudGate.modules.image_service.process_base import ImageServiceProcessorBase
from cloudGate.config import *
from aliyunsdkcore import client


from aliyunsdkecs.request.v20140526 import (
    DescribeImagesRequest,
    CreateImageRequest,
)


class AliyunImageServiceProcessor(ImageServiceProcessorBase):

    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryImages(self, limit, marker, name, visibility, member_status, owner, status,
                    size_min, size_max, sort_key, sort_dir, sort, tag):
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)
        resp = json.loads(response)
        print('queryImages', resp)
        """
        {
            u'PageSize': 10,
            u'RegionId': u'cn-hangzhou',
            u'TotalCount': 34,
            u'PageNumber': 1,
            u'RequestId': u'DA0FEA90-77AB-4CC4-8AB2-4D7BBD939738',
            u'Images': {
                u'Image': [
                    {
                        u'Status': u'Available',
                        u'ProductCode': u'',
                        u'Platform': u'Freebsd',
                        u'Description': u'freebsd1001_64_20G_aliaegis_20150527.vhd',
                        u'IsCopied': False,
                        u'Tags': {
                            u'Tag': []
                        },
                        u'IsSubscribed': False,
                        u'IsSelfShared': u'',
                        u'CreationTime': u'2015-06-19T10:45:56Z',
                        u'OSName': u'FreeBSD  10.1 64\u4f4d',
                        u'DiskDeviceMappings': {
                            u'DiskDeviceMapping': [
                                {
                                    u'Format': u'',
                                    u'ImportOSSBucket': u'',
                                    u'Device': u'/dev/xvda',
                                    u'SnapshotId': u'',
                                    u'ImportOSSObject': u'',
                                    u'Size': u'20'
                                }
                            ]
                        },
                        u'ImageId': u'freebsd1001_64_20G_aliaegis_20150527.vhd',
                        u'Usage': u'instance',
                        u'ImageName': u'freebsd1001_64_20G_aliaegis_20150527.vhd',
                        u'Architecture': u'x86_64',
                        u'ImageOwnerAlias': u'system',
                        u'OSType': u'linux',
                        u'Progress': u'100%',
                        u'Size': 20,
                        u'ImageVersion': u'1.0.0',
                        u'IsSupportIoOptimized': False
                    }
                ]
            }
        }
        """
        return resp['Images']['Image']

    def createImage(self, container_format, disk_format, name, snapshot_id):
        request = CreateImageRequest.CreateImageRequest()
        request.set_accept_format('json')
        request.set_SnapshotId(snapshot_id)

        response = self.clt.do_action(request)
        resp = json.loads(response)
        print('createImage', resp)
        return resp
