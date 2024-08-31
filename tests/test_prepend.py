from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import override
from unittest import TestCase

from prepend import prepend


class TestPrepend(TestCase):
    @override
    def setUp(self) -> None:
        self.tmp = NamedTemporaryFile(mode='w', delete=False)
        self.tmp.write('''foo
bar
baz
''')
        self.tmp.close()
        self.filename = Path(self.tmp.name)

    @override
    def tearDown(self) -> None:
        self.filename.unlink()

    def test_prepend(self) -> None:
        prepend('prepend', self.filename)
        self.assertEqual('''prepend
foo
bar
baz
''', self.filename.read_text())
