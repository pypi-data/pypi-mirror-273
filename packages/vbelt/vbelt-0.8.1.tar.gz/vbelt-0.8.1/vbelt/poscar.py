# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import numpy as np
from .misc import electronegativity, InvalidInput


def nudge(poscar_src, poscar_dest, forces, A=0.01, rattle=0.0, cartesian=True):
    src = Poscar.from_file(poscar_src)

    if forces is not None and src.raw.shape != forces.shape:
        raise ValueError("Incompatible shapes of forces and positions.")

    nudged = src.raw

    if forces is not None:
        norm = np.linalg.norm(forces)

        if norm > 0:
            nudged += A * forces / norm
    else:
        norm = -1

    if rattle > 0:
        # rd is a randomly distrbuted set of displacement with stronger
        # intensities where the forces are intense
        if norm > 0:
            weigths = np.linalg.norm(forces, axis=-1)
        else:
            weigths = np.ones((nudged.shape[0],))
        rd = np.random.normal(size=(nudged.shape))
        rd *= weigths.reshape((-1, 1))
        rd /= np.linalg.norm(rd)

        nudged += rattle * rd

    src.raw = nudged
    src.to_file(poscar_dest, cartesian=cartesian)


def change_bond_length(
    poscar_src,
    poscar_dest,
    fixed_points,
    moved_species,
    amplitude=0,
    relative_amplitude=0,
    cartesian=True,
):
    """Change the length of bonds between `moved_species` and the closest of fixed_points.

    Exactly one of `amplitude` and `relative_amplitude` must be non-zero.
    Positive amplitudes lengthen the bonds, negative shorten them.

    :param poscar_src: source :class:`Poscar` instance
    :param fixed_points: array of coordinates of the fixed centers
    :param moved_species: the name of the species to move
    :param amplitude: (optional) the absolute amplitude of the move in A
    :param relative_amplitude: (optional) the relative amplitude of the move in fraction
    :param cartesian: if True, write the file in cartesian representation,
    :return: a new :class:`Poscar` instance with modified bonds.
    """
    if amplitude == 0 and relative_amplitude == 0:
        raise ValueError("One of amplitude or relative_amplitude must be non-zero.")

    if amplitude != 0 and relative_amplitude != 0:
        raise ValueError("Only one of amplitude or relative_amplitude can be non-zero.")

    relative = amplitude == 0

    dest = poscar_src.copy()

    for k, p1 in enumerate(dest.species[moved_species]):
        d = periodic_dist(dest.cell_parameters, np.array([p1]), fixed_points)
        i = np.argmin(d)
        v = periodic_diff(
            dest.cell_parameters,
            np.array([p1]),
            np.array([fixed_points[i]]),
        )[0]

        if relative:
            dest.species[moved_species][k] += relative_amplitude * v
        else:
            v /= np.linalg.norm(v)
            dest.species[moved_species][k] += amplitude * v

    return dest


def distance(poscar, i, j):
    sp, si = i
    pi = poscar.species[sp][si, :]

    sp, sj = j
    pj = poscar.species[sp][sj, :]

    return periodic_dist(poscar.cell_parameters, pi, pj)


def calc_econ(poscar, at, species):
    sp, j = at

    dists = np.array(
        [
            distance(poscar, at, (sp2, i))
            for sp2 in species
            for i in range(len(poscar.species[sp2]))
            if sp != sp2 or i != j
        ]
    )

    d_p = np.min(dists)

    eps = 1.0

    while eps > 1e-6:
        old_dp = d_p
        weights = np.exp(1.0 - (dists / d_p) ** 6)
        d_p = np.sum(dists * weights) / np.sum(weights)
        eps = abs(d_p - old_dp) / old_dp

    return np.sum(np.exp(1.0 - (dists / d_p) ** 6))


def calc_econ_tol(poscar, at, species, tol=0.5):
    sp, j = at

    dists = np.array(
        [
            distance(poscar, at, (sp2, i))
            for sp2 in species
            for i in range(len(poscar.species[sp2]))
            if sp != sp2 or i != j
        ]
    )

    d_p = np.min(dists)

    eps = 1.0

    while eps > 1e-6:
        old_dp = d_p
        weights = np.exp(1.0 - (dists / d_p) ** 6)
        d_p = np.sum(dists * weights) / np.sum(weights)
        eps = abs(d_p - old_dp) / old_dp

    return len(dists[np.exp(1.0 - (dists / d_p) ** 6) >= tol])


def periodic_dist(lattice, p1, p2):
    d = p1 - p2

    dfrac = np.remainder(d @ np.linalg.inv(lattice) + 0.5, 1.0) - 0.5

    return np.linalg.norm(dfrac @ lattice, axis=-1)


def periodic_diff(lattice, p1, p2):
    d = p1 - p2

    dfrac = np.remainder(d @ np.linalg.inv(lattice) + 0.5, 1.0) - 0.5

    return dfrac @ lattice


def get_disp(poscar1, poscar2, atoms=None):
    if atoms is None:
        p1 = poscar1.raw
        p2 = poscar2.raw
    else:
        p1 = np.ndarray((len(atoms), 3))
        p2 = np.ndarray((len(atoms), 3))

        for i, (sp, j) in enumerate(atoms):
            p1[i] = poscar1.species[sp][j]
            p2[i] = poscar2.species[sp][j]

    return periodic_diff(poscar1.cell_parameters, p1, p2)


