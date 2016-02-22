# -*- encoding: utf-8 -*-
import unittest

import requests
import json

"""
from cloudGate.common.define import *
from cloudGate.config import *

URL = "http://" + HOST + ":" + PORT + BLOCK_STORAGE_BASE_URL
"""
URL = "http://121.199.9.187:8084/block_storage"
session = requests.session()

class BlockStorageTest(unittest.TestCase):
    def printJson(self, s):
        b = json.loads(s)
        print json.dumps(b, indent=4)

    def setUp(self):
        pass

    def tearDown(self):
        session.close()

    """
    def test_attachVolume(self):
        data = {
                "os-attach": {
                    "instance_uuid": "95D9EF50-507D-11E5-B970-0800200C9A66",
                    "mountpoint": None
                }
            } 
        ## volume_id = "d-62nqxxle1"
        response = session.post(URL + "/v2/​tenant_id​/volumes/"+ volume_id + "​/action", data=json.dumps(data))
        self.printJson(response.text)
    
    
    def test_detachVolume(self):
        data = {
            "os-force_detach": {
                "attachment_id": "d8777f54-84cf-4809-a679-468ffed56cf1",
                "connector": {
                    "initiator": "iqn.2012-07.org.fake:01"
                }
            }
        } 
        volume_id = "d-62nqxxle1"
        response = session.post(URL + "/v2/​tenant_id​/volumes/"+ volume_id + "​/action", data=json.dumps(data))
        self.printJson(response.text)
    """

    
    def test_querySnapshots(self):
        response = session.get(URL + "/v2/tenant_id/snapshots")
        self.printJson(response.text)
    

if __name__ == '__main__':
    unittest.main()
