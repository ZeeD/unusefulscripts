from datetime import UTC
from datetime import datetime
from email.utils import parsedate
from http.client import HTTPConnection
from http.client import HTTPResponse
from itertools import takewhile
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING
from urllib.request import urlopen

from sdbus_block.notifications import FreedesktopNotifications

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = getLogger(__name__)


LOCAL_PATH = '/var/lib/slackpkg/ChangeLog.txt'
REMOTE_DOMAIN = 'slackware.mirror.garr.it'
REMOTE_PATH = '/slackware/slackware64-current/ChangeLog.txt'
TEXT_ENCODING = 'latin1'


def remote_last_modified() -> datetime:
    """Find the last modified time on the remote changelog."""
    conn = HTTPConnection(REMOTE_DOMAIN)
    conn.request('HEAD', REMOTE_PATH)
    res = conn.getresponse()
    last_modified_header = res.getheader('last-modified')
    last_modified_parsed = parsedate(last_modified_header)
    if last_modified_parsed is None:
        raise ValueError
    return datetime(*last_modified_parsed[:6], tzinfo=UTC)


def local_last_modified() -> datetime:
    """Find the last modified time on my machine."""
    mtime = Path(LOCAL_PATH).stat().st_mtime
    return datetime.fromtimestamp(mtime, tz=UTC)


def remote_content() -> list[str]:
    """Retrieve the remote changelog."""
    remote: HTTPResponse = urlopen('https://' + REMOTE_DOMAIN + REMOTE_PATH)
    return remote.read().decode(TEXT_ENCODING).split('\n')


def local_content() -> list[str]:
    """Retrieve the local changelog content.

    (in pratice I just need the first row)
    """
    with Path(LOCAL_PATH).open() as local:
        return local.read().split('\n')


def diff(list1: list[str], list2: list[str]) -> 'Iterable[str]':
    """Return all first element of list1; break if found the head of list2.

    not a real differ, it expect list1 = [new1|new2|new3] + list2
    """
    return takewhile(lambda row: row != list2[0], list1)


def notify(news: 'Iterable[str]') -> None:
    """Send a popup to kde with the news."""
    FreedesktopNotifications().notify(
        'SlackNews',
        summary='SlackNews',
        body='<p>' + '<br />'.join(news) + '</p>',
    )


def check() -> None:
    """Check for news; if true, show a popup on kde."""
    remote_dt = remote_last_modified()
    local_dt = local_last_modified()
    local_is_newer = local_dt < remote_dt
    if local_is_newer:  # there are news!
        remote = remote_content()
        local = local_content()
        news = diff(remote, local)
        notify(news)


def loop() -> None:
    """Check every hour."""
    while True:
        try:
            check()
            sleep(60 * 60)  # one hour, in seconds
        except KeyboardInterrupt:
            logger.info('bye!')
            raise SystemExit from None


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    loop()


if __name__ == '__main__':
    main()
