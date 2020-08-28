import mbuild
import numpy as np


NM_TO_BOHR = 18.8972598858
BAR_TO_ATOMIC = 3.3988276e-9


def write_data(system, filen):
    """Write a metalwalls data file from an mbuild.Compound

    Parameters
    ----------
    system : mbuild.Compound
        system to save to file
    filen : string
        filename

    Returns
    -------

    Notes
    -----
    Only writes coordinates. Metalwalls requires that the atoms
    are written in the same order that the atomtypes appear
    in the runtime.inpt file. The contents of system must be properly
    sorted before calling this function
    """
    contents = """# header
step 0
num_atoms {natoms}
num_electrode_atoms 0
# box {boxx} {boyy} {bozz}
# coordinates : {natoms} atoms - step 0
""".format(
        natoms=system.n_particles,
        boxx=system.periodicity[0] * NM_TO_BOHR,
        boyy=system.periodicity[1] * NM_TO_BOHR,
        bozz=system.periodicity[2] * NM_TO_BOHR,
    )

    for child in system.children:
        contents += "{} {} {} {}\n".format(
                child.name,
                child.xyz[0][0] * NM_TO_BOHR,
                child.xyz[0][1] * NM_TO_BOHR,
                child.xyz[0][2] * NM_TO_BOHR,
            )

    with open(filen, "w") as f:
        f.write(contents)


def read_data(filen):
    """Read a metalwalls data file and return an mbuild.Compound

    Parameters
    ----------
    filen : string
        filename to read

    Returns
    -------
    system : mbuild.Compound
        system coordinates contained in data file

    Notes
    -----
    Only reads coordinates.
    """

    data = []
    with open(filen) as f:
        for line in f:
            data.append(line.strip().split())

    # Header formatting checks
    if (
        data[0][0] != "#" or
        data[0][1].lower() != "header" or
        data[1][0].lower() != "step" or
        data[2][0].lower() != "num_atoms" or
        data[3][0].lower() != "num_electrode_atoms" or
        data[4][0] != "#" or
        data[4][1].lower() != "box" or
        data[6][0] != "#" or
        data[6][1].lower() != "coordinates"
        ):
        raise ValueError("Invalid format for metalwalls restart file")

    num_atoms = int(data[2][1])
    boxx = float(data[5][0]) * BOHR_TO_NM
    boyy = float(data[5][1]) * BOHR_TO_NM
    bozz = float(data[5][2]) * BOHR_TO_NM

    system = mbuild.Compound()
    system.periodicity = np.array([boxx,boyy,bozz])

    for (name, x, y, z) in data[7:7+num_atoms]:
        system.add(
            mbuild.Compound(
                name=name,
                pos=[
                    x * BOHR_TO_NM,
                    y * BOHR_TO_NM,
                    z * BOHR_TO_NM
                ]
            )
        )

    return system

def read_restart(filen):
    """Read a metalwalls restart file and return an mbuild.Compound

    Parameters
    ----------
    filen : string
        filename to read

    Returns
    -------
    system : mbuild.Compound
        system coordinates contained in restart file

    Notes
    -----
    Only reads coordinates.
    """
    return read_data(filen)
