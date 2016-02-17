Identity 
相当于“访问控制”
（1）Users

GET
/v3/users
List users
Lists users.          完成 还差一个enable字段，阿里没提供
 
detail
POST
/v3/users
Create user
Creates a user.      完成 有些字段阿里没提供
 
detail
GET
/v3/users/​{user_id}​
Show user details
Shows details for a user.  完成 阿里不提供user_id访问user信息,所以将阿里的UserName作为user_id
 
detail
PATCH
/v3/users/​{user_id}​
Update user
Updates the password for or enables or disables a user.  完成  有些字段无法更新
 
detail
DELETE
/v3/users/​{user_id}​
Delete user
Deletes a user.     完成
 
detail
POST
/v3/users/​{user_id}​/password
Change password for user
Changes the password for a user.   阿里未提供API
 
detail
GET
/v3/users/​{user_id}​/groups
List groups to which a user belongs
Lists groups to which a user belongs.   Openstack界面上没入口

（2）Role

POST
/v3/roles
Create role
Creates a role.   完成 阿里接口创建角色必须绑定策略，策略文档不可选
 
detail
GET
/v3/roles
List roles
Lists roles.    完成
 
detail
GET
/v3/roles/​{role_id}​
Show role details
Shows details for a role.  完成
 
detail
PATCH
/v3/roles/​{role_id}​
Update role
Updates a role.        阿里仅能通过role_name更新策略
 
detail
DELETE
/v3/roles/​{role_id}​      阿里不支持role_id操作role
Delete role
Deletes a role.        完成 将阿里RoleName当作role_id如此界面上呈现的role_id就是rolename
(3) Group
POST
/v3/groups
Create group
Creates a group.  完成
 
detail
GET
/v3/groups
List groups
Lists groups.    完成
 
detail
GET
/v3/groups/​{group_id}​
Show group details
Shows details for a group.   完成
 
detail
PATCH
/v3/groups/​{group_id}​
Update group
Updates a group.   完成
 
detail
DELETE
/v3/groups/​{group_id}​
Delete group
Deletes a group.   完成
 
detail
GET
/v3/groups/​{group_id}​/users
List users in group
Lists the users that belong to a group.  完成
 
detail
PUT
/v3/groups/​{group_id}​/users/​{user_id}​
Add user to group
Adds a user to a group.  完成
 
detail
HEAD
/v3/groups/​{group_id}​/users/​{user_id}​
Check whether user belongs to group
Validates that a user belongs to a group.  完成  界面无此操作
 
detail
DELETE
/v3/groups/​{group_id}​/users/​{user_id}​
Remove user from group
Removes a user from a group.   完成
（4）Policy     horizon没有入口
POST
/v3/policies
Create policy
Creates a policy.
 
detail
GET
/v3/policies
List policies
Lists policies.
 
detail
GET
/v3/policies/​{policy_id}​
Show policy details
Shows details for a policy.
 
detail
PATCH
/v3/policies/​{policy_id}​
Update policy
Updates a policy.
 
detail
DELETE
/v3/policies/​{policy_id}​
Delete policy
Deletes a policy.
