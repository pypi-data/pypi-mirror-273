#!/usr/bin/python

import unittest
from vesselasid.asm import xa


class TestAsm(unittest.TestCase):
    def test_xa(self):
        self.assertEqual([234, 234, 234, 96], xa(["nop", "nop", "nop"]))


if __name__ == "__main__":
    unittest.main()
