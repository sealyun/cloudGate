# -*- coding: utf-8 -*-

import sys
import os.path
import json

basepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basepath)
sys.path.append(os.path.dirname(basepath))

import unittest
import requests

from cloudGate.modules.image_service.aliyun import processor

run = 'test_api'

host = 'http://121.199.9.187:8085'


class TestCase(unittest.TestCase):

    @unittest.skipUnless(run == 'test_list_images', 'reason')
    def test_list_images(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.queryImages(None, None, None, None, None, None, None, None, None, None, None, None, None,)
        print('test_list_images', r, len(r))

    @unittest.skipUnless(run == 'test_create_image', 'reason')
    def test_create_image(self):
        p = processor.AliyunImageServiceProcessor("")
        r = p.createImage(None, None, 'NewImage', 's-62ev59pgw')
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

    @unittest.skipUnless(run == 'test_api', 'reason')
    def test_api(self):
        session = requests.Session()
        session.headers.update({'X-Auth-Token': 'admintest:admintest'})

        response = session.get(host + '/image_service/v1/images/detail')
        self.assertTrue('images' in response.text)
        print('get images', response.status_code)

        headers = {
            'X-Image-Meta-Name': 'test111101',
            'X-Glance-Api-Copy-From': 'http://s-62ev59pgw.vhd'
        }
        response = session.post(host + '/image_service/v1/images', headers=headers)
        id = json.loads(response.text)['image']['id']
        print('create_image', response.text)
        self.assertEqual(response.status_code, 202)

        response = session.patch(host + '/image_service/v1/images/' + id,
                                 json={'op': 'replace', 'path': 'ImageName', 'value': 'newName'})
        print('patch_name', response.text)
        self.assertEqual(response.status_code, 200)

        response = session.get(host + '/image_service/v1/images/' + id)
        print('get image_info', response.text)

        response = session.delete(host + '/image_service/v1/images/' + id)
        print('delete_name', response.text)
        self.assertEqual(response.status_code, 204)
if __name__ == '__main__':
    unittest.main()
