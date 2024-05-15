#!/usr/bin/python

import unittest
from vesselasid.asid import (
    Asid,
    AsidSid,
    ASID_LOAD,
    ASID_UPDATE,
    ASID_ADDR,
    ELEKTRON_MANID,
    lohi,
    encodebits,
)


class FakePort:
    def __init__(self):
        self.last_send = None

    def send(self, data):
        self.last_send = data


class TestBitOps(unittest.TestCase):
    def test_lohi(self):
        for test_x, test_size, test_losize in (
            (65535, 16, 8),
            (4095, 12, 8),
            (2047, 11, 3),
            (1024, 11, 3),
        ):
            lo, hi = lohi(test_x, test_size, test_losize)
            self.assertEqual(
                test_x,
                lo + (hi << test_losize),
                (lo, hi, test_x, test_size, test_losize),
            )

    def test_encodebits(self):
        self.assertEqual(2**4 - 1, encodebits(0, (1, 1, 1, 1), 0))
        self.assertEqual(2**4 - 1 << 1, encodebits(0, (1, 1, 1, 1), 1))
        self.assertEqual(2**4 - 1, encodebits(2**2, (1, 1, None, 1), 0))
        self.assertEqual(2**4 - 1 - 2**2, encodebits(2**2, (1, 1, 0, 1), 0))
        self.assertEqual(2**4 - 1 << 4, encodebits(255, (0, 0, 0, 0), 0))
        self.assertEqual(128, encodebits(128, (0, 0, 0, None), 4))


class TestAsidSid(unittest.TestCase):
    def test_asid_sid(self):
        sid = AsidSid()
        sid.set_state(vol=15)
        self.assertEqual({24: 15}, sid.regs)
        sid.set_state(fc=2048 - 2**3)
        self.assertEqual({21: 0, 22: 255, 24: 15}, sid.state())
        sid.voice[2].set_state(pdc=1024)
        self.assertEqual({9: 0, 10: 4, 21: 0, 22: 255, 24: 15}, sid.state())
        sid.set_state(v3off=1)
        self.assertEqual({9: 0, 10: 4, 21: 0, 22: 255, 24: 15 + 128}, sid.state())
        sid.set_state(f2=1)
        self.assertEqual(
            {9: 0, 10: 4, 21: 0, 22: 255, 23: 2, 24: 15 + 128}, sid.state()
        )
        sid.set_state(fr=3)
        self.assertEqual(
            {9: 0, 10: 4, 21: 0, 22: 255, 23: 2 + 48, 24: 15 + 128}, sid.state()
        )
        sid.set_state(fr=0)
        self.assertEqual(
            {9: 0, 10: 4, 21: 0, 22: 255, 23: 2, 24: 15 + 128}, sid.state()
        )
        sid.set_state(vol=7)
        self.assertEqual({9: 0, 10: 4, 21: 0, 22: 255, 23: 2, 24: 7 + 128}, sid.state())
        sid.voice[2].set_state(s=10, d=10, freq=128)
        self.assertEqual(
            {
                7: 128,
                8: 0,
                9: 0,
                10: 4,
                12: 10,
                13: 10 << 4,
                21: 0,
                22: 255,
                23: 2,
                24: 7 + 128,
            },
            sid.state(),
        )


class TestAsid(unittest.TestCase):
    def setUp(self):
        self.port = FakePort()
        self.asid = Asid(self.port)

    def test_update(self):
        self.assertEqual({}, self.asid.regs)
        self.asid.update({24: 15})
        self.assertEqual(
            (ELEKTRON_MANID, ASID_UPDATE, 0, 0, 0, 1, 0, 0, 0, 0, 15),
            tuple(self.port.last_send.data),
        )
        self.port.last_send = None
        self.asid.update({24: 15})
        self.assertIsNone(self.port.last_send)
        self.asid.update({24: 255})
        self.assertEqual(
            (ELEKTRON_MANID, ASID_UPDATE, 0, 0, 0, 1, 0, 0, 0, 1, 127),
            tuple(self.port.last_send.data),
        )

    def test_addr(self):
        self.asid.addr(65535)
        self.assertEqual(
            (ELEKTRON_MANID, ASID_ADDR, 0x03, 0x7F, 0x7F),
            tuple(self.port.last_send.data),
        )
        self.asid.addr(49152)
        self.assertEqual(
            (ELEKTRON_MANID, ASID_ADDR, 0x02, 0x00, 0x40),
            tuple(self.port.last_send.data),
        )

    def test_loaddiffs(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        b = [1, 2, 3, 4, 4, 4, 7, 8, 9]
        self.asid.loaddiffs(0, a, b)
        self.assertEqual(
            (ELEKTRON_MANID, ASID_LOAD, 0, 4, 4), tuple(self.port.last_send.data)
        )

    def test_load(self):
        self.asid.load(
            [
                255,
                254,
                253,
                252,
                251,
                250,
                249,
                248,
                247,
                246,
                245,
                244,
                243,
                242,
                241,
                240,
            ]
        )
        self.assertEqual(
            (
                ELEKTRON_MANID,
                ASID_LOAD,
                127,
                127,
                126,
                125,
                124,
                123,
                122,
                121,
                127,
                120,
                119,
                118,
                117,
                116,
                115,
                114,
                3,
                113,
                112,
            ),
            tuple(self.port.last_send.data),
        )
        self.asid.load([128, 1, 2, 3])
        self.assertEqual(
            (ELEKTRON_MANID, ASID_LOAD, 1, 0, 1, 2, 3), tuple(self.port.last_send.data)
        )
        self.asid.load([0, 1, 2, 3])
        self.assertEqual(
            (ELEKTRON_MANID, ASID_LOAD, 0, 0, 1, 2, 3), tuple(self.port.last_send.data)
        )
        self.asid.load([0, 1, 128, 129])
        self.assertEqual(
            (ELEKTRON_MANID, ASID_LOAD, 12, 0, 1, 0, 1), tuple(self.port.last_send.data)
        )


if __name__ == "__main__":
    unittest.main()
