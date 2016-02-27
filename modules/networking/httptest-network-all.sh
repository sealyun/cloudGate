#!/bin/sh

echo "---------------------networks test network----------------------"
python httptest.py \
NetworkTest.test_NetworksHandler_GET \
NetworkTest.test_NetworksHandler_POST \
NetworkTest.test_NetworksHandler_GET \
NetworkTest.test_NetworkHandler_GET \
NetworkTest.test_NetworkHandler_PUT \
NetworkTest.test_NetworkHandler_GET \
NetworkTest.test_NetworkHandler_DELETE \
NetworkTest.test_NetworksHandler_GET \






