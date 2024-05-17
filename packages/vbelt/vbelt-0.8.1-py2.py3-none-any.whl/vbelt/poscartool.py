"""A set of useful tools to manipulate VASP's POSCAR files.
"""

# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import re

from .script_utils import (
    MultiCmd,
    positional,
    flag,
    optional,
    error_catch,
    error,
    rest,
)

poscartool = MultiCmd(description=__doc__)


@poscartool.subcmd(
    positional("POSCAR", default="POSCAR", type=str, help="POSCAR file to nudge."),
    positional("OUTCAR", default="OUTCAR", type=str, help="VASP output file."),
    optional(
        "--amplitude",
        "-a",
        type=float,
        default=0.01,
        help="Total amplitude of the nudge in the forces direction.",
    ),
    optional(
        "--rattle",
        "-r",
        type=float,
        default=0.0,
        help="Add a random displacement of total amplitude FLOAT to the nudge.",
    ),
    flag(
        "--inplace",
        "-i",
        help="Directly overwrite the POSCAR instead of creating a new file with .nudge suffix.",
    ),
    optional(
        "--dest", "-o", type=str, default=None, help="Optional destination POSCAR"
    ),
    flag("--cartesian", "-c", help="Write POSCAR in cartesian coordinates."),
)
def nudge(opts):
    from .forces import read_forces
    from .poscar import nudge

    if opts.amplitude > 0:
        with error_catch(), open(opts.outcar) as f:
            _, forces, _ = read_forces(f)
    else:
        forces = None

    if opts.dest is not None:
        dest = opts.dest
    elif opts.inplace:
        dest = opts.poscar
    else:
        dest = opts.poscar + ".nudge"

    with error_catch():
        nudge(
            opts.poscar,
            dest,
            forces,
            A=opts.amplitude,
            rattle=opts.rattle,
            cartesian=opts.cartesian,
        )

    return 0


@poscartool.subcmd(
    positional("POSCAR", help="Source file."),
    positional("FIXED", type=str, help="Atom(s) to keep fixed."),
    positional("MOVED", type=str, help="Atoms to move."),
    positional("AMPLITUDE", help="Amplitude of the move in A or in %."),
    optional("--dest", "-o", type=str, default=None, help="Destionation file."),
    flag("--cartesian", "-C", help="Write POSCAR in cartesian coordinates."),
)
def nudge_bonds(opts):
    """Change the length of the bonds.

    Fixed atom can be either a species ("V": all vanadium atoms are concerned) or an atom specification
    ("V3", only the third vanadium atom is concerned).

    Negative amplitudes shorten the bonds, positive amplitudes lengthen them.
    Write 0.15 to mean "lengthen the bond by 0.15 A" and -1% to mean "shorten
    the bond by 1%"
    """
    from .poscar import change_bond_length, Poscar
    import numpy as np

    src = opts.poscar
    dest = opts.poscar + ".nudged" if opts.dest is None else opts.dest

    src = Poscar.from_file(src)

    sp_name, sp_id = parse_spec(src, opts.fixed)

    if sp_id is None:
        fixed = src.species[sp_name]
    else:
        fixed = np.array([src.species[sp_name][sp_id]])

    if opts.amplitude.endswith("%"):
        amplitude = float(opts.amplitude[:-1]) / 100
        print(amplitude)
        res = change_bond_length(
            src,
            dest,
            fixed,
            opts.moved,
            relative_amplitude=amplitude,
            cartesian=opts.cartesian,
        )
    else:
        amplitude = float(opts.amplitude)
        res = change_bond_length(
            src, dest, fixed, opts.moved, amplitude=amplitude, cartesian=opts.cartesian
        )

    res.to_file(dest)


