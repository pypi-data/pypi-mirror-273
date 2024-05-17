# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
from .misc import InvalidInput


class Kpoints:
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data

    @classmethod
    def from_file(cls, path):
        # TODO
        with open(path) as f:
            next(f)  # first line is ignored

            n = int(next(f).strip())
            mode = next(f).strip()[0].lower()

            if n == 0:
                if mode not in {"m", "g"}:
                    raise InvalidInput(
                        f"Unknown k-point generation automatic mode {mode}"
                    )

                n1, n2, n3 = map(int, next(f).strip().split()[:3])

                return cls(mode, (n1, n2, n3))

            else:
                if mode not in {"c", "k", "r", "l"}:
                    raise InvalidInput("Unknown k-point explicit mode")

                if mode == "l":
                    line_coord = next(f).strip()[0].lower()
                    if line_coord != "f" and line_coord != "r":
                        raise InvalidInput(
                            "I don't want to deal with anything but fractional k points."
                        )

                    segments = []
                    first = None
                    for line in f:
                        if l := line.strip():
                            if first:
                                segments.append(
                                    (first, tuple(map(float, l.split()[:3])))
                                )
                                first = None
                            else:
                                first = tuple(map(float, l.split()[:3]))
                    return cls("line", segments)

                elif mode == "r":
                    points = []

                    for line in f:
                        if l := line.strip():
                            # FIXME does VASP actually takes empty lines here?
                            points.append(tuple(map(float, l.split()[:3])))

                    return cls("list", points)

                elif mode == "c":
                    # If you like cartesian mode feel free to implement the logic missing here
                    raise InvalidInput(
                        "Please don't use cartesian mode, it's a dumb mode I don't like it."
                    )
