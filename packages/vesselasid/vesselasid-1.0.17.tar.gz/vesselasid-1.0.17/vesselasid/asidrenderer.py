from argparse import ArgumentParser, BooleanOptionalAction
import importlib
import inspect
import logging
import time
import os
import platform
import mido
from vesselasid.asid import Asid
from vesselasid.baserender import VesselAsidRenderer


def known_loopbacks(names):
    loopbacks = set()
    for name in names:
        for loopback in ("IAC Driver", "Midi Through"):
            if loopback in name:
                loopbacks.add(name)
                break
    others = set(names) - loopbacks
    return sorted(list(loopbacks), reverse=True), sorted(list(others), reverse=True)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")

    if platform.system() == "Darwin" and os.getenv("MIDO_BACKEND", None) is None:
        mido.set_backend("mido.backends.portmidi")
    if not mido.get_output_names():
        logging.fatal("no output ports available")
        raise ValueError
    if not mido.get_input_names():
        logging.fatal("no input ports available")
        raise ValueError

    parser = ArgumentParser()
    parser.add_argument(
        "--asid-port",
        dest="asid_port",
        type=str,
        default=None,
        help="Set MIDI port for ASID control (available ports %s)"
        % mido.get_output_names(),
    )
    parser.add_argument(
        "--asid-input",
        dest="asid_input",
        default=True,
        action=BooleanOptionalAction,
        help="Use ASID control port for input (synchronous operation)",
    )
    parser.add_argument(
        "--ctrl-port",
        dest="ctrl_port",
        type=str,
        default=None,
        help="Set MIDI port to receive renderer commands (available ports %s"
        % mido.get_input_names(),
    )
    parser.add_argument(
        "--renderers",
        dest="renderers",
        type=str,
        default=None,
        help="path name to file containing renderer classes",
    )
    parser.add_argument(
        "--default-renderer",
        dest="default_renderer",
        type=int,
        default=0,
        help="If set, default renderer",
    )
    options = parser.parse_args()

    renderers = []
    if options.renderers:
        logging.info("importing %s", options.renderers)
        mod = importlib.import_module(options.renderers)
        for cls_name, cls in inspect.getmembers(mod):
            if inspect.isclass(cls) and cls != VesselAsidRenderer:
                if VesselAsidRenderer in inspect.getmro(cls):
                    logging.info("found %s", cls_name)
                    renderers.append((cls_name, cls))
    renderers_map = {}
    for i, j in enumerate(sorted(renderers)):
        logging.info("program %u is %s", i, j[0])
        renderers_map[i] = j

    if not renderers_map:
        logging.fatal("no renderers found")
        raise ValueError

    if options.default_renderer not in renderers_map:
        logging.fatal("default renderer %u not in renders", options.default_renderer)
        raise ValueError

    asid_port = options.asid_port
    if not asid_port:
        asid_port = mido.get_output_names()[0]
        loopbacks, others = known_loopbacks(mido.get_output_names())
        if others:
            asid_port = others[0]
    ctrl_port = options.ctrl_port
    if not ctrl_port:
        ctrl_port = mido.get_input_names()[0]
        loopbacks, others = known_loopbacks(mido.get_input_names())
        if loopbacks:
            ctrl_port = loopbacks[0]
    logging.info("using %s for ASID", asid_port)
    logging.info("using %s for control input", ctrl_port)

    asid_out_port = mido.open_output(asid_port)
    asid_in_port = None
    if options.asid_input:
        asid_in_port = mido.open_input(asid_port)

    asid = Asid(asid_out_port, in_port=asid_in_port)
    asid.start()

    def get_renderer(r):
        logging.info("starting renderer %u (%s)", r, renderers_map[r][0])
        renderer = renderers_map[r][1](asid)
        renderer.start()
        logging.info("renderer %u (%s) started", r, renderers_map[r][0])
        return renderer

    with mido.open_input(ctrl_port) as ctrl_in_port:
        renderer = get_renderer(options.default_renderer)
        try:
            for msg in ctrl_in_port:
                if msg.type == "program_change":
                    if msg.program in renderers_map:
                        renderer.stop()
                        renderer = get_renderer(msg.program)
                    else:
                        logging.error(
                            "no renderer for program %u, not changing program",
                            msg.program,
                        )
                elif hasattr(renderer, msg.type):
                    start_time = time.time()
                    func = getattr(renderer, msg.type)
                    func(msg)
                    logging.debug("%s: %.3fs", msg, time.time() - start_time)
                else:
                    logging.info("no handler for %s, no action", msg)
        except KeyboardInterrupt:
            renderer.stop()


if __name__ == "__main__":
    main()
