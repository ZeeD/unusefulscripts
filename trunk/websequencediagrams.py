#!/usr/bin/env python

from urllib import urlencode, urlopen, urlretrieve
from re import compile

def getSequenceDiagram(text, outputFile, style='default'):
    wsd = 'http://www.websequencediagrams.com/'
    f = urlopen(wsd, urlencode({ 'message': text, 'style': style }))
    m = compile("(\?img=[a-zA-Z0-9]+)").search(f.readline())
    f.close()

    if m is None:
        print "Invalid response from server."
    else:
        urlretrieve(wsd + m.group(0), outputFile)
    return m is not None

if __name__ == '__main__':
    style = "qsd"
    text = "alice->bob: authentication request\nbob-->alice: response"
    pngFile = "out.png"
    getSequenceDiagram(text, pngFile, style)
