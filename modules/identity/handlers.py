# -*- encoding: utf-8 -*-
from cloudGate.httpbase import HttpBaseHandler
from cloudGate.config import *

import sys
import json

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class IdentityBaseHandler(HttpBaseHandler):
    def get(self):
        resp = {
            "versions":{
                "values":[
                    {
                        "id": "v3",
                        "links": [
                            {
                                "href": "http://" + HOST + ":" + PORT + "/v3/",
                                "rel": "self"
                            }
                        ],
                        "media-types": [
                            {
                                "base": "application/json",
                            }
                        ],
                        "status": "stable",
                        "updated": "2015-04-17T00:00:00Z"
                    }
                ]
            }
        }

        self.send_json(resp)

class TokensHandler(IdentityBaseHandler):
    def post(self):
        pass

class AuthTokensHandler(IdentityBaseHandler):
    def token_with_scoped(self, project_id):
        resp = {
                "token": {
                "methods": [
                    "token"
                ],
                "roles": [
                    {
                        "id": "5090055d6bd547dc83e0e8f070803708",
                        "name": "admin"
                    }
                ],
                "expires_at": "2915-11-05T22:00:11.000000Z",
                "project": {
                    "domain": {
                        "id": "default",
                        "name": "Default"
                    },
                    "id": "5b50efd009b540559104ee3c03bbb2b7",
                    "name": "admin"
                },
                "catalog": [
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "b2605da9b25943beb49b2bd86aca2202"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "c4d1184caf8c4351bff4bf502a09684e"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "cd73bda89e3948738c2721a8c3acac54"
                            }
                        ],
                        "type": "image",
                        "id": "495df2483dc145dbb6b34bfbdd787aae",
                        "name": "glance"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "7d03218a7f4246e8b9e3992318bf5397"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "9ad7f8ce438c4212b8aac930bca04c86"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "d84aad1a45c44e4da09b719167383049"
                            }
                        ],
                        "type": "ec2",
                        "id": "54204024bb7d4665a8efc34fc758f1f7",
                        "name": "ec2"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "1077687c18514490a3ec980eadd1bd13"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "1e86d8bef1514c3fba8d157a22ccce88"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "f6a6b7bbba66443ead3a0e31a008c271"
                            }
                        ],
                        "type": "messaging-websocket",
                        "id": "6b8655af7d044a15bec3cdca4f2919f8",
                        "name": "zaqar-websocket"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "083663fd231e40ad97384ad3efb9f1b7"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "0f4b7054ea27450eac43f685a4fc1d2c"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "5f3ea39df2e44378b1802a1a87ef9ac4"
                            }
                        ],
                        "type": "orchestration",
                        "id": "6d6346ff2ca842e5968373fbb93e231f",
                        "name": "heat"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "bc2230a70d6a444e9fba75b85fbda41b"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "d8102dc2b9984d04b30b91b0a6037470"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "f8253a53edd749bf8b107a53a5d47a82"
                            }
                        ],
                        "type": "compute",
                        "id": "75df965385cc4120a17110c1fde00182",
                        "name": "nova"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "0ceeb58592274caea5bc942a07d5473f"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "8126f2c7021d413e9c98ec3a0ba0fd58"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "c693879254544e3fb502e795a3f6acc8"
                            }
                        ],
                        "type": "identity",
                        "id": "78aad571d38049e69c866c2abac76af6",
                        "name": "keystone"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "3654138dc64a45aeb5a8153f2a089c74"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "7a0d12d0b7314afd9b53d1618ab546ea"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "82b68ff3aedb43e2acc8307234d3fd0b"
                            }
                        ],
                        "type": "volume",
                        "id": "80491007c0ab462daaa9087250325f59",
                        "name": "cinder"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "24dfa252fba64469b8b1a832f04bded9"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "e0a01d6cd3be4f6abcc72367b2d87993"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "f33f79d42df247e1bf6daf43a548b014"
                            }
                        ],
                        "type": "cloudformation",
                        "id": "ac5cc6e3c62840818ab338c981d5603f",
                        "name": "heat-cfn"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "3e78c357b3c8469fbea12eb681f88a0c"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "89d2aad3dc8e478fbabb21dd7db0962a"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "b6d4a8cf5e4042848a749a3116497e55"
                            }
                        ],
                        "type": "network",
                        "id": "b33660edd1eb45e485f7e5f14401a739",
                        "name": "neutron"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "1f8287cf963948778ab0eb109d9f857d"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "3adf5f9cc5184d92af5ff0fdef043e4a"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "f747223060b3414f947fdcdca2ce8714"
                            }
                        ],
                        "type": "messaging",
                        "id": "cf3e38e9aed54e2d84ea64485317d7a0",
                        "name": "zaqar"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "08f507ccb552476b98f3af7718f25557"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "d20091ba591347b2b419e5fbde9b7976"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "e6b667776e7245dea6e39f2820e080b0"
                            }
                        ],
                        "type": "compute_legacy",
                        "id": "d442e96b273a48018567aeec5800c3e0",
                        "name": "nova_legacy"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "012c78a6694a494995c58d5955fb7822"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "802d5de210874f068ba31c7e27c29d70"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "b37ada66e02e44c9a9a7976d77365503"
                            }
                        ],
                        "type": "volumev2",
                        "id": "d93e78c7967f49acbdd732b9dd97e0d0",
                        "name": "cinderv2"
                    },
                    {
                        "endpoints": [
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "265ce88a0e1642fc90b2ec20ccb279ff"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "500b7f066d39492faff8a3f710fb5a2f"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "a33b0684f817405280df1f5600777a75"
                            }
                        ],
                        "type": "object-store",
                        "id": "da1b1b5c529946fcb3ee3abdcf376fcb",
                        "name": "swift"
                    }
                ],
                "extras": {},
                "user": {
                    "domain": {
                        "id": "default",
                        "name": "Default"
                    },
                    "id": "10a2e6e717a245d9acad3e5f97aeca3d",
                    "name": "admin"
                },
                "audit_ids": [
                    "wLc7nDMsQiKqf8VFU4ySpg"
                ],
                "issued_at": "2015-11-05T21:32:30.505384Z"
            }
        }
        return resp

    def post(self):
        print self.request.body

        auth = json.loads(self.request.body)

        if "auth" not in auth:
            return

        if "token" in auth["auth"]["identity"]:
            user = self.parse_token(auth["auth"]["identity"]["token"]["id"])
        else:
            user = auth["auth"]["identity"]["password"]["user"]

        if user["name"] == IDENTITY["aliyun"]["user_name"] and \
                user["password"] == IDENTITY["aliyun"]["passwd"]:
            self.add_header('X-Auth-Token', self.create_tocken(user["name"] + user["password"]))
            self.add_header('X-Subject-Token', self.create_tocken(user["name"] + user["password"]))
        else:
            self.set_status(403)
            return

        if "scope" in auth["auth"] and "project" in auth["auth"]["scope"]:
            resp = self.token_with_scoped(auth["auth"]["scope"]["project"]["id"])
        else:
            resp = {
                "token": {
                    "methods": [
                        "password"
                    ],
                    "expires_at": "2915-11-06T15:32:17.893769Z",
                    "extras": {},
                    "user": {
                        "domain": {
                            "id": "default",
                            "name": "Default"
                        },
                        "id": "423f19a4ac1e4f48bbb4180756e6eb6c",
                        "name": user["name"]
                    },
                    "audit_ids": [
                        "ZzZwkUflQfygX7pdYDBCQQ"
                    ],
                    "issued_at": "2015-11-06T14:32:17.893797Z"
                }
            }

        self.send_json(resp)

