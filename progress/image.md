Image
对应ECS的镜像API


GET
/v2/images
List images
(Since Image API v2.0) Lists public virtual machine (VM) images.
 
detail
POST
/v2/images
Create image
(Since Image API v2.0) Creates a virtual machine (VM) image.
 
detail
GET
/v2/images/​{image_id}​
Show image details
(Since Image API v2.0) Shows details for an image.
 
detail
PATCH
/v2/images/​{image_id}​
Update image
(Since Image API v2.0) Updates an image.
 
detail
DELETE
/v2/images/​{image_id}​
Delete image
(Since Image API v2.0) Deletes an image.
 
detail
POST
/v2/images/​{image_id}​/actions/reactivate
Reactivate image
(Since Image API v2.0) Reactivates an image.
 
detail
POST
/v2/images/​{image_id}​/actions/deactivate
Deactivate image
(Since Image API v2.0) Deactivates an image.
 
detail
Image data
Uploads and downloads raw image data.
PUT
/v2/images/​{image_id}​/file
Upload binary image data
(Since Image API v2.0) Uploads binary image data.
 
detail
GET
/v2/images/​{image_id}​/file
Download binary image data
(Since Image API v2.0) Downloads binary image data.

