from vesselasid.asm import xa
from vesselasid.constants import (
    CHARSET_ROM,
    COLOR_RAM,
    DEFAULT_BUFFER,
    KERNEL_CINT,
    SCREEN_RAM,
    SCREEN_RAM2,
    SCREEN_SIZE,
    VICII_BASE,
    VICII_BRCOLOR,
    VICII_CTRL1,
    VICII_CTRL2,
    VICII_MEMPTRS,
)


class RasterGuardVicIIRegister:
    def __init__(self, asid, combos, switcher_origin=DEFAULT_BUFFER):
        self.asid = asid
        self.valmap = {}
        for combo in combos:
            asm_code = [
                "lda #$80",
                "_w1: bit %u" % (VICII_BASE + VICII_CTRL1),
                "bpl _w1",
                "_w2: bit %u" % (VICII_BASE + VICII_CTRL1),
                "bmi _w2",
            ]
            for reg, val in combo:
                asm_code.extend(
                    [
                        "ldx #%u" % val,
                        "stx %u" % reg,
                    ]
                )
            code = xa(asm_code, origin=switcher_origin)
            self.asid.addr(switcher_origin)
            self.asid.load(code)
            self.valmap[combo] = switcher_origin
            switcher_origin += len(code)

    def spin(self, combo):
        self.asid.addr(self.valmap[combo])
        self.asid.run()


class VicIIDoubleBuffer2:
    def __init__(
        self,
        asid,
        screen_buffer1=SCREEN_RAM,
        screen_buffer2=SCREEN_RAM2,
        charset_buffer1=CHARSET_ROM,
        charset_buffer2=CHARSET_ROM,
        default_ctrl1=0x1B,
        default_ctrl2=0xC8,
    ):
        self.asid = asid
        self.screen_buffers = (
            (screen_buffer2, charset_buffer2),
            (screen_buffer1, charset_buffer1),
        )
        self.default_ctrl1 = default_ctrl1
        self.default_ctrl2 = default_ctrl2
        combos = []
        for screen_buffer, charset_buffer in self.screen_buffers:
            for x in (0, 7):
                for y in (0, 7):
                    combos.append(self.make_combo(screen_buffer, charset_buffer, x, y))
        self.guard = RasterGuardVicIIRegister(asid, combos)
        self.swap()

    def make_combo(self, screen_buffer, charset_buffer, x, y):
        return (
            (
                VICII_BASE + VICII_MEMPTRS,
                self.get_vic_ram_val(screen_buffer, charset_buffer),
            ),
            (VICII_BASE + VICII_CTRL1, self.default_ctrl1 + y),
            (VICII_BASE + VICII_CTRL2, self.default_ctrl2 + x),
        )

    def set_x(self, x):
        self.asid.addr(VICII_BASE + VICII_CTRL2)
        self.asid.load([self.default_ctrl2 + x])

    def set_y(self, y):
        self.asid.addr(VICII_BASE + VICII_CTRL1)
        self.asid.load([self.default_ctrl1 + y])

    def vic_1k_addr(self, addr):
        return int((addr % (16 * 0x400)) / 0x400)

    def get_vic_ram_val(self, screen_buffer, charset_buffer):
        return (self.vic_1k_addr(screen_buffer) << 4) + self.vic_1k_addr(charset_buffer)

    def buffers(self):
        return self.screen_buffers[1]

    def swap(self, x=0, y=0):
        screen_buffer, charset_buffer = self.buffers()
        self.guard.spin(self.make_combo(screen_buffer, charset_buffer, x, y))
        self.screen_buffers = tuple(reversed(self.screen_buffers))


class VesselAsidRenderer:
    def __init__(self, asid):
        self.asid = asid

    def start(self):
        self.asid.addr(KERNEL_CINT)
        self.asid.run()
        self.asid.addr(VICII_BASE + VICII_BRCOLOR)
        self.asid.load([0, 0])
        self.asid.addr(COLOR_RAM)
        self.asid.fillbuff(1, SCREEN_SIZE)
        self.asid.addr(SCREEN_RAM)
        self.asid.fillbuff(32, SCREEN_SIZE)

    def stop(self):
        return

    def note_on(self, msg):
        return

    def note_off(self, msg):
        return

    def control_change(self, msg):
        return

    def pitchwheel(self, msg):
        return
