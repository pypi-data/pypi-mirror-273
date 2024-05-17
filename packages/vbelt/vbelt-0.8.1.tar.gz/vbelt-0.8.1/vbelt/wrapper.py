# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
import os.path

from .misc import naturaldelta

from .script_utils import (
    script,
    positional,
    flag,
    optional,
    error_catch,
    PerfCounterCollec,
)


@script(
    positional("OUTCAR", default="OUTCAR", type=str, help="VASP output file"),
    optional(
        "--tol",
        type=float,
        default=None,
        help="Maximum converged force ampliture (A/eV)",
    ),
    flag("--silent", "-q", help="quite mode, just use the return code"),
    flag("--short", "-S", help="short summary"),
)
def check_forces(opts):
    import numpy as np
    from .forces import read_forces

    with error_catch():
        try:
            with open(opts.outcar) as f:
                species, forces, tol = read_forces(f)
        except OSError:
            if not opts.silent:
                print("OUTCAR does not exist.")
            return 1

    if opts.tol is not None:
        tol = opts.tol

    of = 0

    norms = np.linalg.norm(forces, axis=-1)
    (non_conv_where,) = np.where(norms > tol)
    non_conv_where = set(non_conv_where)

    if not (opts.silent or opts.short):
        for sp, n in species:
            print(f"{sp:2} {n:3}")

    if not (opts.silent or opts.short):
        print("       ---        X          Y          Z")
        print("===========================================")
        for sp, n in species:
            for j, (x, y, z) in enumerate(forces[of : of + n], start=of):
                if j in non_conv_where:
                    m = [" ", " ", " "]
                    m[np.argmax(np.abs([x, y, z]))] = "<"
                    print(
                        f"{sp:2} {j+1:3} >>> {x: .05f} {m[0]} {y: .05f} {m[1]} {z: .05f} {m[2]}"
                    )
                else:
                    print(f"{sp:2} {j+1:3}     {x: .05f}   {y: .05f}   {z: .05f}  ")
            of += n

    if non_conv_where:
        if opts.short:
            i = np.argmax(norms)
            left = i
            for sp, n in species:
                if left < n:
                    spec = f"{sp}{left+1}"
                    break
                else:
                    left -= n
            print(f"atom {i}/{spec} : max force (eV/A) = {np.max(norms):.05}")
        elif not opts.silent:
            print(
                f"Convergence not reached: max force {np.max(norms):.05} eV/A > {tol:.02}."
            )
        return 1
    else:
        if opts.short:
            print("Converged.")
        elif not opts.silent:
            print("Convergence reached.")
        return 0


@script(
    positional("OUTCAR", default="OUTCAR", type=str, help="VASP output file"),
    flag("--silent", "-q", help="quite mode, just use the return code"),
)
def check_end(opts):
    from .outcar import normal_end

    with error_catch():
        try:
            with open(opts.outcar) as f:
                res = normal_end(f)
        except OSError:
            if not opts.silent:
                print("OUTCAR does not exist.")
            return 1

    if not opts.silent:
        if res:
            print("Computation ended normally.")
        else:
            print("Computation ended early.")

    return 0 if res else 1


@script(
    positional("DIR", default=".", type=str, help="VASP computation directory"),
    flag("--silent", "-q", help="quite mode, just use the return code"),
    optional("--osz", type=str, default=None, help="path to the OSZICAR file."),
    optional("--out", type=str, default=None, help="path to the OUTCAR file."),
    optional(
        "--tol", type=float, default=None, help="Tolerance on the energy residue."
    ),
)
def check_conv(opts):
    from .outcar import converged

    if opts.osz is None:
        osz = os.path.join(opts.dir, "OSZICAR")
    else:
        osz = opts.osz

    if opts.out is None:
        out = os.path.join(opts.dir, "OUTCAR")
    else:
        out = opts.out

    with error_catch():
        try:
            res, tol, residue = converged(osz, out, tol=opts.tol)
        except OSError:
            if not opts.silent:
                print("OUTCAR or OSZICAR does not exist.")
            return 1

    if not opts.silent:
        if res:
            print(f"Computation converged with tolerance {tol}.")
        elif residue is None:
            print("Abnormal ending of the computation.")
        else:
            print(f"Computation did not converge: {residue} > {tol}.")

    return 0 if res else 1


@script(
    positional("DIR", default=".", type=str, help="VASP computation directory"),
)
def check_coherence(opts):
    """Check the coherence of a computation directory."""
    from .coherence import check_coherence, Info, Bad, Critical

    bad = False, False

    for diag in check_coherence(opts.dir):
        if isinstance(diag, Info):
            print("Info: " + diag.msg)
        elif isinstance(diag, Bad):
            print("Bad: " + diag.msg)
            bad = True
        elif isinstance(diag, Critical):
            print("Error: " + diag.msg)
            bad = True
            break
        else:
            raise NotImplementedError(f"What is {diag}?")

    if bad:
        print("")
        print("╔════════════════════════════════════════╗")
        print("║  Some issues requires your attention!  ║")
        print("╚════════════════════════════════════════╝")
        print("")
        exit(1)