class UsersHandler(IdentityBaseHandler):
    def get(self):
        domian_id = self.get_argument("domain_id", None)
        name = self.get_argument("name", None)
        enabled = self.get_argument("enabled", None)

        users = self.p.queryUsers(domian_id, name, enabled)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "users":[
                {
                    "domian_id":domian_id,
                    "email":u.email,
                    "enabled":u.enabled,
                    "id":u.id,
                    "links":{
                        "self":"http://",
                    },
                    "name":u.name,
                } 
                for u in users
            ]
        }

        self.send_json(resp)

    def post(self):
        user = json.loads(self.request.body)["user"]

        user = self.p.createUser(user["default_project_id"], 
                user["description"], 
                user["domian_id"], 
                user["email"], 
                user["enabled"], 
                user["name"], 
                user["password"])

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)

class UserHandler(IdentityBaseHandler):
    def get(self, user_id):
        user = self.p.queryUserById(user_id)

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)


    def patch(self, user_id):
        user = json.loads(self.request.body)["user"]

        user = self.p.updateUser(user_id, 
                user["default_project_id"],
                user["description"],
                user["email"],
                user["enabled"])

        resp = {
            "user":{
                "default_project_id":user.default_project_id,
                "description":user.description,
                "domian_id":user.domian_id,
                "email":user.email,
                "enabled":user.enabled,
                "id":user.id,
                "links":{
                    "self":"https://"
                },
                "name":user.name
            }
        }

        self.send_json(resp)

    def delete(self, user_id):
        self.p.deleteUserById(user_id)

