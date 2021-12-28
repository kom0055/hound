# -*- coding:UTF-8 -*-
import copy
import datetime
import os
import random
import sys
import time
from datetime import datetime
from datetime import timedelta

import requests

import boss_helper
import feishu_bot
import lagou_helper
import maimai_helper
import moka_helper
import user_config

requests.packages.urllib3.disable_warnings()
boss_helper.get_zp_token()
transfer_2_target_position_flag = True


def sync_moka_jobs_2_maimai():
    moka_jobs_dict = {}
    maimai_jobs_dict = {}
    to_add = 0
    to_close = 0
    to_open = 0
    # moka_jobs = moka_helper.get_moka_all_jobs_from_remote()
    maimai_online_jobs = maimai_helper.get_all_jobs_from_remote()

    # for maimai_online_job in maimai_online_jobs:
    #     if maimai_online_job is None:
    #         continue
    #     maimai_jobs_dict[maimai_online_job['position']] = maimai_online_job
    #
    # for moka_job in moka_jobs:
    #     if moka_job is None:
    #         continue
    #     moka_jobs_dict[moka_job['title']] = moka_job

    for maimai_online_job in maimai_online_jobs:
        if maimai_online_job is None or 'position' not in maimai_online_job:
            continue
        ejid = maimai_online_job['ejid']
        position = maimai_online_job['position']
        maimai_helper.close_job(ejid)
        # if position not in moka_jobs_dict:
        #     maimai_helper.close_job(ejid)
        #     to_close += 1
        #     continue
        # if is_ignore_position(position):
        #     maimai_helper.close_job(ejid)
        #     to_close += 1
        #     continue
        # if maimai_online_job['src_state'] == 1:
        #     continue
        # maimai_helper.open_job(ejid)
        # to_open += 1

    # for moka_job in moka_jobs:
    #     if moka_job is None:
    #         continue
    #     if moka_job['title'] in maimai_jobs_dict:
    #         continue
    #     maimai_job = job_transformer.transfer_moka_2_maimai(moka_job)
    #     if maimai_job is None:
    #         continue
    #     maimai_helper.add_job(maimai_job)
    #     to_add += 1
    print('to_add', to_add)
    print('to_close', to_close)
    print('to_open', to_open)
    maimai_helper.del_all_feeds()
    feishu_bot.send_msg('【脉脉】已添加{}个职位, 关闭{}个职位, 重新打开{}个职位'.format(to_add, to_close, to_open))


def is_ignore_position(position):
    for ignore_key in user_config.ignore_position_name_key_list:
        if ignore_key.lower() in position.lower():
            return True
    return False


def aloha():
    offset = 0
    candidates = []
    part_msgs = maimai_helper.get_msg(offset)
    while len(part_msgs) > 0:
        for msg in part_msgs:
            if msg is None or 'id' not in msg:
                continue
            msg_id = msg['id']
            if 'deleted' not in msg or msg['deleted'] == 2 or 'u2' not in msg or 'id' not in msg['u2']:
                continue

            u2_id = msg['u2']['id']
            # if msg_id != 131837060:
            #     continue
            asked_before = maimai_helper.enter_msg(msg_id)
            if not asked_before:
                # maimai_helper.exchange_mobile(msg_id, u2_id)
                maimai_helper.ask_cv(msg_id, u2_id)
                if 'name' in msg['u2']:
                    candidates.append(msg['u2']['name'])
            maimai_helper.del_msg(msg_id)
        offset += 1
        part_msgs = maimai_helper.get_msg(offset)
    feishu_bot.send_msg('【脉脉】已和{}人索要简历, 列表:{}'.format(len(candidates), candidates))


