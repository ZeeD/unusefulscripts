#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''onemanga.com leecher
    Designed to download all manga pages of a manga for an off-line read :)
'''

IMG_EXT = '.jpg'
CBT_EXT = '.cbt'
IMG_FORMAT = '%s - %s - %s' + IMG_EXT # MANGA - CHAPTER - PAGE.jpg
CBT_FORMAT = '%s - %s' + CBT_EXT      # MANGA - CHAPTER.cbt

BASEURL = 'www.onemanga.com'
BASEURL_1000 = 'www.1000manga.com'

from urllib2 import urlopen, URLError, HTTPError
from os import listdir
from BeautifulSoup import BeautifulSoup
from os.path import join
from sys import stdout,stderr
from tempfile import mkdtemp
from tarfile import open as taropen
from shutil import rmtree
from atexit import register
from httplib import BadStatusLine
from optparse import OptionParser

def list_chapters(manga):
    '''Show on STDOUT the list of the avalable chapters of the manga
        @param manga the name of the manga
    '''
    contents = []
    soup = BeautifulSoup(urlopen('http://%s/%s/' % (BASEURL, manga)).read())
    for td in soup(name='td', attrs={'class': 'ch-subject'}):
        contents.append(td.contents[0].contents[0])
    return '\n'.join(reversed(contents))

def start_chapter(options):
    '''Find the initial chapter to download
        using the --start-chapter and a mix of --out-dir and --cbt options'''
    end = CBT_EXT if options.cbt else IMG_EXT
    entries = sorted(f for f in listdir(options.out_dir) if f.endswith(end))
    if not entries:
        last_chapter = 0
    else:
        last_fn = entries[-1]
        if options.cbt:
            last_chapter = int(last_fn.split(' - ')[-1][:-4])
        else:
            last_chapter = int(last_fn.split(' - ')[-2])
    if int(options.start_chapter) > last_chapter:
        return options.start_chapter
    return str(last_chapter+1)

from sys import stderr

def leech(manga, options):
    '''Download all manga pages
        @param manga the name of the manga
        @start_chapter start downloading from this chapter
        @outdir the directory where the files where downloaded
    '''
    global BASEURL
    chapter = start_chapter(options)
    if options.cbt:
        tmpdirs = []
        register(lambda:[rmtree(tmpdir) for tmpdir in tmpdirs])
    while True:
        if options.debug:
            stderr.write('urlopen(http://%s/%s/%s)\n' %
                    (BASEURL, manga, chapter))
        soup = BeautifulSoup(urlopen('http://%s/%s/%s' %
                (BASEURL, manga, chapter)).read())
        if len(soup('p')) == 2:
            break   # chapter not existent
        if options.debug:
            stderr.write('urlopen(http://%s%s)\n' %
                    (BASEURL, soup('a')[-3].attrs[0][1]))
        try:
            soup = BeautifulSoup(urlopen('http://%s%s' %
                    (BASEURL, soup('a')[-3].attrs[0][1])).read())
            opts = soup('select',attrs={'id':'id_page_select'})[0]('option')
        except Exception as e:
#            import pdb; pdb.set_trace()
            soup = BeautifulSoup(urlopen('%s' % (soup('a')[-3].attrs[0][1], )).read())
            firstPage = dict(soup('div',
                    attrs={'id':'chapter-link'})[0]('a')[0].attrs)['href']
            BASEURL = BASEURL_1000
            soup = BeautifulSoup(urlopen('http://%s%s' % (BASEURL, firstPage)).read())
            opts = soup('select',attrs={'id':'id_page_select'})[0]('option')
        if options.cbt:
            tmpdirs.append(mkdtemp())
        if options.verbose:
            stdout.write('Downloading chapter %s' % chapter)
            stdout.flush()
        for option in opts:
            try:
                page = option.attrs[0][1]
                soup = BeautifulSoup(urlopen('http://%s/%s/%s/%s' %
                        (BASEURL, manga, chapter, page)).read())
                img = soup('div', attrs={'class': 'one-page'})[0]('img')[0]
                imagelink = dict(img.attrs)['src']
                if options.cbt:
                    filename = join(tmpdirs[-1],
                            IMG_FORMAT % (manga, chapter, page))
                else:
                    filename = join(options.out_dir, IMG_FORMAT %
                            (manga,chapter,page))
                with open(filename, 'w') as outfile:
                    outfile.write(urlopen(imagelink).read())
                if options.verbose:
                    stdout.write('.')
                    stdout.flush()
            except (BadStatusLine, URLError, HTTPError):
                stderr.write(
                        "Error on baseurl=%s, manga=%s, chapter=%s, page=%s\n" %
                        (BASEURL, manga, chapter, page))
                opts.append(option)
        if options.cbt:
            tar_filename = join(options.out_dir, CBT_FORMAT % (manga, chapter))
            if options.verbose:
                stdout.write('Compressing')
                stdout.flush()
            tar_file = taropen(tar_filename, 'w:gz')
            tar_file.add(tmpdirs[-1])
            tar_file.close()
        chapter = str(int(chapter) + 1)
        if options.verbose:
            stdout.write('\n')
            stdout.flush()

def main():
    '''"main" function'''
    parser = OptionParser(version='%prog 0.1.5', usage='''%prog [OPTS] MANGA
        Scarica le immagini dei capitoli di MANGA from ''' + BASEURL)
    parser.add_option('-z', '--cbt', action='store_true',
            help='Comprimi i capitoli in file .cbt (AKA .tar.gz rinominati)')
    parser.add_option('-v', '--verbose', action='store_true',
            help='Mostra su STDOUT cosa accade')
    parser.add_option('-d', '--out-dir', type=str, default='.', metavar='DIR',
            help='Scarica le immagini nella directory DIR (default=%default)')
    parser.add_option('-l', '--list', action='store_true',
            help='Non scaricare nulla: invece mostra i capitoli disponibili')
    parser.add_option('-c', '--start-chapter', type=str, default='1',
            metavar='N', help='Inizia a scaricare dal capitolo N')
    parser.add_option('--debug', action='store_true', help=u'Modalità debug')
    # TODO: add an option to create a subdir named MANGA
    options, args = parser.parse_args()
    if not args:
        exit(parser.print_usage())
    manga_name = '_'.join(args) # maybe an overkill
    if options.list:
        exit(list_chapters(manga=manga_name))
    leech(manga=manga_name, options=options)

if __name__ == '__main__':
    main()
