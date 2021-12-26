# -*- coding:UTF-8 -*-

import requests
import time

import user_config
from urllib.parse import quote
import random

requests.packages.urllib3.disable_warnings()

default_timeout = 10


def sleep():
    sleep_time = random.random() * default_timeout + default_timeout
    time.sleep(sleep_time)


def contact_all_geeks():
    geek_names = []
    try:
        for query in user_config.lagou_query_list:
            page = 1
            recommender_geeks = get_recommenders(page, query)
            while len(recommender_geeks) > 0 and len(geek_names) <= 60:
                for geek in recommender_geeks:
                    if geek is None or 'userId' not in geek or 'name' not in geek:
                        continue
                    geek_name = geek['name']
                    geek_id = geek['userId']
                    get_chat_info(geek_id)
                    create_session(geek_id)
                    geek_names.append(geek_name)
                page += 1
                recommender_geeks = get_recommenders(page)

        # page = 1
        # recommender_geeks = get_newest(page)
        # while len(recommender_geeks) > 0:
        #     for geek in recommender_geeks:
        #         if geek is None or 'userId' not in geek or 'name' not in geek:
        #             continue
        #         geek_name = geek['name']
        #         geek_id = geek['userId']
        #         get_chat_info(geek_id)
        #         create_session(geek_id)
        #         geek_names.append(geek_name)
        #     page += 1
        #     recommender_geeks = get_newest(page)

        # page = 1
        # recommender_geeks = get_visitors(page)
        # while len(recommender_geeks) > 0:
        #     for geek in recommender_geeks:
        #         if geek is None or 'userId' not in geek or 'name' not in geek:
        #             continue
        #         geek_name = geek['name']
        #         geek_id = geek['userId']
        #         get_chat_info(geek_id)
        #         create_session(geek_id)
        #         geek_names.append(geek_name)
        #     page += 1
        #     recommender_geeks = get_visitors(page)
    except Exception as e:
        print(e)
    return geek_names


def get_recommenders(page, query=''):
    url = "https://easy.lagou.com/talent/rec/v2/{}.json?positionId={}&showId={}&notSeen=false&strongly=false&isFilterChat=1&{}tagNames={}".format(
        page, user_config.lagou_position_id, user_config.lagou_show_id, query, quote(user_config.lagou_condition))

    recommenders = []
    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '5efe26c4-5fe1-4d27-8164-98aa04520d41',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': '29836d03-2580-4aec-a83f-1eb1fc0f47fd',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/talent/index.htm?positionId=9288532&showId=46c65c609c464d3baa98510ce277d297&notSeen=false&strongly=false&tab=rec&pageNo=1',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return recommenders
        print(response)
        json_data = response.json()
        if json_data is None:
            return recommenders
        if 'content' not in json_data or 'data' not in json_data['content'] \
                or 'page' not in json_data['content']['data'] or 'result' not in json_data['content']['data']['page']:
            return recommenders
        recommenders.extend(json_data['content']['data']['page']['result'])
    except Exception as e:
        print(e)

    return recommenders


def get_newest(page):
    url = "https://easy.lagou.com/talent/newest/v2/{}.json?positionId={}&showId=".format(
        page, user_config.lagou_position_id)
    recommenders = []
    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '6dc790e8-bc67-4589-9519-113a9589c32c',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'bbbfbc8a-2d32-4389-bc33-20f3caf7a61f',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/talent/index.htm?positionId=9288532&showId=&tab=newest&pageNo=1',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return recommenders
        json_data = response.json()
        if json_data is None:
            return recommenders
        if 'content' not in json_data or 'data' not in json_data['content'] \
                or 'page' not in json_data['content']['data'] or 'result' not in json_data['content']['data']['page']:
            return recommenders
        recommenders.extend(json_data['content']['data']['page']['result'])
    except Exception as e:
        print(e)

    return recommenders


def get_visitors(page):
    url = "https://easy.lagou.com/talent/inspect/{}.json?positionId={}&showId=".format(page,
                                                                                       user_config.lagou_position_id)

    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': 'a7e11714-7de7-4420-961b-a23c4ccb3123',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'ecf5bc96-38ba-4230-8ba9-0d31f5c5e018',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/talent/index.htm?positionId=9288532&showId=&tab=inspect&pageNo=1',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    recommenders = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return recommenders
        json_data = response.json()
        if json_data is None:
            return recommenders
        if 'content' not in json_data or 'data' not in json_data['content'] \
                or 'page' not in json_data['content']['data'] or 'result' not in json_data['content']['data']['page']:
            return recommenders
        recommenders.extend(json_data['content']['data']['page']['result'])
    except Exception as e:
        print(e)

    return recommenders


def get_chat_info(geek_id):
    url = "https://easy.lagou.com/im/chat/colleagueChatInfo.json?cUserId={}&positionId={}".format(
        geek_id, user_config.lagou_chat_position_id)

    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '6dc790e8-bc67-4589-9519-113a9589c32c',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'bbbfbc8a-2d32-4389-bc33-20f3caf7a61f',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/talent/index.htm?positionId=9288532&showId=46c65c609c464d3baa98510ce277d297&notSeen=false&strongly=false&tab=rec&pageNo=2&show_id=46c65c609c464d3baa98510ce277d297',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        print(response)

    except Exception as e:
        print(e)


