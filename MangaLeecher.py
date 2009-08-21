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

IMG_FORMAT = '%s - %s - %s.jpg' # MANGA - CHAPTER - PAGE.jpg
CBT_FORMAT = '%s - %s.cbt'      # MANGA - CHAPTER.cbt

def start_chapter(options):
    '''Find the initial chapter to download
        using the --start-chapter and a mix of --out-dir and --cbt options'''
    from os import listdir
    end = '.cbt' if options.cbt else '.jpg'
    entries = listdir(options.out_dir)
    if not entries:
        last_chapter = '0'
    else:
        last_fn = sorted(f for f in entries if f.endswith(end))[-1]
        if options.cbt:
            last_chapter = last_fn.split(' - ')[-1][:-4]
        else:
            last_chapter = last_fn.split(' - ')[-2]
    if int(options.start_chapter) > int(last_chapter):
        return options.start_chapter
    return str(int(last_chapter)+1)

def leech(manga, options):
    '''Download all manga pages
        @param manga the name of the manga
        @start_chapter start downloading from this chapter
        @outdir the directory where the files where downloaded
    '''
    from os.path import join
    from sys import stdout
    from tempfile import mkdtemp
    from tarfile import open as taropen
    from shutil import rmtree
    chapter = start_chapter(options)
    while True:
        soup = BeautifulSoup(urlopen('http://www.onemanga.com/%s/%s/' %
                (manga, chapter)).read())
        if len(soup('p')) == 2:
            break   # chapter not existent
        soup = BeautifulSoup(urlopen('http://www.onemanga.com%s' %
                soup('a')[-3].attrs[0][1]).read())
        if options.cbt:
            tmpdir = mkdtemp()
        if options.verbose:
            stdout.write('Downloading chapter %s' % chapter)
            stdout.flush()
        for option in soup('select',attrs={'id':'id_page_select'})[0]('option'):
            page = option.attrs[0][1]
            soup = BeautifulSoup(urlopen('http://www.onemanga.com/%s/%s/%s' %
                    (manga, chapter, page)).read())
            img = soup('div', attrs={'class': 'one-page'})[0]('img')[0]
            imagelink = dict(img.attrs)['src']
            if options.cbt:
                filename = join(tmpdir, IMG_FORMAT % (manga, chapter, page))
            else:
                filename = join(options.out_dir,IMG_FORMAT%(manga,chapter,page))
            with open(filename, 'w') as outfile:
                outfile.write(urlopen(imagelink).read())
            if options.verbose:
                stdout.write('.')
                stdout.flush()
        if options.cbt:
            tar_filename = join(options.out_dir, CBT_FORMAT % (manga, chapter))
            if options.verbose:
                stdout.write('Compressing')
                stdout.flush()
            tar_file = taropen(tar_filename, 'w:gz')
            tar_file.add(tmpdir)
            tar_file.close()
            rmtree(tmpdir)
        chapter = str(int(chapter) + 1)
        if options.verbose:
            stdout.write('\n')
            stdout.flush()

def main():
    '''"main" function'''
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.1.5', usage='''%prog [OPTS] MANGA
        Scarica le immagini dei capitoli di MANGA from www.onemanga.com''')
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
