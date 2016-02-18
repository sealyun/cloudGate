##Network
对应VPC

###Network
1. List networks
Description: Lists networks to which the tenant has access.
Method: GET
URI: /networking/v2.0/networks
    1)/networking/v2.0/networks.json
    2)/networking/v2.0/networks.json?shared=False&tenant_id=5b50efd009b540559104ee3c03bbb2b7
    3)/networking/v2.0/networks.json?shared=True
    4)/networking/v2.0/networks.json?router:external=True
Progress: OK
Remark: 
    1）在horizon的Admin模块查询网络调用URI:/networking/v2.0/networks.json,在Project模块查询网络调用剩下剩下三个URI，即包含条件参数
    2）阿里云不支持shared和router:external属性，故在cloudGate的处理中当查询条件shared或router:external为True时不执行查询直接返回空结果
    3）openstack查询network字段如下：
        {
            "status": "ACTIVE",
            "subnets": ["54d6f61d-db07-451c-9ab3-b9609b6b6f0b"],
            "name": "private-network",
            "provider:physical_network": null,
            "admin_state_up": true,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "provider:network_type": "local",
            "router:external": true,
            "mtu": 0,
            "shared": true,
            "id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
            "provider:segmentation_id": null
        }
        阿里云返回的VPC查询结果如下：
        {
            "CidrBlock": "172.16.0.0/16",
            "CreationTime": "2014-10-29T13:30:19Z",
            "Description": "",
            "RegionId": "cn-beijing",
            "Status": "Available",
            "VRouterId": "vrt-25bezkd03",
            "VSwitchIds": {"VSwitchId": []},
            "VpcId": "vpc-257gq642n",
            "VpcName": ""
        }
        故只有status、name、id字段可用，其他使用默认值
        
2. Create network
Description: Creates a network.
Method: POST
URI: /networking/v2.0/networks
    1)/networking/v2.0/networks.json
Progress: OK
Remark: 
    1）openstack创建网络时，通过http的body传输如下数据
        {
            "name": "private-network",
            "admin_state_up": true,
            "shared": true,
            "router:external": true,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869"
        }
        因阿里云不支持shared和router:external属性，故当此两个属性为True时，不创建网络，提示不支持。
        创建成功后，阿里云返回数据
        {
          "RequestId": "461D0C42-D5D1-4009-9B6A-B3D5888A19A9",
          "RouteTableId": "vtb-25wm68mnh",
          "VRouterId": "vrt-25bezkd03",
          "VpcId": "vpc-257gq642n"
        }
        openstack需要返回的数据
        {
            "status": "ACTIVE",
            "subnets": [],
            "name": "net1",
            "admin_state_up": true,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "router:external": false,
            "mtu": 0,
            "shared": false,
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
        只网络id可用，其他字段使用默认值

3. Create bulk networks
Description: Creates multiple networks in a single request.
Method: POST
URI: /networking/v2.0/networks
    1)/networking/v2.0/networks.json
Progress: OK
Remark:
    1）openstack界面无同时创建多个网络的入口，后台已实现同时创建多个网络

4. Show network details
Description: Shows details for a network.
Method: GET
URI: /networking/v2.0/networks/​{network_id}
    1)/networking/v2.0/networks/​{network_id}.json
Progress: DOING
Remark:
    1）后台可以通过阿里云查询网络详情，horizon前台页面出错
    2）网络详情字段不匹配问题同上所述

5. Update network
Description: Updates a network.
Method: PUT
URI: /networking/v2.0/networks/​{network_id}
    1)/networking/v2.0/networks/​{network_id}.json
Progress: DOING
Remark:
    1）horizon问题，请求无法发送至cloudGate
    2）cloudGate后台处理应无问题

6. Delete network
Description: Deletes a network and its associated resources.
Method: DELETE
URI: /networking/v2.0/networks/​{network_id}
    1)/networking/v2.0/networks/​{network_id}.json
Progress: OK
Remark:

7. Network API extensions
Description: Network API extensions.
Method: GET
URI: /networking/v2.0/extensions
    1)/networking/v2.0/extensions.json
Progress: OK
Remark:
    1）返回空结果
 
8. Network DHCP agents
Description: Network DHCP agents.
Method: GET
URI: /networking/v2.0/networks/​{network_id}/dhcp-agents
    1)/networking/v2.0/networks/​{network_id}/dhcp-agents.json
Progress: OK
Remark:
    1）返回空结果
    
###Subnet
1. List subnets
Description: Lists subnets to which the tenant has access.
Method: GET
URI: /networking/v2.0/subnets
    1)/networking/v2.0/subnets.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

2. Create subnet
Description: Creates a subnet on a network.
Method: POST
URI: /networking/v2.0/subnets
    1)/networking/v2.0/subnets.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

3. Create bulk subnets
Description: Creates multiple subnets in a single request. Specify a list of subnets in the request body.
Method: POST
URI: /networking/v2.0/subnets
    1)/networking/v2.0/subnets.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