class UserPasswordHandler(IdentityBaseHandler):
    def post(self, user_id):
        user = json.loads(self.request.body)["user"]
        self.p.changeUserPasswd(user_id, user["password"],
                user["original_password"])

class UserGroupsHandler(IdentityBaseHandler):
    def get(self, user_id):
        groups = self.p.queryUserGroups(user_id)

        resp = {
            "groups":[
                {
                    "description":g.description,
                    "domian_id":g.domian_id,
                    "id":g.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":g.name
                }
                for g in groups
            ],
            "links":{
                "self":"http://",
                "previous":null,
                "next":null
            }
        }

        self.send_json(resp)

class UserProjectsHandler(IdentityBaseHandler):
    def get(self, user_id):
        resp = {
            "projects": [
                {
                    "description": "description of this project",
                    "domain_id": "161718",
                    "enabled": True,
                    "id": "456788",
                    "parent_id": "212223",
                    "links": {
                        "self": "http://identity:35357/v3/projects/456788"
                    },
                    "name": "a project name"
                },
                {
                    "description": "description of this project",
                    "domain_id": "161718",
                    "enabled": True,
                    "id": "456789",
                    "parent_id": "212223",
                    "links": {
                        "self": "http://identity:35357/v3/projects/456789"
                    },
                    "name": "another domain"
                }
            ], 
            "links": {
                "self": "http://identity:35357/v3/users/313233/projects",
                "previous": None,
                "next": None 
            }
        }

        self.send_json(resp)

class RolesHandler(IdentityBaseHandler):
    def get(self):
        name = self.get_argument("name", None)

        roles = self.p.queryRolesByName(name)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "roles":[
                {
                    "id":r.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":r.name
                }
                for r in roles
            ]
        }

        self.send_json(resp)

    def post(self):
        role = json.loads(self.request.body)["role"]

        role = self.p.createRole(role["name"])

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

class RoleHandler(IdentityBaseHandler):
    def get(self, role_id):
        role = self.p.queryRoleByid(role_id)

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

    def patch(self, role_id):
        name = json.loads(self.request.body)["role"]["name"]
        role = self.p.updateRole(role_id, name)

        resp = {
            "role": {
                "id":role.id,
                "links":{
                    "self":"http://",
                },
                "name":role.name
            }
        }

        self.send_json(resp)

    def delete(self, role_id):
        self.p.deleteRoleById(role_id)

