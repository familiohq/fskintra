#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json
import time
import os
import sys
import traceback

import skoleintra.config
import skoleintra.pgContactLists
import skoleintra.pgDialogue
import skoleintra.pgDocuments
import skoleintra.pgFrontpage
import skoleintra.pgWeekplans
import skoleintra.schildren

def run(identifier, username, password, hostname):
    skoleintra.config.IDENTIFIER = identifier
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
SUBSCRIBE_CHANNEL = os.environ['SUBSCRIBE_CHANNEL']

redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
pubSub = redisClient.pubsub(ignore_subscribe_messages=True)

pubSub.subscribe(SUBSCRIBE_CHANNEL)

print 'listening on redis %s:%s/%s ... - ctrl+c to interrupt' % (REDIS_HOST, REDIS_PORT, SUBSCRIBE_CHANNEL)

try:
    while True:
        message = pubSub.get_message()
        if message:
            try:
                data = json.loads(message['data'])
                run(data['id'], data['username'], data['password'], data['hostname'])
            except:
                print('E: failed running integration')
                traceback.print_exc(file=sys.stdout)
        time.sleep(0.001)
except KeyboardInterrupt:
    print("W: interrupt received, stopping…")
