#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2024/5/6 08:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd

from meutils.pipe import *


def get_app_access_token():
    payload = {
        "app_id": os.getenv("FEISHU_APP_ID"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    }
    response = httpx.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
        json=payload,
        timeout=30,
    )
    return response.json().get("app_access_token")


def get_spreadsheet_values(spreadsheet_token, sheet_id):
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}"

    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    return response.json()


def create_document(title: str = "一篇新文档🔥", folder_token: Optional[str] = None):
    payload = {
        "title": title,
        "folder_token": folder_token,
    }

    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.post(url, headers=headers, timeout=30, json=payload)
    return response.json()


def get_doc_raw_content(document_id: str = "BxlwdZhbyoyftZx7xFbcGCZ8nah"):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/raw_content"
    headers = {
        "Authorization": f"Bearer {get_app_access_token()}"
    }
    response = httpx.get(url, headers=headers, timeout=30)
    return response.json()


if __name__ == '__main__':
    # print(get_app_access_token())
    # print(get_spreadsheet_values("Qy6OszlkIhwjRatkaOecdZhOnmh", "0f8eb3"))
    pprint(get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "Y9oalh"))
    # pd.DataFrame(
    #     get_spreadsheet_values("Bmjtst2f6hfMqFttbhLcdfRJnNf", "79272d").get('data').get('valueRange').get('values'))

    # print(get_doc_raw_content("TAEFdXmzyobvgUxKM3lcLfc2nxe"))
    # print(create_document())
    # "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=79272d"