def push_resume():
    moka_job_dict = {}

    count = 0
    resume_name_list = []
    resume_list = []
    offset = 0
    tmp_resume_list = maimai_helper.collect_cv(offset)
    while len(tmp_resume_list) > 0:
        resume_list.extend(tmp_resume_list)
        offset += 1
        tmp_resume_list = maimai_helper.collect_cv(offset)

    if resume_list is None or len(resume_list) == 0:
        feishu_bot.send_msg('【脉脉】已上传{}份简历, 列表:{}'.format(count, resume_name_list))
        return
    moka_jobs = moka_helper.get_moka_all_jobs_from_cache()
    if moka_jobs is None or len(moka_jobs) == 0:
        feishu_bot.send_msg('【脉脉】已上传{}份简历, 列表:{}'.format(count, resume_name_list))
        return
    for moka_job in moka_jobs:
        if moka_job is None or 'title' not in moka_job:
            continue
        moka_job_dict[moka_job['title']] = moka_job

    for resume in resume_list:
        if resume is None or 'ejid' not in resume or 'id' not in resume:
            continue
        ejid = resume['ejid']
        u2_id = resume['id']
        if 'position_job' not in resume or 'web_uid' not in resume or 'edu' not in resume or resume[
            'edu'] is None or 'degree' not in resume['edu'] or resume['edu']['degree'] is None or '专' in resume['edu'][
            'degree'] or 'has_attach' not in resume or not resume['has_attach']:
            maimai_helper.pass_cv(ejid, u2_id)
            continue
        position_job = resume['position_job']
        web_uid = resume['web_uid']

        if position_job not in moka_job_dict:
            continue
        file_name = '{}_{}'.format(int(time.time() * 1000), random.randrange(1, 1000))
        moka_job = moka_job_dict[position_job]
        new_file_name = maimai_helper.down_load_cv(web_uid, file_name, ejid)
        resume_info = moka_helper.upload_cv(new_file_name)
        apply_res = moka_helper.apply_cv(moka_job['id'], resume_info, resume['name'])
        if apply_res:
            maimai_helper.pass_cv(ejid, u2_id)
            count += 1
            resume_name_list.append(new_file_name)
        os.remove(new_file_name)
    feishu_bot.send_msg('【脉脉】已上传{}份简历, 列表:{}'.format(count, resume_name_list))


def contact_all_visitors():
    offset = 0
    visitors = maimai_helper.get_job_visitors(offset)
    count = 0
    visitor_name_list = []
    interrupt_flag = False
    while len(visitors) > 0:
        if interrupt_flag:
            break
        for visitor in visitors:
            if interrupt_flag:
                break
            if visitor is None:
                continue
            if 'recent_dc_chat' in visitor and visitor['recent_dc_chat'] == 1:
                continue
            if 'degree_str' not in visitor or '专' == visitor['degree_str']:
                continue
            if 'jinfo' not in visitor:
                continue
            jinfo = visitor['jinfo']
            if jinfo is None or 'ejid' not in jinfo:
                continue
            jid = jinfo['id']
            if 'uid' not in visitor or 'encode_mmid' not in visitor:
                continue

            u2_id = visitor['uid']
            encode_mmid = visitor['encode_mmid']
            maimai_helper.contact_visitor(jid, u2_id)
            interrupt_flag = not maimai_helper.send_greetings(encode_mmid, user_config.maimai_contact_visitor_source,
                                                              user_config.maimai_greeting,
                                                              jid, u2_id)
            if interrupt_flag:
                break
            count += 1
            if 'name' in visitor:
                visitor_name_list.append(visitor['name'])
                print(visitor['name'])
        offset += len(visitors)
        visitors = maimai_helper.get_job_visitors(offset)
    feishu_bot.send_msg('【脉脉】已联系{}个职位来访者,列表:{}'.format(count, visitor_name_list))


