# -*- encoding: utf-8 -*-
import unittest

import requests
import json

from cloudGate.common.define import *
from cloudGate.config import *

URL = "http://" + HOST + ":" + PORT + OBJECT_STORAGE_BASE_URL 
session = requests.session()

class ObjectStorageTest(unittest.TestCase):
    def printJson(self, s):
        b = json.loads(s)
        print json.dumps(b, indent=4)

    def setUp(self):
        pass

    def tearDown(self):
        session.close()

    def test_example(self):
        data = {}
        response = session.post(URL + "", data = json.dumps(data))

        self.printJson(response.text)

    def test_createContainer(self):
        response = session.post(URL + "/v1/tenant_id/cloudgatetestcon")
        print response.text

    def test_listContainers(self):
        response = session.get(URL + "/v1/tenant_id")
        self.printJson(response.text)

    def test_listObjects(self):
        pass


    def test_deleteContainer(self):
        pass

    def test_createObject(self):
        pass

    def test_copyObject(self):
        pass

    def test_deleteObject(self):
        pass

if __name__ == '__main__':
    unittest.main()
