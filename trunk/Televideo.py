#!/usr/bin/env python
# -*- coding: utf-8 -*-

def analizza(pagina, i):
    from urllib2 import urlopen
    return _analizza(urlopen('http://www.televideo.rai.it/televideo/pub/'
            'solotesto.jsp?pagina=%s&sottopagina=0%s' % (pagina, i)).read())

def _analizza(html):
    """WARN: very black magik - la sto scrivendo e non so quel che fa"""
    from BeautifulSoup import BeautifulSoup, NavigableString
    return ''.join(filter(lambda x: isinstance(x, NavigableString),
            BeautifulSoup(html)('td', width='450', height='380', align='center',
            valign='middle')[0]('pre')[0].contents[2:]))

def cli(page):
    from curses import initscr, error, endwin, KEY_DOWN, KEY_UP
    from locale import setlocale, LC_ALL, getpreferredencoding

    setlocale(LC_ALL, '')

    text = []
    for i in 1, 2, 3:
        text += analizza(page, i).encode(getpreferredencoding()).split('\n')

    text_len = len(text)
    i = 0
    screen = initscr()
    screen.keypad(1)
    while True:
        screen_height = screen.getmaxyx()[0]      # terminale ridimensionabile
        screen.erase()
        screen.addstr('\n'.join(text[i:screen_height+i]))
        char = screen.getch()
        if char == ord('q'):
            break
        elif char in (ord('z'), KEY_DOWN) and screen_height + i < text_len:
            i += 1
        elif char in (ord('a'), KEY_UP) and i:
            i -= 1
        else:
            pass            # ignore chars not in (a, q, z, KEY_UP, KEY_DOWN)
    endwin()

def dump(pagina):
    for i in 1, 2, 3:
        print analizza(pagina, i),

def gui(argv, pagina):
    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit

    app = QApplication(argv)
    mainWindow = QMainWindow()
    textEdit = QTextEdit()

    mainWindow.setCentralWidget(textEdit)
    mainWindow.show()
    textEdit.setReadOnly(True)
    textEdit.setText(''.join(analizza(pagina, i) for i in (1, 2, 3)))

    raise SystemExit(app.exec_())


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(version = '%prog 0.8.0')
    parser.add_option('-g', '--gui', action='store_true', default=False,
            help="Force the qt4 gui interface")
    parser.add_option('-c', '--cli', action='store_true', default=False,
            help="Force the ncurses cli interface")
    parser.add_option('-p', '--page', type="int", default=505,
            help="Show this page")
    parser.add_option('-d', '--dump', action='store_true', default=False,
            help="Force the 'just dump the content of the page' iterface")
    options, args = parser.parse_args()

    if sum(int(value) for value in [options.gui, options.cli, options.dump]) > 1:
        raise SystemExit("Puoi scegliere un'unica opzione di visualizzazione!")

    if options.gui:
        gui(args, options.page)
    elif options.cli:
        cli(options.page)
    elif options.dump:
        dump(options.page)
    else:
        from os import environ

        if not environ.has_key('TERM') or environ['TERM'] in ('xterm', 'rxvt',
                'xterm-color'):
            cli(options.page)
        else:
            gui(args, options.page)
