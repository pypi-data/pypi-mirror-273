#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ark
# @Time         : 2024/5/15 15:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://www.volcengine.com/product/doubao?utm_source=5&utm_medium=sembaidu&utm_term=sem_baidu_damoxing_doubao_1&utm_campaign=vgbdpcztn797661721486&utm_content=damoxing_doubao
import os

from meutils.pipe import *
import volcenginesdkcore
import volcenginesdkark
from pprint import pprint
from volcenginesdkcore.rest import ApiException

endpoint_map = {
    "doubao-lite-128k": "ep-20240515062839-jsvtz",
    "doubao-lite-32k": "ep-20240515062431-rkhfp",
    "doubao-lite-4k": "ep-20240515062545-nnq8b",

    "doubao-pro-128k": "ep-20240515073409-dlpqp",
    "doubao-pro-32k": "ep-20240515073434-s4skk",
    "doubao-pro-4k": "ep-20240515073524-xj4m2",  # fc

    "doubao-embedding": "ep-20240516005609-9c9pq"
}

if __name__ == '__main__':
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = os.getenv("ARK_ACCESS_KEY")
    configuration.sk = os.getenv("ARK_SECRET_ACCESS_KEY")
    configuration.region = "cn-beijing"
    # set default configuration
    volcenginesdkcore.Configuration.set_default(configuration)

    # use global default configuration
    api_instance = volcenginesdkark.ARKApi()

    # for endpoint in endpoint_map.values():
    get_api_key_request = volcenginesdkark.GetApiKeyRequest(
        duration_seconds=30 * 24 * 3600,
        resource_type="endpoint",
        resource_ids=list(endpoint_map.values()),
        # resource_ids=["ep-20240515062545-nnq8b"]
    )




    try:
        resp = api_instance.get_api_key(get_api_key_request)
        pprint(resp)
    except ApiException as e:
        print("Exception when calling api: %s\n" % e)


