#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis
# @Time         : 2024/3/26 11:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import os
# from redis import Redis
from redis.asyncio import Redis

if REDIS_URL := os.getenv("REDIS_URL"):
    redis_aclient = Redis.from_url(REDIS_URL)
else:
    redis_aclient = Redis()

if __name__ == '__main__':
    from meutils.pipe import *

    print(arun(redis_aclient.get("test")))

    # print(type(redis_aclient.get("test")))
