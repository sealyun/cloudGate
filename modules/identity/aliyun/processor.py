#www.aliyun.com/product/ram
from cloudGate.modules.identity.process_base import *
from cloudGate.config import *
from aliyunsdkcore import client

from aliyunsdkram.request.v20150501 import ListUsersRequest
from aliyunsdkram.request.v20150501 import GetUserRequest
from aliyunsdkram.request.v20150501 import ListRolesRequest
from aliyunsdkram.request.v20150501 import CreateUserRequest 
from aliyunsdkram.request.v20150501 import UpdateUserRequest
from aliyunsdkram.request.v20150501 import DeleteUserRequest
from aliyunsdkram.request.v20150501 import CreateRoleRequest 
from aliyunsdkram.request.v20150501 import DeleteRoleRequest
from aliyunsdkram.request.v20150501 import ListGroupsRequest
from aliyunsdkram.request.v20150501 import CreateGroupRequest
from aliyunsdkram.request.v20150501 import UpdateGroupRequest

import json

class AliyunIdentityProcessor(IdentityProcessorBase):
    def __init__(self, token):
        self.token = token

        self.access_key = IDENTITY["aliyun"]["access_key"]
        self.access_secrect = IDENTITY["aliyun"]["access_secret"]
        self.regin = IDENTITY["aliyun"]["regin"]

        self.clt = client.AcsClient(self.access_key, self.access_secrect, self.regin)

    def queryUsers(self, domian_id, name, enabled):
        request = ListUsersRequest.ListUsersRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        resp = json.loads(response)

        users = []

        for u in resp["Users"]["User"]:
            r = GetUserRequest.GetUserRequest()
            r.set_UserName(u["UserName"])
            r.set_accept_format('json')
            user = json.loads(self.clt.do_action(r))

            users.append(user["User"])

        return users

    def queryRolesByName(self, name):
        request = ListRolesRequest.ListRolesRequest()
        request.set_accept_format('json')

        response = self.clt.do_action(request)

        resp = json.loads(response)

        return resp["Roles"]["Role"]

    def createUser(self, default_project_id, description, domian_id, email, 
            enabled, name, password):

        request = CreateUserRequest.CreateUserRequest() 
        request.set_accept_format('json')

        if name:
            request.set_UserName(name)
        if email:
            request.set_Email(email)
        if description:
            request.set_Comments(description)

        response = self.clt.do_action(request)

        return json.loads(response)["User"]

    def queryUserById(self, user_name):
        r = GetUserRequest.GetUserRequest()
        r.set_UserName(user_name)
        r.set_accept_format('json')
        resp = self.clt.do_action(r)
        user = json.loads(resp)

        return user["User"]

    def updateUser(self, user_name, default_project_id, description, email, enabled):
        r = UpdateUserRequest.UpdateUserRequest()
        r.set_UserName(user_name)
        r.set_NewUserName(user_name)
        r.set_accept_format('json')

        if description:
            r.set_NewComments(description)
        if email:
            r.set_NewEmail(email)

        resp = self.clt.do_action(r)

        print resp

        user = json.loads(resp)

        return user["User"]

    def deleteUserById(self, user_name):
        r = DeleteUserRequest.DeleteUserRequest()
        r.set_UserName(user_name)
        r.set_accept_format('json')

        resp = self.clt.do_action(r)

        return True

    def queryUserGroups(self, user_name):
        pass

    def createRole(self, name):
        r = CreateRoleRequest.CreateRoleRequest() 
        r.set_RoleName(name)
        r.set_AssumeRolePolicyDocument(json.dumps(
            {
                "Statement": [
                    {
                      "Action": "sts:AssumeRole",
                      "Effect": "Allow",
                      "Principal": {
                        "RAM": [
                          "acs:ram::1953308415728282:root"
                        ]
                      }
                    }
                ],
                "Version": "1"
            }
        ))
        r.set_accept_format('json')

        response = self.clt.do_action(r)
        print response
        resp = json.loads(response)

        return resp["Role"]

    def deleteRoleById(self, role_id):
        r = DeleteRoleRequest.DeleteRoleRequest()
        r.set_RoleName(role_id)
        r.set_accept_format('json')

        response = self.clt.do_action(r)

        return True

    def queryGroups(self, domian_id, name):
        r = ListGroupsRequest.ListGroupsRequest()
        r.set_accept_format('json')

        response = self.clt.do_action(r)

        resp = json.loads(response)

        return resp["Groups"]["Group"]

    def createGroup(self, description, domian_id, name):
        r = CreateGroupRequest.CreateGroupRequest()
        r.set_GroupName(name)
        r.set_Comments(description)
        r.set_accept_format('json')

        response = self.clt.do_action(r)

        print response

        resp = json.loads(response)

        return resp["Group"]

    def updateGroup(self, group_id, description, name):
        r = UpdateGroupRequest.UpdateGroupRequest()

        r.set_GroupName(group_id)
        if name:
            r.set_NewGroupName(name)
        else:
            r.set_NewGroupName(group_id)

        if description:
            r.set_NewComments(description)

        response = self.clt.do_action(r)

        resp = json.loads(response)

        return resp["Group"]


