from handlers import *
from cloudGate.common.define import *

urls_v2_1 = [
    (COMPUTE_BASE_URL, ComputeBaseHandler),
    (COMPUTE_BASE_URL + r"/v2.1/(.*)/servers", ServersHandler),
    (COMPUTE_BASE_URL + r"/v2.1/(.*)/servers/detail", ServersDetailHandler),
    (COMPUTE_BASE_URL + r"/v2.1/(.*)/servers/(.*)", ServerHandler),
    (COMPUTE_BASE_URL + r"/v2.1/(.*)/servers/(.*)/action", ServerActionHandler),
]

#if we support other version api, use urls = urls_v2_1 + urls_other_version
urls = urls_v2_1
