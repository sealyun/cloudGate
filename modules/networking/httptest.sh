#!/bin/sh

echo "-----------------------networks test set begin-----------------------"
echo "1.test list all networks"
echo "2.test create a network"
echo "3.test list all networks"
echo "4.test get the network which just be created"
echo "5.test update network"
echo "6.test get the network which just be updated"
echo "7.test delete the network which just be updated"
echo "8.test list all networks"
echo "-----------------------networks test set end-------------------------"

echo "---------------------loadbalancer test set begin---------------------"
echo "1.test list all loadbalancers"
echo "2.test create a loadbalancer"
echo "3.test list all loadbalancers"
echo "4.test get the loadbalancer which just be created"
echo "5.test get loadbalancer status"
echo "6.test update loadbalancer"
echo "7.test get the loadbalancer which just be updated"
echo "8.test delete the loadbalancer which just be updated"
echo "9.test list all loadbalancers"
echo "---------------------loadbalancer test set end-----------------------"

echo "-----------------------listener test set begin-----------------------"
echo "1.test list all loadbalancers"
echo "2.test create a loadbalancer"
echo "3.test list all listeners"
echo "4.test create a listener"
echo "5.test get the listener which just be created"
echo "6.test get loadbalancer status"
echo "7.test update the listener which just be created"
echo "8.test get the listener which just be updated"
echo "9.test delete the listener which just be updated"
echo "10.test list all listeners"
echo "11.test delete the loadbalancer which just be created"
echo "12.test list all loadbalancers"
echo "-----------------------listener test set end-------------------------"

echo "------------------------pool test set begin------------------------"
echo "1.test list all loadbalancers"
echo "2.test create a loadbalancer"
echo "3.test list all members"
echo "4.test create a member"
echo "5.test list all members"
echo "6.test update the member which just be created"
echo "7.test get the member which just be updated"
echo "8.test delete the member which just be updated"
echo "9.test list all members"
echo "10.test delete the loadbalancer which just be created"
echo "11.test list all loadbalancers"
echo "------------------------pool test set end--------------------------"

#python httptest.py \
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworksHandler_POST \
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_PUT \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_DELETE \
#NetworkTest.test_NetworksHandler_GET \

#python httptest.py \
#LoadBalanceTest.test_LoadbalancersHandler_GET \
#LoadBalanceTest.test_LoadbalancersHandler_POST \
#LoadBalanceTest.test_LoadbalancersHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_GET \
#LoadBalanceTest.test_LoadbalancerStatusesHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_PUT \
#LoadBalanceTest.test_LoadbalancerHandler_GET \
#LoadBalanceTest.test_LoadbalancerHandler_DELETE \
#LoadBalanceTest.test_LoadbalancersHandler_GET \

#python httptest.py \
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

python httptest.py \
LoadBalanceTest.test_LoadbalancersHandler_GET \
LoadBalanceTest.test_LoadbalancersHandler_POST \
LoadBalanceTest.test_LbaasPoolMembersHandler_GET \
LoadBalanceTest.test_LbaasPoolMembersHandler_POST \
LoadBalanceTest.test_LbaasPoolMembersHandler_GET \
LoadBalanceTest.test_LbaasPoolMemberHandler_PUT \
LoadBalanceTest.test_LbaasPoolMemberHandler_GET \
LoadBalanceTest.test_LbaasPoolMemberHandler_DELETE \
LoadBalanceTest.test_LbaasPoolMembersHandler_GET \
LoadBalanceTest.test_LoadbalancerHandler_DELETE \
LoadBalanceTest.test_LoadbalancersHandler_GET \







