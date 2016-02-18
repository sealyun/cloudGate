
import json
from tornado.gen import coroutine
from cloudGate.httpbase import HttpBaseHandler
from api_factory import ImageServiceProcessorFac


class ImageBaseHandler(HttpBaseHandler):

    def get_processor(self):
        token = self.request.headers["X-Auth-Token"]
        print("-----get token:", token)
        i = ImageServiceProcessorFac()
        self.p = i.create_processor(None, token)

        return self.p

    def get(self):
        pass


class ImagesHandler(ImageBaseHandler):

    def get(self):
        limit = self.get_argument("limit", 1024)
        marker = self.get_argument("marker", None)
        name = self.get_argument("name", None)
        visibility = self.get_argument("visibility", None)
        member_status = self.get_argument("member_status", None)
        owner = self.get_argument("owner", None)
        status = self.get_argument("status", None)
        size_min = self.get_argument("size_min", None)
        size_max = self.get_argument("size_max", None)
        sort_key = self.get_argument("sort_key", None)
        sort_dir = self.get_argument("sort_dir", None)
        sort = self.get_argument("sort", None)
        tag = self.get_argument("tag", None)

        self.get_processor()
        images = self.p.queryImages(limit, marker, name, visibility, member_status, owner, status,
                                    size_min, size_max, sort_key, sort_dir, sort, tag)
        resp = {
            "images": [{
                "uri": "",
                "name": i['ImageName'],
                "disk_format": "",
                "container_format": "",
                "size": i['Size'],
                "checksum": "c2e5db72bd7fd153f53ede5da5a06de3",
                "created_at": i["CreationTime"],
                "updated_at": "",
                "deleted_at": "",
                "status": "active" if i["Status"] == "Available" else "",
                "is_public": i['IsSubscribed'],
                "min_ram": None,
                "min_disk": None,
                "owner": i['ImageOwnerAlias'],
                "properties": {
                    "distro": i["OSName"],
                },
                "id": i["ImageId"],
                "protected": False,
            } for i in images
            ]
        }

        self.send_json(resp)

    def post(self):
        self.get_processor()
        name = self.request.headers.get('name')
        container_format = self.request.headers.get('container_format')
        disk_format = self.request.headers.get('disk_format')
        xrid = self.request.headers.get('X-Image-Meta-Property-Ramdisk_id')
        xkid = self.request.headers.get('X-Image-Meta-Property-Kernel_id')
        sid = self.request.headers.get('X-Glance-Api-Copy-From')
        # ('self.request', HTTPServerRequest(protocol='http', host='121.199.9.187:8085', method='POST', uri='/image_service/v1/images', version='HTTP/1.1', remote_ip='121.199.9.187', headers={'Content-Length': '0', 'Host': '121.199.9.187:8085', 'X-Auth-Token': 'adminadmin', 'Accept-Encoding': 'gzip, deflate', 'X-Image-Meta-Container_format': 'aki', 'Content-Type': 'application/octet-stream', 'X-Image-Meta-Property-Architecture': '111', 'Accept': '*/*', 'X-Image-Meta-Protected': 'True', 'X-Image-Meta-Property-Ramdisk_id': 'win2012_64_dataCtr_R2_en_40G_alibase_20150429.vhd', 'Connection': 'keep-alive', 'X-Image-Meta-Min_disk': '1', 'X-Image-Meta-Is_public': 'False', 'X-Image-Meta-Min_ram': '1', 'X-Image-Meta-Property-Kernel_id': 'coreos681_64_20G_aliaegis_20150618.vhd', 'User-Agent': 'python-glanceclient', 'X-Image-Meta-Property-Description': '111', 'X-Image-Meta-Disk_format': 'aki', 'X-Image-Meta-Name': '111'}))
        i = self.p.createImage(name, container_format, disk_format, sid)
        resp = {
            "image": {
                "status": "queued",
                "name": "Ubuntu",
                "tags": [],
                "container_format": "bare",
                "created_at": "2015-11-29T22:21:42Z",
                "size": None,
                "disk_format": "raw",
                "updated_at": "2015-11-29T22:21:42Z",
                "visibility": "private",
                "locations": [],
                "location": "http://www.baidu.com",
                "self": "/v2/images/b2173dd3-7ad6-4362-baa6-a68bce3565cb",
                "min_disk": 0,
                "protected": False,
                "id": "b2173dd3-7ad6-4362-baa6-a68bce3565cb",
                "file": "/v2/images/b2173dd3-7ad6-4362-baa6-a68bce3565cb/file",
                "checksum": None,
                "owner": "bab7d5c60cd041a0a36f7c4b6e1dd978",
                "virtual_size": None,
                "min_ram": 0,
                "schema": "/v2/schemas/image",
            }
        }

        self.set_status(202)
        self.send_json(resp)


