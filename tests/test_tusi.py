from pathlib import Path
from unittest import TestCase

from msgplugins.tusi.tusi import TusiMultipleCountPool


class TestTusi(TestCase):
    def setUp(self) -> None:
        self.pool = TusiMultipleCountPool()

    def test_tusi(self):
        def cb(res: list[Path]):
            print(res)

        while True:
            p = input("prompt:")
            self.pool.txt2img(p, cb)
