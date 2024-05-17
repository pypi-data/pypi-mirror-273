# vbelt: The VASP user toolbelt.
# Copyright (C) 2023  Théo Cavignac
# Licensed under EUPL
import os

import numpy as np

from .poscar import Poscar
from .potcar import Potcar, predict_nelect
from .incar import parse_incar_all
from .kpoints import Kpoints


class Problem:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def badness(self):
        return self._badness


class Info(Problem):
    _badness = 1


class Bad(Problem):
    _badness = 2


class Critical(Problem):
    _badness = 3


def check_coherence(directory):
    try:
        incar = parse_incar_all(os.path.join(directory, "INCAR"))
        poscar = Poscar.from_file(os.path.join(directory, "POSCAR"))
        potcar = Potcar.from_file(os.path.join(directory, "POTCAR"))
        kpoints = Kpoints.from_file(os.path.join(directory, "KPOINTS"))
    except FileNotFoundError:
        yield Critical("Missing input files")
        return

    if kpoints.kind == "line":
        mode = "bands"
    elif incar.get("ISMEAR", "1") == "-2":
        mode = "cDFT"
    elif "defect" in os.path.realpath(directory):
        mode = "defect"
    elif int(incar.get("NSW", 0)) == 0 and float(incar.get("EDIFFG", "10")) == 10:
        mode = "sp"
    else:
        mode = "optim"

    if set(incar.keys()) - known_keys:
        yield Bad("Unknown INCAR keys.")

    if mode == "defect" and incar.get("ISYM", "1") != "0":
        yield Bad("ISYM != 0 in defect mode.")

    if (mode == "defect" or mode == "optim" or mode == "cDFT") and float(
        incar.get("EDIFF", "1e-4")
    ) > 1e-5:
        yield Bad("EDIFF > 1e-5 in defect or optim mode.")

    if mode == "sp" and float(incar.get("EDIFF", "1e-4")) > 1e-6:
        yield Bad("EDIFF > 1e-6 in sp mode.")

    enmax = max(sp["enmax"] for sp in potcar.species)
    min_encut = enmax * 1.3

    if float(incar.get("ENCUT", enmax)) < min_encut:
        yield Bad(f"ENCUT < {min_encut:.0}.")

    if mode in {"optim", "DoS", "bands"}:
        if incar.get("LWAVE", ".TRUE.") != ".FALSE.":
            yield Info("You may want to set LWAVE = .FALSE.")
        if incar.get("LCHARG", ".TRUE.") != ".FALSE.":
            yield Info("You may want to set LCHARG = .FALSE.")

    if mode == "optim":
        if float(incar.get("EDIFFG", "10")) < -1e-2:
            yield Bad("EDIFFG < -1e-2.")
        if float(incar.get("EDIFFG", "10")) > 0:
            yield Bad("EDIFFG > 0.")

    expected = predict_nelect(poscar, potcar)
    nelect = incar.get("NELECT", expected)

    if expected != nelect:
        yield Info(f"Charged cell {expected - nelect} e")

    if mode == "DoS" or mode == "sp":
        if int(incar.get("ISMEAR", 1)) != -5:
            yield Bad("ISMEAR should be -5")

    elif mode == "defect":
        if int(incar.get("ISMEAR", 1)) != -4:
            yield Bad("ISMEAR should be -4")

    elif mode == "optim" or mode == "bands":
        if int(incar.get("ISMEAR", 1)) != 0:
            yield Bad("ISMEAR should be 0")

        if float(incar.get("SIGMA", 0.2)) > 0.05:
            yield Bad("SIGMA seems too big.")

    if mode == "DoS" or mode == "bands":
        if float(incar.get("EMIN", 0)) > float(incar.get("EMAX", 0)):
            yield Bad("EMIN > EMAX")

        if int(incar.get("NEDOS", 301)) < 1000:
            yield Bad("Low NEDOS")

    if set(poscar.species.keys()) != {sp["name"] for sp in potcar.species}:
        yield Critical("POTCAR and POSCAR don't specify the same species!")

    if kpoints.kind == "list":
        yield Info("Explicit list of k-points, you're on your own.")

    elif kpoints.kind == "g" or kpoints.kind == "m":
        b1, b2, b3 = map(np.linalg.norm, poscar.reciprocal())
        n1, n2, n3 = kpoints.data

        if mode in {"DoS", "sp"}:
            if kpoints.kind != "g":
                yield Bad("For energy computation, prefer Gamma centered mesh.")

        if mode == "optim":
            if kpoints.kind != "m":
                yield Bad("For optimization, prefer non constrained MP mesh.")

        d1, d2, d3 = n1 / b1, n2 / b2, n3 / b3

        if max([d1, d2, d3]) / min([d1, d2, d3]) > 1.1:
            yield Bad(f"k-point density is not homogeneous {d1:.0}:{d2:.0}{d3:.0f}")

        if mode == "optim":
            if min([d1, d2, d3]) < 4:
                yield Critical(
                    f"k-point density is REALLY low. {min([d1, d2, d3]):.0f}"
                )

            elif min([d1, d2, d3]) < 6:
                yield Bad(f"k-point density is pretty low. {min([d1, d2, d3]):.0}")
        else:
            if min([d1, d2, d3]) < 7:
                yield Critical(
                    f"k-point density is REALLY low. {min([d1, d2, d3]):.0f}"
                )

            elif min([d1, d2, d3]) < 9:
                yield Bad(f"k-point density is pretty low. {min([d1, d2, d3]):.0f}")

    return True


