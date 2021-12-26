# -*- coding:UTF-8 -*-
import json
import os
import time

import requests
from urllib.parse import quote, unquote

import user_config
import random

requests.packages.urllib3.disable_warnings()
default_timeout = 3


def sleep():
    sleep_time = random.random() * default_timeout + default_timeout
    time.sleep(sleep_time)


def get_all_jobs_from_remote():
    offset = 0
    jobs = []
    maimai_jobs = get_jobs(offset)
    while len(maimai_jobs) > 0:
        jobs.extend(maimai_jobs)
        offset += 1
        maimai_jobs = get_jobs(offset)
    with open(file=user_config.maimai_job_file, mode='w', encoding='utf-8')as f_w:
        json.dump(jobs, f_w)
    return jobs


def get_all_jobs_from_cache():
    jobs = []
    with open(file=user_config.maimai_job_file, mode='r', encoding='utf-8')as f_r:
        jobs = json.load(f_r)
    return jobs


def get_jobs(offset):
    jobs = []
    url = "https://maimai.cn/api/ent/job/list?channel=www&page={}&version=1.0.0".format(offset)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/positions/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return None
        json_data = response.json()
        if json_data is None:
            return None
        if 'data' not in json_data or 'list' not in json_data['data']:
            return jobs
        jobs.extend(json_data['data']['list'])
        return jobs
    except Exception as e:
        print(e)
        return jobs


def open_job(ejid):
    url = "https://maimai.cn/api/ent/job/open?channel=www&ejid={}&version=1.0.0".format(ejid)
    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/positions/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}

    try:
        requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
    except Exception as e:
        print(e)
    return


def close_job(ejid):
    if ejid in user_config.maimai_ignore_ejid:
        return
    url = "https://maimai.cn/api/ent/job/close?channel=www&ejid={}&version=1.0.0".format(ejid)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/positions/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie
    }
    try:
        requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
    except Exception as e:
        print(e)
        return
    return


def update_job(job_detail, ejid):
    url = "https://maimai.cn/sdk/jobs/publish_job/update_job?u={}".format(user_config.maimai_uid)

    payload = 'appid=2&ejid={}&infos={}&u={}'.format(ejid, quote(json.dumps(job_detail)), user_config.maimai_uid)
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://maimai.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/positions/add/jGNhBwJTgPo0jhrFLnieTw',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


def add_job(job_detail):
    url = "https://maimai.cn/sdk/jobs/publish_job/add_job?u={}".format(user_config.maimai_uid)
    payload = 'appid=2&infos={}&u={}'.format(quote(json.dumps(job_detail)), user_config.maimai_uid)
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://maimai.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/positions/add',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
        print(response)
    except Exception as e:
        print(e)
    return


def get_msg(offset):
    url = "https://maimai.cn/groundhog/msg/v5/get_msg?u={}&channel=web_im&version=5.0.2&_csrf={}&_csrf_token={}&ver_code=web_1&push_permit=1&appid=1&count=100&page={}".format(
        user_config.maimai_uid, user_config.maimai_pc_csrf, user_config.maimai_pc_csrf_token, offset)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/chat?fr=ent&target=',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    msg_list = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return msg_list
        json_data = response.json()
        if json_data is msg_list:
            return None
        if 'messages' not in json_data:
            return msg_list
        msg_list.extend(json_data['messages'])

        return msg_list

    except Exception as e:
        print(e)
        return msg_list


def del_msg(msg_id):
    url = "https://maimai.cn/groundhog/msg/v5/del_msg?u={}&channel=web_im&version=5.0.2&_csrf={}&_csrf_token={}&ver_code=web_1&push_permit=1&appid=1&mid={}".format(
        user_config.maimai_uid, user_config.maimai_pc_csrf, user_config.maimai_pc_csrf_token, msg_id)
    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/chat?fr=ent&target=',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
    except Exception as e:
        print(e)
        return


