# -*- coding:UTF-8 -*-

import requests
import json
import datetime
import user_config
import feishu_bot


def random_problem():
    url = "https://leetcode.com/graphql/"

    payload = json.dumps({
        "query": "\n    query randomQuestion($categorySlug: String, $filters: QuestionListFilterInput) {\n  randomQuestion(categorySlug: $categorySlug, filters: $filters) {\n    titleSlug\n  }\n}\n    ",
        "variables": {
            "categorySlug": "",
            "filters": {}
        },
        "operationName": "randomQuestion"
    })
    headers = {
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'authorization': '',
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Referer': 'https://leetcode.com/problemset/all/',
        'x-csrftoken': 'zVXhfWg3mjLQxIaUgbDw7jCzdgiPj2tyNPAlyi2RlOmhzGlDA8HYflE14Tj66oVZ',
        'sec-ch-ua-platform': '"macOS"',
        'Cookie': 'LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTIzMzAzOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTM2N2E0NGUxNjQ1Y2VkYjk5MWRiZTgxZjBjZGUwNjI2M2UwYmUyOSIsImlkIjoxMjMzMDM5LCJlbWFpbCI6IjM2MjUxOTQ4OUBxcS5jb20iLCJ1c2VybmFtZSI6InZ2dnZhaW5tYW4iLCJ1c2VyX3NsdWciOiJ2dnZ2YWlubWFuIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL3Z2dnZhaW5tYW4vYXZhdGFyXzE1NTIzNjA2MDMucG5nIiwicmVmcmVzaGVkX2F0IjoxNjM3MTE1MTAwLCJpcCI6IjYwLjE5MS4xMDIuMjE5IiwiaWRlbnRpdHkiOiIwMzIxNDViODQ3N2Q2YjNmYjM0ZTBlNTk1NGI1OWIyNCIsInNlc3Npb25faWQiOjE0NzMzMDc1LCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.iK4-01d4ws9woagW3NGBmqEXPcaqxY2xVOCIf-loAP8; csrftoken=NLrkHSs0scYqkig5SH9oa945x80zyu5yklO6wt0hcy6cEZzNwMCmlhr9rnqsxAE9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    json_data = response.json()
    if json_data is None:
        return ''
    if 'data' not in json_data or 'randomQuestion' not in json_data['data'] \
            or 'titleSlug' not in json_data['data']['randomQuestion']:
        return ''
    return json_data['data']['randomQuestion']['titleSlug']


if __name__ == '__main__':
    problem = random_problem()
    problem_url = 'https://leetcode.com/problems/{}'.format(problem)
    now = datetime.datetime.now()
    now_str = now.strftime('%Y年%m月%d日')
    model = user_config.get_problem_card_model(now_str, problem, problem_url)

    print(now_str)
    feishu_bot.send_card('oc_3dcfde3b13a3c8ff90cd1f0d22b5cce9', model)