def contact_all_viewers():
    jobs = []
    jobs.extend(user_config.maimai_high_level_jd)
    jobs.extend(maimai_helper.get_all_jobs_from_cache())
    viewers = []
    interrupt_flag = False
    if jobs is None or len(jobs) == 0:
        return
    for job in jobs:
        if interrupt_flag:
            break
        if job is None or 'jid' not in job or 'ejid' not in job:
            continue
        jid = job['jid']
        tmp_viewers = maimai_helper.get_all_job_viewers(jid)
        for viewer in tmp_viewers:
            if interrupt_flag:
                break
            if viewer is None or 'id' not in viewer:
                continue
            if 'recent_dc_chat' in viewer and viewer['recent_dc_chat'] == 1:
                continue
            if 'sdegree' not in viewer or '专' == viewer['sdegree']:
                continue
            u2_id = viewer['id']
            maimai_helper.contact_visitor(jid, u2_id)
            interrupt_flag = not maimai_helper.send_greetings_v2(jid, user_config.maimai_greeting, u2_id,
                                                                 user_config.maimai_contact_visitor_fr)
            if interrupt_flag:
                break
            if 'name' in viewer:
                viewers.append(viewer['name'])
                print(viewer['name'])
    feishu_bot.send_msg('【脉脉】已联系{}个职位查看者,列表:{}'.format(len(viewers), viewers))


def contact_all_recommenders():
    jobs = []
    jobs.extend(user_config.maimai_high_level_jd)
    jobs.extend(maimai_helper.get_all_jobs_from_cache())
    recommenders = []
    interrupt_flag = False
    if jobs is None or len(jobs) == 0:
        return
    for job in jobs:
        if interrupt_flag:
            break
        if job is None or 'jid' not in job or 'ejid' not in job:
            continue
        jid = job['jid']
        tmp_recommenders = maimai_helper.get_all_job_recommenders(jid)
        for recommender in tmp_recommenders:
            if interrupt_flag:
                break
            if recommender is None or 'id' not in recommender:
                continue
            if 'recent_dc_chat' in recommender and recommender['recent_dc_chat'] == 1:
                continue
            if 'sdegree' not in recommender or '专' == recommender['sdegree']:
                continue
            u2_id = recommender['id']
            maimai_helper.contact_visitor(jid, u2_id)
            interrupt_flag = not maimai_helper.send_greetings_v2(jid, user_config.maimai_greeting, u2_id,
                                                                 user_config.maimai_contact_recommend_fr)
            if interrupt_flag:
                break
            if 'name' in recommender:
                recommenders.append(recommender['name'])
                print(recommender['name'])
    feishu_bot.send_msg('【脉脉】已联系{}个职位推举者,列表:{}'.format(len(recommenders), recommenders))


def contact_all_talents():
    jobs = []
    jobs.extend(user_config.maimai_high_level_jd)
    jobs.extend(maimai_helper.get_all_jobs_from_cache())
    talents_list = []
    interrupt_flag = False
    if jobs is None or len(jobs) == 0:
        return
    for job in jobs:
        if interrupt_flag:
            break
        if job is None or 'jid' not in job or 'ejid' not in job:
            continue
        jid = job['jid']
        ejid = job['ejid']
        talent_list = maimai_helper.get_all_match_talent_list(ejid)
        for talent in talent_list:
            if interrupt_flag:
                break
            if talent is None or 'uid' not in talent or 'encode_mmid' not in talent:
                continue
            if 'recent_dc_chat' in talent and talent['recent_dc_chat'] == 1:
                continue
            if 'degree_str' not in talent or '专' == talent['degree_str']:
                continue
            encode_mmid = talent['encode_mmid']
            u2_id = talent['uid']
            maimai_helper.contact_visitor(jid, u2_id)
            interrupt_flag = not maimai_helper.send_greetings(encode_mmid, user_config.maimai_contact_recommend_source,
                                                              user_config.maimai_greeting,
                                                              jid, u2_id)
            if interrupt_flag:
                break
            if 'name' in talent:
                talents_list.append(talent['name'])
                print(talent['name'])
    feishu_bot.send_msg('【脉脉】已联系{}个职位推荐者,列表:{}'.format(len(talents_list), talents_list))