known_keys = {
    "ADDGRID",
    "AEXX",
    "AGGAC",
    "AGGAX",
    "ALDAC",
    "ALGO",
    "AMIN",
    "AMIX",
    "AMIX_MAG",
    "ANDERSEN_PROB",
    "ANTIRES",
    "APACO",
    "BMIX",
    "BMIX_MAG",
    "CH_LSPEC",
    "CH_NEDOS",
    "CH_SIGMA",
    "CLL",
    "CLN",
    "CLNT",
    "CLZ",
    "CMBJ",
    "CMBJA",
    "CMBJB",
    "CSHIFT",
    "DEPER",
    "DIMER_DIST",
    "DIPOL",
    "DQ",
    "EBREAK",
    "EDIFF",
    "EDIFFG",
    "EFIELD",
    "EFIELD_PEAD",
    "EINT",
    "EMAX",
    "EMIN",
    "ENAUG",
    "ENCUT",
    "ENCUTFOCK",
    "ENCUTGW",
    "ENCUTGWSOFT",
    "ENINI",
    "EPSILON",
    "ESTOP",
    "EVENONLY",
    "EVENONLYGW",
    "FERDO",
    "FERWE",
    "FINDIFF",
    "GGA",
    "GGA_COMPAT",
    "HFLMAX",
    "HFRCUT",
    "HFSCREEN",
    "HILLS_BIN",
    "HILLS_H",
    "HILLS_W",
    "HITOLER",
    "I_CONSTRAINED_M",
    "IALGO",
    "IBAND",
    "IBRION",
    "ICHARG",
    "ICHIBARE",
    "ICORELEVEL",
    "IDIPOL",
    "IEPSILON",
    "IGPAR",
    "IMAGES",
    "IMIX",
    "INCREM",
    "INIMIX",
    "INIWAV",
    "IPEAD",
    "ISIF",
    "ISMEAR",
    "ISPIN",
    "ISTART",
    "ISYM",
    "IVDW",
    "IWAVPR",
    "KBLOCK",
    "KGAMMA",
    "KPAR",
    "KPOINT_BSE",
    "KPUSE",
    "KSPACING",
    "LADDER",
    "LAECHG",
    "LAMBDA",
    "LANGEVIN_GAMMA",
    "LANGEVIN_GAMMA_L",
    "LASPH",
    "LASYNC",
    "LATTICE_CONSTRAINTS",
    "LBERRY",
    "LBLUEOUT",
    "LBONE",
    "LCALCEPS",
    "LCALCPOL",
    "LCHARG",
    "LCHIMAG",
    "LCORR",
    "LDAU",
    "LDAUJ",
    "LDAUL",
    "LDAUPRINT",
    "LDAUTYPE",
    "LDAUU",
    "LDIAG",
    "LDIPOL",
    "LEFG",
    "LELF",
    "LEPSILON",
    "LFINITE_TEMPERATURE",
    "LFOCKACE",
    "LFOCKAEDFT",
    "LHARTREE",
    "LHFCALC",
    "LHYPERFINE",
    "LKPROJ",
    "LLRAUG",
    "LMAXFOCK",
    "LMAXFOCKAE",
    "LMAXMIX",
    "LMAXPAW",
    "LMAXTAU",
    "LMIXTAU",
    "LMODELHF",
    "LMONO",
    "LMP2LT",
    "LNABLA",
    "LNMR_SYM_RED",
    "LNONCOLLINEAR",
    "LOCPROJ",
    "LOPTICS",
    "LORBIT",
    "LORBMOM",
    "LPARD",
    "LPEAD",
    "LPLANE",
    "LREAL",
    "LRPA",
    "LSCAAWARE",
    "LSCALAPACK",
    "LSCALU",
    "LSCSGRAD",
    "LSELFENERGY",
    "LSEPB",
    "LSEPK",
    "LSMP2LT",
    "LSORBIT",
    "LSPECTRAL",
    "LSPECTRALGW",
    "LSPIRAL",
    "LSUBROT",
    "LTHOMAS",
    "LUSE_VDW",
    "LVDW_EWALD",
    "LVDW_ONECELL",
    "LVDWEXPANSION",
    "LVHAR",
    "LVTOT",
    "LWANNIER90",
    "LWANNIER90_RUN",
    "LWAVE",
    "LWRITE_MMN_AMN",
    "LWRITE_UNK",
    "LWRITE_WANPROJ",
    "LZEROZ",
    "M_CONSTR",
    "MAGMOM",
    "MAXMEM",
    "MAXMIX",
    "MDALGO",
    "METAGGA",
    "MINROT",
    "MIXPRE",
    "ML_FF_AFILT2_MB",
    "ML_FF_CDOUB",
    "ML_FF_CSF",
    "ML_FF_CSIG",
    "ML_FF_CSLOPE",
    "ML_FF_CTIFOR",
    "ML_FF_EATOM",
    "ML_FF_IAFILT2_MB",
    "ML_FF_IBROAD1_MB",
    "ML_FF_IBROAD2_MB",
    "ML_FF_ICOUPLE_MB",
    "ML_FF_ICUT1_MB",
    "ML_FF_ICUT2_MB",
    "ML_FF_IERR",
    "ML_FF_IREG_MB",
    "ML_FF_ISAMPLE",
    "ML_FF_ISCALE_TOTEN_MB",
    "ML_FF_ISOAP1_MB",
    "ML_FF_ISOAP2_MB",
    "ML_FF_ISTART",
    "ML_FF_IWEIGHT",
    "ML_FF_LAFILT2_MB",
    "ML_FF_LBASIS_DISCARD",
    "ML_FF_LCONF_DISCARD",
    "ML_FF_LCOUPLE_MB",
    "ML_FF_LCRITERIA",
    "ML_FF_LEATOM_MB",
    "ML_FF_LHEAT_MB",
    "ML_FF_LMAX2_MB",
    "ML_FF_LMLFF",
    "ML_FF_LNORM1_MB",
    "ML_FF_LNORM2_MB",
    "ML_FF_MB_MB",
    "ML_FF_MCONF",
    "ML_FF_MCONF_NEW",
    "ML_FF_MHIS",
    "ML_FF_MRB1_MB",
    "ML_FF_MRB2_MB",
    "ML_FF_MSPL1_MB",
    "ML_FF_MSPL2_MB",
    "ML_FF_NATOM_COUPLED_MB",
    "ML_FF_NDIM_SCALAPACK",
    "ML_FF_NHYP1_MB",
    "ML_FF_NHYP2_MB",
    "ML_FF_NMDINT",
    "ML_FF_NR1_MB",
    "ML_FF_NR2_MB",
    "ML_FF_NWRITE",
    "ML_FF_RCOUPLE_MB",
    "ML_FF_RCUT1_MB",
    "ML_FF_RCUT2_MB",
    "ML_FF_SIGV0_MB",
    "ML_FF_SIGW0_MB",
    "ML_FF_SION1_MB",
    "ML_FF_SION2_MB",
    "ML_FF_W1_MB",
    "ML_FF_W2_MB",
    "ML_FF_WTIFOR",
    "ML_FF_WTOTEN",
    "ML_FF_WTSIF",
    "NBANDS",
    "NBANDSGW",
    "NBANDSO",
    "NBANDSV",
    "NBLK",
    "NBLOCK",
    "NBMOD",
    "NBSEEIG",
    "NCORE",
    "NCORE_IN_IMAGE1",
    "NCRPA_BANDS",
    "NDAV",
    "NEDOS",
    "NELECT",
    "NELM",
    "NELMDL",
    "NELMIN",
    "NFREE",
    "NGX",
    "NGXF",
    "NGY",
    "NGYF",
    "NGYROMAG",
    "NGZ",
    "NGZF",
    "NKRED",
    "NKREDX",
    "NKREDY",
    "NKREDZ",
    "NLSPLINE",
    "NMAXFOCKAE",
    "NMAXFOCKAE",
    "LMAXFOCKAE",
    "NOMEGA",
    "NOMEGAPAR",
    "NOMEGAR",
    "NPACO",
    "NPAR",
    "NPPSTR",
    "NSIM",
    "NSTORB",
    "NSUBSYS",
    "NSW",
    "NTARGET_STATES",
    "NTAUPAR",
    "NUPDOWN",
    "NWRITE",
    "ODDONLY",
    "ODDONLYGW",
    "OFIELD_A",
    "OFIELD_KAPPA",
    "OFIELD_Q6_FAR",
    "OFIELD_Q6_NEAR",
    "OMEGAMAX",
    "OMEGAMIN",
    "OMEGATL",
    "PARAM1",
    "PARAM2",
    "PFLAT",
    "PHON_LBOSE",
    "PHON_LMC",
    "PHON_NSTRUCT",
    "PHON_NTLIST",
    "PHON_TLIST",
    "PLEVEL",
    "PMASS",
    "POMASS",
    "POTIM",
    "PREC",
    "PRECFOCK",
    "PROUTINE",
    "PSTRESS",
    "PSUBSYS",
    "PTHRESHOLD",
    "QMAXFOCKAE",
    "QSPIRAL",
    "QUAD_EFG",
    "RANDOM_SEED",
    "ROPT",
    "RWIGS",
    "SAXIS",
    "SCALEE",
    "SCSRAD",
    "SHAKEMAXITER",
    "SHAKETOL",
    "SIGMA",
    "SMASS",
    "SMEARINGS",
    "SPRING",
    "STEP_MAX",
    "STEP_SIZE",
    "SYMPREC",
    "SYSTEM",
    "TEBEG",
    "TEEND",
    "TIME",
    "TSUBSYS",
    "VALUE_MAX",
    "VALUE_MIN",
    "VCA",
    "VCAIMAGES",
    "VCUTOFF",
    "VDW_A1",
    "VDW_A2",
    "VDW_C6",
    "VDW_CNRADIUS",
    "VDW_D",
    "VDW_R0",
    "VDW_RADIUS",
    "VDW_S6",
    "VDW_S8",
    "VDW_SR",
    "VOSKOWN",
    "WC",
    "WEIMIN",
    "ZVAL",
}
