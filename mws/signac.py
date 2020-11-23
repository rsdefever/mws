def check_simulation(filen, nsteps):
    """Check the energy file to determine if the simualtion is complete

    Parameters
    ----------
    filen : string
        energy file name to check
    nsteps : int
        number of steps in simulation

    Returns
    -------
    complete : bool
        True if the simulation has reached nsteps, else false
    """
    try:
        with open(filen) as f:
            for line in f:
                pass
            last = line.strip().split()
    except OSError:
        return False


    try:
        if int(last[0]) == nsteps:
            return True
        else:
            return False
    except (ValueError, IndexError):
        return False