@poscartool.subcmd(
    positional("POSCAR", help="Source file."),
    positional("DEST", default=None, help="Destionation file."),
)
def xyz(opts):
    from .poscar import Poscar

    if opts.dest:
        dest = opts.dest
    else:
        dest = opts.poscar + ".xyz"

    poscar = Poscar.from_file(opts.poscar)
    poscar.recenter()

    with error_catch(), open(dest, "w") as f:
        print(len(poscar.raw), file=f)

        print(poscar.system_name, file=f)

        for sp, pos in poscar.species.items():
            for p in pos:
                print(sp, *p, file=f)


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("ATOM1", type=str, help="First atom."),
    positional(
        "ATOM2",
        default=None,
        type=str,
        help="Second atom, if ommited all atoms are considered.",
    ),
    optional(
        "--max", "-m", default=None, type=int, help="Maximum number of distances shown."
    ),
    flag("--raw", help="Just ouput values in A."),
)
def dist(opts):
    from .poscar import distance, Poscar

    poscar = Poscar.from_file(opts.poscar)
    at1 = parse_spec(poscar, opts.atom1)

    if at1[1] is None:
        error(f"First atom need to be numbered (ex: {at1[0]}1)")

    sp1 = spec(poscar, at1)

    if opts.atom2 is None:
        with error_catch():
            dists = [
                (distance(poscar, at1, (sp, i)), spec(poscar, (sp, i)))
                for sp, p in poscar.species.items()
                for i in range(len(p))
                if sp1 != spec(poscar, (sp, i))
            ]

        dists.sort()

        if opts.max is not None:
            dists = dists[: opts.max]

        for i, (d, sp) in enumerate(dists):
            if opts.raw:
                print(d)
            else:
                bond = f"{sp1}--{sp}"
                print(f"{bond:12}: {d: 9.5f} A")
    else:
        (s2, i2) = at2 = parse_spec(poscar, opts.atom2)

        if i2 is None:
            with error_catch():
                dists = [
                    (distance(poscar, at1, (s2, i)), spec(poscar, (s2, i)))
                    for i in range(len(poscar.species[s2]))
                    if sp1 != spec(poscar, (s2, i))
                ]

            dists.sort()

            if opts.max is not None:
                dists = dists[: opts.max]

            for d, sp in dists:
                if sp == sp1:
                    continue
                if opts.raw:
                    print(d)
                else:
                    bond = f"{sp1}--{sp}"
                    print(f"{bond:12}: {d: 9.5f} A")
        else:
            sp2 = spec(poscar, at2)
            d = distance(poscar, at1, at2)
            if opts.raw:
                print(d)
            else:
                print(f"{sp1}--{sp2}: {d:0.5f} A")


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("ATOM", type=str, help="Investigated atom."),
    positional("SPECIES", type=str, help="Coordinating species."),
    optional("--method", "-m", default="econ", help="Computation method."),
)
def coord(opts):
    """Evaluate a coordination number for a given atom and a coordinating species."""
    from .poscar import Poscar, coord_methods

    poscar = Poscar.from_file(opts.poscar)
    at = parse_spec(poscar, opts.atom)

    fn = coord_methods.get(opts.method, None)

    if fn is None:
        error(f"Unkown method {opts.method}, try one of {list(coord_methods.keys())}.")

    with error_catch():
        coord = fn(poscar, at, opts.species.split(","))

    print(f"{coord:0.03f}")


@poscartool.subcmd(
    positional("POSCAR1", help="Displaced positions."),
    positional("POSCAR2", help="Reference positions."),
    optional("--ref", "-r", default=None, help="Atom to consider fixed."),
    flag("--direct", "-d", help="Output in lattice coordinates."),
    flag("--no-center", "-C", help="Do not force the mean displacement to be null."),
    rest("ATOMS", default=[], help="Atoms to consider."),
)
def disp(opts):
    """Compute the displacement between two structures."""
    from .poscar import get_disp, Poscar
    import numpy as np

    poscar1 = Poscar.from_file(opts.poscar1)
    poscar2 = Poscar.from_file(opts.poscar2)

    # FIXME normalize the rotation
    # We need to normalize the positions if they are not exactly in the same representation.
    # That is, we need to be sure that the same cell is represented in both case.

    print(poscar1.cell_parameters)
    print(poscar2.cell_parameters)

    if opts.ref is not None:
        with error_catch():
            sp, i = parse_spec(poscar1, opts.ref)

        offset = poscar1.species[sp][i] - poscar2.species[sp][i]

        poscar1.raw = poscar1.raw - offset.reshape((1, 3))

    if not opts.atoms:
        ats = None
    else:
        ats = [parse_spec(poscar1, at) for at in opts.atoms]

    with error_catch():
        disps = get_disp(poscar1, poscar2, ats)

    norms = np.linalg.norm(disps, axis=-1)

    if not opts.no_center:
        disps -= np.sum(disps, axis=0)

    if opts.direct:
        disps = disps @ np.linalg.inv(poscar1.cell_parameters)

    if ats is None:
        ats = list(range(len(disps)))

    for at, (x, y, z), n in zip(ats, disps, norms):
        sp = spec(poscar1, at)
        print(f"{sp:<3}:", f"{x:9.05f}, {y:9.05f}, {z:9.05f} ({n:9.05f} A)")


