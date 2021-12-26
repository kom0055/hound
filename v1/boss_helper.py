# -*- coding:UTF-8 -*-
import copy
import re
import time
import datetime
import requests

# 获取最近联系人
import user_config
import random

default_timeout = 10


def sleep():
    sleep_time = random.random() * default_timeout + default_timeout
    time.sleep(sleep_time)


def get_zp_token():
    ts = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
    url = "https://www.zhipin.com/wapi/zppassport/get/zpToken?v={}".format(ts)

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'traceid': '80072A8F-106E-490B-B241-91C94D204D75',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/job/list',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response is None:
            return
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or not 'token' in json_data['zpData']:
            return
        user_config.boss_zp_token = json_data['zpData']['token']
    except Exception as e:
        print(e)


def get_contacts(page):
    contacts = []
    url = "https://www.zhipin.com/wapi/zprelation/friend/getBossFriendListV2.json"

    payload = 'page={}&friendIds=&dzFriendIds='.format(page)
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': 'E6D37C30-170D-4C1E-8EEF-6485A034C195',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': user_config.boss_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return contacts
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'friendList' not in json_data['zpData']:
            return contacts
        contacts.extend(json_data['zpData']['friendList'])

    except Exception as e:
        print(e)
    return contacts


def is_geek_asked(geek_id, expect_id, job_id, security_id):
    url = "https://www.zhipin.com/wapi/zpchat/session/bossEnter"

    payload = 'geekId={}&expectId={}&jobId={}&securityId={}'.format(
        geek_id, expect_id, job_id, security_id
    )
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': '47F3BF0A-7E5D-4006-9FF4-969B0A9ED951',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': user_config.boss_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return False
        json_data = response.json()
        if json_data is None:
            return False
        if 'zpData' in json_data and 'requestResume' in json_data['zpData'] and json_data['zpData'][
            'requestResume'] != 0:
            return True
        return False
    except Exception as e:
        print(e)
    return False


