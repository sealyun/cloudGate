# -*- encoding: utf-8 -*-
from handlers import *
from cloudGate.common.define import IDENTITY_BASE_URL

urls = [
    (r"/", IdentityBaseHandler),
    (r"/v2.0/tokens", TokensHandler),
    (IDENTITY_BASE_URL + r"/v3/auth/tokens", AuthTokensHandler),

    (IDENTITY_BASE_URL + r"/v3/users", UsersHandler),
    #(IDENTITY_BASE_URL + r"/v3/users/(.*)", UserHandler),
    #(IDENTITY_BASE_URL + r"/v3/users/(.*)/password", UserPasswordHandler),
    #(IDENTITY_BASE_URL + r"/v3/users/(.*)/groups", UserGroupsHandler),
    (IDENTITY_BASE_URL + r"/v3/users/(.*)/projects", UserProjectsHandler),

    (IDENTITY_BASE_URL + r"/v3/roles", RolesHandler),
    (IDENTITY_BASE_URL + r"/v3/roles/(.*)", RoleHandler),

    (IDENTITY_BASE_URL + r"/v3/groups", GroupsHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/(.*)", GroupHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/(.*)/users", GroupUsersHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/(.*)/users/(.*)", GroupUserHandler),

    (IDENTITY_BASE_URL + r"/v3/policies", PoliciesHandler),
    (IDENTITY_BASE_URL + r"/v3/policies/(.*)", PolicyHandler), 

    (IDENTITY_BASE_URL + r"/v3/projects", ProjectsHandler), 
]
