# -*- coding:UTF-8 -*-


# 需要修改的

# 个人信息
# moka配置
target_jon_title = ''
moka_token = ''
personal_info_list = [
    {
        "chinese_name": '',
        'email': '',
        'moka_token': moka_token,
        'moka_uid': 123456,
        'moka_recommender_code': ''
    }
]

recommender_info = {
    "id": 0,
    "name": '',
    "phone": "",
    "email": '',
    "employeeId": "",
    "orgId": '',
    "fullPhone": "",
    "countryCallingCode": None,
    "orgName": '',
    "role": 0,
    "deptIds": [],
    "lastVisitAt": "2021-06-24T02:26:32.000Z",
    "recommendMoney": 0,
    "recommendScore": 30,
    "recommendRulesCount": 9,
    "recommendCode": ''
}
# 脉脉配置
maimai_pc_cookie = ''
maimai_pc_header_csrf_token = ''
maimai_pc_csrf_token = maimai_pc_header_csrf_token
maimai_pc_csrf = ''

maimai_mobile_cookie = ''
maimai_mobile_csrf_token = ''
maimai_mobile_csrf = ''
maimai_mobile_access_token = ''
maimai_mobile_launch_uuid = ''
maimai_uid = 123456
maimai_greeting = '你好，我是xxxx，我这有职位很适合你，你方便和我简单的沟通一下吗？希望你会感兴趣'
maimai_mobile_session_uuid = ''
maimai_mobile_sm_did = ''
maimai_mobile_udid = ''
maimai_mobile_req_id = ''
maimai_logs_sid = ''
maimai_mobile_web_view_user_agent = ''

maimai_high_level_jd = [
    {'jid': 123456,
     'ejid': ''},
]

maimai_ignore_ejid = []

maimai_moka_job_map = [
    {
        'id': '',
        'title': ''
    }]

# boss配置

boss_cookie = ''
boss_token = ''
boss_zp_token = '~'
boss_anti_token = ''
boss_job_list = [
    {'encryptJobId': ''},
    {'encryptJobId': ''}
]
boss_activation_list = [2501, 2502, 2503, 2504, 2505, 0]
# lagou 配置
lagou_cookie = ''
lagou_show_id = ''
lagou_position_id = ''
lagou_chat_position_id = ''
lagou_greeting_id = ''
lagou_condition = 'go,hadoop,idea,java,linux,mybatis,mysql,oracle,php,spring,sql,tcp/ip,web后端开发,云计算｜云存储,区块链,移动服务端开发'
lagou_query_list = ['isBigCompany=1&', 'isEliteSchool=1&', 'isOverSea=1&']
# 无需修改
# multi-part/form sequence
boundry = '-----------------------------2385610611750'

# 飞书 bot
APP_ID = ''
APP_SECRET = ''

# moka
# "15547" 技术  "15548" 产品, "15549" 设计, "15550" 运营 , "15552" 职能类, "15553" 销售, "70632" 技术-杭州 ,"77394" 技术-北京  ,"66288" 风控
moka_zhineng_ids = []
moka_target_job_ids = ['']
moka_stage_dict = {
    '初筛': True,
    'rejected': True,
    '面试': False,
    '用人部门筛选': True,
    '沟通offer': False,
    '待入职': False,
    'hired': False,
}
ignore_position_name_key_list = ['CTO']
moka_time_template = '%a %m %d %Y 00:00:00 GMT+0800 (中国标准时间)'
moka_high_level_jid = ''

# 脉脉
maimai_contact_visitor_source = 'jobInteractionsVisitors'
maimai_contact_recommend_source = 'recruiterTabCandidateRecommend'
maimai_contact_visitor_fr = 'visitor_pc_v0.1'
maimai_contact_recommend_fr = 'recommend_pc_v0.1'

# 缓存文件
moka_job_file = 'moka_jobs.text'
maimai_job_file = 'maimai_jobs.text'


def get_problem_card_model(now, problem, problem_url):
    model = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "**每日一题 {}**\n".format(now),
                    "tag": "lark_md"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "content": "🔺 [{}]({})".format(problem, problem_url),
                    "tag": "lark_md"
                }
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": "💪 每日一题",
                "tag": "plain_text"
            }
        }
    }
    return model


if __name__ == '__main__':
    import json
    from urllib.parse import urlparse

    urls_pic = set()
    hosts_pic = set()
    with open(file='picture.txt', mode='r', encoding='utf-8') as f_r:
        for line in f_r.readlines():
            try:
                pic_infos = json.loads(line)
                for pic_info in pic_infos:
                    url = pic_info['url']
                    urls_pic.add(url)
                    o = urlparse(url)
                    hosts_pic.add(o.hostname)
            except Exception:
                pass

    print(len(hosts_pic))
    print(hosts_pic)

    urls_video = set()
    hosts_video = set()
    with open(file='video_url.txt', mode='r', encoding='utf-8') as f_r:
        for line in f_r.readlines():
            try:
                video_urls = line.split('|')
                for video_url in video_urls:
                    o = urlparse(video_url)
                    urls_video.add(o.hostname)
                    hosts_video.add(o.hostname)
            except Exception:
                pass
    print(urls_video)
    print(len(urls_video))
