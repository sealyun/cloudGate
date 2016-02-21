from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import *

class ObjectStorageBaseHandler(HttpBaseHandler):   
    #add init a processor
    """
    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        print ("-----get token:", token)
        i = ObjectStorageProcessorFac()
        self.p = i.create_processor(None, token)

        return self.p

    def get(self):
        pass
    """
    def __init__(self, application, request, **kwargs):
        super(ObjectStorageBaseHandler, self).__init__(application, request, **kwargs)
        token = self.request.headers["X-Auth-Token"]
        print ("-----get token:", token)
        i = ObjectStorageProcessorFac()
        self.p = i.create_processor(None, token)

        return self.p

    def get(self, tenant_id):
        containers = self.p.queryContainers()

        resp = []
        i = 0
        container = {}

        for c in containers:
            container["count"] = i
            container["bytes"] = c[""]
            container["name"] = c[""]
            i++
            resp.append(container)

        self.send_json(resp)


class ContainerHandler(ObjectStorageBaseHandler):
    def get(self, account, container):
        limit = self.get_argument("limit", None)
        marker = self.get_argument("marker", None)
        end_marker = self.get_argument("end_marker", None)
        prefix = self.get_argument("prefix", None)
        format = self.get_argument("format", None)
        delimiter = self.get_argument("delimiter", None)
        path = self.get_argument("path", None)

        objects = self.p.queryObjects(account, container, limit,
                marker, end_marker, prefix, format, delimiter, path)

        resp = [
            {
                "hash":o.hash,
                "last_modified":o.last_modified,
                "bytes":o.bytes,
                "name":o.name,
                "content_type":o.content_type
            }
            for o in objects
        ]

        self.send_json(resp)

    def put(self, account, container):
        x_container_read = self.get_header("X-Container-Read")
        x_container_write = self.get_header("X-Container-Write")
        x_container_sync_to = self.get_header("X-Container-Sync-To")
        x_container_sync_key = self.get_header("X-Container-Sync-Key")
        x_versions_location = self.get_header("X-Versions-Location")
        x_container_meta_name = self.get_header("X-Container-Meta-name")
        content_type = self.get_header("Content-Type")
        x_detect_content_type = self.get_header("X-Detect-Content-Type")
        x_container_meta_tempurl_key = self.get_header("X-Container-Meta-Tempurl-Key")
        x_container_meta_tempurl_key_2 = self.get_header("X-Container-Meta-Tempurl-Key-2")
        x_trans_id_extra = self.get_header("X-Trans-Id-Extra")

        self.p.createContainer(account, container,
                x_container_read,
                x_container_write,
                x_container_sync_to,
                x_container_sync_key,
                x_versions_location,
                x_container_meta_name,
                content_type,
                x_detect_content_type,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra)

    def delete(self, account, container):
        x_container_meta_tempurl_key = self.get_header("X-Container-Meta-Tempurl-Key")
        x_container_meta_tempurl_key_2 = self.get_header("X-Container-Meta-Tempurl-Key-2")
        x_trans_id_extra = self.get_header("X-Trans-Id-Extra")

        self.p.deleteContainer(account, container,
                x_container_meta_tempurl_key,
                x_container_meta_tempurl_key_2,
                x_trans_id_extra)

class ObjectHandler(ObjectStorageBaseHandler):
    def prepare(self, account, container, object_):
        #if http method is COPY, call self.copy()
        pass

    def put(self, account, container, object_):
        multipart_manifest = self.get_argument("multipart-manifest", None)
        temp_url_sig = self.get_argument("temp_url_sig", None)
        temp_url_expires = self.get_argument("temp_url_expires", None)
        filename = self.get_argument("filename", None)

        x_object_manifest = self.get_header("X-Object-Manifest")
        content_length = self.get_header("Content-Length")
        transfer_encoding = self.get_header("Transfer-Encoding")
        content_type = self.get_header("Content-Type")
        x_detect_content_type = self.get_header("X-Detect-Content-Type")
        x_copy_from = self.get_header("X-Copy-From")
        etag = self.get_header("ETag")
        content_disposition = self.get_header("Content-Disposition")
        content_encoding = self.get_header("Content-Encoding")
        x_delete_at = self.get_header("X-Delete-At")
        x_delete_after = self.get_header("X-Delete-After")
        x_object_meta_name = self.get_header("X-Object-Meta-name")
        if_none_match = self.get_header("If-None-Match")
        x_trans_id_extra = self.get_header("X-Trans-Id-Extra")

        self.p.createObject(account, container, object_,
                multipart_manifest,
                temp_url_sig,
                temp_url_expires,
                filename,
                x_object_manifest,
                content_length,
                transfer_encoding,
                content_type,
                x_detect_content_type,
                x_copy_from,
                etag,
                content_disposition,
                content_encoding,
                x_delete_at,
                x_delete_after,
                x_object_meta_name,
                if_none_match,
                x_trans_id_extra)

    def copy(self, account, container, object_):
        destination = self.get_header("Destination")
        content_type = self.get_header("Destination")
        content_encoding = self.get_header("Destination")
        content_disposition = self.get_header("Destination")
        x_object_meta_name = self.get_header("Destination")
        x_fresh_metadata = self.get_header("Destination")
        x_trans_id_extra = self.get_header("X-Trans-Id-Extra")

        if self.copyObject(account, container, object_,
                destination,
                content_type,
                content_encoding,
                content_disposition,
                x_object_meta_name,
                x_fresh_metadata,
                x_trans_id_extra):
            self.set_status(201)
        else:
            self.set_status(400)
            return

    def delete(self, account, container, object_):
        multipart_manifest = self.get_argument("multipart-manifest", None)
        x_trans_id_extra = self.get_header("X-Trans-Id-Extra")

        self.p.deleteObject(account, container, object_, multipart_manifest, x_trans_id_extra)
