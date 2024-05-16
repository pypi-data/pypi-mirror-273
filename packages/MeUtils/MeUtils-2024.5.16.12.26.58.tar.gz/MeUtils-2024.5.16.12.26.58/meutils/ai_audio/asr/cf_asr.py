#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : cf_asr
# @Time         : 2024/5/7 16:43
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.str_utils import chinese_convert

# curl https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/openai/whisper \
#   -X POST \
#   -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
#   --data-binary "@talking-llama.mp3"


cloudflare_account_id, api_key = os.getenv("CLOUDFLARE_API_TOKEN").split('-', maxsplit=1)

base_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run"

headers = {"Authorization": f"Bearer {api_key}"}

httpx_client = httpx.Client(base_url=base_url, follow_redirects=True, timeout=100, headers=headers)

file = open("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_audio/tts/demo.mp3", 'rb')
payload = {"file": (file.name, file)}


with timer('asr'):
    response = httpx_client.post(f"@cf/openai/whisper", files=payload)
    print(chinese_convert(bjson(response.json())))
