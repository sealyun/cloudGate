class ComputeProcessorBase():

    def queryServers(self, tenant_id, changes_since, 
            image, flavor, name, status, host, limit, marker):
        pass

    def createServer(self, tenant_id, name, imageRef, flavorRef, metadata):
        pass

    def queryServersDetails(self, tenant_id, changes_since, image, 
            flavor, name, status, host, limit, marker):
        pass

    def queryServer(self, tenant_id, server_id):
        pass

    def updateServerName(self, tenant_id, server_id, name, imageRef, flavorRef, metadata):
        pass

    def updateServerIP(self, tenant_id, server_id, accessIPv4, accessIPv6):
        pass

    def updateServerOSDCFdiskConfig(self, tenant_id, server_id, OSDCFdiskConfig):
        pass

    def deleteServer(self, tenant_id, server_id):
        pass

    #define interface of server action
    def ServerAction(self, tenat_id, server_id, action):
        #do nothing just define interface
        pass