def upload_boss_resume():
    boss_job_dict = {}
    moka_job_dict = {}
    boss_job_list = boss_helper.get_job_detail_list()
    if boss_job_list is None or len(boss_job_list) == 0:
        return
    for boss_job in boss_job_list:
        if boss_job is None:
            continue
        if 'jobId' not in boss_job:
            continue
        boss_job_dict[boss_job['jobId']] = boss_job
    if len(boss_job_dict) == 0:
        return
    moka_jobs = moka_helper.get_moka_all_jobs_from_cache()
    if moka_jobs is None or len(moka_jobs) == 0:
        return
    for moka_job in moka_jobs:
        if moka_job is None or 'title' not in moka_job:
            continue
        moka_job_dict[moka_job['title']] = moka_job
    if len(moka_job_dict) == 0:
        return
    page_int = 1
    contacts = boss_helper.get_contacts(page_int)
    user_len = len(user_config.personal_info_list)
    resume_name_lists = []
    for i in range(0, user_len):
        resume_name_lists.append([])

    while len(contacts) > 0:
        for contact in contacts:
            if contact is None or 'encryptUid' not in contact or 'securityId' not in contact or 'uid' not in contact:
                continue
            security_id = contact['securityId']
            encrypt_uid = contact['encryptUid']
            uid = contact['uid']

            geek_info = boss_helper.get_geek_info(uid, security_id)
            if geek_info is None or 'edu' not in geek_info or geek_info[
                'edu'] is None:
                continue
            if '专' in geek_info['edu']:
                boss_helper.del_msg(encrypt_uid, security_id)
                continue
            low_degree = False
            if 'eduExpList' not in geek_info or geek_info['eduExpList'] is None:
                continue
            for exp in geek_info['eduExpList']:
                if exp is None or 'degree' not in exp:
                    continue
                if '专' in exp['degree']:
                    low_degree = True
                    break
            if low_degree:
                boss_helper.del_msg(encrypt_uid, security_id)
                continue
            if 'resumeVisible' in geek_info and geek_info['resumeVisible'] != 1:
                continue
            if 'jobId' not in geek_info:
                continue
            job_id = geek_info['jobId']
            job_name = ''
            if job_id in boss_job_dict:
                boss_job = boss_job_dict[job_id]
                if boss_job is not None:
                    if 'jobName' in boss_job and boss_job['jobName'] is not None:
                        job_name = boss_job['jobName']
            moka_job_job_id = user_config.moka_high_level_jid
            if not transfer_2_target_position_flag:
                if job_name not in moka_job_dict:
                    continue
                moka_job = moka_job_dict[job_name]
                moka_job_job_id = moka_job['id']

            index = 0
            if job_name == user_config.target_jon_title:
                index = int(time.time() * 1000) % user_len
            # 下载简历
            file_name = boss_helper.down_load_resume(encrypt_uid)
            if file_name is not None:
                resume_info = moka_helper.upload_cv(file_name, index)
                os.remove(file_name)

                apply_res = moka_helper.apply_cv(moka_job_job_id, resume_info, geek_info['name'], index)
                if apply_res:
                    if 'name' in contact:
                        resume_name = contact['name']
                        if 'positionName' in geek_info:
                            resume_name = geek_info['positionName'] + '-' + resume_name
                        resume_name_list = resume_name_lists[index]
                        resume_name_list.append(resume_name)
                    boss_helper.del_msg(encrypt_uid, security_id)
                    continue

        page_int += 1
        contacts = boss_helper.get_contacts(page_int)
    for i in range(0, user_len):
        resume_name_list = resume_name_lists[i]
        feishu_bot.send_msg('【BOSS】已上传{}份简历, 列表:{}'.format(len(resume_name_list), resume_name_list), i)


