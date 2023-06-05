#!/usr/bin/env python

def analizza(pagina):
    from urllib2 import urlopen
    from BeautifulSoup import BeautifulSoup
    # WARN: very black magik - la sto scrivendo e non so quel che fa
    return ''.join(BeautifulSoup(urlopen(
            'http://www.televideo.rai.it/televideo/pub/catturaSottopagine.jsp?'
            'pagina=%d' % pagina, timeout=3).read())('pre')[0].contents[5:20:7]) # 5,12,19

def cli(page):
    from curses import initscr, error, endwin, KEY_DOWN, KEY_UP
    from locale import setlocale, LC_ALL, getpreferredencoding

    setlocale(LC_ALL, '')

    text = analizza(page).encode(getpreferredencoding()).split('\n')

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
    print(analizza(pagina))

def gui(argv, pagina):
    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit

    app = QApplication(argv)
    mainWindow = QMainWindow()
    textEdit = QTextEdit()

    mainWindow.setCentralWidget(textEdit)
    mainWindow.show()
    textEdit.setReadOnly(True)
    textEdit.setText(analizza(pagina))

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
