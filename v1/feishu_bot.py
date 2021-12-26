# -*- coding:UTF-8 -*-

import json
import requests

import user_config

requests.packages.urllib3.disable_warnings()


def send_msg(msg, index=0):
    i_token = get_tenant_access_token()
    send_message(i_token, msg, index)


def send_message(token, msg, index):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=email"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    text_msg = {
        'text': msg
    }
    simple_info = user_config.personal_info_list[index % len(user_config.personal_info_list)]
    req_body = {
        "receive_id": simple_info['email'],
        "content": json.dumps(text_msg),
        "msg_type": "text"
    }

    data = bytes(json.dumps(req_body), encoding='utf8')
    try:
        response = requests.request("POST", url, headers=headers, data=data, verify=False)
        print(response)
    except Exception as e:
        print(e)
        return


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    req_body = {
        "app_id": user_config.APP_ID,
        "app_secret": user_config.APP_SECRET
    }

    data = bytes(json.dumps(req_body), encoding='utf8')

    try:
        response = requests.request("POST", url, headers=headers, data=data, verify=False)
        print(response)
        if response is None:
            return ""
        json_data = response.json()
        if json_data is None:
            return ""
        if 'code' not in json_data or json_data['code'] != 0:
            return ""
        if 'tenant_access_token' not in json_data:
            return ""
        return json_data['tenant_access_token']
    except Exception as e:
        print(e)
        return ""


def send_card(receive_id, content):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    i_token = get_tenant_access_token()
    req_body = {
        "receive_id": "{}".format(receive_id),
        "content": json.dumps(content),
        "msg_type": "interactive"
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + i_token
    }
    data = bytes(json.dumps(req_body), encoding='utf8')
    response = requests.request("POST", url, headers=headers, data=data)

    print(response.text)


if __name__ == '__main__':
    i = get_tenant_access_token()
    send_msg('你好')
