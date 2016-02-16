# -*- coding: utf-8 -*-

import sys
import os.path

basepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basepath)
sys.path.append(os.path.dirname(basepath))

import unittest
import requests

from cloudGate.modules.image_service.aliyun import processor

run = 'test_list_images'


class TestCase(unittest.TestCase):

    @unittest.skipUnless(run == 'test_list_images', 'reason')
    def test_list_images(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.queryImages(None, None, None, None, None, None, None, None, None, None, None, None, None,)
        print(r)

        # response = requests.get('http://localhost:8085/image_service/v2/images')
        # print(response.text)

if __name__ == '__main__':
    unittest.main()