class Poscar:
    def __init__(self, cell_parameters, species, species_names=None):
        """Create a Poscar type object, storing unit cell infos.

        :param cell_parameters: a 3x3 np.array with lattice vectors in line
        :param species: a dict[str, np.array] where the key is the name of the
          species and the array list positions.
          WARNING: Positions are in cartesian representation, not in fractional
          representation. Unit is Angstrom.
        """
        self.cell_parameters = cell_parameters
        self.species = species
        self._system_name = None
        if species_names is None:
            self._species_names = sorted(
                self.species.keys(), key=lambda p: electronegativity[p]
            )
        else:
            self._species_names = list(species_names)

    @property
    def raw(self):
        return np.vstack([self.species[n] for n in self._species_names])

    @raw.setter
    def raw(self, raw_data):
        offset = 0
        for n in self._species_names:
            slc = slice(offset, offset + len(self.species[n]), 1)
            self.species[n] = raw_data[slc]
            offset += len(self.species[n])

    @property
    def system_name(self):
        if self._system_name:
            return self._system_name
        else:
            species = list(self.species.items())
            # sort by increasing electronegativity
            species.sort(key=lambda p: electronegativity[p[0]])
            return " ".join(f"{label}{len(pos)}" for label, pos in species)

    @system_name.setter
    def system_name(self, val):
        self._system_name = val if val is None else str(val)

    def copy(self):
        "Fresh copy of the object."
        return self.__class__(
            self.cell_parameters.copy(),
            {sp: pos.copy() for sp, pos in self.species.items()},
            species_names=self._species_names,
        )

    @classmethod
    def from_cell(cls, cell):
        species = {}
        positions = cell.positions
        accum = 0
        for name, number in zip(cell.atoms_types, cell.nb_atoms):
            species[name] = positions[accum : accum + number]
            accum += number

        species_names = list(cell.atoms_types)
        params = cell.cell_parameters

        return Poscar(params, species, species_names=species_names)

    @classmethod
    def from_file(cls, filename, recenter=True):
        """Read structure from a POSCAR file.

        :param filename: the path to the file to read.
        :param recenter: (optional, :code:`True`)
        """
        with open(filename) as f:
            next(f)  # system name
            fac = float(next(f))
            params = fac * np.array(
                [
                    np.array(l.strip().split(), dtype="float")
                    for _, l in zip(range(3), f)
                ]
            )

            labels = next(f).strip().split()
            atoms_pop = list(map(int, next(f).strip().split()))
            if len(labels) != len(atoms_pop):
                raise InvalidInput(f"{filename} is not a coherent POSCAR file.")

            mode = next(f).strip()[0].lower()

            if mode == "s":
                # selective dynamics, skip line
                mode = next(f).strip()[0].lower()

            species = {}
            for spec, n in zip(labels, atoms_pop):
                if spec in species:
                    raise NotImplementedError(
                        "Repeated non contiguous species block is not supported."
                    )
                pos = []
                for _, line in zip(range(n), f):
                    ls = line.strip()
                    if not ls:
                        raise InvalidInput(f"{filename} is not a coherent POSCAR file.")
                    x, y, z, *_ = ls.split()
                    if mode == "d":
                        # Fractional coordinates
                        pos.append(np.array([x, y, z], dtype="float").dot(params))
                    else:
                        # Cartesian coordinates
                        pos.append(np.array([x, y, z], dtype="float"))
                species[spec] = np.array(pos)

        p = Poscar(params, species, species_names=labels)
        return p

    def to_file(self, path="POSCAR", cartesian=True):
        """Write a POSCAR file.

        The property system_name may be set to change the comment at the top of
        the file.
        :param path: path to the file to write
        :param cartesian: if True, write the file in cartesian representation,
          if False, write in fractional representation
        """
        with open(path, "w+") as out:
            species = [(n, self.species[n]) for n in self._species_names]

            out.write(f"{self.system_name}\n")
            out.write("1.0\n")
            np.savetxt(
                out, self.cell_parameters, "%15.12f", delimiter="\t", newline="\n"
            )

            out.write(" ".join(f"{name:6}" for name, _lst in species))
            out.write("\n")
            out.write(" ".join(f"{len(lst):6}" for _name, lst in species))
            out.write("\n")

            if cartesian:
                out.write("Cartesian\n")
                for _name, lst in species:
                    for pos in lst:
                        out.write("  ".join(f"{x:.8f}" for x in pos))
                        out.write("\n")
            else:
                out.write("Direct\n")
                inv_params = np.linalg.inv(self.cell_parameters)
                for _name, lst in species:
                    for pos in lst:
                        d_pos = pos.dot(inv_params)
                        out.write("  ".join(f"{x:.8f}" for x in d_pos))
                        out.write("\n")

    def recenter(self):
        "Ensure all coordinates are between 0 and 1 in fractional representation."
        pfrac = np.remainder(self.raw @ np.linalg.inv(self.cell_parameters), 1.0)

        self.raw = pfrac @ self.cell_parameters

    def reciprocal(self):
        "Reciprocal lattice vectors"
        return 2 * np.pi * np.linalg.inv(self.cell_parameters.T)


coord_methods = {
    "econ": calc_econ,
    "econ_tol": calc_econ_tol,
}
