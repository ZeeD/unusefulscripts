#!/usr/bin/env python

import urllib2
import json
from datetime import date, datetime

class Channel(object):
    fmt_str = 'http://guidatv.sky.it/app/guidatv/contenuti/data/grid/%s/ch_%s.js'

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.events = []

    @property
    def url(self):
        t = date.today()

        return Channel.fmt_str % ('%02d_%02d_%02d' % (t.year % 100, t.month, t.day), self.id)

class Event(object):
    def __init__(self, starttime, dur, title):
        self.starttime = starttime
        self.dur = dur
        self.title = title

class NotHasHattr(Exception):
    def __init__(self, obj, k):
        self.obj = obj
        self.k = k

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.obj, self.k)

class NotIsInstance(Exception):
    def __init__(self, obj, cls):
        self.obj = obj
        self.cls = cls

    def __str__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.obj, self.cls)

def fetch(url):
    return json.loads(urllib2.urlopen(url).read())

def fetch_channels():
    list_url = 'http://guidatv.sky.it/app/guidatv/contenuti/data/grid/grid_digitale_channels.js'

    return [ Channel(obj['id'], obj['name']) for obj in fetch(list_url) ]

def fetch_channel(channel_url):
    json = fetch(channel_url)

    return [ Event(obj['starttime'], obj['dur'], obj['title']) for obj in json['plan'] ]

def display(channels):
    n = datetime.now()
    now = '%02d:%02d' % (n.hour, n.minute)

    for channel in channels:
        rowdata = [ channel.name ]
        i = 0
        for j, event in enumerate(channel.events):
            if i >= 4:
                break
            if event.starttime < now:
                continue
            if i == 0:
                rowdata += [ '%30s@%s' % (channel.events[j-1].title, channel.events[j-1].starttime) ]
            rowdata += [ '%30s@%s' % (event.title, event.starttime) ]
            i += 1
        print('|'.join('%20s' % e for e in rowdata))

def main():
    channels = fetch_channels()
    for channel in channels:
        try:
            events = fetch_channel(channel.url)
        except urllib2.HTTPError as e:
            print('%s -> %s' % (channel.url, e))
        else:
            channel.events += events
    display(channels)

if __name__ == '__main__':
    main()
