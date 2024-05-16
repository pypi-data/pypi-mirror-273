import logging
from vesselasid.baserender import VesselAsidRenderer


class ExampleAsidRenderer(VesselAsidRenderer):
    def __init__(self, asid):
        self.asid = asid

    def start(self):
        self.asid.start()
        self.asid.addr(0x0400)
        self.asid.fillbuff(0, 1000)

    def stop(self):
        self.asid.stop()

    def note_on(self, msg):
        self.asid.fillbuff(msg.note, 1000)

    def note_off(self, msg):
        logging.debug(msg)

    def control_change(self, msg):
        logging.debug(msg)

    def pitchwheel(self, msg):
        logging.debug(msg)
