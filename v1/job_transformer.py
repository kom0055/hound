import re


def transfer_moka_2_maimai(moka_job):
    if moka_job is None or 'jobDescription' not in moka_job or 'title' not in moka_job:
        return None
    desc = moka_job['jobDescription']
    pattern = re.compile(r'</p>', re.S)
    desc = pattern.sub('\n', desc)
    pattern = re.compile(r'<[^>]+>', re.S)
    desc = pattern.sub('', desc)
    maimai_job = {
        "position": moka_job['title'],
        "company": "得物App",
        "major_new": "0107",
        "profession_new": "0104",
        "description": desc,
        "is_hunter": False,
        "stags": "",
        "province": "上海",
        "city": "杨浦区",
        "email": "362519489@qq.com",
        "custom_text": "",
        "address": "互联宝地",
        "is_public": 1,
        "is_regular": 0,
        "major_keywords": "",
        "cid": 16281625,
        "profession": "",
        "major": "",
        "profession_path": "",
        "major_name_lv2": "",
        "profession_path_new": "01,0104",
        "salary_min": 20000,
        "salary_max": 40000,
        "work_time": 5,
        "degree": 0,
        "salary_share": 16,
        "profession_text": "电子商务",
        "major_text": "",
        "major_new_lv2": "",
        "major_code_lv1": ""
    }

    return maimai_job


# {
#                 "jid": 4426772,
#                 "ejid": "MEufoe8sLdme9wndb0TMMA",
#                 "position": "舆情监测（上海）",
#                 "company": "得物App",
#                 "province": "上海",
#                 "city": "杨浦区",
#                 "sdegree": "不限",
#                 "worktime": "不限",
#                 "salary": "10k-15k/月",
#                 "crtime": "2021-06-24 15:28:36",
#                 "state": "close",
#                 "src_state": 2,
#                 "exposure_state": 0,
#                 "judge": "pass",
#                 "src_judge": 2,
#                 "resume_cnt": 0,
#                 "viewed_cnt": 0,
#                 "is_public": 1
#             }

def transfer_maimai_2_moka(maimai_job):
    if maimai_job is None:
        return None
