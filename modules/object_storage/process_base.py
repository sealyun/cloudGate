class ObjectStorageBaseProcessor():
    def queryObjects(self, account, container, limit,
            marker, end_marker, prefix, format, delimiter, path):
        pass

    def queryContainers(self):
        pass

    def createContainer(self, account, container, x_container_read,
                x_container_write,
                x_container_sync_to,
                x_container_sync_key,
                x_versions_location,
                x_container_meta_name,
                content_type,
                x_detect_content_type,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra):
        pass

    def deleteContainer(self, account, container,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra):
        pass

    def queryObjects(self, account, container, limit,
            marker, end_marker, prefix, format_, delimiter, path):
        pass

    def deleteObject(self, account, container, object_, multipart_manifest, x_trans_id_extra):
        pass
