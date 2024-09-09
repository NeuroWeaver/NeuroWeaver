from fxpmath import Fxp
from collections.abc import Iterable
import numpy as np
from tqdm import tqdm

FXP_CONFIGS = {
    "FXP32": {"signed": True, "n_int": 15, "n_frac": 16, "overflow": "saturate", "n_word": 32}
}


def sigmoid_pw(xval, dtype):
    if not isinstance(xval, Iterable):
        xval = np.asarray([xval])

    def inner(x, slope, start):
        result = (((x) >> slope) + start)
        return result

    pw5 = Fxp(5.0, **FXP_CONFIGS[dtype])
    pw2375 = Fxp(2.375, **FXP_CONFIGS[dtype])
    pw1 = Fxp(1.0, **FXP_CONFIGS[dtype])

    conds = [
        xval < -pw5.val,
        (xval < -pw2375.val) & (xval >= -pw5.val),
        (xval < -pw1.val) & (xval >= -pw2375.val),
        (xval < 0) & (xval >= -pw1.val),
        (xval >= 0) & (xval < (pw1.val)),
        (xval >= pw1.val) & (xval < (pw2375.val)),
        (xval >= pw2375.val) & (xval < (pw5.val)),
        (xval >= pw5.val)]

    p5 = Fxp(0.5, **FXP_CONFIGS[dtype]).val
    p625 = Fxp(0.625, **FXP_CONFIGS[dtype]).val
    p84375 = Fxp(0.84375, **FXP_CONFIGS[dtype]).val
    p375 = Fxp(0.375, **FXP_CONFIGS[dtype]).val
    p15625 = Fxp(0.15625, **FXP_CONFIGS[dtype]).val

    fns = [lambda x: 0,
           lambda x: inner(x, 5, p15625),
           lambda x: inner(x, 3, p375),
           lambda x: inner(x, 2, p5),
           lambda x: inner(x, 2, p5),
           lambda x: inner(x, 3, p625),
           lambda x: inner(x, 5, p84375),
           lambda x: pw1.val]

    res = np.piecewise(xval, conds, fns)
    return res


def convert(src_path, dst_path):
    src_f = open(src_path, "r")
    dst_f = open(dst_path, "w")

    converter = Fxp(0, **FXP_CONFIGS["FXP32"])

    for line in tqdm(src_f.readlines()):
        fxp_value = converter.set_val(int(line.rstrip()), raw=True)

        dst_f.write(str(fxp_value))
        dst_f.write("\n")


convert(src_path="input.txt", dst_path="input1_raw.txt")
convert(src_path="out.txt", dst_path="output.txt")