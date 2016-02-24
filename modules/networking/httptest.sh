#!/bin/sh

#networks test set
echo "-----------------------networks test set begin-----------------------"
echo "---test sequence---"
echo "->test list all networks"
echo "->test create a network"
echo "->test list all networks"
echo "->test get the network which just be created"
echo "->test update network"
echo "->test get the network which just be updated"
echo "->test delete the network which just be updated"
echo "->test get the network which just be deleted"
echo "->test list all networks"
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworksHandler_POST \
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_PUT \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_DELETE \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworksHandler_GET \
echo "-----------------------networks test set end-------------------------"

#loadbalancer test set
echo "---------------------loadbalancer test set begin---------------------"
echo "---test sequence---"
echo "->test list all loadbalancers"
echo "->test create a loadbalancer"
echo "->test list all loadbalancers"
echo "->test get the loadbalancer which just be created"
echo "->test get loadbalancer status"
echo "->test update loadbalancer"
echo "->test get the loadbalancer which just be updated"
echo "->test delete the loadbalancer which just be updated"
echo "->test get the loadbalancer which just be deleted"
echo "->test list all loadbalancers"
#LoadBalanceTest.test_LoadbalancersHandler_GET \
#LoadBalanceTest.test_LoadbalancersHandler_POST \
#LoadBalanceTest.test_LoadbalancersHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_GET \
#LoadBalanceTest.test_LoadbalancerStatusesHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_PUT \
#LoadBalanceTest.test_LoadbalancerHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_DELETE \
#LoadBalanceTest.test_LoadbalancerHandler_GET \
#LoadBalanceTest.test_LoadbalancersHandler_GET \
echo "---------------------loadbalancer test set end-----------------------"

#listener test set
echo "-----------------------listener test set begin-----------------------"
echo "---test sequence---"
echo "->test list all loadbalancers"
echo "->test create a loadbalancer"
echo "->test list all listeners"
echo "->test create a listener"
echo "->test get the listener which just be created"
echo "->test get loadbalancer status"
echo "->test update the listener which just be created"
echo "->test get the listener which just be updated"
echo "->test delete the listener which just be updated"
echo "->test get the listener which just be deleted"
echo "->test delete the loadbalancer which just be created"
echo "->test list all loadbalancers"
#LoadBalanceTest.test_LoadbalancersHandler_GET \
#LoadBalanceTest.test_LoadbalancersHandler_POST \
#LoadBalanceTest.test_LbaasListenersHandler_GET \
#LoadBalanceTest.test_LbaasListenersHandler_POST \
#LoadBalanceTest.test_LbaasListenerHandler_GET \
#LoadBalanceTest.test_LoadbalancerStatusesHandler_GET \
#LoadBalanceTest.test_LbaasListenerHandler_PUT \
#LoadBalanceTest.test_LbaasListenerHandler_GET \
#LoadBalanceTest.test_LbaasListenerHandler_DELETE \
#LoadBalanceTest.test_LbaasListenersHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_DELETE \
#LoadBalanceTest.test_LoadbalancersHandler_GET \
echo "-----------------------listener test set end-------------------------"

python httptest.py \







