# Hound

## What's Hound

Hound is an experiment tool for learning python, besides effect for auto hunting.

This repo is just for learning python, we recommend that you use this repo to learning python obeying the law.
Oppositely, if you use this tool to make you purpose that result in any violation of the law in you country or district,
we take no responsibilities for we already claim that.

It's suitable for you if you have no enough time to seek candidates, hound will auto seek candidates, start conversation
and send invitation.

## V1

In this version, you will need configure in user_config.py .

## V2

## Deploy

Just clone this repo, and install python3 runtime, then install packages from requirements.txt .

And we recommend you make a cron table. Just like below:

`0 11 * * * flock -xn /tmp/leet_code_problem.lock -c 'cd /opt/repo/hound && nohup /usr/local/bin/python3 leetcode.py  >> leetcode.log 2>&1 &'`