def collect_cv(page):
    url = "https://maimai.cn/jobs/b/resume_handle?channel=www&count=20&ejid=&is_return_total=true&jsononly=1&page={}&rtype=1&version=4.0.0".format(
        page)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/resumes/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}

    resume_list = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return None
        json_data = response.json()
        if json_data is None:
            return resume_list
        if 'data' not in json_data or 'resume_list' not in json_data['data']:
            return resume_list
        resume_list.extend(json_data['data']['resume_list'])
        return resume_list
    except Exception as e:
        print(e)
        return resume_list


def down_load_cv(web_uid, file_name, e_jid):
    url = "https://maimai.cn/down_resume?webuid={}&filename={}&ejid={}".format(web_uid, file_name, e_jid)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://maimai.cn/jobs/jobs_resume?webuid={}&ejid={}&fr=webResume&mobile=1&is_from_pc=true'.format(
            web_uid, e_jid),
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return file_name
        with open(file_name, 'wb') as f:
            f.write(response.content)
        disposition = response.headers['Content-Disposition']
        if disposition is None:
            return file_name
        to_split = disposition.split("''")
        if to_split is None or len(to_split) < 2:
            return file_name
        new_file_name = unquote(to_split[1]).replace('/', '-')
        os.rename(file_name, new_file_name)
        return new_file_name
    except Exception as e:
        print(e)
        return file_name


def pass_cv(ejid, u2_id):
    url = "https://maimai.cn/sdk/jobs/jobs_resume_process?channel=www&ejid={}&pass_primary_filter=1&u={}&uid2={}&version=1.0.0".format(
        ejid, user_config.maimai_uid, u2_id)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/recruit/resumes/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}

    try:
        requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
    except Exception as e:
        print(e)


def ask_cv(msg_id, u2_id):
    url = "https://maimai.cn/groundhog/job/v3/direct/resume_req?mid={}&u2={}&ejid=0cIZWQkEjTQPyecjMBn2lA&btn=bar&u={}&channel=www&version=4.0.0&_csrf={}&_csrf_token={}".format(
        msg_id, u2_id, user_config.maimai_uid, user_config.maimai_pc_csrf, user_config.maimai_pc_csrf_token)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/chat?fr=ent&target=',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        print(response)
        return
    except Exception as e:
        print(e)
        return


def enter_msg(msg_id):
    url = "https://maimai.cn/groundhog/msg/v5/enter_msg?mid={}&u={}&channel=web_im&version=5.2.18&_csrf={}&_csrf_token={}&ver_code=web_1&push_permit=1&appid=1".format(
        msg_id, user_config.maimai_uid, user_config.maimai_pc_csrf, user_config.maimai_pc_csrf_token)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/chat?fr=ent&target=',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return False
        json_data = response.json()
        if json_data is None:
            return False
        if 'btn_list' not in json_data or json_data['btn_list'] is None:
            return False
        btn_list = json_data['btn_list']
        for btn in btn_list:
            if btn is None or 'events' not in btn or btn['events'] is None:
                continue
            events = btn['events']
            for event in events:
                if event is None or 'event_key' not in event:
                    continue
                if event['event_key'] == 'jobs_d_o_hr_bar_send_resume_click':
                    return False
        return True
    except Exception as e:
        print(e)
        return False


def exchange_mobile(msg_id, u_id):
    url = "https://maimai.cn/groundhog/job/v3/direct/mobile_req?mid={}&u2={}&ejid=0cIZWQkEjTQPyecjMBn2lA&btn=bar&u={}&channel=www&version=4.0.0&_csrf={}&_csrf_token={}".format(
        msg_id, u_id, user_config.maimai_uid, user_config.maimai_pc_csrf, user_config.maimai_pc_csrf_token)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/chat?fr=ent&target=',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        requests.request("GET", url, headers=headers, data=payload, verify=False)
        sleep()
        return
    except Exception as e:
        print(e)
        return


