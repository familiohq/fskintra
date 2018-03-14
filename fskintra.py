#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json
import time
import os

import skoleintra.config
import skoleintra.pgContactLists
import skoleintra.pgDialogue
import skoleintra.pgDocuments
import skoleintra.pgFrontpage
import skoleintra.pgWeekplans
import skoleintra.schildren

def run(username, password, hostname):
    skoleintra.config.USERNAME = username
    skoleintra.config.PASSWORD = skoleintra.config.b64enc(password)
    skoleintra.config.HOSTNAME = hostname
    skoleintra.config.CACHEPREFIX = '%s-%s' % (username, hostname)

    cnames = skoleintra.schildren.skoleGetChildren()
    for cname in cnames:
        skoleintra.schildren.skoleSelectChild(cname)

        skoleintra.pgContactLists.skoleContactLists()
        skoleintra.pgFrontpage.skoleFrontpage()
        skoleintra.pgDialogue.skoleDialogue()
        skoleintra.pgDocuments.skoleDocuments()
        skoleintra.pgWeekplans.skoleWeekplans()

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
INTEGRATION_CHANNEL = os.environ['INTEGRATION_CHANNEL']

redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
pubSub = redisClient.pubsub(ignore_subscribe_messages=True)

pubSub.subscribe(INTEGRATION_CHANNEL)

print 'listening on redis %s:%s/%s ... - ctrl+c to interrupt' % (REDIS_HOST, REDIS_PORT, INTEGRATION_CHANNEL)

try:
    while True:
        message = pubSub.get_message()
        if message:
            try:
                data = json.loads(message['data'])
                run(data['username'], data['password'], data['hostname'])
            except:
                print('E: failed running integration')
        time.sleep(0.001)
except KeyboardInterrupt:
    print("W: interrupt received, stopping…")
