#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : keys4openai
# @Time         : 2024/5/14 16:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
1. 如果有需要增加tokens计算，可放大
2. 平滑+前后置内容
3. 淘汰策略+轮询策略
    前置淘汰
    后置淘汰：根据具体错误
4. 统计信息
5. 日志监控
"""

from meutils.pipe import *
from openai import AsyncClient
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


# np.random.choice()


class PollKeys(object):  # 轮询

    def __init__(self, provider='kimi'):
        self.provider = provider
        self.base_url = f"https://any2chat.chatfire.cn/{self.provider}"

    @classmethod
    def get_next_api_key(cls, provider):
        """轮询"""

        self = cls(provider=provider)
        while True:
            if api_key := r.lpop(self.provider):  # 左边值放在右边
                r.rpush(self.provider, api_key)
                # r.incr(f'api_key_count:{api_key}')  # 增加计数器
                return api_key

    @diskcache(location='check_api_key_cache', ttl=1 * 60, ignore=['self'])
    def check_api_key(self, api_key):
        """定时检测：半小时检测一遍"""
        logger.debug("@@@@@@@@2")
        payload = {
            "token": api_key  # "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9..."
        }
        response = httpx.Client(base_url=self.base_url).post("/token/check", json=payload)
        return response.json()

    def update_api_keys(self, api_keys):
        """定时更新&空闲更新
        1、 通过飞书更新keys
        2、检测key
        3、更新key
        """

        r.delete(self.provider)
        r.rpush(self.provider, *filter(self.check_api_key, api_keys))

    def get_api_keys(self):
        """从飞书"""
        return ['api_key-1', 'api_key-2', 'api_key-3']


if __name__ == '__main__':
    print(str(PollKeys().check_api_key('')))
