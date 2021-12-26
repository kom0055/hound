# -*- coding:UTF-8 -*-
import copy
import time
import urllib.parse

import requests
import json
import os

from requests_toolbelt import MultipartEncoder

import random
import user_config

default_timeout = 3
requests.packages.urllib3.disable_warnings()


def sleep():
    sleep_time = random.random() * default_timeout + default_timeout
    time.sleep(sleep_time)


def get_moka_part_jobs(zhineng_id, offset):
    url = "https://app.mokahr.com/api/outer/ats-jc-apply/website/jobs"

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'use-http-status': '0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'moka-tracing': '{"op_no":"bd155b03-91c8-4d00-8e16-2d75907b9f89","locale":"zh_CN","time_zone":"GMT+08:00","source":"apply-web","org_id":"thedu"}',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://app.mokahr.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.mokahr.com/recommendation-apply/thedu/4256',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cookie': user_config.moka_token}

    jobs = []
    payload = json.dumps({
        "limit": 15,
        "offset": offset,
        "siteId": 4256,
        "orgId": "thedu",
        "site": "recommendation",
        "needStat": True,
        "zhinengId": zhineng_id
    })
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return jobs
        json_data = response.json()
        if json_data is None:
            return jobs
        if 'data' not in json_data or 'jobs' not in json_data['data']:
            return jobs
        jobs.extend(json_data['data']['jobs'])
        return jobs
    except Exception as e:
        print(e)
        return jobs


def get_job_detail(jobId):
    url = "https://app.mokahr.com/api/outer/ats-jc-apply/website/job"

    payload = json.dumps({
        "orgId": "thedu",
        "jobId": jobId,
        "siteId": 4256
    })
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'use-http-status': '0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'moka-tracing': '{"op_no":"e379e89b-4f55-49b7-9522-24c2089001b3","locale":"zh_CN","time_zone":"GMT+08:00","source":"apply-web","org_id":"thedu"}',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://app.mokahr.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.mokahr.com/recommendation-apply/thedu/4256',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cookie': user_config.moka_token
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        sleep()
        if response is None:
            return None
        json_data = response.json()
        if json_data is None:
            return None
        if 'data' not in json_data:
            return None
        return json_data['data']
    except Exception as e:
        print(e)
        return None


def get_moka_all_jobs_from_remote():
    jobs = copy.deepcopy(user_config.maimai_moka_job_map)
    for zhineng_id in copy.deepcopy(user_config.moka_zhineng_ids):
        divided_jobs = []
        offset = 0
        simple_jobs = get_moka_part_jobs(zhineng_id, offset)
        while len(simple_jobs) > 0:
            for simple_job in simple_jobs:
                if simple_job is None or 'id' not in simple_job:
                    continue
                detail_job = get_job_detail(simple_job['id'])
                divided_jobs.append(detail_job)
            offset = len(divided_jobs)
            simple_jobs = get_moka_part_jobs(zhineng_id, offset)
        jobs.extend(divided_jobs)
    with open(file=user_config.moka_job_file, mode='w', encoding='utf-8') as f_w:
        json.dump(jobs, f_w)

    return jobs


def get_moka_all_jobs_from_cache():
    jobs = []
    with open(file=user_config.moka_job_file, mode='r', encoding='utf-8') as f_r:
        jobs = json.load(f_r)
    return jobs


def upload_cv(resume_file, index=0):
    url = "https://app.mokahr.com/api/outer/ats-candidate-extractor/resume/uploadAndParse/candidate"
    user_simple_info = user_config.personal_info_list[index % len(user_config.personal_info_list)]
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'use-http-status': '0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'moka-tracing': '{"op_no":"e379e89b-4f55-49b7-9522-24c2089001b3","locale":"zh_CN","time_zone":"GMT+08:00","source":"apply-web","org_id":"thedu"}',
        'Content-Type': 'multipart/form-data;boundary={}'.format(user_config.boundry),
        'Accept': '*/*',
        'Origin': 'https://app.mokahr.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.mokahr.com/recommendation-apply/thedu/4256',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cookie': user_simple_info['moka_token']}
    try:
        with open(resume_file, 'rb') as f:
            file_name = os.path.basename(resume_file)
            upload_file = {
                'orgId': 'thedu',
                'resume': (file_name, f),

                'uploadSource': 'recommend'
            }

            multipart_encoder = MultipartEncoder(fields=upload_file,
                                                 boundary=user_config.boundry)
            response = requests.request("POST", url, headers=headers, data=multipart_encoder, verify=False)
            sleep()
            if response is None:
                return False
            json_data = response.json()
            if json_data is None:
                return None
            if 'data' not in json_data:
                return None
            return json_data['data']
    except Exception as e:
        print(e)
        return None