def send_job_position(job_id, u2id, security_id):
    url = "https://www.zhipin.com/wapi/zpchat/message/sendJobLocation"

    payload = 'jobId={}&toUserId={}&securityId={}'.format(job_id, u2id, security_id)
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': 'E0B03CA7-90B1-471B-A8F5-AE31B3915690',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': 'UGKMak6AJhsjRIgc',
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        requests.request("POST", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


# 询问简历, 联系人信息的 securityId
def ask_for_cv(security_id):
    url = "https://www.zhipin.com/wapi/zpchat/exchange/request"

    payload = 'type=4&securityId={}'.format(security_id)
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': 'A55F8744-8AFA-474A-911C-B7CD3DBB9997',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': user_config.boss_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
        print(response)
    except Exception as e:
        print(e)


# 下载简历, 联系人信息的 encryptUid
def down_load_resume(encrypt_uid):
    url = "https://www.zhipin.com/wapi/zpgeek/resume/preview4boss/{}?previewType=1".format(encrypt_uid)

    payload = {}
    headers = {
        'sec-fetch-mode': 'cors',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': '*/*',
        'referer': 'https://www.zhipin.com/web/common/pdfjs/build/pdf.worker.js',
        'sec-fetch-dest': 'empty',
        'authority': 'www.zhipin.com',
        'cookie': user_config.boss_cookie,
        'sec-fetch-site': 'same-origin'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if 'html' in response.headers['Content-Type']:
            return
        file_name_suffix = 'pdf'

        suffix_group = re.match(r'.*/([^;]*)', response.headers['Content-Type'], re.M | re.I)
        if suffix_group is not None and len(suffix_group.groups()) > 0:
            file_name_suffix = suffix_group.group(1)
        file_name = '{}.{}'.format(encrypt_uid, file_name_suffix)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name
    except Exception as e:
        print(e)
    return None


# 获取所有jd
def get_job_detail_list():
    url = "https://www.zhipin.com/wapi/zpjob/job/data/list?position=0&type=0&searchStr=&page=100&"
    job_list = []
    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': '6E3E5171-8547-4E8F-9F9E-2C082085B656',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/frame/job/list',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return job_list
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'data' not in json_data['zpData']:
            return job_list
        for job in json_data['zpData']['data']:
            job_list.append(job)
    except Exception as e:
        print(e)
    return job_list


# 增加crawled分组, 以甄别是否询问过
def add_group(label_tag):
    url = "https://www.zhipin.com/wapi/zprelation/userMark/addLabel?label={}".format(label_tag)

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'traceid': 'F5BD4138-283A-4B9F-8C05-FDF41DA27FD6',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'token': user_config.boss_token,
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    try:
        requests.request("GET", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


# 获取最近联系人信息, 主要拿到labels, 甄别是否拿过简历
def get_geek_info(uid, security_id):
    url = "https://www.zhipin.com/wapi/zpboss/h5/chat/geek.json?uid={}&geekSource=0&securityId={}".format(uid,
                                                                                                          security_id)

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',

        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'token': user_config.boss_token,
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return None
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'data' not in json_data['zpData']:
            return None
        return json_data['zpData']['data']

    except Exception as e:
        print(e)
    return None


# 获取看过我的牛人
def get_have_seen_me(job_id, page=1):
    url = "https://www.zhipin.com/wapi/zprelation/interaction/bossGetGeek?status=2&source=0&gender=0&exchangeResumeWithColleague=0&switchJobFrequency=0&activation=0&recentNotView=0&school=0&major=0&experience=0&degree=0&salary=0&intention=0&cityCode=&districtCode=&businessId=&jobId={}&page={}&tag=2".format(
        job_id, page)

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': '86B1BF1E-C8D9-4E68-8177-F4A6590CB878',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    seen_list = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return seen_list
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'geekList' not in json_data['zpData']:
            return seen_list
        seen_list.extend(json_data['zpData']['geekList'])
    except Exception as e:
        print(e)
    return seen_list


def send_contact_geek_req(suid, jid, expect_id, lid, security_id):
    url = "https://www.zhipin.com/wapi/zpboss/h5/chat/start?"
    payload = 'gid=3728be2b1889dd701Hd909i6EFI~&suid{}=&jid={}&expectId={}&lid={}&from=&securityId={}'.format(
        suid, jid, expect_id, lid, security_id)
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': 'F489C67F-73D8-4C94-90B3-82C5EF89E0AD',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
        json_data = response.json()
        if json_data is not None and 'zpData' in json_data and 'status' in json_data['zpData']:
            return json_data['zpData']['status'] == 1
    except Exception as e:
        print(e)
    return True


# 获取推荐牛人
def get_recommenders(job_id, offset, activation):
    now_time_stamp = int(time.time() * 1000)
    url = "https://www.zhipin.com/wapi/zpjob/rec/geek/list?age=22,35&gender=0&exchangeResumeWithColleague=1301&switchJobFrequency=0&activation={}&recentNotView=2301&school=1104,1103,1102,1105,1106&major=0&experience=105,106,107&degree=203,204,205&salary=0&intention=703,704,701&refresh={}&jobid={}&source=0&cityCode=101210100&districtCode=&businessId=&jobId={}&page={}&_={}".format(
        activation, now_time_stamp, job_id, job_id, offset, now_time_stamp)
    recommenders = []
    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': 'DD6C6143-9681-4B0E-B64D-8F0B0B91030C',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return recommenders
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'geekList' not in json_data['zpData']:
            return recommenders
        recommenders.extend(json_data['zpData']['geekList'])
    except Exception as e:
        print(e)
    return recommenders


# 获取精选牛人, 需要额外的卡, 故不使用
def get_redefined(encrypt_job_id, offset=1):
    url = "https://www.zhipin.com/wapi/zpitem/web/refinedGeek/list?page={}&encryptJobId={}".format(
        encrypt_job_id, offset
    )

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': 'CC2F349B-18A5-44B3-8425-631BDE87DD1A',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


# 获取新牛人
def get_fresh(job_id, page, activation):
    now_time_stamp = int(time.time() * 1000)
    url = "https://www.zhipin.com/wapi/zprelation/interaction/bossGetGeek?status=1age=22,35&gender=0&exchangeResumeWithColleague=1301&switchJobFrequency=0&activation={}&recentNotView=2301&school=1104,1103,1102,1105,1106&major=0&experience=105,106,107&degree=203,204,205&salary=0&intention=703,704,701&refresh={}&jobid={}&source=0&cityCode=101210100&districtCode=&businessId=&jobId={}&page={}&_={}".format(
        activation, now_time_stamp, job_id, job_id, page, now_time_stamp)
    payload = {}
    fresh_list = []
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': '62DAEF4B-6E43-4ED2-B830-E06C03E9C101',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return fresh_list
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'geekList' not in json_data['zpData']:
            return fresh_list
        fresh_list.extend(json_data['zpData']['geekList'])
    except Exception as e:
        print(e)
    return fresh_list


# 获取收藏的牛人, 暂时不用
def get_favorite(page):
    url = "https://www.zhipin.com/wapi/zprelation/bossTag/bossGetGeek?tag=4&page={}".format(page)
    favorite_list = []
    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': 'B4900B2D-4626-4D55-9F8B-5CBFB3663E99',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    response = requests.request("GET", url, headers=headers, data=payload)
    sleep()


def get_geeks_seen_before(job_id, page=1):
    url = "https://www.zhipin.com/wapi/zprelation/interaction/bossGetGeek?status=8&source=0&gender=0&exchangeResumeWithColleague=0&switchJobFrequency=0&activation=0&recentNotView=0&school=0&major=0&experience=0&degree=0&salary=0&intention=0&cityCode=&districtCode=&businessId=&jobId={}&page={}&tag=8".format(
        job_id, page
    )

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': '914F8433-2FFB-43C0-AC37-B12495005684',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    seen_list = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return seen_list
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'geekList' not in json_data['zpData']:
            return seen_list
        seen_list.extend(json_data['zpData']['geekList'])
    except Exception as e:
        print(e)
    return seen_list


# 同事推荐, 目前没啥价值
def duplicate_colleague(job_id, page=1):
    url = "https://www.zhipin.com/wapi/zpboss/h5/boss/recommendGeekList?jobId={}&page={}&status=5".format(
        job_id, page
    )

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': 'B40E3EA1-BB75-44C5-9C64-D512B2B37D4E',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    response = requests.request("GET", url, headers=headers, data=payload)
    sleep()


# 获取对我感兴趣的
def get_interesting(job_id, page=1):
    url = "https://www.zhipin.com/wapi/zprelation/interaction/bossGetGeek?jobid={}&status=4&source=0&gender=0&exchangeResumeWithColleague=0&switchJobFrequency=0&activation=0&recentNotView=0&school=0&major=0&experience=0&degree=0&salary=0&intention=0&cityCode=&districtCode=&businessId=&page={}&tag=4".format(
        job_id, page
    )

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'traceid': 'FEAD5670-F2A2-4B37-ACB6-ABAE8567B414',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
        'zp_token': user_config.boss_zp_token,
        'x-anti-request-token': user_config.boss_anti_token,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/vue/index/',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}

    interesting_list = []
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return interesting_list
        json_data = response.json()
        if json_data is None or 'zpData' not in json_data or 'geekList' not in json_data['zpData']:
            return interesting_list
        interesting_list.extend(json_data['zpData']['geekList'])
    except Exception as e:
        print(e)
    return interesting_list


def contact_all_geeks(job_id, activation):
    geek_names = []
    try:
        page = 1
        recommender_geeks = get_recommenders(job_id, page, activation)
        filter_job_list = list(map(lambda x: x['encryptJobId'], copy.deepcopy(user_config.boss_job_list)))
        while len(recommender_geeks) > 0:
            for geek in recommender_geeks:
                geek_name = contact_geek(geek)
                if geek_name is None:
                    continue
                geek_names.append(geek_name)
            page += 1
            recommender_geeks = get_recommenders(job_id, page, activation)

        # page = 1
        # fresh_list = get_fresh(job_id, page, activation)
        # while len(fresh_list) > 0 and page < 3:
        #     for geek in fresh_list:
        #         geek_name = contact_geek(geek)
        #         if geek_name is None:
        #             continue
        #         geek_names.append(geek_name)
        #     page += 1
        #     fresh_list = get_fresh(job_id, page, activation)

        # page = 1
        # seen_list = get_geeks_seen_before(job_id, page)
        # while len(seen_list) > 0:
        #     for geek in seen_list:
        #         geek_name = contact_geek(geek)
        #         if geek_name is None:
        #             continue
        #         geek_names.append(geek_name)
        #     page += 1
        #     seen_list = get_geeks_seen_before(job_id, page)
        #
        # page = 1
        # interesting_list = get_interesting(job_id, page)
        # while len(interesting_list) > 0:
        #     for geek in interesting_list:
        #         geek_name = contact_geek(geek)
        #         if geek_name is None:
        #             continue
        #         geek_names.append(geek_name)
        #     page += 1
        #     interesting_list = get_interesting(job_id, page)
        #
        # page = 1
        # have_seen_me_list = get_have_seen_me(job_id, page)
        # while len(have_seen_me_list) > 0:
        #     for geek in have_seen_me_list:
        #         geek_name = contact_geek(geek)
        #         if geek_name is None:
        #             continue
        #         geek_names.append(geek_name)
        #     page += 1
        #     have_seen_me_list = get_have_seen_me(job_id, page)
    except Exception as e:
        print(e)
    return geek_names


def contact_geek(geek):
    if geek is None or 'haveChatted' in geek and geek['haveChatted'] != 0 or 'geekCard' not in geek:
        return None
    # if 'cooperate' in geek and geek['cooperate'] == 2:
    #     return None
    if 'geekCard' not in geek or 'matches' not in geek['geekCard']:
        return None
    # match_skills = list(map(lambda x: x.lower(), geek['geekCard']['matches']))
    # if 'java' not in match_skills and 'expectPositionName' in geek['geekCard'] and 'java' not in \
    #         geek['geekCard']['expectPositionName'].lower():
    #     return None
    geek_card = geek['geekCard']
    if 'geekDegree' in geek_card and geek_card['geekDegree'] is not None:
        if '专' in geek_card['geekDegree']:
            return None
    if 'geekEdus' in geek_card and geek_card['geekEdus'] is not None and len(geek_card['geekEdus']) > 0:
        for geek_edu in geek_card['geekEdus']:
            if 'degreeName' in geek_edu and geek_edu['degreeName'] is not None:
                if '专' in geek_edu['degreeName']:
                    return None
            if 'endDate' in geek_edu and geek_edu['endDate'] is not None:
                graduate_str = geek_edu['endDate']
                graduate_date = time.mktime(time.strptime(graduate_str, '%Y.%m'))
                now_time = time.time()
                if now_time < graduate_date:
                    return None

    security_id = ''
    expect_id = ''
    lid = ''
    suid = ''
    jid = ''
    if 'suid' in geek and geek['suid'] is not None:
        suid = geek['suid']
    if 'securityId' in geek_card and geek_card['securityId'] is not None:
        security_id = geek_card['securityId']
    if 'expectId' in geek_card and geek_card['expectId'] is not None:
        expect_id = geek_card['expectId']
    if 'lid' in geek_card and geek_card['lid'] is not None:
        lid = geek_card['lid']
    if 'encryptJobId' in geek_card and geek_card['encryptJobId'] is not None:
        jid = geek_card['encryptJobId']
    if not send_contact_geek_req(suid, jid, expect_id, lid, security_id):
        raise Exception('已经无法再联系啦')
    if 'geekName' in geek_card:
        return geek['geekCard']['geekName']
    return None


def clear_tips(friend_id):
    url = "https://www.zhipin.com/wapi/zprelation/friend/syncFriendStatusInfo?friendId={}".format(friend_id)

    payload = {}
    headers = {
        'authority': 'www.zhipin.com',
        'traceid': '326C1969-79ED-4090-8068-8F28EB86FDCD',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'token': user_config.boss_token,
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        requests.request("GET", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


# 将候选人标记为爬取过简历
def mark_label(encrypt_friend_id, security_id, labels):
    url = "https://www.zhipin.com/wapi/zprelation/noteandlabel/save.json"

    payload = 'encryptFriendId={}&securityId{}=&labels={}&note='.format(encrypt_friend_id, security_id,
                                                                        ','.join(labels))
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': 'A4CF59B1-0045-44AD-A72A-F524D64E64BF',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': user_config.boss_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        requests.request("POST", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


def del_msg(geek_id, security_id):
    url = "https://www.zhipin.com/wapi/zprelation/friend/delete.json"

    payload = 'geekId={}&securityId={}'.format(geek_id, security_id)
    headers = {
        'authority': 'www.zhipin.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'traceid': '525DB931-0DC0-4D65-9FF9-2A8B91DF298E',
        'accept': 'application/json, text/plain, */*',
        'zp_token': user_config.boss_zp_token,
        'token': user_config.boss_token,
        'origin': 'https://www.zhipin.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhipin.com/web/boss/index',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'cookie': user_config.boss_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        sleep()
    except Exception as e:
        print(e)


def del_all_msg():
    page_int = 1
    contacts = get_contacts(page_int)
    while len(contacts) > 0:
        for contact in contacts:
            if contact is None or 'encryptUid' not in contact or 'securityId' not in contact:
                continue
            security_id = contact['securityId']
            encrypt_uid = contact['encryptUid']
            del_msg(encrypt_uid, security_id)
            if 'name' in contact:
                print(contact['name'])

        contacts = get_contacts(page_int)


if __name__ == '__main__':
    default_timeout = 0
    del_all_msg()
