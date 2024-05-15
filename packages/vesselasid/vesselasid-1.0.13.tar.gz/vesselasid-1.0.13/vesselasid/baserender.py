from vesselasid.asm import xa
from vesselasid.constants import (
    SCREEN_RAM,
    SCREEN_RAM2,
    CHARSET_RAM,
    VICII_BASE,
    VICII_MEMPTRS,
    VICII_VERTCONTROL,
)


class RasterGuardVicIIRegister:
    def __init__(self, asid, vals, switcher_origin=0xC000):
        self.asid = asid
        self.valmap = {}
        for reg, val in vals:
            code = xa(
                [
                    "ldx #%u" % val,
                    "lda #$80",
                    "_w1: bit %u" % (VICII_BASE + VICII_VERTCONTROL),
                    "bpl _w1",
                    "_w2: bit %u" % (VICII_BASE + VICII_VERTCONTROL),
                    "bmi _w2",
                    "stx %u" % (VICII_BASE + reg),
                ],
                origin=switcher_origin,
            )
            self.asid.addr(switcher_origin)
            self.asid.load(code)
            self.valmap[(reg, val)] = switcher_origin
            switcher_origin += len(code)

    def spin(self, reg, val):
        self.asid.addr(self.valmap[(reg, val)])
        self.asid.run()


class VicIIDoubleBuffer:
    def __init__(
        self,
        asid,
        screen_buffer1=SCREEN_RAM,
        screen_buffer2=SCREEN_RAM2,
        charset_buffer1=CHARSET_RAM,
        charset_buffer2=CHARSET_RAM,
    ):
        self.asid = asid
        self.screen_buffers = (
            (screen_buffer2, charset_buffer2),
            (screen_buffer1, charset_buffer1),
        )
        combos = [
            (VICII_MEMPTRS, self.get_vic_ram_val(screen_buffer, charset_buffer))
            for screen_buffer, charset_buffer in self.screen_buffers
        ]
        self.guard = RasterGuardVicIIRegister(asid, combos)
        self.swap()

    def vic_1k_addr(self, addr):
        return int((addr % (16 * 0x400)) / 0x400)

    def get_vic_ram_val(self, screen_buffer, charset_buffer):
        return (self.vic_1k_addr(screen_buffer) << 4) + self.vic_1k_addr(charset_buffer)

    def buffers(self):
        return self.screen_buffers[1]

    def swap(self):
        self.screen_buffers = tuple(reversed(self.screen_buffers))
        screen_buffer, charset_buffer = self.buffers()
        self.guard.spin(
            VICII_MEMPTRS, self.get_vic_ram_val(screen_buffer, charset_buffer)
        )


class VesselAsidRenderer:
    def __init__(self, asid):
        self.asid = asid

    def start(self):
        return

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