def get_feeds(page):
    feeds_list = []
    url = "https://open.taou.com/maimai/feed/v5/user?access_token={}&appid=4&channel=AppStore&density=3&device=iPhone11%2C6&launch_uuid={}&net=wifi&push_permit=0&rn_version=0.63.2&screen_height=2688&screen_width=1242&session_uuid={}&sm_did={}&u={}&udid={}&vc=14.6&version=6.0.80&webviewUserAgent={}&before_id=0&no_interact_feed=1&only_realname_status=1&page={}&rn=1&u2=37904819&use_native_net=1&isPost=0".format(
        user_config.maimai_mobile_access_token, user_config.maimai_mobile_launch_uuid,
        user_config.maimai_mobile_session_uuid, user_config.maimai_mobile_sm_did, user_config.maimai_uid,
        user_config.maimai_mobile_web_view_user_agent,
        user_config.maimai_mobile_udid, page)

    payload = {}
    headers = {
        'Host': 'open.taou.com',
        'x-maimai-reqid': user_config.maimai_mobile_req_id,
        'accept': '*/*',
        'credentials': 'same-origin',
        'user-agent': '{iPhone11,6} [iOS 14.6]/MaiMai 6.0.80(6.0.80.1)',
        'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return feeds_list
        json_data = response.json()
        if json_data is None or 'feeds' not in json_data:
            return feeds_list
        feeds = json_data['feeds']
        if feeds is None or len(feeds) == 0:
            return feeds_list
        for feed in feeds:
            if feed is None or 'id' not in feed:
                continue
            feeds_list.append(feed['id'])
        return feeds_list
    except Exception as e:
        print(e)
        return feeds_list


def del_feed(feed_id):
    url = "https://open.taou.com/maimai/feed/v5/del?access_token={}&appid=4&channel=AppStore&density=3&device=iPhone11%2C6&launch_uuid={}&net=wifi&push_permit=0&rn_version=0.63.2&screen_height=2688&screen_width=1242&session_uuid={}&sm_did={}&u={}&udid={}&vc=14.6&version=6.0.80&webviewUserAgent={}&appid=4&channel=AppStore&fid={}&rn=1&rn=1&screen_height=2688&screen_width=1242&use_native_net=1&version=6.0.80&webviewUserAgent={}&isPost=0".format(
        user_config.maimai_mobile_access_token, user_config.maimai_mobile_launch_uuid,
        user_config.maimai_mobile_session_uuid, user_config.maimai_mobile_sm_did, user_config.maimai_uid,
        user_config.maimai_mobile_udid, user_config.maimai_mobile_web_view_user_agent, feed_id,
        user_config.maimai_mobile_web_view_user_agent)

    payload = {}
    headers = {
        'Host': 'open.taou.com',
        'x-maimai-reqid': user_config.maimai_mobile_req_id,
        'accept': '*/*',
        'user-agent': '{iPhone11,6} [iOS 14.6]/MaiMai 6.0.80(6.0.80.1)',
        'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        print(response)
    except Exception as e:
        print(e)


def del_all_feeds():
    page = 0
    total_feeds = []
    feeds = get_feeds(page)
    while len(feeds) > 0:
        total_feeds.extend(feeds)
        page += 1
        feeds = get_feeds(page)
    for feed in total_feeds:
        if feed is None:
            continue
        del_feed(feed)


def get_job_visitors(offset):
    visitors = []
    url = "https://maimai.cn/sdk/jobs/job_visitors?u={}&channel=AppStore&device=iPhone11%2C6&access_token={}&version=6.0.80&_csrf={}&_csrf_token={}&ejid=&offset={}&jsononly=1&count=10&".format(
        user_config.maimai_uid, user_config.maimai_mobile_access_token, user_config.maimai_mobile_csrf,
        user_config.maimai_mobile_csrf_token, offset)

    payload = {}
    headers = {
        'Host': 'maimai.cn',
        'Cookie': user_config.maimai_mobile_cookie, 'accept': '*/*',
        'x-csrf-token': user_config.maimai_mobile_csrf_token,
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/{iPhone11,6} [iOS 14.6]/MaiMai 6.0.80(6.0.80.1)',
        'referer': 'https://maimai.cn/jobs/b/job_interactions?fr=recruiterTab',
        'accept-language': 'zh-cn'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return visitors
        json_data = response.json()
        if json_data is None or 'data' not in json_data:
            return visitors
        if json_data['data'] is None or len(json_data['data']) == 0:
            return visitors
        visitors.extend(json_data['data'])
    except Exception as e:
        print(e)
    return visitors


def get_job_recommenders(jid, page):
    url = "https://maimai.cn/api/ent/discover/recommend?channel=www&filter_unmatch=1&jid={}&page={}&version=1.0.0".format(
        jid, page
    )
    recommender = []
    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/discover/recommend/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return recommender
        print(response)
        json_data = response.json()
        if json_data is None or 'contacts' not in json_data:
            return recommender
        recommender.extend(json_data['contacts'])
    except Exception as e:
        print(e)
    return recommender


def get_job_viewers(jid, page):
    url = "https://maimai.cn/api/ent/position/visitors?channel=www&filter_unmatch=1&jid={}&page={}&version=1.0.0".format(
        jid, page
    )
    viewers = []
    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/discover/recommend/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return viewers
        print(response)
        json_data = response.json()
        if json_data is None or 'data' not in json_data or 'list' not in json_data['data']:
            return viewers
        viewers.extend(json_data['data']['list'])
    except Exception as e:
        print(e)
    return viewers


def contact_visitor(jid, u2_id):
    payload = {}
    headers = {
        'Host': 'maimai.cn',
        'Cookie': user_config.maimai_mobile_cookie,
        'x-maimai-reqid': user_config.maimai_mobile_req_id,
        'accept': '*/*',
        'user-agent': '{iPhone11,6} [iOS 14.6]/MaiMai 6.0.80(6.0.80.1)',
        'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9'
    }
    url = "https://maimai.cn/jobs/b/new_direct_chat?access_token={}&appid=4&channel=AppStore&density=3&device=iPhone11%2C6&launch_uuid={}&net=wifi&push_permit=0&rn_version=0.63.2&screen_height=2688&screen_width=1242&session_uuid={}&sm_did={}&u={}&udid={}&vc=14.6&version=6.0.80&webviewUserAgent={}&jid={}&fr={}&u2={}&jsononly=1".format(
        user_config.maimai_mobile_access_token, user_config.maimai_mobile_launch_uuid,
        user_config.maimai_mobile_session_uuid, user_config.maimai_mobile_sm_did, user_config.maimai_uid,
        user_config.maimai_mobile_udid, user_config.maimai_mobile_web_view_user_agent, jid,
        user_config.maimai_contact_visitor_source, u2_id)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        print(response)
    except Exception as e:
        print(e)


def send_greetings(encode_mmid, from_source, greet_template, jid, u2_id):
    url = "https://maimai.cn/sdk/jobs/recruiter/send?_csrf={}&_csrf_token={}&access_token={}&candidate={}&channel=AppStore&device=iPhone11%2C6&fr={}&greet_text={}&is_has_name=1&jid={}&pay_num=0&u={}&u2={}&version=6.0.80".format(
        user_config.maimai_mobile_csrf, user_config.maimai_mobile_csrf_token, user_config.maimai_mobile_access_token,
        encode_mmid, from_source, quote(greet_template),
        jid, user_config.maimai_uid, u2_id)

    payload = {}
    headers = {
        'Host': 'maimai.cn',
        'Cookie': user_config.maimai_mobile_cookie,
        'accept': '*/*',
        'x-csrf-token': user_config.maimai_mobile_csrf_token,
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/{iPhone11,6} [iOS 14.6]/MaiMai 6.0.80(6.0.80.1)',
        'referer': 'https://maimai.cn/jobs/b/new_direct_chat?jid={}&fr={}&u2={}'.format(jid,
                                                                                        from_source,
                                                                                        u2_id),
        'accept-language': 'zh-cn'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return True
        print(response)
        json_data = response.json()
        if json_data is not None and 'data' in json_data and 'ret' in json_data['data'] and 1 != json_data['data'][
            'ret']:
            return False
    except Exception as e:
        print(e)
    return True


def send_greetings_v2(jid, greet_template, u2_id, fr):
    url = "https://maimai.cn/groundhog/job/v3/direct/recruiter/send?channel=www&comfirmed=1&fr={}&greet_text={}&is_has_name=1&jid={}&u={}&u2={}&version=5.0.2".format(
        fr, quote(greet_template), jid, user_config.maimai_uid, u2_id)

    payload = {}
    headers = {
        'authority': 'maimai.cn',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-csrf-token': user_config.maimai_pc_header_csrf_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'same-origin',
        'sec-fetch-dest': 'empty',
        'referer': 'https://maimai.cn/ent/talents/discover/recommend/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.maimai_pc_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return True
        json_data = response.json()
        if json_data is not None and 'ret' in json_data and 1 != json_data['ret']:
            return False
    except Exception as e:
        print(e)
    return True


def get_match_talent_list(ejid, page):
    url = "https://maimai.cn/sdk/jobs/talent/v3/match_talent_list?access_token={}&appid=4&channel=AppStore&count=20&ejid={}&fr={}&log_sid={}&page={}&rn=1&screen_height=2688&screen_width=1242&u={}&version=6.0.80&webviewUserAgent={}".format(
        user_config.maimai_mobile_access_token, ejid, user_config.maimai_contact_recommend_source,
        user_config.maimai_logs_sid, page, user_config.maimai_uid, user_config.maimai_mobile_web_view_user_agent)
    talents = []
    payload = {}
    headers = {
        'Host': 'maimai.cn',
        'Cookie': user_config.maimai_mobile_cookie, 'x-maimai-reqid': user_config.maimai_mobile_req_id,
        'accept': '*/*',
        'accept-language': 'zh-cn',
        'user-agent': 'NeiTui/6.0.80.1 CFNetwork/1240.0.4 Darwin/20.5.0'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        json_data = response.json()
        if json_data is None or 'data' not in json_data:
            return talents

        talents.extend(json_data['data'])

    except Exception as e:
        print(e)
    return talents


def get_all_match_talent_list(ejid):
    offset = 0
    talent_list = []
    tmp_talent_list = get_match_talent_list(ejid, offset)
    while len(tmp_talent_list) > 0:
        offset += 1
        talent_list.extend(tmp_talent_list)
        tmp_talent_list = get_match_talent_list(ejid, offset)
    return talent_list


def get_all_job_viewers(jid):
    page = 0
    viewers = []
    tmp_viewers = get_job_viewers(jid, page)
    while len(tmp_viewers) > 0:
        page += 1
        viewers.extend(tmp_viewers)
        tmp_viewers = get_job_viewers(jid, page)
    return viewers


def get_all_job_recommenders(jid):
    page = 0
    recommenders = []
    tmp_viewers = get_job_recommenders(jid, page)
    while len(tmp_viewers) > 0:
        page += 1
        recommenders.extend(tmp_viewers)
        tmp_viewers = get_job_recommenders(jid, page)
    return recommenders


def del_all_msg():
    offset = 0
    part_msgs = get_msg(offset)
    while len(part_msgs) > 0:
        for msg in part_msgs:
            if msg is None or 'id' not in msg:
                continue
            msg_id = msg['id']
            del_msg(msg_id)
            if 'u2' in msg and 'name' in msg['u2']:
                print(msg['u2']['name'])
        offset += 1
        part_msgs = get_msg(offset)


if __name__ == '__main__':
    default_timeout = 0

    uids = []
    for uid in uids:
        del_msg(uid)
    del_all_msg()
    del_all_feeds()