@script(
    positional("DIR", default=".", type=str, help="VASP computation directory"),
    optional("--dos", type=str, default=None, help="path to the DOSCAR file."),
    optional("--out", type=str, default=None, help="path to the OUTCAR file."),
    optional("--width", "-w", type=int, default=80, help="width of the plot."),
    optional("--height", type=int, default=50, help="height of the plot."),
    optional("--min", type=float, default=None, help="Lower energy bound of the plot"),
    optional("--max", type=float, default=None, help="Higher energy bound of the plot"),
)
def termdos(opts):
    """Dirty plot a dos in a terminal.

    Remark: Requires PyDEF
    """
    from pydef import load_cell

    if opts.dos is None:
        dos = os.path.join(opts.dir, "DOSCAR")
    else:
        dos = opts.dos

    if opts.out is None:
        out = os.path.join(opts.dir, "OUTCAR")
    else:
        out = opts.out

    with error_catch():
        cell = load_cell(out, dos)

    with error_catch():
        cell.load_dos()

    fermi = cell.fermi_energy
    if fermi is None:
        fermi = cell.fermi_level

    if fermi is None:
        print("No Fermi level found. Energy axis is unshifted.")
        fermi = 0.0

    for line in draw_dos(
        opts.height,
        opts.width,
        cell.dos_energy - fermi,
        cell.total_dos,
        low_bound=opts.min,
        high_bound=opts.max,
    ):
        print(line)


def draw_dos(nx, ny, energy, dos, low_bound=None, high_bound=None):
    import numpy as np

    if not np.all(np.diff(energy) > 0):
        raise ValueError("Energy axis not strictly increasing.")

    _low_bound = low_bound or np.min(energy)
    _high_bound = high_bound or np.max(energy)

    x = np.linspace(_low_bound, _high_bound, nx)

    y = np.interp(x, energy, dos)

    maxy = np.max(dos)

    quant = [quantize(ny, d, maxy) for d in y]

    prev_prev = quant[0]
    prev = quant[0]

    wrapped = []

    for n in quant[1:]:
        wrapped.append((prev_prev, prev, n))
        prev_prev = prev
        prev = n

    wrapped.append((prev_prev, prev, n))

    for e, (nprev, n, nnext) in zip(x, wrapped):
        if e % 10:
            prefix = f"{e:>7.3f} |"
        else:
            prefix = " " * 7 + " |"

        d1 = (n - nprev) // 2
        d2 = (nnext - n) // 2

        if d1 == d2 == 0:
            yield prefix + " " * n + "|"
        if d1 * d2 > 0:  # same sign
            if d1 > 0:
                yield prefix + " " * n + "<" + "=" * min(d1, d2)
            else:
                k = n + max(d1, d2)
                yield prefix + " " * k + "=" * (n - k) + ">"
        else:
            if d1 > 0:
                k1 = n - d1
                k2 = d2 - n
                yield prefix + " " * k1 + "°" * (n - k1) + "\\" + "." * k2
            else:
                k2 = n - d1
                k1 = d1 - n
                yield prefix + " " * k2 + "." * (n - k2) + "/" + "°" * k2


def quantize(ny, val, max):
    return int(ny * val / max)


@script(
    positional("PATH", default=".", help="Computation directory"),
    flag("--timing", help="show the timing informations"),
)
def report(opts):
    pc = PerfCounterCollec()

    with pc.imports:
        # numpy may be a significant time consumer
        import numpy as np
        from datetime import datetime, timedelta
        from .outcar_utils import get_val, get_int, get_float
        from .outcar import converged
        from .forces import read_forces

    outcar = os.path.join(opts.path, "OUTCAR")
    oszicar = os.path.join(opts.path, "OSZICAR")

    last_tot = None

    with pc.first_pass:
        with open(outcar) as f:
            date, time = get_val(f, "date").split()
            line = next(f)

            if line.startswith(" running on"):
                # vasp 5
                ncore = get_int([line], "running on", after="total cores")
            else:
                # vasp 6
                nmpi = get_int([line], "running", after="mpi-ranks")
                nthreads = get_int([line], "with", after="threads/rank")
                ncore = nmpi * nthreads

            for line in f:
                if line.startswith("  free  energy"):
                    last_tot = line
                    break

            for line in f:
                if line.startswith("  free  energy"):
                    last_tot = line
                elif line.startswith(" total amount of memory"):
                    break

            if last_tot is not None:
                elapsed = timedelta(seconds=get_float(f, "Elapsed time (sec):"))

    dt = datetime.fromisoformat(date.replace(".", "-") + " " + time)
    ago = datetime.now() - dt

    print("At", time, "on", date, f"({naturaldelta(ago)} ago)")
    print("Running on", ncore, "cores")

    if last_tot is None:
        print("Calculation stopped abnormally.")
        return

    total_energy = float(last_tot.split("=")[1].split()[0].strip())

    with pc.convergence_check:
        conv, _, _ = converged(oszicar, outcar)

    if conv:
        print(f"Computation converged within {naturaldelta(elapsed)}.")
    else:
        print("Computation did not converge.")

    with pc.get_forces, error_catch(), open(outcar) as f:
        species, forces, tol = read_forces(f)

    max_f = np.max(np.linalg.norm(forces, axis=-1))

    print(f"Total energy: {total_energy:0.05f} eV")
    print(f"Maximum residual force: {max_f:0.02e}")

    if opts.timing:
        print(pc.summary())