def apply_cv(job_id, ori_info, name_default, index=0):
    if ori_info is None:
        return False
    if 'academicDegree' in ori_info and '专' in ori_info['academicDegree']:
        return False
    if 'graduateDate' in ori_info:
        graduate_date = time.mktime(time.strptime(ori_info['graduateDate'], '%Y-%m'))
        now_time = time.time()
        if now_time < graduate_date:
            return False
    if 'birthYear' in ori_info and len(ori_info['birthYear']) > 0:
        birth_year = ori_info['birthYear']
        age = int(time.strftime("%Y", time.localtime())) - int(birth_year)
        # if age >= 38:
        #     return False
    url = "https://app.mokahr.com/api/outer/ats-jc-apply/website/apply"
    upload_info = {
        "portrait": None,
        "attachments": [],
        "resumeName": ori_info['resumeName']
    }

    if 'resumeKey' in ori_info:
        upload_info['resumeKey'] = ori_info['resumeKey']
    if 'resumeName' in ori_info:
        upload_info['resumeName'] = ori_info['resumeName']

    base_info = {
        'name': name_default
    }

    if 'name' in ori_info and len(ori_info['name']) > 0:
        base_info['name'] = ori_info['name']

    if 'phone' in ori_info:
        base_info['phone'] = ori_info['phone']
    if 'email' in ori_info:
        base_info['email'] = ori_info['email']
    if 'gender' in ori_info:
        base_info['gender'] = ori_info['gender']
    if 'age' in ori_info:
        base_info['age'] = ori_info['age']
    if 'experience' in ori_info:
        base_info['experience'] = ori_info['experience']
    if 'academicDegree' in ori_info:
        base_info['academicDegree'] = ori_info['academicDegree']
    if 'location' in ori_info:
        base_info['location'] = ori_info['location']
    if 'nationality' in ori_info:
        base_info['nationality'] = ori_info['nationality']
    if 'ethnic' in ori_info:
        base_info['ethnic'] = ori_info['ethnic']
    if 'lastCompany' in ori_info:
        base_info['lastCompany'] = ori_info['lastCompany']
    if 'industry' in ori_info:
        base_info['industry'] = ori_info['industry']
    if 'forwardIndustry' in ori_info:
        base_info['forwardIndustry'] = ori_info['forwardIndustry']
    if 'lastUpdate' in ori_info:
        base_info['lastUpdate'] = ori_info['lastUpdate']
    if 'startFrom' in ori_info:
        base_info['startFrom'] = ori_info['startFrom']
    if 'skill' in ori_info:
        base_info['skill'] = ori_info['skill']
    if 'awards' in ori_info:
        base_info['awards'] = ori_info['awards']
    if 'fullPhone' in ori_info:
        base_info['fullPhone'] = ori_info['fullPhone']
    if 'citizenId' in ori_info:
        base_info['citizenId'] = ori_info['citizenId']
    personal_info = user_config.personal_info_list[index % (len(user_config.personal_info_list))]
    user_simple_info = copy.deepcopy(user_config.recommender_info)

    user_simple_info['id'] = personal_info['moka_uid']
    user_simple_info['name'] = personal_info['chinese_name']
    user_simple_info['email'] = personal_info['email']
    user_simple_info['recommendCode'] = personal_info['moka_recommender_code']
    user_info = {
        "orgId": "thedu",
        "jobId": job_id,
        "activationToken": None,
        "sourceToken": None,
        "applyInfo": {},
        "uploadInfo": upload_info,
        "basicInfo": base_info,
        "jobIntention": {
            "salary": "",
            "forwardLocation": "",
            "aimSalary": ""
        },
        "languageInfo": [],
        "selfDescription": {
            "personal": ""
        },
        "awardInfo": [],
        "device": "pc",
        "recommender": user_simple_info,
        "recommendInfo": {
            "recommendReason": "无"
        },
        "siteId": "4256",
        "acquisitionMode": 8
    }
    if 'experienceInfo' in ori_info:
        user_info['experienceInfo'] = ori_info['experienceInfo']
    if 'educationInfo' in ori_info:
        user_info['educationInfo'] = ori_info['educationInfo']
    if 'practiceInfo' in ori_info:
        user_info['practiceInfo'] = ori_info['practiceInfo']
    if 'projectInfo' in ori_info:
        user_info['projectInfo'] = ori_info['projectInfo']
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'use-http-status': '0',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'moka-tracing': '{"op_no":"f28751a4-65ae-481d-97c1-b0a783877b71","locale":"zh_CN","time_zone":"GMT+08:00","source":"apply-web","org_id":"thedu"}',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://app.mokahr.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.mokahr.com/recommendation-apply/thedu/4256',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cookie': personal_info['moka_token']}
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(user_info))
        sleep()
        if response is None:
            return False
        json_data = response.json()
        if json_data is None:
            return False
        if 'code' not in json_data or json_data['code'] != 0 or 'success' not in json_data \
                or not json_data['success']:
            return False
        return True
    except Exception as e:
        print(e)
        return False


def get_interviewee_list(page, job_id, start_date, end_date):
    url = "https://app.mokahr.com/api/user/recommendation/applications?page={}&candidateName=&jobId={}&startDate={}&endDate={}".format(
        page, job_id, urllib.parse.quote(start_date), urllib.parse.quote(end_date))

    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'moka-tracing': '{"op_no":"bf5eb7c0-e36d-4696-bd1c-5c5a16f16755","locale":"zh_CN","time_zone":"GMT+08:00","source":"apply-web","org_id":"thedu"}',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.mokahr.com/recommendation-apply/thedu/4256',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cookie': user_config.moka_token,
        'If-None-Match': 'W/"5bac-Q0ONB+x9XHhUMdmOGUvvV7b7YB0"'
    }
    interviewee_list = []

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        sleep()
        if response is None:
            return interviewee_list
        json_data = response.json()
        if json_data is None:
            return interviewee_list
        if 'rows' not in json_data or len(json_data['rows']) == 0:
            return interviewee_list
        interviewee_list.extend(json_data['rows'])
    except Exception as e:
        print(e)
    return interviewee_list


if __name__ == '__main__':
    upload_cv('start 孙凯百胜中国全国分拨中心经理 end')
