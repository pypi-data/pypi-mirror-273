# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
from itertools import islice
import numpy as np

from .misc import InvalidInput
from .outcar_utils import get_species, get_array, get_float


def read_forces(file):
    for line in file:
        if "POTCAR" in line:
            break
    else:
        raise InvalidInput("Could not find the list of potential.")

    first = line

    nb_specs = 1
    for line in file:
        if "POTCAR" not in line:
            break  # works in v5
        elif line == first:
            break  # works in v6
        nb_specs += 1

    species = [get_species(file) for _ in range(nb_specs)]

    nb_atoms = get_array(
        file,
        "ions per type",
        expect_equal=True,
        map_=int,
    )

    nb_tot = sum(nb_atoms)

    assert len(nb_atoms) == nb_specs

    tol = get_float(file, "EDIFFG", expect_equal=True, after="stop")

    assert tol is not None

    if tol > 0:
        tol *= 10.0
    else:
        tol *= -1.0

    raw = None

    while True:
        for line in file:
            if "TOTAL-FORCE" in line:
                break
        else:
            break  # EOF

        raw = list(islice(file, 1, 1 + nb_tot))

    if raw is None:
        raise InvalidInput("Forces not found.")

    forces = np.array([line.split()[3:] for line in raw], dtype=float)

    return list(zip(species, nb_atoms)), forces, tol
