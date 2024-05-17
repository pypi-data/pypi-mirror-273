"""A set of tools tyo manipulate charge density files from VASP.

PARCHG, CHGCAR and (oneshot) CHG are supported.
MD CHG are not supported yet.
"""
# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
import sys
import os.path

from .script_utils import (
    MultiCmd,
    error,
    positional,
    flag,
    optional,
    error_catch,
    PerfCounterCollec,
)


chargetool = MultiCmd(description=__doc__)

@chargetool.subcmd(
    positional("CHGCAR", help="file to extract data from"),
    flag("--split", help="split CHGCAR into up and down channels"),
    flag("--spin", help="extract the spin density"),
    flag("--total", help="extract the total density"),
    flag("--timing", help="show the timing informations"),
    optional("--dest", "-o", type=str, default=None, help="output file path"),
)
def extract(opts):
    from .charge_utils import Charge

    pc = PerfCounterCollec()

    with pc.reading:
        if opts.chgcar == "-":
            chg = Charge.from_file(sys.stdin)
            name = "CHGCAR"
        else:
            with open(opts.chgcar) as f:
                chg = Charge.from_file(f)
            name = opts.chgcar

    if opts.dest is not None:
        name = opts.dest
    out_prefix, ext = os.path.splitext(name)

    if opts.split:
        if chg.dif_part is None:
            error("There is no spin data available in the input file.")

        with pc.processing:
            up, down = chg.split()

        with pc.writing, open(out_prefix + ".up" + ext, "w") as f:
            up.write_to(f)

        with pc.writing, open(out_prefix + ".down" + ext, "w") as f:
            down.write_to(f)

    elif opts.spin:
        if chg.dif_part is None:
            error("There is no spin data available in the input file.")

        with pc.writing, open(out_prefix + ".spin" + ext, "w") as f:
            chg.dif_part.write_to(f)

    elif opts.total:
        with pc.writing, open(out_prefix + ".total" + ext, "w") as f:
            chg.total_only().write_to(f)

    else:
        error("No action required.")

    if opts.timing:
        print(pc.summary())


@chargetool.subcmd(
    positional("COEF_A", type=float, help="coeficient for the first file"),
    positional("CHGCAR_A", help="first file to extract data from"),
    positional("COEF_B", type=float, help="coeficient for the second file"),
    positional("CHGCAR_B", help="second file to extract data from"),
    optional("--dest", "-o", type=str, default=None, help="output file path"),
)
def sum(opts):
    from .charge_utils import Charge

    if opts.chgcar_a == "-":
        chg_a = Charge.from_file(sys.stdin)
        name = "CHGCAR"
    else:
        with open(opts.chgcar_a) as f:
            chg_a = Charge.from_file(f)
        name = opts.chgcar_a

    if opts.chgcar_b == "-":
        chg_b = Charge.from_file(sys.stdin)
    else:
        with open(opts.chgcar_b) as f:
            chg_b = Charge.from_file(f)

    chg_sum = opts.coef_a * chg_a + opts.coef_b * chg_b

    out_prefix, ext = os.path.splitext(name)
    dest = opts.dest or (out_prefix + ".sum" + ext)
    with open(dest, "w") as f:
        chg_sum.write_to(f)
