#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import os
import sys
import traceback
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import skoleintra.config
import skoleintra.pgContactLists
import skoleintra.pgDialogue
import skoleintra.pgDocuments
import skoleintra.pgFrontpage
import skoleintra.pgWeekplans
import skoleintra.schildren

class NotificationServer(BaseHTTPRequestHandler):
    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        run(data['id'], data['username'], data['password'], data['hostname'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write('{ "foo": "bar" }')

def run(identifier, username, password, hostname):
    skoleintra.config.IDENTIFIER = identifier
    skoleintra.config.USERNAME = username
    skoleintra.config.PASSWORD = skoleintra.config.b64enc(password)
    skoleintra.config.HOSTNAME = hostname
    skoleintra.config.CACHEPREFIX = '%s-%s' % (username, hostname)

    # skoleintra.config.SKIP_CACHE = True

    cnames = skoleintra.schildren.skoleGetChildren()
    for cname in cnames:
        skoleintra.schildren.skoleSelectChild(cname)

        # skoleintra.pgContactLists.skoleContactLists()
        # skoleintra.pgFrontpage.skoleFrontpage()
        skoleintra.pgDialogue.skoleDialogue()
        # skoleintra.pgDocuments.skoleDocuments()
        # skoleintra.pgWeekplans.skoleWeekplans()

    skoleintra.config.log(u'Afslutter kørsel for bruger %s' % username)

PORT = int(os.environ['PORT'])

httpd = HTTPServer(('', PORT), NotificationServer)
print 'Listening for notifications on port %s... (press ctrl+c to interrupt)' % PORT

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("W: interrupt received, stopping…")
