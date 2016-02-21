# -*- encoding: utf-8 -*-
import unittest

import requests
import json

from cloudGate.common.define import *
from cloudGate.config import *

URL = "http://" + HOST + ":" + PORT + IDENTITY_BASE_URL
session = requests.session()

class IdentityTest(unittest.TestCase):
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

    def test_createPolicy(self):
        data = {
            "policy": {
                "blob": "{'foobar_user': 'role:compute-user'}",
                "project_id": "0426ac1e48f642ef9544c2251e07e261",
                "type": "application/json",
                "user_id": "0ffd248c55b443eaac5253b4e9cbf9b5"
            }    
        }

        response = session.post(URL + "/v3/policies", data=json.dumps(data))

        self.policy = json.loads(response)["policy"]

        self.printJson(response.text)

    def test_listPolicies(self):
        response = session.get(URL + "/v3/policies")

        self.printJson(response.text)

    def test_showPolicyDetails(self):
        response = session.get(URL + "/v3/policies/" + self.policy["id"])

        self.printJson(response.text)

    def test_updatePolicy(self):
        data = {
            "policy": {
                "blob": '{
                    "foobar_user": [
                        "role:compute-user"
                    ]
                }',
                "project_id": "456789",
                "type": "application/json",
                "user_id": "616263"
            } 
        }

        response = session.patch(URL + "/v3/policies/" + self.policy["id"], data=json.dumps(data))

        self.printJson(response.text)

    def test_deletePolicy(self):
        session.delete(URL + "/v3/policies/" + self.policy["id"])

if __name__ == '__main__':
    unittest.main()
