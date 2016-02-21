from handlers import *
from cloudGate.common.define import *

urls_v2_1 = [
    (COMPUTE_BASE_URL, ComputeBaseHandler),
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers", ServersHandler), #/v2.1/{tenant_id}/servers
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers/detail", ServersDetailHandler), #/v2.1/{tenant_id}/servers/detail
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers/([^/]+)", ServerHandler), #/v2.1/tenant_id}/servers/{server_id}
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers/([^/]+)/action", ServerActionHandler), #/v2.1/{tenant_id}/servers/{server_id}/action
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers/([^/]+)/os-volume_attachments", ServerVolumeHandler), #/v2.1/{tenant_id}/servers/{server_id}/os-volume_attachments
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/servers/([^/]+)/os-volume_attachments/([^/]+)", VolumeAttachmentHandler), #/v2.1/{tenant_id}/servers/{server_id}/os-volume_attachments/{attachment_id}
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/flavors", FlavorsHandler),
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/flavors/detail", FlavorsDetailHandler),
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/flavors/([^/]+)", FlavorHandler),
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/flavors/([^/]+)", FlavorHandler),
    (COMPUTE_BASE_URL + r"/v2.1/([^/]+)/extensions", ExtensionsHandler),
]

#if we support other version api, use urls = urls_v2_1 + urls_other_version
urls = urls_v2_1