@poscartool.subcmd(
    positional("POSCAR", help="Positions to process."),
    optional("--dest", "-o", default="POSCAR.sub", help="Displaced positions."),
    optional("--ref", "-r", default=None, help="Reference atom to group around."),
    optional("--offset", "-s", default=None, help="Offset to apply to all atoms."),
    rest("ATOMS", help="Atoms to keep."),
)
def subset(opts):
    from itertools import groupby
    import numpy as np
    from .poscar import Poscar, periodic_diff

    poscar = Poscar.from_file(opts.poscar)

    with error_catch():
        ats = {
            k: [i for _, i in l]
            for k, l in groupby(
                (parse_spec(poscar, at) for at in opts.atoms),
                lambda p: p[0],
            )
        }
    if opts.ref is not None:
        with error_catch():
            rsp, ri = parse_spec(poscar, opts.ref)
            rpos = poscar.species[rsp][ri].reshape((1, 3))

    if opts.offset is not None:
        with error_catch():
            offset = np.array(opts.offset.split(","), dtype=float).reshape(1, 3)
    else:
        offset = np.zeros((1, 3))

    species = {}
    for k, l in ats.items():
        species[k] = np.ndarray((len(l), 3))

        for i, j in enumerate(l):
            species[k][i] = poscar.species[k][j]

        if opts.ref is not None:
            species[k] = periodic_diff(poscar.cell_parameters, species[k], rpos)

        species[k] += offset

    new = Poscar(poscar.cell_parameters, species)

    with error_catch():
        new.to_file(opts.dest)


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("CENTER", type=str, help="Center atom."),
    positional(
        "ATOMS",
        type=str,
        help="Neighbors to take into account.",
    ),
    optional(
        "--max", "-m", default=None, type=int, help="Maximum number of distances shown."
    ),
    optional(
        "--tol",
        "-t",
        default=0.05,
        type=float,
        help="Tolerance in A to consider two atoms equivalent.",
    ),
)
def pointsym(opts):
    """Evaluate the point symmetry around a given atom."""
    import numpy as np
    from .poscar import distance, Poscar, periodic_diff
    from pymatgen.core import Molecule
    from pymatgen.symmetry.analyzer import PointGroupAnalyzer

    poscar = Poscar.from_file(opts.poscar)
    (sp1, i1) = at1 = parse_spec(poscar, opts.center)

    if i1 is None:
        error(f"First atom need to be numbered (ex: {at1[0]}1)")

    if opts.atoms is None:
        error("Neighbors detection is not implemented. Provide the ATOMS parameter.")

    (s2, i2) = parse_spec(poscar, opts.atoms)

    with error_catch():
        dists = [
            (distance(poscar, at1, (s2, i)), pos, s2)
            for i, pos in enumerate(poscar.species[s2])
            if sp1 != spec(poscar, (s2, i))
        ]

    dists.sort(key=lambda t: (t[0], *t[1], t[2]))

    if opts.max is None:
        error("Neighbors automatic selection is not implemented. Use the --max flag.")

    dists = dists[: opts.max]

    pos_center = poscar.species[sp1][i1, :]
    positions = np.array(
        [
            [0, 0, 0],  # makes pos_center the origin
            *(
                periodic_diff(poscar.cell_parameters, pos, pos_center)
                for _, pos, _ in dists
            ),
        ]
    )
    species = [sp1, *(sp for _, _, sp in dists)]

    mol = Molecule(species, positions)

    with error_catch():
        print(
            PointGroupAnalyzer(
                mol,
                tolerance=opts.tol,
                eigen_tolerance=opts.tol / 20,
                matrix_tolerance=opts.tol / 3,
            ).get_pointgroup()
        )


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("CENTER", type=str, help="Center atom."),
    positional(
        "ATOMS",
        type=str,
        help="Neighbors to take into account.",
    ),
    optional(
        "--max",
        "-m",
        default=None,
        type=int,
        help="Maximum number of neighbors considered.",
    ),
)
def volume(opts):
    """Evaluate the volume of a polyhedron around a given atom."""
    import numpy as np
    from .poscar import distance, Poscar, periodic_diff
    from scipy.spatial import ConvexHull

    poscar = Poscar.from_file(opts.poscar)
    (sp1, i1) = at1 = parse_spec(poscar, opts.center)

    if i1 is None:
        error(f"First atom need to be numbered (ex: {at1[0]}1)")

    if opts.atoms is None:
        error("Neighbors detection is not implemented. Provide the ATOMS parameter.")

    (s2, i2) = parse_spec(poscar, opts.atoms)

    with error_catch():
        dists = [
            (distance(poscar, at1, (s2, i)), pos, s2)
            for i, pos in enumerate(poscar.species[s2])
            if sp1 != spec(poscar, (s2, i))
        ]

    dists.sort(key=lambda t: (t[0], *t[1], t[2]))

    if opts.max is None:
        error("Neighbors automatic selection is not implemented. Use the --max flag.")

    dists = dists[: opts.max]

    pos_center = poscar.species[sp1][i1, :]
    positions = np.array(
        [periodic_diff(poscar.cell_parameters, pos, pos_center) for _, pos, _ in dists]
    )

    hull = ConvexHull(positions)

    print(hull.volume, "A^3")


