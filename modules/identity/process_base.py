class IdentityProcessorBase():

    def queryUsers(self, domian_id, name, enabled):
        pass

    def queryRolesByName(self, name):
        pass

    def createUser(self, default_project_id, description, domian_id, email, 
            enabled, name, password):
        pass

    def queryUserById(self, user_id):
        pass

    def updateUser(self, user_name, default_project_id, description, email, enabled):
        pass

    def deleteUserById(self, user_name):
        pass

    def queryUserGroups(self, user_name):
        pass

    def createRole(self, name):
        pass

    def deleteRoleById(self, role_id):
        pass

    def queryGroups(self, domian_id, name):
        pass

    def createGroup(self, description, domian_id, name)
        pass