4. Show subnet details
Description: Shows details for a subnet.
Method: GET
URI: /networking/v2.0/subnets/​{subnet_id}
    1)/networking/v2.0/subnets/​{subnet_id}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

5. Update subnet
Description: Updates a subnet.
Method: PUT
URI: /networking/v2.0/subnets/​{subnet_id}
    1)/networking/v2.0/subnets/​{subnet_id}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

6. Delete subnet
Description: Deletes a subnet.
Method: DELETE
URI: /networking/v2.0/subnets/​{subnet_id}
    1)/networking/v2.0/subnets/​{subnet_id}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据
 
###Port
1. List ports
Description: Lists ports to which the tenant has access.
Method: GET
URI: /networking/v2.0/ports
    1)/networking/v2.0/ports.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

2. Create port
Description: Creates a port on a network.
Method: POST
URI: /networking/v2.0/ports
    1)/networking/v2.0/ports.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

3. Create bulk ports
Description: Creates multiple ports in a single request. Specify a list of subnets in the request body.
Method: POST
URI: /networking/v2.0/ports
    1)/networking/v2.0/ports.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

4. Show port details
Description: Shows details for a port.
Method: GET
URI: /networking/v2.0/subnets/​{port}
    1)/networking/v2.0/subnets/​{port}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

5. Update port
Description: Updates a port.
Method: PUT
URI: /networking/v2.0/ports/​{port_id}
    1)/networking/v2.0/ports/​{port_id}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据

6. Delete port
Description: Deletes a port.
Method: DELETE
URI: /networking/v2.0/ports/​{port_id}
    1)/networking/v2.0/ports/​{port_id}.json
Progress: UNSUPPORT
Remark:
    1）阿里云不支持子网相关API
    2）后台Handler以实现，阿里云对应Processor为构造假数据


##Load Balance
###---TODO---
LBaaS v2.0 
相当于SLB
GET
/v2.0/lbaas/loadbalancers
List load balancers
Lists all load balancers for the tenant account.
 
detail
POST
/v2.0/lbaas/loadbalancers
Create load balancer
Creates a load balancer.
 
detail
GET
/v2.0/lbaas/loadbalancers/​{loadbalancer_id}​
Show load balancer details
Shows details for a load balancer.
 
detail
PUT
/v2.0/lbaas/loadbalancers/​{loadbalancer_id}​
Update load balancer
Updates a load balancer.
 
detail
DELETE
/v2.0/lbaas/loadbalancers/​{loadbalancer_id}​
Remove load balancer
Removes a load balancer and its associated configuration from the tenant account.
 
detail
GET
/v2.0/lbaas/loadbalancers/​{loadbalancer_id}​/statuses
Show load balancer status tree
Shows the status tree for a load balancer.
 
detail
GET
/v2.0/lbaas/listeners
List listeners
Lists all listeners.
 
detail
POST
/v2.0/lbaas/listeners
Create listener
Creates a listener.
 
detail
GET
/v2.0/lbaas/listeners/​{listener_id}​
Show listener details
Shows details for a listener.
 
detail
PUT
/v2.0/lbaas/listeners/​{listener_id}​
Update listener
Updates a listener.
 
detail
DELETE
/v2.0/lbaas/listeners/​{listener_id}​
Remove listener
Removes a listener.
 
detail
GET
/v2.0/lbaas/pools
List pools
Lists all pools that are associated with your tenant account.
 
detail
POST
/v2.0/lbaas/pools
Create pool
Creates a pool.
 
detail
GET
/v2.0/lbaas/pools/​{pool_id}​
Show pool details
Shows details for a pool.
 
detail
PUT
/v2.0/lbaas/pools/​{pool_id}​
Update pool
Updates a pool.
 
detail
DELETE
/v2.0/lbaas/pools/​{pool_id}​
Remove pool
Removes a pool.
 
detail
GET
/v2.0/lbaas/pools/​{pool_id}​/members
List pool members
Lists members of a pool.
 
detail
POST
/v2.0/lbaas/pools/​{pool_id}​/members
Add member to pool
Adds a member to a pool.
 
detail
GET
/v2.0/lbaas/pools/​{pool_id}​/members/​{member_id}​
Show pool member details
Shows details for a pool member.
 
detail
PUT
/v2.0/lbaas/pools/​{pool_id}​/members/​{member_id}​
Update pool member
Updates attributes for a pool member.
 
detail
DELETE
/v2.0/lbaas/pools/​{pool_id}​/members/​{member_id}​
Remove member from pool
Removes a member from a pool and its associated configuration from the tenant account.
 
detail
POST
/v2.0/lbaas/health_monitors
Create health monitor
Creates a health monitor.
 
detail
GET
/v2.0/lbaas/health_monitors/​{health_monitor_id}​
Show health monitor details
Shows details for a health monitor.
 
detail
PUT
/v2.0/lbaas/health_monitors/​{health_monitor_id}​
Update health monitor
Updates a health monitor.
 
detail
DELETE
/v2.0/lbaas/health_monitors/​{health_monitor_id}​
Remove health monitor
Removes a health monitor and its associated configuration from the tenant account.
