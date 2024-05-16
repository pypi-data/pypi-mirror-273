import os
import tempfile
from subprocess import Popen, PIPE


def xa(code, origin=0xC000):
    full_code = "\n".join(["* = %u" % origin] + code + ["rts"])
    with tempfile.TemporaryDirectory() as tmpdir:
        code_file = os.path.join(tmpdir, "code.s")
        with open(code_file, "w") as f:
            f.write(full_code)
        with Popen(["xa", "-o", "-", code_file], stdout=PIPE, stderr=PIPE) as p:
            ocode = list(p.communicate()[0])
        if not ocode:
            raise ValueError(code)
        return ocode
