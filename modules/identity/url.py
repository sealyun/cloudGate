# -*- encoding: utf-8 -*-
from handlers import *
from cloudGate.common.define import IDENTITY_BASE_URL

urls = [
    (r"/", IdentityBaseHandler),
    (r"/v2.0/tokens", TokensHandler),
    (IDENTITY_BASE_URL + r"/v3/auth/tokens", AuthTokensHandler),

    (IDENTITY_BASE_URL + r"/v3/users", UsersHandler),
    (IDENTITY_BASE_URL + r"/v3/users/(^[a-zA-Z0-9\.@\-_]+$)", UserHandler),
    #(IDENTITY_BASE_URL + r"/v3/users/(^[a-zA-Z0-9\.@\-_]+$)/password", UserPasswordHandler),
    (IDENTITY_BASE_URL + r"/v3/users/(^[a-zA-Z0-9\.@\-_]+$)/groups", UserGroupsHandler),
    (IDENTITY_BASE_URL + r"/v3/users/([a-zA-Z0-9]+)/projects", UserProjectsHandler),

    (IDENTITY_BASE_URL + r"/v3/roles", RolesHandler),
    (IDENTITY_BASE_URL + r"/v3/roles/(.*)", RoleHandler),

    (IDENTITY_BASE_URL + r"/v3/groups", GroupsHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/([a-z0-9A-Z\-]+)", GroupHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/([a-z0-9A-Z]*)/users", GroupUsersHandler),
    (IDENTITY_BASE_URL + r"/v3/groups/(a-z0-9A-Z]*)/users/(.*)", GroupUserHandler),

    (IDENTITY_BASE_URL + r"/v3/policies", PoliciesHandler),
    (IDENTITY_BASE_URL + r"/v3/policies/(.*)", PolicyHandler), 

    (IDENTITY_BASE_URL + r"/v3/projects", ProjectsHandler), 
]
