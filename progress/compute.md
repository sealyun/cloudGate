Compute
Server ---对应阿里云的ECS 实例API

GET
/v2.1/​{tenant_id}​/servers
List servers
Lists IDs, names, and links for all servers.
 
detail
POST
/v2.1/​{tenant_id}​/servers
Create server
Creates a server.
 
detail
GET
/v2.1/​{tenant_id}​/servers/detail
List details for servers
Lists all servers with details.
 
detail
GET
/v2.1/​{tenant_id}​/servers/​{server_id}​
Show server details
Shows details for a server.
 
detail
PUT
/v2.1/​{tenant_id}​/servers/​{server_id}​
Update server
Updates the editable attributes of a server.
 
detail
DELETE
/v2.1/​{tenant_id}​/servers/​{server_id}​
Delete server
Deletes a server.


Servers actions (servers, action)
Performs actions on a server. Specify the action in the request body.
You can associate a fixed or floating IP address with a server instance, or disassociate a fixed or floating IP address from a server instance. You can attach a volume to a server.
You can create an image from a server, evacuate a server from a failed host to a new host, and force-delete a server before deferred cleanup. You can reboot, rebuild, rescue, resize, confirm the resize of, revert a pending resize for, shelve, shelf-offload, unshelve, start, stop, and unrescue a server.
You can get an RDP, serial, SPICE, or VNC console for a server.
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Add (associate) fixed IP (addFixedIp action)
Adds a fixed IP address to a server instance, which associates that address with the server. The fixed IP address is retrieved from the network that you specify in the request.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Add (associate) floating IP (addFloatingIp action)
Adds a floating IP address to a server, which associates that address with the server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Attach volume (attach action)
Attaches a volume to a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Confirm resized server (confirmResize action)
Confirms a pending resize action for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Create image (createImage action)
Creates an image from a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Evacuate server (evacuate action)
Evacuates a server from a failed host to a new one.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Force-delete server (forceDelete action)
Force-deletes a server before deferred cleanup.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Show console output (os-getConsoleOutput action)
Shows console output for a server instance.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Get RDP console (os-getRDPConsole action)
Gets an RDP console for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Get serial console (os-getSerialConsole action)
Gets a serial console for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Get SPICE console (os-getSPICEConsole action)
Gets a SPICE console for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Get VNC console (os-getVNCConsole action)
Gets a VNC console for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Reboot server (reboot action)
Reboots a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Rebuild server (rebuild action)
Rebuilds a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Remove (disassociate) fixed IP (removeFixedIp action)
Removes, or disassociates, a fixed IP address from a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Remove (disassociate) floating IP (removeFloatingIp action)
Removes, or disassociates, a floating IP address from a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Rescue server (rescue action)
Puts a server in rescue mode and changes its status to RESCUE.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Resize server (resize action)
Resizes a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Restore soft-deleted instance (restore action)
Restores a previously soft-deleted server instance. You cannot use this method to restore deleted instances.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Revert resized server (revertResize action)
Cancels and reverts a pending resize action for a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Shelve server (shelve action)
Shelves a server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Shelf-offload (remove) server (shelveOffload action)
Shelf-offloads, or removes, a shelved server.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Start server (os-start action)
Starts a stopped server and changes its status toACTIVE.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Stop server (os-stop action)
Stops a running server and changes its status toSHUTOFF.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Unrescue server (unrescue action)
Unrescues a server. Changes status to ACTIVE.
 
detail
POST
/v2.1/​{tenant_id}​/servers/​{server_id}​/action
Unshelve (restore) shelved server (unshelve action)
Unshelves, or restores, a shelved server.

