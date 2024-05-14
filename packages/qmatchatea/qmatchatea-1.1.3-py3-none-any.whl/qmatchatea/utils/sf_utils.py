# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Here we mainly retrieve the Fock representation of linear optics operators.
We furthermore added a two operations for the state preparation and a barrier insertion,
which are used internally by the Fortran.

Moreover, we provide a function to initialize a Gaussian Boson Sampling circuit,
which is a really interesting research topic, and another to compute the
occupation profile of a photonic output.

Functions and classes
---------------------

"""
from collections import OrderedDict

try:
    from strawberryfields import ops
    import strawberryfields.backends.fockbackend as fock

    SF_IS_IMPORTED = True
except ModuleNotFoundError:
    SF_IS_IMPORTED = False
import numpy as np


__all__ = ["Barrier", "optical_gates", "GBS_circ", "occupation_profile"]

if SF_IS_IMPORTED:

    class Barrier(ops.Operation):
        """
        New sf operation to apply MPS canonization during MPI protocol.
        When a barrier is set then the canonization is restored. It has no effect
        in a serial simulation. If used in a python sf simulation the application
        will fail
        """

        def __init__(self):
            super().__init__([])

else:

    class Barrier:
        """
        New sf operation to apply MPS canonization during MPI protocol.
        When a barrier is set then the canonization is restored. It has no effect
        in a serial simulation. If used in a python sf simulation the application
        will fail
        """

        def __init__(self):
            raise ImportError(
                "Strawberryfields is not imported, barriers are not available"
            )


def fock_preparation(state, trunc):
    """
    Returns the tensor to bring a vacuum state in
    a predetermined Fock state

    Parameters
    ----------
    state: int
        The Fock state level
    trunc: int
        Fock cutoff
    """

    tens = np.zeros((trunc, trunc))
    tens[state, 0] = 1

    return tens


def vacuum_preparation(trunc):
    """
    Returns the tensor to bring a vacuum state in
    a vacuum state

    Parameters
    ----------
    trunc: int
        Fock cutoff
    """

    tens = np.eye(trunc)
    return tens


def sf_barrier(trunc):
    """
    Returns a vector with all 0 and 1 in the first place,
    which is not used in the simulation. Barriers are important
    for MPI processes.

    Parameters
    ----------
    trunc: int
        Fock cutoff
    """
    tens = np.zeros((trunc, trunc))
    tens[0, 0] = 1
    return tens


if SF_IS_IMPORTED:
    optical_gates = OrderedDict()
    optical_gates["a"] = fock.ops.a
    optical_gates["Dgate"] = fock.ops.displacement
    optical_gates["Sgate"] = fock.ops.squeezing
    optical_gates["Kgate"] = fock.ops.kerr
    optical_gates["Rgate"] = fock.ops.phase
    optical_gates["BSgate"] = fock.ops.beamsplitter
    optical_gates["Vgate"] = fock.ops.cubicPhase
    # optical_gates['MZgate'] = fockops.mzgate
    optical_gates["S2gate"] = fock.ops.two_mode_squeeze
    optical_gates["CKgate"] = fock.ops.cross_kerr
    optical_gates["Fock"] = fock_preparation
    optical_gates["Vacuum"] = vacuum_preparation
    optical_gates["Barrier"] = sf_barrier
else:
    optical_gates = OrderedDict()


def GBS_circ(prog, unitary, squeeze_params=None):
    """Build a GBS circuit on a program, given the interferometer unitary

    Parameters
    ----------
    prog : strawberryfields.Program
        Strawberry fields program
    unitary: ndarray, dtype=complex
        Unitary matrix to be decomposed in the interferometer
    squeeze_params: ndarray (num_modes, 2), optional
        Parameters for the squeezing operators. Default (1, 0)

    Returns
    -------
    prog: strawberryfields.Program
        Strawberry fields program with the GBS applied
    """
    if not SF_IS_IMPORTED:
        raise ImportError("Strawberryfields library is not imported or installed.")
    num_modes = prog.num_subsystems
    interf = ops.Interferometer(unitary)
    if squeeze_params is None:
        squeeze_params = np.zeros((num_modes, 2))

    assert (
        squeeze_params.shape[0] != num_modes
    ), f"Number of squeeze parameters must be equal to number of modes m={num_modes}"
    assert (
        squeeze_params.shape[1] != 2
    ), f"Each mode should have only 2 parameters, not {squeeze_params.shape[1]}"

    commands = interf.decompose(prog.register)
    with prog.context as qub:
        # Sqeezing
        for jj in range(num_modes):
            ops.Sgate(squeeze_params[jj, 0], squeeze_params[jj, 1]) | qub[jj]
    # Interferometer
    for comm in commands:
        prog.append(comm.op, comm.reg)

    return prog


def occupation_profile(measures, density=False):
    """Compute the occupation profile of the measured state

    Parameters
    ----------
    measures: dict
        Measure of the quantum optics experiment
    density: bool
        If True normalize the number of occurrencies to 1

    Return
    ------
    occupation: ndarray, dtype=int, shape(N, 2)
        Occupation profile. The first column is the number of photons,
        the second column is the number of occurrences
    """
    keys = np.array(list(measures.keys()))

    # Polish keys to have the number of photons in the state
    number_of_photons = []
    for kk in keys:
        polished_kk = kk.replace(" ", "").split(",")
        n_phot = np.array(polished_kk, dtype=int).sum()
        number_of_photons.append(n_phot)

    occupation = {}
    # Combine all the measurements
    for ii, kk in enumerate(keys):
        n_phot = number_of_photons[ii]
        n_occ = measures[kk]
        if n_phot in occupation:
            occupation[n_phot] += n_occ
        else:
            occupation[n_phot] = n_occ

    n_phot = np.array(list(occupation.keys()))
    n_occ = np.array(list(occupation.values()), dtype=float)
    order = np.argsort(n_phot)
    n_phot = n_phot[order].reshape(-1, 1)
    n_occ = n_occ[order].reshape(-1, 1)
    if density:
        n_occ = n_occ / n_occ.sum()
    occupation = np.hstack((n_phot, n_occ))

    return occupation
