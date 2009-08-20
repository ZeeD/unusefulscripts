#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''onemanga.com leecher
    Designed to download all manga pages of a manga for an off-line read :)
'''

from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

def list_chapters(manga):
    '''Show on STDOUT the list of the avalable chapters of the manga
        @param manga the name of the manga
    '''
    contents = []
    soup = BeautifulSoup(urlopen('http://www.onemanga.com/%s/' % manga).read())
    for td in soup(name='td', attrs={'class': 'ch-subject'}):
        contents.append(td.contents[0].contents[0])
    return '\n'.join(reversed(contents))

def leech(manga, start_chapter, outdir):
    '''Download all manga pages
        @param manga the name of the manga
        @start_chapter start downloading from this chapter
        @outdir the directory where the files where downloaded
    '''
    from os.path import join
    chapter = start_chapter
    while True:
        soup = BeautifulSoup(urlopen('http://www.onemanga.com/%s/%s/' %
                (manga, chapter)).read())
        if len(soup('p')) == 2:
            break   # chapter not existent
        soup = BeautifulSoup(urlopen('http://www.onemanga.com%s' %
                soup('a')[-3].attrs[0][1]).read())
        for option in soup('select',attrs={'id':'id_page_select'})[0]('option'):
            page = option.attrs[0][1]
            soup = BeautifulSoup(urlopen('http://www.onemanga.com/%s/%s/%s' %
                    (manga, chapter, page)).read())
            img = soup('div', attrs={'class': 'one-page'})[0]('img')[0]
            imagelink = dict(img.attrs)['src']
            filename = join(outdir, '%s - %s - %s.jpg' % (manga, chapter, page))
            with open(filename, 'w') as outfile:
                outfile.write(urlopen(imagelink).read())
        chapter = str(int(chapter) + 1)

def main():
    '''"main" function'''
    from sys import argv    # TODO: use OptionParser!
    progname, args = argv[0], argv[1:]
    if not args:
        exit("Usage: %s [OPTIONS] manganame [start_chapter]" % progname)
    if len(args) == 1:
        exit(list_chapters(manga=args[0]))
    from os import curdir
    leech(manga=args[0], outdir=curdir, start_chapter=args[1])

if __name__ == '__main__':
    main()
