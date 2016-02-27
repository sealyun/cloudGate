#!/bin/sh

echo "---------------------loadbalancer test loadbalancer all----------------------"
python httptest.py \
LoadBalanceTest.test_LoadbalancersHandler_GET \
LoadBalanceTest.test_LoadbalancersHandler_POST \
LoadBalanceTest.test_LoadbalancersHandler_GET \
LoadBalanceTest.test_LoadbalancerHandler_GET \
LoadBalanceTest.test_LoadbalancerStatusesHandler_GET \
LoadBalanceTest.test_LoadbalancerHandler_PUT \
LoadBalanceTest.test_LoadbalancerHandler_GET \
LoadBalanceTest.test_LoadbalancerHandler_DELETE \
LoadBalanceTest.test_LoadbalancersHandler_GET \








