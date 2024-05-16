import copy
from collections import defaultdict
import random
import mido

CONTROL_BITS = {
    b: 2**i
    for i, b in enumerate(
        ["GATE", "SYNC", "RING", "TEST", "TRIANGLE", "SAWTOOTH", "PULSE", "NOISE"]
    )
}
WAVEFORM_BITS = {"PULSE", "SAWTOOTH", "TRIANGLE"}
MOD_BITS = {"RING", "SYNC"}


ID_REG = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 12,
    11: 13,
    12: 14,
    13: 15,
    14: 16,
    15: 17,
    16: 19,
    17: 20,
    18: 21,
    19: 22,
    20: 23,
    21: 24,
    22: 4,
    23: 11,
    24: 18,
}

ELEKTRON_MANID = 0x2D
ASID_START = 0x4C
ASID_STOP = 0x4D
ASID_UPDATE = 0x4E
ASID_UPDATE_BOTH = 0x51
ASID_RUN = 0x52
ASID_LOAD = 0x53
ASID_ADDR = 0x54
ASID_LOAD_RECT = 0x55
ASID_ADDR_RECT = 0x56
ASID_FILL_BUFFER = 0x57
ASID_FILL_RECT_BUFFER = 0x58
ASID_COPY_BUFFER = 0x59
ASID_COPY_RECT_BUFFER = 0x5A
ASID_STASH_REU_BUFFER = 0x5B
ASID_FETCH_REU_BUFFER = 0x5C
ASID_FILL_REU_BUFFER = 0x5D

VOICE_REGS = 7


def lohi(x, size, losize):
    hisize = size - losize
    if size > 16 or losize > size or losize > 8 or hisize > 8 or x > 2**size - 1:
        raise ValueError
    lomask = 2**losize - 1
    lo = x & lomask
    himask = 2**hisize - 1
    hi = (x >> losize) & himask
    return [lo, hi]


def encodebits(val, bits, start=0):
    mask = 0
    new_val = 0
    if start:
        mask = 2**start - 1
    for i, bit in enumerate(bits, start=start):
        if bit is None:
            mask += 2**i
        elif bit:
            new_val += 2**i
    leftover = 7 - i
    if leftover:
        mask += (2**leftover - 1) << len(bits)
    return (val & mask) + new_val


class AsidSidVoice:
    def __init__(self, v):
        self.regs = {}
        self.v = v

    def _reg(self, reg):
        return ((self.v - 1) * VOICE_REGS) + reg

    def _set_voicereg(self, reg, val):
        self.regs.update({self._reg(reg): val})

    def _get_voicereg(self, reg):
        return self.regs.get(self._reg(reg), 0)

    def set_freq(self, val):
        lo, hi = lohi(val, 16, 8)
        self._set_voicereg(0, lo)
        self._set_voicereg(1, hi)

    def set_pdc(self, val):
        lo, hi = lohi(val, 12, 8)
        self._set_voicereg(2, lo)
        self._set_voicereg(3, hi)

    def set_ctrl(self, val):
        self._set_voicereg(4, val)

    def set_ad(self, a, d):
        existing_a, existing_d = lohi(self._get_voicereg(5), 8, 4)
        if a is None:
            a = existing_a
        if d is None:
            d = existing_d
        self._set_voicereg(5, (a << 4) + d)

    def set_sr(self, s, r):
        existing_s, existing_r = lohi(self._get_voicereg(6), 8, 4)
        if s is None:
            s = existing_s
        if r is None:
            r = existing_r
        self._set_voicereg(6, (s << 4) + r)

    def set_state(self, a=None, d=None, s=None, r=None, pdc=None, freq=None, ctrl=None):
        if a is not None or d is not None:
            self.set_ad(a, d)
        if s is not None or r is not None:
            self.set_sr(s, r)
        if pdc is not None:
            self.set_pdc(pdc)
        if freq is not None:
            self.set_freq(freq)
        if ctrl is not None:
            self.set_ctrl(ctrl)


class AsidSid:
    def __init__(self):
        self.regs = {}
        self.voice = {i + 1: AsidSidVoice(i + 1) for i in range(3)}

    def set_state(
        self,
        vol=None,
        fc=None,
        fr=None,
        fex=None,
        f3=None,
        f2=None,
        f1=None,
        lp=None,
        bp=None,
        hp=None,
        v3off=None,
    ):
        ctrl = self.regs.get(24, 0)
        if vol is not None:
            mask = (2**4 - 1) << 4
            ctrl = (ctrl & mask) + vol
        ctrl = encodebits(ctrl, (lp, bp, hp, v3off), start=4)
        if ctrl != self.regs.get(24, 0):
            self.regs.update({24: ctrl})
        if fc is not None:
            lo, hi = lohi(fc, 11, 3)
            self.regs.update({21: lo})
            self.regs.update({22: hi})
        fctrl = self.regs.get(23, 0)
        if fr is not None:
            mask = 2**4 - 1
            fctrl = fctrl & mask
            fctrl += fr << 4
        fctrl = encodebits(fctrl, (f1, f2, f3, fex))
        if fctrl != self.regs.get(23, 0):
            self.regs.update({23: fctrl})

    def state(self):
        state = copy.deepcopy(self.regs)
        for voice in self.voice.values():
            state.update(voice.regs)
        return state


