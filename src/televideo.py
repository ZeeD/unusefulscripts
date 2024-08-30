from curses import KEY_DOWN
from curses import KEY_UP
from curses import endwin
from curses import initscr
from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from os import environ
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTextEdit

logger = getLogger(__name__)


def analizza(pagina: int) -> str:
    soup = urlopen(
        f'http://www.televideo.rai.it/televideo/pub/catturaSottopagine.jsp?pagina={pagina}',
        timeout=3,
    ).read()
    return ''.join(
        str(e)
        for e in BeautifulSoup(soup, features='html.parser')('pre')[0].contents
    )


def cli(page: int) -> None:
    text = analizza(page).split('\n')

    text_len = len(text)
    i = 0
    screen = initscr()
    try:
        screen.keypad(True)  # noqa: FBT003
        while True:
            screen_height = screen.getmaxyx()[0]  # terminale ridimensionabile
            screen.erase()
            screen.addstr('\n'.join(text[i : screen_height + i]))
            char = screen.getch()
            if char == ord('q'):
                break
            if char in (ord('z'), KEY_DOWN) and screen_height + i < text_len:
                i += 1
            elif char in (ord('a'), KEY_UP) and i:
                i -= 1
            else:
                pass  # ignore chars not in (a, q, z, KEY_UP, KEY_DOWN)
    finally:
        endwin()


def dump(pagina: int) -> None:
    logger.info(analizza(pagina))


def gui(argv: list[str], pagina: int) -> None:
    app = QApplication(argv)
    main_window = QMainWindow()
    text_edit = QTextEdit()

    main_window.setCentralWidget(text_edit)
    main_window.show()
    text_edit.setReadOnly(True)
    text_edit.setText(analizza(pagina))

    raise SystemExit(app.exec_())


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    parser = OptionParser(version='%prog 0.8.0')
    parser.add_option(
        '-g',
        '--gui',
        action='store_true',
        default=False,
        help='Force the qt4 gui interface',
    )
    parser.add_option(
        '-c',
        '--cli',
        action='store_true',
        default=False,
        help='Force the ncurses cli interface',
    )
    parser.add_option(
        '-p', '--page', type='int', default=505, help='Show this page'
    )
    parser.add_option(
        '-d',
        '--dump',
        action='store_true',
        default=False,
        help='Force the "just dump the content of the page" iterface',
    )
    options, args = parser.parse_args()

    if (
        sum(int(value) for value in [options.gui, options.cli, options.dump])
        > 1
    ):
        logger.error("Puoi scegliere un'unica opzione di visualizzazione!")
        raise SystemExit

    if options.gui:
        gui(args, options.page)
    elif options.cli:
        cli(options.page)
    elif options.dump:
        dump(options.page)
    elif 'TERM' not in environ or environ['TERM'] in (
        'xterm',
        'rxvt',
        'xterm-color',
        'xterm-256color',
    ):
        cli(options.page)
    else:
        gui(args, options.page)


if __name__ == '__main__':
    main()
