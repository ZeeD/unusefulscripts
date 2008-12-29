#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-10-13 - Uso di optparse per capire che cavolo fa il programma
# 2007-08-21 - Passaggio a PyQt4 (pykde dava errori)
# 2007-08-21 - Verifica se viene lanciato da terminale
# 2007-08-12 - Interfaccia grafica tramite pykde
# 2007-08-08 - Patch per KEY_UP / KEY_DOWN
# 2007-08-08 - Uso di curses
# 2007-08-08 - Patch per <a href='...'>777</a>
# 2007-08-07 - Versione iniziale
# Televideo.py
#
# sostituto di
# alias televideo='for i in 1 2 3;do lynx "www.televideo.rai.it/televideo/pub/solotesto.jsp?pagina=505&sottopagina=0$i" -accept_all_cookies -dump -nolist|head -50|tail -19;done|less'

from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString

indirizzo = 'http://www.televideo.rai.it/televideo/pub/solotesto.jsp?pagina=%s&sottopagina=0%s'

def analizza(html):
    """WARN: very black magik - la sto scrivendo e non so quel che fa"""
    return ''.join(filter(lambda x:isinstance(x, NavigableString),
            BeautifulSoup(html)('td', width='450', height='380', align='center',
            valign='middle')[0]('pre')[0].contents[2:])).encode('iso-8859-15')

def cli(pagina):
    from curses import initscr, error, endwin, KEY_DOWN, KEY_UP

    testo = []
    for i in 1, 2, 3:
        html = urlopen(indirizzo % (pagina, i)).read()
        testo.extend(analizza(html).split('\n'))

    lunghezzaTesto = len(testo)
    i = 0
    schermo = initscr()
    schermo.keypad(1)
    while True:
        altezzaSchermo = schermo.getmaxyx()[0]      # terminale ridimensionabile
        schermo.erase()
        try:
            schermo.addstr('\n'.join(testo[i:altezzaSchermo+i]))
        except error:
            pass # non l'ho ben capito, ma mi adeguo
        carattere = schermo.getch()
        if carattere == ord('q'):
            break
        elif altezzaSchermo + i < lunghezzaTesto and carattere in (ord('z'),
                KEY_DOWN):
            i += 1
        elif i > 0 and carattere in (ord('a'), KEY_UP):
            i -= 1
    endwin()

def dump(pagina):
    for i in 1, 2, 3:
        print analizza(urlopen(indirizzo % (pagina, i)).read())

def gui(argv, pagina):
    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit

    app = QApplication(argv)
    mainWindow = QMainWindow()
    textEdit = QTextEdit()

    mainWindow.setCentralWidget(textEdit)
    mainWindow.show()
    textEdit.setReadOnly(True)
    textEdit.setText('\n'.join(analizza(urlopen(indirizzo % (pagina,
            i)).read()).decode('iso-8859-15') for i in (1, 2, 3)))

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
