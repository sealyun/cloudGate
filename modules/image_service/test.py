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
        print('test_list_images', r, len(r))

    @unittest.skipUnless(run == 'test_create_image', 'reason')
    def test_create_image(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.createImage(None, None, 'NewImage', 'coreos681_64_20G_aliaegis_20150618.vhd')
        print('test_create_image', r)

    @unittest.skipUnless(run == 'test_query_image_by_id', 'reason')
    def test_query_image_by_id(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.queryImageId('coreos681_64_20G_aliaegis_20150618.vhd')
        print('test_query_image_by_id', r)

    @unittest.skipUnless(run == 'test_delete_image_by_id', 'reason')
    def test_delete_image_by_id(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.deleteImage('centos5u10_32_20G_aliaegis_20150130.vhd')
        print('test_delete_image_by_id', r)

    @unittest.skipUnless(run == 'test_update_image_name', 'reason')
    def test_update_image_name(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.updateImage('coreos681_64_20G_aliaegis_20150618.vhd', 'Mohanson')
        print('test_update_image_name', r)

if __name__ == '__main__':
    unittest.main()
