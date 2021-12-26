from analysis_source import *


def analysis():
    sendDict = {}
    notice_send_count_key = '通知发送量'
    distinct_notice_send_count_key = '通知去重发送量'
    ann_send_count_key = '公告发送量'
    distinct_ann_send_count_key = '公告去重发送量'
    know_send_count_key = '知识发送量'
    distinct_know_send_count_key = '知识去重发送量'
    notice_read_count_key = '通知阅读量'
    ann_read_count_key = '公告阅读量'
    know_read_count_key = '知识阅读量'
    for bucket in sendTotal:
        date = bucket['key_as_string']
        arr1 = bucket['group_by_status']['buckets']
        notice_count = 0
        annon_count = 0
        know_count = 0
        notice_distinct_count = 0
        annon_distinct_count = 0
        know_distinct_count = 0

        for b in arr1:
            if b['key'] == 1:
                notice_count = b['doc_count']
                notice_distinct_count = b['distinct_name']['value']
            elif b['key'] == 2:
                annon_count = b['doc_count']
                annon_distinct_count = b['distinct_name']['value']
            else:
                know_count = b['doc_count']
                know_distinct_count = b['distinct_name']['value']
        d1 = {
            notice_send_count_key: notice_count, ann_send_count_key: annon_count, know_send_count_key: know_count,
            distinct_notice_send_count_key: notice_distinct_count, distinct_ann_send_count_key: annon_distinct_count,
            distinct_know_send_count_key: know_distinct_count
        }
        sendDict[date] = d1

    readDict = {}
    for bucket in readTotal:
        date = bucket['key_as_string']
        arr1 = bucket['group_by_status']['buckets']
        notice_count = 0
        annon_count = 0
        know_count = 0
        for b in arr1:
            if b['key'] == 1:
                notice_count = b['doc_count']
            elif b['key'] == 2:
                annon_count = b['doc_count']
            else:
                know_count = b['doc_count']
        d1 = {
            notice_read_count_key: notice_count, ann_read_count_key: annon_count, know_read_count_key: know_count
        }
        readDict[date] = d1

    import csv

    with open(file='消息中心统计.csv', encoding='utf-8', mode='w') as f:
        csv_writer = csv.writer(f)
        heads = ['']
        notice_send_arr = [notice_send_count_key]
        distinct_notice_send_arr = [distinct_notice_send_count_key]
        ann_send_arr = [ann_send_count_key]
        distinct_ann_send_arr = [distinct_ann_send_count_key]
        know_send_arr = [know_send_count_key]
        distinct_know_send_arr = [distinct_know_send_count_key]
        notice_read_arr = [notice_read_count_key]
        ann_read_arr = [ann_read_count_key]
        know_read_arr = [know_read_count_key]
        for d in sendDict:
            heads.append(d)
            v = sendDict[d]
            notice_send_arr.append(v[notice_send_count_key])
            ann_send_arr.append(v[ann_send_count_key])
            know_send_arr.append(v[know_send_count_key])
            distinct_notice_send_arr.append(v[distinct_notice_send_count_key])
            distinct_ann_send_arr.append(v[distinct_ann_send_count_key])
            distinct_know_send_arr.append(v[distinct_know_send_count_key])
        for d in readDict:
            v = readDict[d]
            notice_read_arr.append(v[notice_read_count_key])
            ann_read_arr.append(v[ann_read_count_key])
            know_read_arr.append(v[know_read_count_key])
        csv_writer.writerow(heads)
        csv_writer.writerow(notice_send_arr)
        csv_writer.writerow(distinct_notice_send_arr)
        csv_writer.writerow(ann_send_arr)
        csv_writer.writerow(distinct_ann_send_arr)
        csv_writer.writerow(know_send_arr)
        csv_writer.writerow(distinct_know_send_arr)
        csv_writer.writerow(notice_read_arr)
        csv_writer.writerow(ann_read_arr)
        csv_writer.writerow(know_read_arr)


if __name__ == '__main__':
    analysis()
