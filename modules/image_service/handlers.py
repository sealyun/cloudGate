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
        limit = self.get_argument("limit", None)
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
            "images": [
                {
                    "status": i['Status'],
                    "name": i['ImageName'],
                    "tags": [],
                    "container_format": '',
                    "create_at": i['CreationTime'],
                    "disk_format": '',
                    "updated_at": '',
                    "visibility": i['IsSubscribed'],
                    "self": "/v2/images/" + i['ImageId'],
                    "min_disk": 0,
                    "protected": i['IsCopied'],
                    "id": i['ImageId'],
                    "file": "/v2/images/" + i['ImageId'] + "/file",
                    "checksum": None,
                    "owner": i['ImageOwnerAlias'],
                    "size": i['Size'],
                    "min_ram": None,
                    "schema": '',
                    "virtual_size": i['Size']
                }
                for i in images
            ]
        }

        self.send_json(resp)

    def post(self):
        image = json.loads(self.request.body)
        print(post)

        name = image.get("name")

        i = self.p.createImage(
            image["name"],
            image["container_format"],
            image["disk_format"],
            image["id"]
        )

        if not i:
            return

        resp = {
            "status": i.status,
            "name": i.name,
            "tags": i.tags,
            "container_format": i.container_format,
            "create_at": i.create_at,
            "size": i.size,
            "disk_format": i.disk_format,
            "updated_at": i.updated_at,
            "visibility": i.visibility,
            "locations": i.locations,
            "self": "/v2/images/" + i.id,
            "min_disk": i.min_disk,
            "protected": i.protected,
            "id": i.id,
            "file": "/v2/images/" + i.id + "/file",
            "checksum": i.checksum,
            "owner": i.owner,
            "virtual_size": i.virtual_size,
            "min_ram": i.min_ram,
            "schema": i.schema,
        }

        self.set_status(201)
        self.send_json(resp)


class ImageHandler(ImageBaseHandler):

    def get(self, image_id):
        i = self.p.queryImageId(image_id)
        if not i:
            return

        resp = {
            "status": i.status,
            "name": i.name,
            "tags": i.tags,
            "container_format": i.container_format,
            "create_at": i.create_at,
            "disk_format": i.disk_format,
            "updated_at": i.updated_at,
            "visibility": i.visibility,
            "self": "/v2/images/" + i.id,
            "min_disk": i.min_disk,
            "protected": i.protected,
            "id": i.id,
            "file": "/v2/images/" + i.id + "/file",
            "checksum": i.checksum,
            "owner": i.owner,
            "size": i.size,
            "min_ram": i.min_ram,
            "schema": i.schema,
            "virtual_size": i.virtual_size
        }

        self.send_json(resp)

    def patch(self, image_id):
        update_list = json.laods(self.request.body)
        #"op" "path" "value"

        i = updateImage(image_id, update_list)

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

    def delete(self, image_id):
        res = self.p.deleteImage(image_id)

        if res:
            self.set_status(204)
        else:
            self.set_status(403)


class ImageActionReactivateHandler(ImageBaseHandler):

    def post(self, image_id):
        i = self.p.reactivateImage(image_id)
        if i:
            self.set_status(204)
        else:
            return

        resp = {
            "status": i.status,
            "name": i.name,
            "tags": i.tags,
            "container_format": i.container_format,
            "create_at": i.create_at,
            "disk_format": i.disk_format,
            "updated_at": i.updated_at,
            "visibility": i.visibility,
            "self": "/v2/images/" + i.id,
            "min_disk": i.min_disk,
            "protected": i.protected,
            "id": i.id,
            "file": "/v2/images/" + i.id + "/file",
            "checksum": i.checksum,
            "owner": i.owner,
            "size": i.size,
            "min_ram": i.min_ram,
            "schema": i.schema,
            "virtual_size": i.virtual_size
        }

        self.send_json(resp)


class ImageActionDeactivateHandler(ImageBaseHandler):

    def post(self, image_id):
        i = self.p.deactivateImage(image_id)
        if i:
            self.set_status(204)
        else:
            return

        resp = {
            "status": i.status,
            "name": i.name,
            "tags": i.tags,
            "container_format": i.container_format,
            "create_at": i.create_at,
            "disk_format": i.disk_format,
            "updated_at": i.updated_at,
            "visibility": i.visibility,
            "self": "/v2/images/" + i.id,
            "min_disk": i.min_disk,
            "protected": i.protected,
            "id": i.id,
            "file": "/v2/images/" + i.id + "/file",
            "checksum": i.checksum,
            "owner": i.owner,
            "size": i.size,
            "min_ram": i.min_ram,
            "schema": i.schema,
            "virtual_size": i.virtual_size
        }

        self.send_json(resp)

# TODO need upload download binary file


class ImageFileHandler(ImageBaseHandler):

    def put(self, image_id):
        pass

    def get(self, image_id):
        pass
