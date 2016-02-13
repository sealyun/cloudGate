# -*- coding:utf-8 -*-
from httpbase import *

MODULES_SWITCH = {
    "identity": 1,
    "mould": 0,
    "block_storage":0,
    "clustering":0,
    "compute":0,
    "data_processing":0,
    "database_service":0,
    "image_service":0,
    "networking":0,
    "object_storage":0,
    "orchestration":0,
    "shared_file_systems":0,
    "telemetry":0,
}

URL_SETTINGS = []

if MODULES_SWITCH["identity"]:
    from cloudGate.modules.identity.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["mould"]:
    from cloudGate.modules.mould.url import urls 

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["block_storage"]:
    from cloudGate.modules.block_storage.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["clustering"]:
    from cloudGate.modules.clustering.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["compute"]:
    from cloudGate.modules.compute.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["data_processing"]:
    from cloudGate.modules.data_processing.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["database_service"]:
    from cloudGate.modules.database_service.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["image_service"]:
    from cloudGate.modules.image_service.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["networking"]:
    from cloudGate.modules.networking.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["object_storage"]:
    from cloudGate.modules.object_storage.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["orchestration"]:
    from cloudGate.modules.orchestration.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["shared_file_systems"]:
    from cloudGate.modules.shared_file_systems.url import urls

    URL_SETTINGS = URL_SETTINGS + urls

if MODULES_SWITCH["telemetry"]:
    from cloudGate.modules.telemetry.url import urls

    URL_SETTINGS = URL_SETTINGS + urls
