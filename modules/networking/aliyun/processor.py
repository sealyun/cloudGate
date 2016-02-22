# -*- coding:utf-8 -*-

from cloudGate.modules.networking.process_base import *
from cloudGate.config import *

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526 import CreateVpcRequest
from aliyunsdkecs.request.v20140526 import DeleteVpcRequest
from aliyunsdkecs.request.v20140526 import ModifyVpcAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeRouteTablesRequest
from aliyunsdkecs.request.v20140526 import CreateRouteEntryRequest
from aliyunsdkecs.request.v20140526 import DeleteRouteEntryRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerRequest
from aliyunsdkslb.request.v20140515 import SetLoadBalancerNameRequest
from aliyunsdkslb.request.v20140515 import DeleteLoadBalancerRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerHTTPListenerAttributeRequest
from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest

import json

class AliyunNetworkingProcessor(NetworkingProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def getNetwotks(self, shared, tenantID, routerExternal):
        networks = []
        #Unsupport shared network and external network
        if shared == "True" or routerExternal == "True":
            print "Unsupport shared network and external network"
            return networks

        pagePos = 1
        pageSize = 50
        while True :
            request = DescribeVpcsRequest.DescribeVpcsRequest()
            request.set_PageNumber(pagePos)
            request.set_PageSize(pageSize)
            request.set_accept_format('json')
            response = self.clt.do_action(request)
            resp = json.loads(response)
            pagePos = pagePos + 1

            print "response: ", resp
            ''' response data
            {
              "PageNumber": 1,
              "PageSize": 10,
              "RequestId": "DA1DAE87-43FA-472F-98BB-4FDBAA4A688D",
              "TotalCount": 1,
              "Vpcs": {
                "Vpc":[
                  {
                    "CidrBlock": "172.16.0.0/16",
                    "CreationTime": "2014-10-29T13:30:19Z",
                    "Description": "",
                    "RegionId": "cn-beijing",
                    "Status": "Available",
                    "VRouterId": "vrt-25bezkd03",
                    "VSwitchIds": {
                      "VSwitchId": []
                    },
                    "VpcId": "vpc-257gq642n",
                    "VpcName": ""
                  }
                ]
              }
            }
            '''

            if "Vpcs" not in resp.keys():
                break

            if len(resp["Vpcs"]["Vpc"]) <= 0:
                break

            for vpc in resp["Vpcs"]["Vpc"]:
                network = {}

                if vpc["Status"] == "Available":
                    network["status"] = "ACTIVE"
                else:
                    network["status"] = vpc["Status"]
                #network["subnets"] = self.getSubsetIDList(vpc["VRouterId"])
                network["subnets"] = []
                network["subnets"].append(vpc["CidrBlock"])
                network["name"] = vpc["VpcName"]
                network["provider:physical_network"] = None
                network["admin_state_up"] = True
                network["tenant_id"] = tenantID
                network["provider:network_type"] = "local"
                network["router:external"] = False
                network["mtu"] = 0
                network["shared"] = False
                network["id"] = vpc["VpcId"]
                network["provider:segmentation_id"] = None

                networks.append(network)

        print "networks: ", networks
        return networks

    def createNetwork(self, inNetwork):
        print inNetwork
        name = inNetwork["name"]
        adminStateUp = inNetwork["admin_state_up"]
        shared = inNetwork["shared"]
        routerExternal = inNetwork["router:external"]
        tenantID = inNetwork["tenant_id"]

        #Unsupport shared network and external network
        if shared or routerExternal:
            print "Unsupport shared network and external network"
            return None

        request = CreateVpcRequest.CreateVpcRequest()
        request.set_VpcName(name)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp
        ''' response data
        {
          "RequestId": "461D0C42-D5D1-4009-9B6A-B3D5888A19A9",
          "RouteTableId": "vtb-25wm68mnh",
          "VRouterId": "vrt-25bezkd03",
          "VpcId": "vpc-257gq642n"
        }
        '''

        if "VpcId" not in resp.keys():
            return None

        outNetwork = self.getNetwork(resp["VpcId"])

        '''
        outNetwork = {}
        outNetwork["status"] = "ACTIVE"
        #outNetwork["subnets"] = self.getSubsetIDList(resp["VpcId"])
        outNetwork["subnets"] = []
        outNetwork["subnets"].append(resp["RouteTableId"])
        outNetwork["name"] = name
        outNetwork["admin_state_up"] = adminStateUp
        outNetwork["tenant_id"] = tenantID
        outNetwork["router:external"] = False
        outNetwork["mtu"] = 0
        outNetwork["shared"] = shared
        outNetwork["id"] = resp["VpcId"]
        '''

        return outNetwork

    def createNetworks(self, inNetworks):
        outNetworks = []
        for inNetwork in inNetworks:
            outNetwork = self.createNetwork(inNetwork)
            outNetworks.append(outNetwork)
        return outNetworks

    def getAPIExtensions(self):
        return []

    def getNetwork(self, networkID):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Vpcs" not in resp.keys():
            return None

        if len(resp["Vpcs"]["Vpc"]) <= 0:
            return None

        networks = []
        for vpc in resp["Vpcs"]["Vpc"]:
            network = {}

            if vpc["Status"] == "Available":
                network["status"] = "ACTIVE"
            else:
                network["status"] = vpc["Status"]
            #network["subnets"] = self.getSubsetIDList(vpc["VRouterId"])
            network["subnets"] = []
            network["subnets"].append(vpc["CidrBlock"])
            network["name"] = vpc["VpcName"]
            network["router:external"] = False
            network["admin_state_up"] = True
            network["tenant_id"] = ""
            network["mtu"] = 0
            network["shared"] = False
            network["port_security_enabled"] = True
            network["id"] = vpc["VpcId"]

            if network["id"] == networkID:
                networks.append(network)

        if len(networks) > 0:
            return networks[0]
        else:
            return None

    def updateNetwork(self, networkID, inNetwork):
        networkName = inNetwork["name"]

        request = ModifyVpcAttributeRequest.ModifyVpcAttributeRequest()
        request.set_VpcName(networkName)
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        return self.getNetwork(networkID)

    def deleteNetwork(self, networkID):
        request = DeleteVpcRequest.DeleteVpcRequest()
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return False

        return True

    def getDHCPAgents(self, networkID):
        #TODO
        #Aliyun does not support
        return []

    def getSubsetIDList(self, routerID):
        #Subnet id is router table id
        routeTableIDList = []
        routeTableList = self.getRouteTableList(routerID)

        print "---router id: ", routerID
        print "---route table list: "
        print routeTableList

        for routeTable in routeTableList:
            routeTableID = routeTable["RouteTableId"]
            routeTableIDList.append(routeTableID)

        return routeTableIDList

    def getRouteTableList(self, routerID):
        routeTableList = []

        pagePos = 1
        pageSize = 50

        while True:
            request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
            request.set_PageNumber(pagePos)
            request.set_PageSize(pageSize)
            request.set_VRouterId(routerID)
            request.set_accept_format('json')
            response = self.clt.do_action(request)
            resp = json.loads(response)
            pagePos = pagePos + 1

            print "response: ", resp

            if "Code" in resp.keys() and "Message" in resp.keys():
                break

            if "RouteTables" not in resp.keys():
                break

            if len(resp["RouteTables"]["RouteTable"]) <= 0:
                break

            for routeTable in resp["RouteTables"]["RouteTable"]:
                for routerEntry in routeTable["RouteEntrys"]["RouteEntry"]:
                    routeTableList.append(routerEntry)
                    ''' response data
                        routerEntry: {
                          "DestinationCidrBlock": "192.168.10.1/32",
                          "InstanceId": "i-25skktcp4",
                          "RouteTableId": "vtb-25vtxl5ct",
                          "Status": "Available",
                          "Type": "Custom"
                        }
                    '''

        return routeTableList

    def getRouterIDByNetworkID(self, networkID):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(1)
        request.set_PageSize(50)
        request.set_VpcId(networkID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Vpcs" not in resp.keys():
            return None

        if len(resp["Vpcs"]["Vpc"]) <= 0:
            return None

        for vpc in resp["Vpcs"]["Vpc"]:
            if len(vpc["VRouterId"]) > 0:
                return vpc["VRouterId"]

        return None

    def getSubsets(self, displayName, networkID, gatewayIP, ipVersion, cidr, id, enableDHCP, ipv6RaMode, ipv6AddressMode):
        subnets = []

        routerID = self.getRouterIDByNetworkID(networkID)
        routeTableList = self.getRouteTableList(routerID)
        for routeTable in routeTableList:
            subnet = {}
            subnet["name"] = ""
            subnet["enable_dhcp"] = True
            subnet["network_id"] = networkID
            subnet["tenant_id"] = ""
            subnet["dns_nameservers"] = []
            subnet["allocation_pools"] = []
            subnet["host_routes"] = []
            subnet["ip_version"] = 4
            cidr = routeTable["DestinationCidrBlock"]
            subnet["cidr"] = cidr
            subnet["gateway_ip"] = cidr[0:cidr.index('/')]
            subnet["id"] = routeTable["RouteTableId"]

            subnets.append(subnet)

        return subnets

    def createSubnet(self, inSubnet):
        #TODO
        #Aliyun does not support

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        return outSubnet

    def createSubnets(self, inSubnets):
        #TODO
        #Aliyun does not support

        outSubnets = []

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        outSubnets.append(outSubnet)
        return outSubnets

    def getSubnet(self, subnetID):
        #TODO
        #Aliyun does not support

        subnet = {}
        subnet["name"] = ""
        subnet["enable_dhcp"] = ""
        subnet["network_id"] = ""
        subnet["tenant_id"] = ""
        subnet["dns_nameservers"] = ""
        subnet["allocation_pools"] = ""
        subnet["host_routes"] = ""
        subnet["ip_version"] = ""
        subnet["gateway_ip"] = ""
        subnet["cidr"] = ""
        subnet["id"] = ""

        return subnet

    def updateSubnet(self, subnetID, inSubnet):
        #TODO
        #Aliyun does not support

        outSubnet = {}
        outSubnet["name"] = ""
        outSubnet["enable_dhcp"] = ""
        outSubnet["network_id"] = ""
        outSubnet["tenant_id"] = ""
        outSubnet["dns_nameservers"] = ""
        outSubnet["allocation_pools"] = ""
        outSubnet["host_routes"] = ""
        outSubnet["ip_version"] = ""
        outSubnet["gateway_ip"] = ""
        outSubnet["cidr"] = ""
        outSubnet["id"] = ""

        return outSubnet

    def deleteSubnet(self, subnetID):
        #TODO
        #Aliyun does not support

        return True

    def getPorts(self, status, displayName, adminState, networkID, tenantID, deviceOwner, macAddress, portID, securityGroups, deviceID):
        #TODO
        #Aliyun does not support

        outPorts = []

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        outPorts.append(outPort)
        return outPorts

    def createPort(self, inPort):
        #TODO
        #Aliyun does not support

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        return outPort

    def createPorts(self, inPorts):
        #TODO
        #Aliyun does not support

        outPorts = []

        outPort = {}
        outPort["status"] = ""
        outPort["name"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["mac_address"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""

        outPorts.append(outPort)
        return outPorts

    def getPort(self, portID):
        #TODO
        #Aliyun does not support

        port = {}
        port["status"] = ""
        port["name"] = ""
        port["allowed_address_pairs"] = ""
        port["admin_state_up"] = ""
        port["network_id"] = ""
        port["tenant_id"] = ""
        port["extra_dhcp_opts"] = ""
        port["device_owner"] = ""
        port["mac_address"] = ""
        port["fixed_ips"] = ""
        port["id"] = ""
        port["security_groups"] = ""
        port["device_id"] = ""

        return port

    def updatePort(self, portID, inPort):
        #TODO
        #Aliyun does not support

        outPort = {}
        outPort["status"] = ""
        outPort["binding:host_id"] = ""
        outPort["allowed_address_pairs"] = ""
        outPort["extra_dhcp_opts"] = ""
        outPort["device_owner"] = ""
        outPort["binding:profile"] = ""
        outPort["fixed_ips"] = ""
        outPort["id"] = ""
        outPort["security_groups"] = ""
        outPort["device_id"] = ""
        outPort["name"] = ""
        outPort["admin_state_up"] = ""
        outPort["network_id"] = ""
        outPort["tenant_id"] = ""
        outPort["binding:vif_details"] = ""
        outPort["binding:vnic_type"] = ""
        outPort["binding:vif_type"] = ""
        outPort["mac_address"] = ""

        return outPort

    def deletePort(self, portID):
        #TODO
        #Aliyun does not support

        return True

    def getLoadBalancers(self):
        loadbalancers = []

        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return loadbalancers

        ''' response data
        {
            "RequestId": "365F4154-92F6-4AE4-92F8-7FF34B540710",
            "LoadBalancers": {
                "LoadBalancer": [
                    {
                        "LoadBalancerId": "139a00604ad-cn-east-hangzhou-01",
                        "LoadBalancerName": "abc",
                        "Address": "100.98.28.56",
                        "AddressType": "intranet",
                        "RegionId": "cn-east-hangzhou-01",
                        "VSwitchId": "vsw-255ecrwq4",
                        "VpcId": "vpc-25dvzy9f9",
                        "NetworkType": "vpc",
                        "LoadBalancerStatus ": "active",
                        "MasterZoneId":"cn-hangzhou-b",
                        "SlaveZoneId":"cn-hangzhou-d"
                    }
                ]
            }
        }
        '''
        for lb in resp["LoadBalancers"]["LoadBalancer"]:
            loadbalancer = {}
            loadbalancer["description"] = ""
            loadbalancer["admin_state_up"] = True
            loadbalancer["tenant_id"] = ""
            loadbalancer["provisioning_status"] = lb["LoadBalancerStatus"]
            loadbalancer["listeners"] = []
            loadbalancer["vip_address"] = lb["Address"]
            loadbalancer["vip_subnet_id"] = ""
            loadbalancer["id"] = lb["LoadBalancerId"]
            loadbalancer["operating_status"] = "ONLINE"
            loadbalancer["name"] = lb["LoadBalancerName"]

            loadbalancers.append(loadbalancer)

        return loadbalancers

    def createLoadBalancer(self, inLoadBalancer):
        request = CreateLoadBalancerRequest.CreateLoadBalancerRequest()
        request.set_LoadBalancerName(inLoadBalancer["name"])
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        ''' response data
        {
            "RequestId":"365F4154-92F6-4AE4-92F8-7FF34B540710",
            "LoadBalancerId":"139a00604ad-cn-east-hangzhou-01",
            "Address":"42.250.6.36",
            "NetworkType":"classic"
            "MasterZoneId":"cn-hangzhou-b",
            "SlaveZoneId":"cn-hangzhou-d",
            "LoadBalancerName":"abc"
        }
        '''

        lb = resp

        outLoadBalancer = {}
        outLoadBalancer["description"] = ""
        outLoadBalancer["admin_state_up"] = True
        outLoadBalancer["tenant_id"] = ""
        outLoadBalancer["provisioning_status"] = "active"
        outLoadBalancer["listeners"] = []
        outLoadBalancer["vip_address"] = lb["Address"]
        outLoadBalancer["vip_subnet_id"] = ""
        outLoadBalancer["id"] = lb["LoadBalancerId"]
        outLoadBalancer["operating_status"] = "ONLINE"
        outLoadBalancer["name"] = lb["LoadBalancerName"]
        outLoadBalancer["provider"] = ""

        return outLoadBalancer

    def getLoadBalancer(self, lbID):
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(lbID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        ''' response data
        {
            "RequestId": "365F4154-92F6-4AE4-92F8-7FF34B540710",
            "LoadBalancerId": "139a00604ad-cn-east-hangzhou-01",
            "RegionId": "cn-east-hangzhou-01",
            "LoadBalancerName": "abc",
            "LoadBalancerStatus ": "active",
            "Address": "42.250.6.36",
            "AddressType": "internet",
            "InternetChargeType": "paybybandwidth",
            "Bandwidth": "5",
            "CreateTime": "2014-01-01 00:00:00",
            "ListenerPorts": {
              "ListenerPort": [
                  80,
                  443
              ]
            },
            "BackendServers": {
              "BackendServer": [
                  {
                      "ServerId": "vm-233",
                      "Weight": 100
                  },
                  {
                      "ServerId": "vm-234",
                      "Weight": 90
                  }
              ]
            }
            "MasterZoneId":"cn-hangzhou-b",
            "SlaveZoneId":"cn-hangzhou-d"
        }
        '''

        lb = resp

        loadBalancer = {}
        loadBalancer["description"] = ""
        loadBalancer["admin_state_up"] = True
        loadBalancer["tenant_id"] = ""
        loadBalancer["provisioning_status"] = lb["LoadBalancerStatus"]
        loadBalancer["listeners"] = lb["ListenerPorts"]["ListenerPort"]
        loadBalancer["vip_address"] = lb["Address"]
        loadBalancer["vip_subnet_id"] = ""
        loadBalancer["id"] = lb["LoadBalancerId"]
        loadBalancer["operating_status"] = "ONLINE"
        loadBalancer["name"] = lb["LoadBalancerName"]

        return loadBalancer

    def updateLoadBalancer(self, lbID, inLoadBalancer):
        adminStateUp = inLoadBalancer["admin_state_up"]
        description = inLoadBalancer["description"]
        name = inLoadBalancer["name"]

        request = SetLoadBalancerNameRequest.SetLoadBalancerNameRequest()
        request.set_LoadBalancerName(name)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        return self.getLoadBalancer(lbID)

    def deleteLoadBalancer(self, lbID):
        request = DeleteLoadBalancerRequest.DeleteLoadBalancerRequest()
        request.set_LoadBalancerId(lbID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return False

        return True

    def getLoadBalancerStatuses(self, lbID):
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(lbID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return None

        ''' response data
        {
            "RequestId": "365F4154-92F6-4AE4-92F8-7FF34B540710",
            "LoadBalancerId": "139a00604ad-cn-east-hangzhou-01",
            "RegionId": "cn-east-hangzhou-01",
            "LoadBalancerName": "abc",
            "LoadBalancerStatus ": "active",
            "Address": "42.250.6.36",
            "AddressType": "internet",
            "InternetChargeType": "paybybandwidth",
            "Bandwidth": "5",
            "CreateTime": "2014-01-01 00:00:00",
            "ListenerPorts": {
              "ListenerPort": [
                  80,
                  443
              ]
            },
            "BackendServers": {
              "BackendServer": [
                  {
                      "ServerId": "vm-233",
                      "Weight": 100
                  },
                  {
                      "ServerId": "vm-234",
                      "Weight": 90
                  }
              ]
            }
            "MasterZoneId":"cn-hangzhou-b",
            "SlaveZoneId":"cn-hangzhou-d"
        }
        '''

        lb = resp

        loadBanlanceStatus = {}

        loadBanlanceStatus["name"] = lb["LoadBalancerName"]
        loadBanlanceStatus["id"] = lb["LoadBalancerId"]
        loadBanlanceStatus["operating_status"] = "INLINE"
        loadBanlanceStatus["provisioning_status"] = lb["LoadBalancerStatus"]

        loadBanlanceStatus["listeners"] = []
        for listenerPort in lb["ListenerPorts"]["ListenerPorts"]:
            listener = {}
            #query listener by DescribeLoadBalancerHTTPListenerAttribute
            #use loadbalance id and listener port
            listener["name"] = ""
            listener["id"] = ""
            listener["operating_status"] = "ONLINE"
            listener["provisioning_status"] = self.getListenerStatus(lb["LoadBalancerId"], listenerPort)

            listener["pools"] = []
            pool = {}
            pool["name"] = ""
            pool["provisioning_status"] = ""
            pool["health_monitor"] = ""
            pool["id"] = ""
            pool["operating_status"] = "ONLINE"
            pool["members"] = []
            for server in lb["BackendServers"]["BackendServer"]:
                #query server status by aliyun api DescribeHealthStatus
                #use loadbalance id and port id and compare server id
                member = {}
                member["address"] = ""
                member["protocol_port"] = ""
                member["id"] = server["ServerId"]
                member["operating_status"] = "ONLINE"
                member["provisioning_status"] = self.getMemserStatus(lb["LoadBalancerId"], listenerPort, server["ServerId"])

                pool["members"].append(member)

            listener["pools"].append(pool)

            loadBanlanceStatus["listeners"].append(listener)

        return loadBanlanceStatus

    def getListenerStatus(self, lbID, lnPort):
        #query listener by DescribeLoadBalancerHTTPListenerAttribute
        #use loadbalance id and listener port

        request = DescribeLoadBalancerHTTPListenerAttributeRequest.DescribeLoadBalancerHTTPListenerAttributeRequest()
        request.set_LoadBalancerId(lbID)
        request.set_ListenerPort(lnPort)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return ""

        ''' response data
        {
            "RequestId":"365F4154-92F6-4AE4-92F8-7FF34B540710",
            "ListenerPort":80,
            "BackendServerPort":80,
            "Bandwidth":-1,
            "Status":"stopped",
            "Schedule":"wrr",
            "XForwardedFor":"on"
        }
        '''

        status = resp["Status"]
        if status == "running":
            return "ACTIVE"
        else:
            return "INACTIVE"

    def getMemserStatus(self, lbID, lnPortID, svrID):
        #query server status by aliyun api DescribeHealthStatus
        #use loadbalance id and port id and compare server id

        request = DescribeLoadBalancerHTTPListenerAttributeRequest.DescribeLoadBalancerHTTPListenerAttributeRequest()
        request.set_LoadBalancerId(lbID)
        request.set_ListenerPort(lnPortID)
        request.set_accept_format('json')
        response = self.clt.do_action(request)
        resp = json.loads(response)

        print "response: ", resp

        if "Code" in resp.keys() and "Message" in resp.keys():
            return ""

        '''
        {
            "RequestId":"365F4154-92F6-4AE4-92F8-7FF34B540710",
            "LoadBalancerId":"139a00604ad-cn-east-hangzhou-01",
            "BackendServers":{
                “BackendServer”: [
                    {
                        "ServerId": "vm-233",
                        "ServerHealthStatus:"normal"
                    },
                    {
                        “ServerId": "vm-234",
                        "ServerHealthStatus:"abnormal"
                    }
                ]
            }
        }
        '''

        for svr in resp["BackendServers"]["BackendServer"]:
            if svr["ServerId"] == svrID:
                status = svr["ServerHealthStatus"]
                if status == "normal":
                    return "ACTIVE"
                break
        return "INACTIVE"