class ImageHandler(ImageBaseHandler):

    def get(self, image_id):
        self.set_header('Content-Type', 'application/json')
        self.get_processor()
        i = self.p.queryImageId(image_id)
        if not i:
            return
        resp = {
            "images": [
                {
                    "uri": "",
                    "name": i['ImageName'],
                    "disk_format": "",
                    "container_format": "",
                    "size": i['Size'],
                    "checksum": "c2e5db72bd7fd153f53ede5da5a06de3",
                    "created_at": i["CreationTime"],
                    "updated_at": "",
                    "deleted_at": "",
                    "status": "active" if i["Status"] == "Available" else "",
                    "is_public": i['IsSubscribed'],
                    "min_ram": None,
                    "min_disk": None,
                    "owner": i['ImageOwnerAlias'],
                    "properties": {
                        "distro": i["OSName"],
                    },
                    "id": i["ImageId"],
                }
            ]
        }
        self.send_json(resp)

    def head(self, image_id):
        self.set_header('Content-Type', 'application/json')
        self.get_processor()
        i = self.p.queryImageId(image_id)
        if not i:
            return
        resp = {
            "images": [
                {
                    "uri": "",
                    "name": i['ImageName'],
                    "disk_format": "",
                    "container_format": "",
                    "size": i['Size'],
                    "checksum": "c2e5db72bd7fd153f53ede5da5a06de3",
                    "created_at": i["CreationTime"],
                    "updated_at": "",
                    "deleted_at": "",
                    "status": "active" if i["Status"] == "Available" else "",
                    "is_public": i['IsSubscribed'],
                    "min_ram": None,
                    "min_disk": None,
                    "owner": i['ImageOwnerAlias'],
                    "properties": {
                        "distro": i["OSName"],
                    },
                    "id": i["ImageId"],
                }
            ]
        }
        for k, v in resp['images'][0].items():
            try:
                self.set_header(k, v)
            except:
                pass
        self.send_json(resp)

    def patch(self, image_id):
        self.get_processor()
        update_list = json.laods(self.request.body)
        #"op" "path" "value"
        if update_list['op'] == 'replace' and update_list['path'] == 'ImageName':
            i = self.p.updateImage(image_id, update_list['value'])

            resp = {
                "id": i.id,
                "name": i.name,
                "status": i.status,
                "visibility": i.visibility,
                "size": i.size,
                "checksum": i.checksum,
                "tags": i.tags,
                "create_at": i.create_at,
                "updated_at": i.updated_at,
                "self": "/v2/images/" + i.id,
                "file": "/v2/images/" + i.id + "/file",
                "schema": i.schema,
                "owner": i.owner,
                "min_ram": i.min_ram,
                "min_disk": i.min_disk,
                "disk_format": i.disk_format,
                "virtual_size": i.virtual_size
                # "container_format":i.container_format,
            }
            self.send_json(resp)
        return

    def delete(self, image_id):
        self.get_processor()
        res = self.p.deleteImage(image_id)
        self.set_status(204)


class ImageActionReactivateHandler(ImageBaseHandler):

    def post(self, image_id):
        self.get_processor()
        i = self.p.reactivateImage(image_id)
        if i:
            self.set_status(204)
        else:
            return


class ImageActionDeactivateHandler(ImageBaseHandler):

    def post(self, image_id):
        self.get_processor()
        i = self.p.deactivateImage(image_id)
        if i:
            self.set_status(204)
        else:
            return

# TODO need upload download binary file


class ImageFileHandler(ImageBaseHandler):

    def put(self, image_id):
        self.get_processor()
        pass

    def get(self, image_id):
        self.get_processor()
        pass