@poscartool.subcmd(
    positional("POSCAR", type=str, help="POSCAR file to observe."),
    positional("CENTER", type=str, help="Center atom."),
    positional(
        "ATOMS",
        type=str,
        help="Neighbors to take into account.",
    ),
    optional(
        "--max", "-m", default=None, type=int, help="Maximum number of distances shown."
    ),
    optional(
        "--tol",
        "-t",
        default=0.05,
        type=float,
        help="Tolerance in A to consider two atoms equivalent.",
    ),
)
def poly(opts):
    """Collect informations on a polyhedron."""
    import numpy as np
    from .poscar import distance, Poscar, periodic_diff
    from pymatgen.core import Molecule
    from pymatgen.symmetry.analyzer import PointGroupAnalyzer
    from scipy.spatial import ConvexHull

    poscar = Poscar.from_file(opts.poscar)
    (sp1, i1) = at1 = parse_spec(poscar, opts.center)

    if i1 is None:
        error(f"First atom need to be numbered (ex: {at1[0]}1)")

    if opts.atoms is None:
        error("Neighbors detection is not implemented. Provide the ATOMS parameter.")

    (s2, i2) = parse_spec(poscar, opts.atoms)

    with error_catch():
        dists = [
            (distance(poscar, at1, (s2, i)), pos, s2, i)
            for i, pos in enumerate(poscar.species[s2])
            if sp1 != spec(poscar, (s2, i))
        ]

    dists.sort(key=lambda t: (t[0], *t[1], t[2], t[3]))

    if opts.max is None:
        error("Neighbors automatic selection is not implemented. Use the --max flag.")

    dists = dists[: opts.max]

    pos_center = poscar.species[sp1][i1, :]
    positions = np.array(
        [
            [0, 0, 0],  # makes pos_center the origin
            *(
                periodic_diff(poscar.cell_parameters, pos, pos_center)
                for _, pos, _, _ in dists
            ),
        ]
    )
    species = [sp1, *(sp for _, _, sp, _ in dists)]

    mol = Molecule(species, positions)

    with error_catch():
        for d, _, sp, i in dists:
            if sp == sp1:
                continue
            bond = f"{sp1}--{sp}{i+1}"
            print(f"{bond:12}: {d: 9.5f} A")

        hull = ConvexHull(positions[1:])

        print(f"Volume = {hull.volume:0.05f} A^3")

        group = PointGroupAnalyzer(
            mol,
            tolerance=opts.tol,
            eigen_tolerance=opts.tol / 20,
            matrix_tolerance=opts.tol / 3,
        ).get_pointgroup()

        print("Point symmetry =", group)


def spec(poscar, sp):
    if isinstance(sp, int):
        i = sp
        for n in poscar._species_names:
            if i < len(poscar.species[n]):
                return f"{n}{i + 1}"
            else:
                i -= len(poscar.species[n])
        raise ValueError(f"{i} is larger than the number of atoms.")
    else:
        n, i = sp
        return f"{n}{i + 1}"


def parse_spec(poscar, spec):
    try:
        i = int(spec) - 1
    except ValueError:
        with error_catch():
            if m := re.match("([A-Z][a-z]?)([0-9]+)", spec):
                sp, i = m.groups()
                return (sp, int(i) - 1)
            elif m := re.match("([A-Z][a-z]?)", spec):
                (sp,) = m.groups()
                return (sp, None)
            else:
                raise ValueError(f"Unrecognize atom specification {spec}")
    for n in poscar._species_names:
        if i < len(poscar.species[n]):
            return (n, i)
        else:
            i -= len(poscar.species[n])
    raise ValueError(f"{i} is larger than the number of atoms.")