def ask_all_contacts():
    # boss_job_dict = {}
    asked_names = []
    # moka_job_dict = {}
    # boss_job_list = boss_helper.get_job_detail_list()
    # if boss_job_list is None or len(boss_job_list) == 0:
    #     return
    # for boss_job in boss_job_list:
    #     if boss_job is None:
    #         continue
    #     if 'jobId' not in boss_job:
    #         continue
    #     boss_job_dict[boss_job['jobId']] = boss_job
    # if len(boss_job_dict) == 0:
    #     return
    # moka_jobs = moka_helper.get_moka_all_jobs_from_cache()
    # if moka_jobs is None or len(moka_jobs) == 0:
    #     return
    # for moka_job in moka_jobs:
    #     if moka_job is None or 'title' not in moka_job:
    #         continue
    #     moka_job_dict[moka_job['title']] = moka_job
    # if len(moka_job_dict) == 0:
    #     return

    page_int = 1
    contacts = boss_helper.get_contacts(page_int)
    while len(contacts) > 0:
        for contact in contacts:
            if contact is None or 'encryptUid' not in contact or 'securityId' not in contact or 'uid' not in contact:
                continue
            security_id = contact['securityId']
            encrypt_uid = contact['encryptUid']
            uid = contact['uid']
            geek_info = boss_helper.get_geek_info(uid, security_id)
            if geek_info is None:
                continue
            if 'resumeVisible' in geek_info and geek_info['resumeVisible'] == 1:
                continue
            if 'bothTalked' in geek_info and not geek_info['bothTalked']:
                continue
            if 'securityId' in geek_info and 'toPositionId' in geek_info and 'encryptUid' in geek_info and 'encryptExpectId' in geek_info:
                if boss_helper.is_geek_asked(geek_info['encryptUid'], geek_info['encryptExpectId'],
                                             geek_info['toPositionId'],
                                             geek_info['securityId']):
                    continue

            # if 'jobId' not in geek_info:
            #     continue
            # job_id = geek_info['jobId']
            # job_name = ''

            # if job_id in boss_job_dict:
            #     boss_job = boss_job_dict[job_id]
            #     if boss_job is not None:
            #         if 'jobName' in boss_job and boss_job['jobName'] is not None:
            #             job_name = boss_job['jobName']

            # if not transfer_2_target_position_flag and job_name not in moka_job_dict:
            #     continue

            # 索要简历
            if 'bothTalked' in geek_info and geek_info['bothTalked']:
                boss_helper.ask_for_cv(security_id)
                boss_helper.del_msg(encrypt_uid, security_id)
                if 'name' in contact:
                    asked_names.append(contact['name'])
        page_int += 1
        contacts = boss_helper.get_contacts(page_int)
    feishu_bot.send_msg('【BOSS】已和{}人索要简历,列表:{}'.format(len(asked_names), asked_names))


def contact_boss_geek():
    geek_names = []
    boss_job_list = []
    # copy.deepcopy(user_config.boss_job_list)
    boss_job_list.extend(boss_helper.get_job_detail_list())
    for job in boss_job_list:
        for activation in user_config.boss_activation_list:
            if job is None or 'encryptJobId' not in job:
                continue
            geek_names.extend(boss_helper.contact_all_geeks(job['encryptJobId'], activation))
    feishu_bot.send_msg('【BOSS】已联系{}人推荐职位,列表:{}'.format(len(geek_names), geek_names))


def analyze_all_interviewee_list():
    analyze_interview_list('全部职位', '', '', '')
    now = datetime.now()
    this_week_start = now - timedelta(days=now.weekday())
    this_week_end = now + timedelta(days=6 - now.weekday())
    start_date = time.strftime(user_config.moka_time_template, time.localtime(time.mktime(this_week_start.timetuple())))
    end_date = time.strftime(user_config.moka_time_template, time.localtime(time.mktime(this_week_end.timetuple())))
    moka_helper.default_timeout = 0
    for job_id in copy.deepcopy(user_config.moka_target_job_ids):
        analyze_interview_list('全时间目标职位', job_id, '', '')
        analyze_interview_list('本周目标职位', job_id, start_date, end_date)


