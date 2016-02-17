Network
对应VPC
GET
/v2/networks
List networks
Lists networks to which the tenant has access.
 
detail
POST
/v2/networks
Create network
Creates a network.
 
detail
POST
/v2/networks
Bulk create networks
Creates multiple networks in a single request.
 
detail
GET
/v2/networks/​{network_id}​
Show network details
Shows details for a network.
 
detail
PUT
/v2/networks/​{network_id}​
Update network
Updates a network.
 
detail
DELETE
/v2/networks/​{network_id}​
Delete network
Deletes a network and its associated resources.
 
detail
Subnets
Lists, shows information for, creates, updates, and deletes subnet resources.
GET
/v2.0/subnets
List subnets
Lists subnets to which the tenant has access.
 
detail
POST
/v2.0/subnets
Create subnet
Creates a subnet on a network.
 
detail
POST
/v2.0/subnets
Bulk create subnet
Creates multiple subnets in a single request. Specify a list of subnets in the request body.
 
detail
GET
/v2.0/subnets/​{subnet_id}​
Show subnet details
Shows details for a subnet.
 
detail
PUT
/v2.0/subnets/​{subnet_id}​
Update subnet
Updates a subnet.
 
detail
DELETE
/v2.0/subnets/​{subnet_id}​
Delete subnet
Deletes a subnet.
 
detail
Ports
Lists, shows information for, creates, updates, and deletes ports.
GET
/v2.0/ports
List ports
Lists ports to which the tenant has access.
 
detail
POST
/v2.0/ports
Create port
Creates a port on a network.
 
detail
POST
/v2.0/ports
Bulk create ports
Creates multiple ports in a single request. Specify a list of ports in the request body.
 
detail
GET
/v2.0/ports/​{port_id}​
Show port details
Shows details for a port.
 
detail
PUT
/v2.0/ports/​{port_id}​
Update port
Updates a port.
 
detail
DELETE
/v2.0/ports/​{port_id}​
Delete port
Deletes a port.

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
