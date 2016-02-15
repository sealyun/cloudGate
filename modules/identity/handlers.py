# -*- encoding: utf-8 -*-
from cloudGate.common.define import *
from cloudGate.httpbase import HttpBaseHandler
from cloudGate.config import *
from api_factory import *

import sys
import json

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class IdentityBaseHandler(HttpBaseHandler):
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        print ("-----get token:", token)
        i = IdentityProcessorFac()
        self.p = i.create_processor(None, token)

        return self.p

    def get(self):
        resp = {
            "versions":{
                "values":[
                    {
                        "id": "v3.4",
                        "links": [
                            {
                                "href": "http://" + HOST + ":" + PORT + IDENTITY_BASE_URL + "/v3/",
                                "rel": "self"
                            }
                        ],
                        "media-types": [
                            {
                                "base": "application/json",
                                "type": "application/vnd.openstack.identity-v3+json"
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
                    "name": "fht"
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
                                "url": "http://121.199.9.187:8081/compute/v2.1/tenant_id",
                                "region": "RegionOne",
                                "interface": "public",
                                "id": "bc2230a70d6a444e9fba75b85fbda41b"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "http://121.199.9.187:8081/compute/v2.1/tenant_id",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "d8102dc2b9984d04b30b91b0a6037470"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "http://121.199.9.187:8081/compute/v2.1/tenant_id",
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
                                "url": "http://121.199.9.187:8081/identity/v3/",
                                "region": "RegionOne",
                                "interface": "admin",
                                "id": "c693879254544e3fb502e795a3f6acc8"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "http://121.199.9.187:8081/identity/v3/",
                                "region": "RegionOne",
                                "interface": "internal",
                                "id": "c693879254544e3fb502e795a3f6acc8"
                            },
                            {
                                "region_id": "RegionOne",
                                "url": "http://121.199.9.187:8081/identity/v3/",
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
        domain_id = self.get_argument("domain_id", None)
        name = self.get_argument("name", None)
        enabled = self.get_argument("enabled", None)

        self.get_processor()

        users = self.p.queryUsers(domain_id, name, enabled)

        resp = {
            "links": {
                "next":None,
                "previous":None,
                "self":"http://"
            },
            "users":[
                {
                    "domain_id":"",
                    "email":u["Email"],
                    "enabled":"",
                    "id":u["UserName"],
                    "description":u["Comments"],
                    "links":{
                        "self":"http://" + HOST + ":" + PORT + IDENTITY_BASE_URL + "/v3/users/" + u["UserName"],
                    },
                    "name":u["UserName"],
                } 
                for u in users
            ]
        }

        self.send_json(resp)

    def post(self):
        user = json.loads(self.request.body)["user"]

        self.get_processor()
        
        u = self.p.createUser(user["default_project_id"], 
                user["description"], 
                user["domain_id"], 
                user["email"], 
                user["enabled"], 
                user["name"], 
                user["password"])

        resp = {
            "user":{
                "default_project_id":user["default_project_id"],
                "description":u["Comments"],
                "domain_id":user["domain_id"],
                "email":u["Email"],
                "enabled":user["enabled"],
                "id":u["UserName"],
                "links":{
                    "self":"https://"
                },
                "name":u["UserName"]
            }
        }

        self.send_json(resp)

class UserHandler(IdentityBaseHandler):
    def get(self, user_name):
        self.get_processor()

        user = self.p.queryUserById(user_name)

        resp = {
            "user":{
                "default_project_id":"",
                "description":user["Comments"],
                "domain_id":"",
                "email":user["Email"],
                "enabled":"",
                "id":user["UserName"],
                "links":{
                    "self":"https://"
                },
                "name":user["UserName"]
            }
        }

        self.send_json(resp)


    def patch(self, user_name):
        user = json.loads(self.request.body)["user"]

        self.get_processor()

        u = self.p.updateUser(user_name, 
                user["default_project_id"],
                user["description"],
                user["email"],
                user["enabled"])

        resp = {
            "user":{
                "default_project_id":user["default_project_id"],
                "description":u["Comments"],
                "domain_id":"",
                "email":u["Email"],
                "enabled":user["enabled"],
                "id":u["UserName"],
                "links":{
                    "self":"https://"
                },
                "name":u["UserName"]
            }
        }

        self.send_json(resp)

    def delete(self, user_name):
        self.get_processor()
        if self.p.deleteUserById(user_name):
            self.set_status(203)
        else:
            self.set_status(403)

class UserPasswordHandler(IdentityBaseHandler):
    def post(self, user_id):
        user = json.loads(self.request.body)["user"]
        self.p.changeUserPasswd(user_id, user["password"],
                user["original_password"])

class UserGroupsHandler(IdentityBaseHandler):
    def get(self, user_name):
        self.get_processor()

        groups = self.p.queryUserGroups(user_name)

        resp = {
            "groups":[
                {
                    "description":g["Comments"],
                    "domain_id":g.domain_id,
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
                "previous":None,
                "next":None
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
                        "self": ""
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
                        "self": ""
                    },
                    "name": "another domain"
                }
            ], 
            "links": {
                "self": "",
                "previous": None,
                "next": None 
            }
        }

        self.send_json(resp)

class RolesHandler(IdentityBaseHandler):
    def get(self):
        name = self.get_argument("name", None)

        self.get_processor()
        roles = self.p.queryRolesByName(name)

        resp = {
            "links": {
                "next":None,
                "previous":None,
                "self":"http://" + HOST + ":" + PORT + IDENTITY_BASE_URL + "/v3/roles"
            },
            "roles":[
                {
                    "id":r["RoleName"],
                    "links":{
                        "self":"http://" + HOST + ":" + PORT + IDENTITY_BASE_URL + "/v3/roles/" + r["RoleId"]
                    },
                    "name":r["RoleName"]
                }
                for r in roles
            ]
        }

        self.send_json(resp)

    def post(self):
        role = json.loads(self.request.body)["role"]

        self.get_processor()

        role = self.p.createRole(role["name"])

        resp = {
            "role": {
                "id":role["RoleId"],
                "links":{
                    "self":"http://" + HOST + ":" + PORT + IDENTITY_BASE_URL + "/v3/roles/" + role["RoleId"]
                },
                "name":role["RoleName"]
            }
        }

        self.send_json(resp)

class RoleHandler(IdentityBaseHandler):
    def get(self, role_id):
        self.get_processor()
        role = self.p.queryRoleByid(role_id)

        resp = {
            "role": {
                "id":role["RoleName"],
                "links":{
                    "self":"http://",
                },
                "name":role["RoleName"]
            }
        }

        self.send_json(resp)

    def patch(self, role_id):
        self.get_processor()
        name = json.loads(self.request.body)["role"]["name"]
        role = self.p.updateRole(role_id, name)

        resp = {
            "role": {
                "id":"",
                "links":{
                    "self":"http://",
                },
                "name":""
            }
        }

        self.send_json(resp)

    def delete(self, role_id):
        self.get_processor()
        self.p.deleteRoleById(role_id)

class GroupsHandler(IdentityBaseHandler):
    def get(self):
        domain_id = self.get_argument("domain_id", None)
        name = self.get_argument("name", None)

        self.get_processor()

        groups = self.p.queryGroups(domain_id, name)

        resp = {
            "links": {
                "next":None,
                "previous":None,
                "self":"http://"
            },
            "groups":[
                {
                    "domain_id":domain_id,
                    "description":g["Comments"],
                    "id":g["GroupName"],
                    "links":{
                        "self":"http://"
                    },
                    "name":g["GroupName"]
                }
                for g in groups
            ]
        }

        self.send_json(resp)

    def post(self):
        self.get_processor()
        group = json.loads(self.request.body)["group"]

        if "description" in group:
            description = group["description"]
        else:
            description = ""
        if "domain_id" in group:
            domain = group["domain_id"]
        else:
            domain = ""

        group = self.p.createGroup(description, domain, group["name"])

        resp = {
            "group": {
                "domain_id":"",
                "description":group["Comments"],
                "id":group["GroupName"],
                "links":{
                    "self":"http://"
                },
                "name":group["GroupName"]
            }
        }

        self.send_json(resp)

class GroupHandler(IdentityBaseHandler):
    def get(self, group_id):
        self.get_processor()
        group = self.p.queryGroup(group_id)

        resp = {
            "group": {
                "domain_id":"",
                "description":group["Comments"],
                "id":group["GroupName"],
                "links":{
                    "self":"http://"
                },
                "name":group["GroupName"]
            }
        }

        self.send_json(resp)

    def patch(self, group_id):
        self.get_processor()
        group = json.loads(self.request.body)["group"]

        description = ""
        name = ""
        if "description" in group:
            description = group["description"]
        if "name" in group:
            name = group["name"]

        group = self.p.updateGroup(group_id, description, name)

        resp = {
            "group": {
                "domain_id":"",
                "description":group["Comments"],
                "id":group["GroupName"],
                "links":{
                    "self":"http://"
                },
                "name":group["GroupName"]
            }
        }

        self.send_json(resp)

    def delete(self, group_id):
        self.get_processor()
        self.p.deleteGroupById(group_id)

class GroupUsersHandler(IdentityBaseHandler):
    def get(self, group_id):
        self.get_processor()
        domain_id = ""
        description = ""
        name = ""
        enabled = ""

        users = self.p.queryUsersInGroup(group_id, domain_id, description, name, enabled)

        resp = {
            "users":[
                {
                    "name":u["UserName"],
                    "links":{
                        "self":"http://"
                    },
                    "domain_id":"",
                    "enabled":True,
                    "email":"email",
                    "id":u["UserName"]
                }
                for u in users
            ],
            "links":{
                "self":"http://",
                "previous":None,
                "next":None
            }
        }

        self.send_json(resp)

class GroupUserHandler(IdentityBaseHandler):
    def put(self, group_id, user_id):
        self.get_processor()
        self.p.addUserInGroup(group_id, user_id)

    def head(self, group_id, user_id):
        self.get_processor()
        res = self.p.checkUserBelongsToGroup(group_id, user_id)
        if res:
            self.set_status(204)
        else:
            self.set_status(400)

    def delete(self, group_id, user_id):
        self.get_processor()
        self.p.deleteUserFromGroup(group_id, user_id)

class PoliciesHandler(IdentityBaseHandler):
    def get(self):
        type = self.get_argument("type", None)

        policies = self.p.queryPolicies(type)

        resp = {
            "links": {
                "next":None,
                "previous":None,
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

class ProjectsHandler(IdentityBaseHandler):
    def get(self):
        resp = {
                "links": {
                    "next": None,
                    "previous": None,
                    "self": "http://121.199.9.187:8081/v3/projects"
                },
            "projects": [
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "0c4e939acacf4376bdcd1129f1a054ad",
                    "links": {
                        "self": ""
                    },
                    "name": "admin",
                    "parent_id":None 
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "0cbd49cbf76d405d9c86562e1d579bd3",
                    "links": {
                        "self": ""
                    },
                    "name": "demo",
                    "parent_id": None
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "2db68fed84324f29bb73130c6c2094fb",
                    "links": {
                        "self": ""
                    },
                    "name": "swifttenanttest2",
                    "parent_id": None
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "3d594eb0f04741069dbbb521635b21c7",
                    "links": {
                        "self": ""
                    },
                    "name": "service",
                    "parent_id": None
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "43ebde53fc314b1c9ea2b8c5dc744927",
                    "links": {
                        "self": ""
                    },
                    "name": "swifttenanttest1",
                    "parent_id": None
                },
                {
                    "description": "",
                    "domain_id": "1bc2169ca88e4cdaaba46d4c15390b65",
                    "enabled": True,
                    "id": "4b1eb781a47440acb8af9850103e537f",
                    "links": {
                        "self": ""
                    },
                    "name": "swifttenanttest4",
                    "parent_id": None
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "5961c443439d4fcebe42643723755e9d",
                    "links": {
                        "self": ""
                    },
                    "name": "invisible_to_admin",
                    "parent_id": None
                },
                {
                    "description": None,
                    "domain_id": "default",
                    "enabled": True,
                    "id": "fdb8424c4e4f4c0ba32c52e2de3bd80e",
                    "links": {
                        "self": ""
                    },
                    "name": "alt_demo",
                    "parent_id": None
                }
            ]
        }

        self.send_json(resp)
