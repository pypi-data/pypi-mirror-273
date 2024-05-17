# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import collections
from .outcar_utils import get_float, get_int
from .forces import read_forces
from .misc import InvalidInput
import numpy as np


def normal_end(file):
    for line in file:
        if line.startswith(" General timing and accounting informations"):
            return True
    return False


def converged(oszicar, outcar, tol=None):
    """Detect the kind of computation and return the converge criterion.

    .. seealso::

        :func:`forces_converged`, :func:`energy_converged`

    :param oszicar: path to the OSZICAR file
    :param outcar: path to the OUTCAR file
    :param tol: (optional, None) tolerance on the energy residue
    :return: :code:`(bool, float, float|None)` tuple with meaning:
      - converged
      - tolerance (in eV/A for optimizations, in eV otherwise)
      - maximum force (in eV/A) or residual energy (in eV) or None on abnormal ending
    """
    with open(outcar) as f:
        nsw = get_int(f, "NSW", after="number of steps", expect_equal=True)

    if nsw is None:
        return False, 0.0, None
    elif nsw > 1:
        return forces_converged(outcar, tol=tol)
    else:
        return energy_converged(oszicar, outcar, tol=tol)


def forces_converged(outcar, tol=None):
    """Check for the convergence of a forces calculation.

    :return: :code:`(bool, float, float|None)` tuple with meaning:
      - converged
      - tolerance (in eV/A)
      - maximum force (in eV/A) or None on abnormal ending
    """
    with open(outcar) as f:
        try:
            _, forces, _tol = read_forces(f)
            if not normal_end(f):
                return False, _tol, None
        except InvalidInput:
            return False, 0.0, None

    _tol = tol or _tol

    return (
        np.all(np.linalg.norm(forces, axis=-1) < _tol),
        _tol,
        np.max(np.linalg.norm(forces, axis=-1)),
    )


def energy_converged(oszicar, outcar, tol=None):
    """Check for the convergence of an energy calculation.

    :return: :code:`(bool, float, float|None)` tuple with meaning:
      - converged
      - tolerance (in eV)
      - final energy residue (in eV) or None on abnormal ending
    """
    with open(outcar) as f:
        if tol is None:
            _tol = get_float(f, "EDIFF ", after="stopping", expect_equal=True)
            if _tol is None:
                raise InvalidInput("Could not find the EDIFF tolerance.")
        else:
            _tol = tol
        if not normal_end(f):
            return False, _tol, None

    with open(oszicar) as f:
        t = tail(f, 2)
        second_to_last = next(t)
        last = next(t)

    try:
        ediff = float(second_to_last.split()[3])
    except ValueError:
        return False, _tol, None

    return ((abs(ediff) < _tol and "F=" in last), _tol, abs(ediff))


def tail(it, n):
    return iter(collections.deque(it, maxlen=n))
