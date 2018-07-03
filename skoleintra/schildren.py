# -*- coding: utf-8 -*-

import config
import surllib

def urlPrefix():
    return 'http://%s/Infoweb/Fi2/' % config.HOSTNAME

def url():
    return '%sFaneblade.asp' % urlPrefix()

NAMES_IGNORE = [u'Skolebestyrelsen', u'Kontaktforældre']

# map of children => pageToSelectChild
_children = None


def skoleGetChildren():
    '''Returns of list of "available" children in the system'''
    global _children

    # reset list of children
    _children = None

    # reset login
    surllib.resetSkoleLogin()

    # ensure that we are logged in
    surllib.skoleLogin() # done automatically later

    config.log(u'Henter liste af børn')

    if not _children:
        data = surllib.skoleGetURL(url(), asSoup=True, noCache=True)
        if not data:
            return []

        _children = {}
        for a in data.findAll('a'):
            href = a['href']
            name = a.span.text

            if name in NAMES_IGNORE:
                config.log(u'Ignorerer [%s]' % name)
                continue

            _children[name] = href

    return sorted(_children.keys())


def skoleSelectChild(name):
    global _children
    assert(name in _children)

    if name == config.CHILDNAME:
        config.log(u'[%s] er allerede valgt som barn' % name)
    else:
        config.log(u'Vælger [%s]' % name)
        url = urlPrefix() + _children[name]
        surllib.skoleGetURL(url, False, noCache=True)
        config.CHILDNAME = name

if False:
    c = skoleGetChildren()
    print repr(_children)
    for cname in c:
        print cname
        skoleSelectChild(cname)
