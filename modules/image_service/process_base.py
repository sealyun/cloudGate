class ImageServiceProcessorBase:

    def queryImages(self, limit, marker, name, visibility, member_status, owner, status,
                    size_min, size_max, sort_key, sort_dir, sort, tag):
        pass

    def createImage(self, container_format, disk_format, name, id):
        pass

    def queryImageId(self, image_id):
        pass

    def deleteImage(self, image_id):
        pass

    def updateImage(self):
        pass

    def reactivateImage(self):
        pass