def create_session(geek_id):
    url = "https://easy.lagou.com/im/session/batchCreate/{}.json".format(geek_id)

    payload = "greetingId={}&positionId={}&inviteDeliver=true".format(user_config.lagou_greeting_id,
                                                                      user_config.lagou_chat_position_id)
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '6dc790e8-bc67-4589-9519-113a9589c32c',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'bbbfbc8a-2d32-4389-bc33-20f3caf7a61f',
        'origin': 'https://easy.lagou.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/talent/index.htm?positionId=9288532&showId=46c65c609c464d3baa98510ce277d297&notSeen=false&strongly=false&tab=rec&pageNo=2&show_id=46c65c609c464d3baa98510ce277d297',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
        print(response)

    except Exception as e:
        print(e)


def get_chat_list(page):
    url = "https://easy.lagou.com/im/session/list.json?pageNo={}&pageSize=10&createBy=0&unReadOnly=0&resumeState=1&isNewChat=true".format(
        page)
    chats = []
    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'traceparent': '00-d308b86e913146742351df534980b478-c96bb7fb0a536e24-01',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/im/chat/index.htm',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return chats
        json_data = response.json()
        if json_data is None or 'content' not in json_data or 'rows' not in json_data['content']:
            return chats
        return json_data['content']['rows']
    except Exception as e:
        print(e)
    return chats


def send_invite(geek_id):
    url = "https://easy.lagou.com/im/chat/send/invite/{}.json".format(geek_id)

    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'content-length': '0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': 'a7e11714-7de7-4420-961b-a23c4ccb3123',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'ecf5bc96-38ba-4230-8ba9-0d31f5c5e018',
        'origin': 'https://easy.lagou.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/im/chat/index.htm',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    sleep()
    print(response.text)


def del_msg(geek_id):
    url = "https://easy.lagou.com/im/session/delete/{}.json".format(geek_id)

    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'content-length': '0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': 'a7e11714-7de7-4420-961b-a23c4ccb3123',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': 'ecf5bc96-38ba-4230-8ba9-0d31f5c5e018',
        'origin': 'https://easy.lagou.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/im/chat/index.htm',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    sleep()
    print(response.text)


def ask_resume():
    page = 0
    all_chats = []
    chats = get_chat_list(page)
    geek_names = []
    while len(chats) > 0:
        all_chats.extend(chats)
        page += 1
        chats = get_chat_list(page)

    for chat in all_chats:
        if chat is None or 'sessionId' not in chat:
            continue
        geek_id = chat['sessionId']
        send_invite(geek_id)
        del_msg(geek_id)
        if 'name' in chat:
            geek_names.append(chat['name'])
    return geek_names


def get_cv_list(page):
    url = "https://easy.lagou.com/can/new/list.json"
    resume_list = []
    payload = "can=true&pageSize=20&stage=NEW&needQueryAmount=true&pageNo={}&famousCompany=0".format(page)
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '1e9c7604-a26a-4a0c-bae5-3360c820553c',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': '3a5fb402-c81a-4f1f-ba9c-93094f108d31',
        'origin': 'https://easy.lagou.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/can/new/index.htm?can=true&famousCompany=0&needQueryAmount=true&pageNo=1&pageSize=20&stage=NEW',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return resume_list
        json_data = response.json()
        if json_data is None:
            return resume_list
        if 'content' not in json_data or 'rows' not in json_data['content']:
            return resume_list
        resume_list.extend(json_data['content']['rows'])
    except Exception as e:
        print(e)
    return resume_list


def download_resume(resume):
    if 'id' not in resume:
        return None
    resume_id = resume['id']
    file_name = '{}.pdf'.format(resume_id)
    if 'candidateName' in resume:
        file_name = '{}-{}.pdf'.format(resume['candidateName'], time.time())
    url = "https://easy.lagou.com/resume/download.htm?resumeId={}&preview=2".format(resume_id)

    payload = {}
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://easy.lagou.com/can/new/index.htm',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None or response.content is None:
            return None
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name
    except Exception as e:
        print(e)
    return None


def pass_cv(resume):
    if 'id' not in resume:
        return
    resume_id = resume['id']

    url = "https://easy.lagou.com/can/batch/toStageLink.json"

    payload = "resumeIds={}".format(resume_id)
    headers = {
        'authority': 'easy.lagou.com',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'x-anit-forge-code': '48f9c451-4776-45c0-9d7e-1f29c804541b',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'x-anit-forge-token': '358498d0-8263-4697-bc4c-ee033f9b3f3f',
        'origin': 'https://easy.lagou.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://easy.lagou.com/can/new/index.htm?can=true&famousCompany=0&needQueryAmount=true&pageNo=1&pageSize=20&stage=NEW',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.lagou_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
    except Exception as e:
        print(e)