def analyze_interview_list(title, job_id, start_date, end_date):
    page = 1
    interviewee_dict = {}
    interviewee_list = moka_helper.get_interviewee_list(page, job_id, start_date, end_date)
    count = 0
    stage_count_dict = {}
    while len(interviewee_list) > 0:
        for interviewee in interviewee_list:
            count += 1
            if interviewee is None:
                continue
            stage = ''
            if 'stage' in interviewee:
                stage = interviewee['status']
            stage_count = 0
            if stage in stage_count_dict:
                stage_count = stage_count_dict[stage]
            stage_count += 1
            stage_count_dict[stage] = stage_count
            classified_job_dict = {}
            classified_interviewee = []
            if stage in interviewee_dict:
                classified_job_dict = interviewee_dict[stage]
            job_title = ''
            if 'jobTitle' in interviewee:
                job_title = interviewee['jobTitle']
            if job_title in classified_job_dict:
                classified_interviewee = classified_job_dict[job_title]
            classified_interviewee.append(interviewee)
            classified_job_dict[job_title] = classified_interviewee
            interviewee_dict[stage] = classified_job_dict
        page += 1
        interviewee_list = moka_helper.get_interviewee_list(page, job_id, start_date, end_date)

    msg = '【moka】【{}】总计推荐{}人 : '.format(title, count)
    for stage in interviewee_dict:
        classified_job_dict = interviewee_dict[stage]
        msg += '\r\n\r\n阶段【{}】共计{} 人'.format(stage, stage_count_dict[stage])
        if stage not in user_config.moka_stage_dict or not user_config.moka_stage_dict[stage]:
            for job_title in classified_job_dict:
                tmp_interviewee_list = classified_job_dict[job_title]
                tmp_msg = '\r\n职位【{}】共计{} 人,'.format(job_title, len(tmp_interviewee_list))

                tmp_msg += '列表 {}'.format(
                    list(map(lambda x: x['name'], tmp_interviewee_list)))
                msg += tmp_msg
    feishu_bot.send_msg(msg)


def contact_lagou_geek():
    geek_names = lagou_helper.contact_all_geeks()
    feishu_bot.send_msg('【拉钩】已联系{}人推荐职位,列表:{}'.format(len(geek_names), geek_names))


def ask_lagou_resume():
    asked_names = lagou_helper.ask_resume()
    feishu_bot.send_msg('【拉钩】已和{}人索要简历,列表:{}'.format(len(asked_names), asked_names))


def upload_lagou_resume():
    page = 1
    total_resume = []
    resume_names = []
    resume = lagou_helper.get_cv_list(page)
    while len(resume) > 0:
        total_resume.extend(resume)
        page += 1
        resume = lagou_helper.get_cv_list(page)
    for resume in total_resume:
        if resume is None or 'id' not in resume:
            continue

        file_name = lagou_helper.download_resume(resume)
        if file_name is not None:
            resume_name = ''
            if 'candidateName' in resume:
                resume_name = resume['candidateName']
            resume_info = moka_helper.upload_cv(file_name)
            os.remove(file_name)
            apply_res = moka_helper.apply_cv(user_config.moka_high_level_jid, resume_info, resume_name)
            if apply_res:
                lagou_helper.pass_cv(resume)
                if 'positionName' in resume:
                    resume_name = resume['positionName'] + '-' + resume_name
                resume_names.append(resume_name)

            continue
    feishu_bot.send_msg('【拉钩】已上传{}份简历, 列表:{}'.format(len(resume_names), resume_names))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(0)
    arg_input = sys.argv[1]
    func_dict = {
        'analyze_interviewees': [analyze_all_interviewee_list],
        'aloha': [aloha],
        'resume': [push_resume],
        'job': [sync_moka_jobs_2_maimai],
        'viewers_greetings': [contact_all_viewers, contact_all_visitors, contact_all_recommenders, contact_all_talents],
        'recommenders_greetings': [contact_all_recommenders, contact_all_talents],
        'upload_boss_resume': [upload_boss_resume],
        'contact_boss': [contact_boss_geek],
        'ask_boss_resume': [ask_all_contacts],
        'contact_lagou_geek': [contact_lagou_geek],
        'ask_lagou_resume': [ask_lagou_resume],
        'upload_lagou_resume': [upload_lagou_resume],
    }
    if arg_input not in func_dict:
        exit(0)
    func_list = func_dict[arg_input]
    for func in func_list:
        func()