class Asid:
    def __init__(self, port, in_port=None, update_cmd=ASID_UPDATE, cache=True):
        self.port = port
        self.in_port = in_port
        self.update_cmd = update_cmd
        self.cache = cache
        self.regs = None
        self._resetreg()
        self.sid = AsidSid()
        if self.in_port:
            while self.in_port.poll():
                self.in_port.receive()

    def _resetreg(self):
        self.regs = defaultdict(int)

    def _sysex(self, data):
        msg = mido.Message("sysex", data=[ELEKTRON_MANID] + data)
        self.port.send(msg)
        if self.in_port:
            self.in_port.receive()

    def run(self):
        self._sysex([ASID_RUN])

    def loaddiffs(self, addr, a, b, shuffle=True, overhead=9):
        pos = None
        strictdifflist = []

        for i, x_y in enumerate(zip(a, b)):
            x, y = x_y
            if x == y:
                if pos is not None:
                    strictdifflist.append((pos, i))
                    pos = None
            else:
                if pos is None:
                    pos = i

        if pos is not None:
            strictdifflist.append((pos, i + 1))

        difflist = strictdifflist[:1]
        for diff in strictdifflist[1:]:
            x, y = diff
            last_x, last_y = difflist[-1]
            if x - last_y < overhead:
                difflist[-1] = (last_x, y)
            else:
                difflist.append(diff)

        if shuffle:
            random.shuffle(difflist)
        for x, y in difflist:
            code = b[x:y]
            self.addr(addr + x)
            self.load(code)
        return difflist

    def _encode_code(self, code):
        data = []
        while code:
            batch = code[:7]
            code = code[7:]
            msb = 0
            for i in range(len(batch)):
                if batch[i] & 0x80:
                    msb += 2**i
                    batch[i] -= 0x80
            data.extend([msb] + batch)
        return data

    def load(self, code):
        self._sysex([ASID_LOAD] + self._encode_code(code))

    def addrrect(self, rowstart, rowsize, inc):
        self._sysex([ASID_ADDR_RECT] + self._encode_code([rowstart, rowsize, inc]))

    def loadrect(self, code):
        self._sysex([ASID_LOAD_RECT] + self._encode_code(code))

    def addr(self, addr):
        self._sysex([ASID_ADDR] + self._encode_code(lohi(addr, 16, 8)))

    def fillbuff(self, val, count):
        self._sysex([ASID_FILL_BUFFER] + self._encode_code([val] + lohi(count, 16, 8)))

    def fillrect(self, val, count):
        self._sysex(
            [ASID_FILL_RECT_BUFFER] + self._encode_code([val] + lohi(count, 16, 8))
        )

    def _encodecopy(self, copyfrom, count):
        return self._encode_code(lohi(copyfrom, 16, 8) + lohi(count, 16, 8))

    def copybuff(self, copyfrom, count):
        self._sysex([ASID_COPY_BUFFER] + self.encodecopy(copyfrom, count))

    def copyrect(self, copyfrom, count):
        self._sysex([ASID_COPY_RECT_BUFFER] + self.encodecopy(copyfrom, count))

    def _encodereu(self, reuaddr, count):
        return self._encode_code(
            list(int(reuaddr).to_bytes(length=3, byteorder="little", signed=False))
            + lohi(count, 16, 8)
        )

    def stashbuff(self, reuaddr, count):
        self._sysex([ASID_STASH_REU_BUFFER] + self._encodereu(reuaddr, count))

    def fetchbuff(self, reuaddr, count):
        self._sysex([ASID_FETCH_REU_BUFFER] + self._encodereu(reuaddr, count))

    def rfillbuff(self, reuaddr, count):
        self._sysex([ASID_FILL_REU_BUFFER] + self._encodereu(reuaddr, count))

    def start(self):
        self._sysex([ASID_START])
        self._resetreg()

    def stop(self):
        self._sysex([ASID_STOP])
        self._resetreg()

    def update(self, changes=None):
        if changes is None:
            changes = self.sid.state()
        masks = [0, 0, 0, 0]
        msbs = [0, 0, 0, 0]
        vals = []

        for reg_id, reg in sorted(ID_REG.items()):
            new_val = changes.get(reg, None)
            if new_val is None:
                continue
            if self.cache:
                if new_val == self.regs[reg]:
                    continue
            self.regs[reg] = new_val
            meta_byte = int(reg_id / 7)
            meta_bit = reg_id % 7
            masks[meta_byte] |= 2**meta_bit
            if new_val & 0x80:
                msbs[meta_byte] |= 2**meta_bit
            vals.append(new_val & 0x7F)
        if vals:
            self._sysex([self.update_cmd] + masks + msbs + vals)
