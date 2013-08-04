#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import datetime
import dbus
import email.utils
import functools
import httplib
import itertools
import os
import time
import urllib2
import sys

LOCAL_PATH = '/var/lib/slackpkg/ChangeLog.txt'
REMOTE_DOMAIN = 'mirror2.mirror.garr.it'
REMOTE_PATH = '/pub/1/slackware/slackware64-current/ChangeLog.txt'
TEXT_ENCODING = 'latin1'


class debug(object):
    '''decorate function to trace the callstack'''
    enabled = False
    fmt = '{}%s [%s: %s]\n'

    def __init__(self, fun):
        self.fun = fun
        self.fmt = debug.fmt.format(self.fun.func_name)

    def __call__(self, *args):
        try:
            ret = self.fun(*args)
            if debug.enabled:
                sys.stderr.write(self.fmt % (args, 'ret', ret))
            return ret
        except Exception as e:
            if debug.enabled:
                sys.stderr.write(self.fmt % (args, 'e', e))
            raise


@debug
def remote_last_modified():
    '''find the last modified time on the remote changelog'''
    conn = httplib.HTTPConnection(REMOTE_DOMAIN)
    conn.request('HEAD', REMOTE_PATH)
    res = conn.getresponse()
    last_modified_header = res.getheader('last-modified')
    last_modified_parsed = email.utils.parsedate(last_modified_header)
    return datetime.datetime(*last_modified_parsed[:6])


@debug
def local_last_modified():
    '''find the last modified time on my machine'''
    mtime = os.path.getmtime(LOCAL_PATH)
    return datetime.datetime.fromtimestamp(mtime)


@debug
def remote_content():
    '''retrieve the remote changelog'''
    remote = urllib2.urlopen('http://' + REMOTE_DOMAIN + REMOTE_PATH)
    return remote.read().decode(TEXT_ENCODING).split('\n')


@debug
def local_content():
    '''retrieve the local changelog content
    (in pratice I just need the first row)
    '''
    with open(LOCAL_PATH) as local:
        return local.read().decode(TEXT_ENCODING).split('\n')


@debug
def diff(list1, list2):
    '''not a real differ, it expect list1 = [new1|new2|new3] + list2
    return all first element of list1; break if found in the head row of list2
    '''
    return itertools.takewhile(lambda row: row != list2[0], list1)


@debug
def notify(news):
    '''send a popup to kde with the news'''

    dbus.SessionBus().get_object('org.kde.knotify', '/Notify').event(
        'warning',
        'kde',
        [],
        'SlackNews',
        '<p>' + '<br />'.join(news) + '</p>',
        [],
        [],
        0,
        0,
        dbus_interface='org.kde.KNotify')


@debug
def main():
    '''main loop body
    check for news; if true, show a popup on kde.
    '''
    remote = remote_last_modified()
    local = local_last_modified()
    local_is_newer = local < remote
    if local_is_newer:  # there are news!
        remote = remote_content()
        local = local_content()
        news = diff(remote, local)
        notify(news)


@debug
def loop():
    '''main loop
    every hour call the main loop body
    '''
    while True:
        try:
            main()
            time.sleep(60 * 60)     # one hour, in seconds
        except KeyboardInterrupt:
            raise SystemExit('\nbye!')


if __name__ == '__main__':
    #debug.enabled = True
    #main()
    loop()