class GroupsHandler(IdentityBaseHandler):
    def get(self):
        domian_id = self.get_argument("domian_id", None)
        name = self.get_argument("name", None)

        groups = self.p.queryGroups(domian_id, name)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "groups":[
                {
                    "domian_id":g.domian_id,
                    "description":g.description,
                    "id":g.id,
                    "links":{
                        "self":"http://"
                    },
                    "name":g.name
                }
                for g in groups
            ]
        }

        self.send_json(resp)

    def post(self):
        group = json.loads(self.request.body)["group"]

        group = self.p.createGroup(group["description"],
                group["domian_id"],
                group["name"])

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

class GroupHandler(IdentityBaseHandler):
    def get(self, group_id):
        group = self.p.queryGroup(group_id)

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

    def patch(self, group_id):
        group = json.loads(self.request.body)["group"]

        group = self.p.updateGroup(group_id, 
                group["description"],
                group["name"])

        resp = {
            "group": {
                "domian_id":group.domian_id,
                "description":group.description,
                "id":group.id,
                "links":{
                    "self":"http://"
                },
                "name":group.name
            }
        }

        self.send_json(resp)

    def delete(self, group_id):
        self.p.deleteGroupById(group_id)

class GroupUsersHandler(IdentityBaseHandler):
    def get(self, group_id):
        domian_id = self.get_arguments("domian_id",None)
        description = self.get_arguments("description",None)
        name = self.get_arguments("name",None)
        enabled = self.get_arguments("enabled",None)

        users = self.p.queryUsersInGroup(group_id, domian_id, description, name, enabled)

        resp = {
            "users":[
                {
                    "name":u.name,
                    "links":{
                        "self":"http://"
                    },
                    "domian_id":u.domian_id,
                    "enabled":u.enabled,
                    "email":u.email,
                    "id":u.id
                }
                for u in users
            ],
            "links":{
                "self":"http://",
                "previous":null,
                "next":null
            }
        }

        self.send_json(resp)

class GroupUserHandler(IdentityBaseHandler):
    def put(self, group_id, user_id):
        self.p.addUserInGroup(group_id, user_id)

    def head(self, group_id, user_id):
        res = self.p.checkUserBelongsToGroup(group_id, user_id)
        if res:
            #HTTP 204
            pass
        else:
            pass

    def delete(self, group_id, user_id):
        self.p.deleteUserFromGroup(group_id, user_id)

class PoliciesHandler(IdentityBaseHandler):
    def get(self):
        type = self.get_argument("type", None)

        policies = self.p.queryPolicies(type)

        resp = {
            "links": {
                "next":null,
                "previous":null,
                "self":"http://"
            },
            "policies":[
                {
                    "blob":json.loads(p.blob),
                    "id":p.id,
                    "links":{
                        "self":"http://"
                    },
                    "project_id":p.project_id,
                    "type":p.type,
                    "user_id":p.user_id
                }
                for p in policies
            ]
        }

        self.send_json(resp)

    def post(self):
        policy = json.loads(self.request.body)["policy"]

        policy = self.p.createPolicy(policy["blob"],
                policy["project_id"],
                policy["type"],
                policy["user_id"])

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "project_id":policy.project_id,
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

class PolicyHandler(IdentityBaseHandler):
    def get(self, policy_id):
        policy = self.p.queryPolicie(policy_id)

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "id":policy.id,
                "project_id":policy.project_id,
                "links":{
                    "self":"http://"
                },
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

    def patch(self, policy_id):
        policy = json.loads(self.request.body)["policy"]

        policy = self.p.updatePolicy(policy_id,
                policy["blob"],
                policy["project_id"],
                policy["type"],
                policy["user_id"])

        resp = {
            "policy":{
                "blob":json.loads(policy.blob),
                "id":policy.id,
                "project_id":policy.project_id,
                "links":{
                    "self":"http://"
                },
                "type":policy.type,
                "user_id":policy.user_id
            }
        }

        self.send_json(resp)

    def delete(self, policy_id):
        self.p.deletePolicy(policy_id)
