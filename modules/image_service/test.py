# -*- coding: utf-8 -*-
import unittest
import requests

run = 'test_1'

class TestCase(unittest.TestCase):

    @unittest.skipUnless(run == 'test_1', 'reason')
    def test_1(self):
        response = requests.get('http://localhost:8085/image_service/v2/images')
        print(response.text)

if __name__ == '__main__':
    unittest.main()
